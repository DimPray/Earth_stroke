# -*- coding: utf-8 -*-
# 模块导入
import numpy as np
import netCDF4 as nc
from osgeo import gdal, osr
import os
import glob

# ---------------------------------Step1:先将 nc 数据转为 tif 数据---------------------------------------
# leaf = False
leaf = True

if leaf:

    def NC_to_tiffs(data, Output_folder):
        nc_data_obj = nc.Dataset(data)
        # print(nc_data_obj,type(nc_data_obj)) # 了解NC_DS的数据类型，<class 'netCDF4._netCDF4.Dataset'>
        # print(nc_data_obj.variables) # 了解变量的基本信息
        # print(nc_data_obj)

        Lat = nc_data_obj.variables['lat'][:]
        Lon = nc_data_obj.variables['lon'][:]
        PM_arr = np.asarray(nc_data_obj.variables['PM10'])  # 这里根据需求输入想要转换的波段名称

        # 影像的左上角和右下角坐标
        LonMin, LatMax, LonMax, LatMin = [Lon.min(), Lat.max(), Lon.max(), Lat.min()]
        # 分辨率计算
        N_Lat = len(Lat)
        N_Lon = len(Lon)
        Lon_Res = (LonMax - LonMin) / (float(N_Lon)-1)
        Lat_Res = (LatMax - LatMin) / (float(N_Lat)-1)

        driver = gdal.GetDriverByName('GTiff')
        # I:/Hubei_database/0. Raw datasets/Pollutant/PM2.5/PM2.5_13-20/2013/CHAP_PM2.5_D1K_20130101_V4.nc
        out_tif_name = Output_folder + '/' + 'PM10' + '_' + data.split('_')[5] + '_' + 'WGS84.tif'
        geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
        out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)
        out_tif.SetGeoTransform(geotransform)
        # 获取地理坐标系统信息，用于选取需要的地理坐标系统
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
        out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息

        # 去除异常值
        PM_arr[PM_arr[:, :] == 65535] = 0

        out_tif.GetRasterBand(1).WriteArray(PM_arr[::1])
        # 将数据写入内存，此时没有写入硬盘 此处[::-1]用于图像的垂直镜像对称，避免图像颠倒
        out_tif.FlushCache()  # 将数据写入硬盘
        del out_tif  # 注意必须关闭tif文件

    def main():
        Input_folder = 'I:/Hubei_database/0. Raw datasets/Pollutant/PM10/PM10_13-20/'
        Output_folder = 'I:/Hubei_database/0. Raw datasets/Pollutant/PM10/PM10_13-20_tif/'
        # 读取所有nc数据
        for folder in os.listdir(Input_folder):
            data_list = glob.glob(Input_folder + folder + '/' + '/*.nc')
            # print(data_list)
            for i in range(len(data_list)):
                data = data_list[i]
                NC_to_tiffs(data, Output_folder)
                print(data + '-----转tif成功')
            print('----转换结束----')

    if __name__ == '__main__':
        main()

# ---------------------------------Step2:裁剪武汉市的 tif 数据---------------------------------------
# leaf = True
leaf = False

if leaf:
    input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

    path_input = r"I:/Hubei_database/0. Raw datasets/Pollutant/PM10/PM10_13-20_tif/"
    path_output = r'I:/nc_task/3_air-related/PM10_13-20_WGS84_daily/'  # PM25_20130101_WGS84.tif

    for raster in os.listdir(path_input):
        # print(raster)
        input_raster = gdal.Open(path_input + '/' + raster)
        output_raster = path_output + '/' + 'PM10' + raster.split('_')[1] + '_wuhan_WGS84.tif'
        ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                       cropToCutline=True, dstNodata=0)