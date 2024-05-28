# -*- coding: utf-8 -*-

import os
import h5py
import numpy as np
import pandas as pd
import geopandas as gpd
from osgeo import gdal, osr
import datetime

# -------------------------------------------Step 1:将.h5数据转换为.tif------------------------------------------------
leaf = False
# leaf = True

if leaf:
    TopLeftLongitude = 7087254.893403063
    Lon_Res = 926.6258333333334
    TopLeftLatitude = 5896446.849020582
    Lat_Res = 926.6254166666668

    # save function
    def save(file, img_arr, width, height):
        driver = gdal.GetDriverByName('GTiff')
        out_img = driver.Create(file, width, height, 1, gdal.GDT_Byte)
        input_image = gdal.Open('G:/Data Accumulation/20_SSM/metadata/Image_projection_example.tif')
        projection = input_image.GetProjection()
        out_img.SetProjection(projection)

        # 设置geotransform 只需要左上角经纬度和横纵分辨率
        geotransform = (TopLeftLongitude, Lon_Res, 0, TopLeftLatitude, 0, -Lat_Res)
        out_img.SetGeoTransform(geotransform)  # 设置投影坐标
        out_img.GetRasterBand(1).WriteArray(img_arr)
        out_img.FlushCache()

    # batch save 'sm_night'
    def restore(file):
        # path = 'G:/Data Accumulation/20_SSM/SSM_13-20/'
        # for hdf_fold in os.listdir(path):
        #     for hdf in os.listdir(path + hdf_fold):
        f = h5py.File(path + hdf_fold + '/' + file, 'r')
        for k in f.keys():
            out = 'G:/Data Accumulation/20_SSM/SSM_13-20_WGS84_daily/' + file.split('.')[0] + '_' + k + '.tif'
            img_raw = f[k]
            arr = np.array(img_raw[:, :])
            height, width = arr.shape
            save(out, arr, width, height)

    # 遍历所有文件并保存为tif格式
    path = 'G:/Data Accumulation/20_SSM/SSM_13-20/'
    for hdf_fold in os.listdir(path):
        for file in os.listdir(path + hdf_fold):
            print(file)
            restore(file)

# -------------------------------------------Step 2:按照武汉市边界裁剪.tif------------------------------------------------
leaf = True
# leaf = False

if leaf:
    input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

    path_input = r"G:/Data Accumulation/20_SSM/SSM_13-20_WGS84_daily/"
    path_output = r'I:/nc_task/2_soil-related/SSM_13-20_WGS84_daily/'  # SM_2013001_sm_night.tif
    time = datetime.date(2013, 1, 1)
    num = 0

    for raster in os.listdir(path_input):
        input_raster = gdal.Open(path_input + raster)
        name = str(time + datetime.timedelta(days=num))
        output_raster = path_output + 'SSM_' + str(time + datetime.timedelta(days=num)) + '_wuhan_WGS84.tif'
        ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape, cropToCutline=True, dstNodata=0)
        print(output_raster)
        num += 1

    print('All done!')
