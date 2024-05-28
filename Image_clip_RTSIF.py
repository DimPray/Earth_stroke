from osgeo import gdal
import os

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

path_input = r"I:/Hubei_database/0. Raw datasets/RTSIF/RTSIF_13-20/"
path_output = r'I:/nc_task/4_biology-related/RTSIF_13-20_WGS84_8days/'  # RTSIF_2013-01-01.tif

for folder in os.listdir(path_input):
    for raster in os.listdir(path_input + folder):
        print(raster)
        input_raster = gdal.Open(path_input + folder + '/' + raster)
        output_raster = path_output + raster.split('.')[0] + '_wuhan_WGS84.tif'
        ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                       cropToCutline=True, dstNodata=0)

print('All done!')