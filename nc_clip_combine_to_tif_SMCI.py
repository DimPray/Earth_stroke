import os
import xarray as xr
import geopandas as gpd
import numpy as np
import netCDF4 as nc
from osgeo import gdal, osr
import glob
import datetime

# -------------------------------------------Step 1:将nc裁剪后合并输出------------------------------------------------
leaf = True

if leaf:

     # read .shp file
     shp_path = "I:/nc_task/shp/"
     shp_path = os.path.join(shp_path, "Wuhan_County.shp")
     shp_roi = gpd.read_file(shp_path)
     # print(shp_roi)
     # print(shp_roi.total_bounds)
     # array([113.69659603, 29.97181897, 115.07704017, 31.36291319])  From lower left point to upper right point

     # acquire coordinates of the outer enclosing rectangle (lower left and upper right)
     aoi_lat = [float(shp_roi.total_bounds[1]), float(shp_roi.total_bounds[3])]
     aoi_lon = [float(shp_roi.total_bounds[0]), float(shp_roi.total_bounds[2])]
     # print(aoi_lat, aoi_lon)

     nc_daily_data_sum = []
     path = 'G:/Data Accumulation/19_SMCI1.0/10cm_SMCI_13-20/SMCI_1km_13_20_10cm/'
     for year in range(2013, 2021):
          nc_daily_data = path + 'SMCI_1km_' + str(year) + '_10cm.nc'

          with xr.open_dataset(nc_daily_data) as file_nc:
               start_date = str(year) + "-01-01"
               end_date = str(year) + "-12-31"
               # print(start_date, end_date)
               SMCI_days_wuhan = file_nc["SMCI"].sel(
                    time=slice(start_date, end_date),
                    lat=slice(aoi_lat[1], aoi_lat[0]),
                    lon=slice(aoi_lon[0], aoi_lon[1]))
               # print(slice(start_date, end_date))
               # print(slice(aoi_lat[1], aoi_lat[0]))
               # print(slice(aoi_lon[0], aoi_lon[1]))
               print(SMCI_days_wuhan)
               SMCI_days_wuhan_tif = SMCI_days_wuhan['SMCI'].sel(time='time',)
               nc_daily_data_sum.append(SMCI_days_wuhan)

     data_result = xr.concat(nc_daily_data_sum, dim='time')
     print(data_result)
     data_result.to_netcdf('G:/Data Accumulation/19_SMCI1.0/10cm_SMCI_13-20/nc_10cm_13-20_wuhan.nc')  # 输出合并后的nc文件

# -------------------------------------------Step 2:将nc存为单独的tif文件------------------------------------------------
leaf = False

if leaf:
     def NC_to_tiffs(data, Output_folder):
          nc_data_obj = nc.Dataset(data)
          # print(nc_data_obj,type(nc_data_obj)) # 了解NC_DS的数据类型，<class 'netCDF4._netCDF4.Dataset'>
          # print(nc_data_obj.variables) # 了解变量的基本信息
          # print(nc_data_obj)

          Lat = nc_data_obj.variables['lat'][:]
          Lon = nc_data_obj.variables['lon'][:]
          u_arr = np.asarray(nc_data_obj.variables['SMCI'])  # 这里根据需求输入想要转换的波段名称

          # 影像的左上角和右下角坐标
          LonMin, LatMax, LonMax, LatMin = [Lon.min(), Lat.max(), Lon.max(), Lat.min()]
          # 分辨率计算
          N_Lat = len(Lat)
          N_Lon = len(Lon)
          Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)
          Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)
          date = datetime.date(2013, 1, 1)
          # print(date)
          # print(date + datetime.timedelta(days=2))

          for i in range(len(u_arr[:])):
               # 创建.tif文件
               driver = gdal.GetDriverByName('GTiff')  # nc_10cm_13-20_wuhan.nc
               out_tif_name = Output_folder + '/' + 'SMCI_10cm_' + str(date + datetime.timedelta(days=i)) + '_wuhan_WGS84.tif'
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
               u_arr[u_arr[:, :] == -32767] = 0

               # 数据写出
               out_tif.GetRasterBand(1).WriteArray(u_arr[i][::1])
               # 将数据写入内存，此时没有写入硬盘 此处[::-1]用于图像的垂直镜像对称，避免图像颠倒
               out_tif.FlushCache()  # 将数据写入硬盘

          del out_tif  # 注意必须关闭tif文件

     def main():
          Input_folder = 'G:/Data Accumulation/19_SMCI1.0/SMCI_1km_13_20_wuhan'
          Output_folder = 'I:/nc_task/2_soil-related/SMCI_13-20_WGS84_daily'
          # 读取所有nc数据
          data_list = glob.glob(Input_folder + '/*.nc')
          for i in range(len(data_list)):
               data = data_list[i]
               NC_to_tiffs(data, Output_folder)
               print(data + '-----转tif成功')
          print('----转换结束----')

     if __name__ == '__main__':
          main()