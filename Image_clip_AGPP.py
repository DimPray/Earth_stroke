from osgeo import gdal
import os

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

path_input = r"G:/Data Accumulation/18_AGPP/AGPP_13-20/"
path_output = r'I:/nc_task/4_biology-related/AGPP_13-20_WGS84_yearly/'  # AGPP_2013.tif

for raster in os.listdir(path_input):
    # print(raster)
    input_raster = gdal.Open(path_input + raster)
    output_raster = path_output + raster[0:-4] + '_wuhan_WGS84.tif'
    ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                   cropToCutline=True, dstNodata=0)

print('All done!')