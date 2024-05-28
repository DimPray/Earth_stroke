from osgeo import gdal
import os

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

path_input = r"I:/Hubei_database/0. Raw datasets/ODIAC/ODIAC_13-20/"
path_output = r'I:/nc_task/3_air-related/ODIAC_13-20_WGS84_monthly/'  # odiac2020b_1km_excl_intl_1411.tif

for raster in os.listdir(path_input):
    print(raster)
    input_raster = gdal.Open(path_input + raster)
    output_raster = path_output + 'ODIAC_20' + raster.split('_')[4].split('.')[0] + '_wuhan_WGS84.tif'
    ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                   cropToCutline=True, dstNodata=0)

print('All done!')