import os
import xarray as xr
import geopandas as gpd
import numpy as np
import netCDF4 as nc
from osgeo import gdal, osr
import glob
import datetime

# -------------------------------------------Step 1:将nc存为单独的tif文件------------------------------------------------
# leaf = True
leaf = False

if leaf:
     def NC_to_tiffs(data, Output_folder):
          nc_data_obj = nc.Dataset(data)
          # print(nc_data_obj,type(nc_data_obj)) # 了解NC_DS的数据类型，<class 'netCDF4._netCDF4.Dataset'>
          # print(nc_data_obj.variables) # 了解变量的基本信息
          # print(nc_data_obj)

          Lat = nc_data_obj.variables['latitude'][:]
          Lon = nc_data_obj.variables['longitude'][:]
          u_arr = np.asarray(nc_data_obj.variables['pre'])  # 这里根据需求输入想要转换的波段名称
          Time = nc_data_obj.variables['time'][0]  # 637.0 = 2013-01; 649

          # 影像的左上角和右下角坐标
          LonMin, LatMax, LonMax, LatMin = [Lon.min(), Lat.max(), Lon.max(), Lat.min()]
          # 分辨率计算
          N_Lat = len(Lat)
          N_Lon = len(Lon)
          Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)
          Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)
          date = datetime.date(int((Time - 1)/12 + 1960), 1, 1)

          for i in range(len(u_arr[:])):
               # 创建.tif文件
               driver = gdal.GetDriverByName('GTiff')  # CN_Prec_MonthlyMean_1km_2013.nc
               out_tif_name = Output_folder + '/' + 'Prec_' + str(date + datetime.timedelta(days=i)) + '_WGS84.tif'
               print(out_tif_name)
               out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)

               # 设置影像的显示范围
               # -Lat_Res一定要是-的
               geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
               out_tif.SetGeoTransform(geotransform)

               # 获取地理坐标系统信息，用于选取需要的地理坐标系统
               srs = osr.SpatialReference()
               srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
               out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息

               # 去除异常值
               # u_arr[u_arr[:, :] == 9.969209968386869e+36] = 0

               # 数据写出
               out_tif.GetRasterBand(1).WriteArray(u_arr[i].T)
               # 将数据写入内存，此时没有写入硬盘 此处[::-1]用于图像的垂直镜像对称，避免图像颠倒
               out_tif.FlushCache()  # 将数据写入硬盘

          del out_tif  # 注意必须关闭tif文件

     def main():
          Input_folder = 'G:/Data Accumulation/16_Monthly precipitation/PREC_13-20/'
          Output_folder = 'G:/Data Accumulation/16_Monthly precipitation/PREC_13-20_tif'
          # 读取所有nc数据
          data_list = glob.glob(Input_folder + '/*.nc')
          for i in range(len(data_list)):
               data = data_list[i]
               print(data)
               NC_to_tiffs(data, Output_folder)
               print(data + '-----转tif成功')
          print('----转换结束----')

     if __name__ == '__main__':
          main()


# -------------------------------------------Step 2:裁剪出武汉区域的tif文件------------------------------------------------
leaf = True
# leaf = False

if leaf:
    input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

    path_input = r"G:/Data Accumulation/16_Monthly precipitation/PREC_13-20_tif"
    path_output = r'I:/nc_task/1_water-related/PREC_13-20_WGS84_monthly'  # Prec_2013-01-01_WGS84.tif

    for raster in os.listdir(path_input):
        # print(raster)
        input_raster = gdal.Open(path_input + '/' + raster)
        output_raster = path_output + '/' + 'PREC_' + raster.split('-')[0].split('_')[-1] \
                        + '-' + raster.split('-')[2].split('_')[0] + '_wuhan_WGS84.tif'
        print(output_raster)
        ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                       cropToCutline=True, dstNodata=0)
    print('All done!')