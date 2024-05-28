from osgeo import gdal
import os

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

path_input = r"G:/Data Accumulation/24_LNTL/LNTL_13-20"
path_output = r'I:/nc_task/5_human-related/LNTL_13-20_WGS84_yearly'  # LongNTL_2013.tif
# print(os.listdir(path_input))
for num in range(1, len(os.listdir(path_input)), 4):
    # print(os.listdir(path_input)[num])
    raster = os.listdir(path_input)[num]
    input_raster = gdal.Open(path_input + '/' + raster)
    # print(input_raster)
    output_raster = path_output + '/' + 'L' + raster[4:12] + '_polygon_WGS84.tif'
    ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
                   cropToCutline=True, dstNodata=0)

print('All done!')