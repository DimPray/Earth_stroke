from osgeo import gdal, osr, gdalnumeric
from osgeo.gdalconst import *
from pyproj import CRS, Proj, transform
import numpy as np
import os

def wgs84_UTM(aim_path, out_path, UTM_Zone, pixel_spacing):

    '''
    aim_path:需要更改的目标文件路径和名称
    out_path:输出影像的路径和名称
    UTM_Zone:条带号，比如UTM50 UTM_Zone=50
    pixel_spacing:栅格大小,单位是米
    '''
    pixel_spacing = int(pixel_spacing)
    # 待转换的UTM投影
    EPSG_code = '326%02d' % UTM_Zone
    epsg_to = int(EPSG_code)
    # 目标影像信息
    aim_ds = gdal.Open(aim_path)
    print(aim_ds)
    proj = aim_ds.GetProjection()
    Proj_in = proj.split('EPSG","')
    epsg_from = int((str(Proj_in[-1]).split(']')[0])[0:-1])
    epsg_to = int(epsg_to)
    geo_t = aim_ds.GetGeoTransform()
    x_size = aim_ds.RasterXSize  # 栅格矩阵的列数
    y_size = aim_ds.RasterYSize  # 栅格矩阵的行数

    osng = osr.SpatialReference()
    osng.ImportFromEPSG(epsg_to)
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromEPSG(epsg_from)

    inProj = Proj(init='epsg:%d' %epsg_from)
    outProj = Proj(init='epsg:%d' %epsg_to)
    # 以下几行没看懂，源代码说是先选取部分数据
    nrow_skip = round((0.06*y_size)/2)
    ncol_skip = round((0.06*x_size)/2)

    ulx, uly = transform(inProj, outProj, geo_t[0] + nrow_skip * geo_t[1], geo_t[3] + nrow_skip * geo_t[5])
    lrx, lry = transform(inProj, outProj, geo_t[0] + geo_t[1] * (x_size-ncol_skip),
                                        geo_t[3] + geo_t[5] * (y_size-nrow_skip))

    ulx = np.ceil(ulx/pixel_spacing) * pixel_spacing + 0.5 * pixel_spacing
    uly = np.floor(uly/pixel_spacing) * pixel_spacing - 0.5 * pixel_spacing
    lrx = np.floor(lrx/pixel_spacing) * pixel_spacing - 0.5 * pixel_spacing
    lry = np.ceil(lry/pixel_spacing) * pixel_spacing + 0.5 * pixel_spacing

    col = int((lrx - ulx)/pixel_spacing)
    rows = int((uly - lry)/pixel_spacing)

    (lrx, lry) = (ulx + col * pixel_spacing, uly -
                  rows * pixel_spacing)
    driver = gdal.GetDriverByName("GTiff")

    dataset = driver.Create(out_path, col, rows, 1, gdal.GDT_Float32)
    # 计算新的仿射参数
    new_geo = (ulx, pixel_spacing, geo_t[2], uly, geo_t[4], - pixel_spacing)
    # 设置新的仿射参数
    dataset.SetGeoTransform(new_geo)
    dataset.SetProjection(osng.ExportToWkt())
    # 重采样
    gdal.ReprojectImage(aim_ds, dataset, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.gdalconst.GRA_NearestNeighbour)

    del dataset

# file_input = r"I:/nc_task/1_water-related/test/PREC_2013-01_wuhan_WGS84.tif"
# file_output = r"I:/nc_task/1_water-related/result_pro.tif"
# pro_raster = wgs84_UTM(aim_path=file_input, out_path=file_output, UTM_Zone=50, pixel_spacing=1000)

input_path = r"I:/nc_task/5_human-related/POPC_13-20_WGS84_yearly/"
output_path = r"I:/nc_task/5_human-related/POPC_13-20_WGS84_UTM_50N_yearly/"

for raster in os.listdir(input_path):

    file_input = input_path + raster
    file_output = output_path + 'POPC' + file_input.split('POPC')[2].split('.')[0] + '_UTM_50N.tif'
    pro_raster = wgs84_UTM(aim_path=file_input, out_path=file_output, UTM_Zone=50, pixel_spacing=100)