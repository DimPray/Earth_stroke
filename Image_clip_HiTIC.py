from osgeo import gdal
import os

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"
path_input = 'G:/Data Accumulation/17_HiTIC-Monthly/HiTIC_Monthly_China_2003_2020[GeoTIFF]/'
path_output = 'I:/nc_task/3_air-related/HiTIC_13-20_WGS84_monthly/'
names = ['ATin', 'ATout', 'DI', 'ET', 'HI', 'HMI', 'MDI', 'NET', 'SAT', 'sWBGT', 'WBT', 'WCT']

for name in names:
    for file in os.listdir(path_input):
        if name in file:
            raster_path = path_input + file
            for raster in os.listdir(path_input + file):  # HiTIC_Monthly_China_ATin_2013-01-01.tif
                print(raster)
                input_raster = gdal.Open(raster_path + '/' + raster)
                output_raster = path_output + name + '_' + raster[-14:-4] + '_wuhan_WGS84.tif'
                ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                               cropToCutline=True, dstNodata=0)
                print(output_raster)
