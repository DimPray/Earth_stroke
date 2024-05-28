from osgeo import gdal
import numpy as np
import os

input_path = 'I:/nc_task/3_air-related/PM25_13-20_WGS84_UTM_50N_daily/'
output_path = 'I:/nc_task/3_air-related/PM25_13-20_WGS84_UTM_50N_yearly/'
years = range(2013, 2021, 1)
for year in years:

    for i in range(0, len(os.listdir(input_path)), 1):
        if str(year) in os.listdir(input_path)[i]:

            # read
            dataset = gdal.Open(input_path + os.listdir(input_path)[i])
            projection = dataset.GetProjection()  # 投影
            geotrans = dataset.GetGeoTransform()  # 几何信息
            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数
            im_bands = dataset.RasterCount  # 波段数

            # change
            img_array = dataset.ReadAsArray()
            # img_array[img_array[:] == img_array[0, 0]] = 0.0
            if 0 == i:
                out_array = img_array[np.newaxis, :, :]
            else:
                out_array = np.ma.concatenate((out_array, img_array[np.newaxis, :, :]), axis=0)

    array_max = np.ma.max(out_array, axis=0)
    array_mean = np.ma.mean(out_array, axis=0)
    # print(array_max, array_mean)

    # write
    driver = gdal.GetDriverByName('GTiff')  # 创建驱动
    dst_ds = driver.Create(output_path + 'PM25_' + str(year) + '_wuhan_WGS84_UTM_50N_max.tif', im_width, im_height, im_bands, gdal.GDT_CFloat64)  # 创建文件
    dst_ds.SetProjection(projection)
    dst_ds.SetGeoTransform(geotrans)  # 设置几何信息
    dst_ds.GetRasterBand(1).WriteArray(array_max)  # 将数组写入

    driver = gdal.GetDriverByName('GTiff')  # 创建驱动
    dst_ds = driver.Create(output_path + 'PM25_' + str(year) + '_wuhan_WGS84_UTM_50N_mean.tif', im_width, im_height, im_bands, gdal.GDT_CFloat64)  # 创建文件
    dst_ds.SetProjection(projection)
    dst_ds.SetGeoTransform(geotrans)  # 设置几何信息
    dst_ds.GetRasterBand(1).WriteArray(array_mean)  # 将数组写入

    dst_ds.FlushCache()  # 写入硬盘
    dst_ds = None

print('All done!')

