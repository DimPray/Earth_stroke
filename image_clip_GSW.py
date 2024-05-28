from osgeo import gdal
import os

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

path_input = r"G:/Data Accumulation/water-related/"
path_output = r'I:/nc_task/1_water-related/GSW_13-20_WGS84_monthly/'  # hubei_GSW1_4_2013_01.tif
for raster in os.listdir(path_input):
    # print(raster)
    input_raster = gdal.Open(path_input + raster)
    output_raster = path_output + 'GSW_' + raster.split('_')[3] + '-' + raster.split('_')[4].split('.')[0] + '_wuhan_WGS84.tif'
    ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                   cropToCutline=True, dstNodata=0)

print('All done!')