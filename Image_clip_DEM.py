from osgeo import gdal

input_shape = r"I:/nc_task/shp/Wuhan_County.shp"

path_input = r"I:/nc_task/2_soil-related/新建文件夹/"
path_output = r'I:/nc_task/2_soil-related/DEM_2015_WGS84/'

raster = 'DEM_merge_wuhan_2015.tif'

input_raster = gdal.Open(path_input + raster)
output_raster = path_output + 'DEM_2015_wuhan_WGS84.tif'
ds = gdal.Warp(output_raster, input_raster, format='GTiff', cutlineDSName=input_shape,
               cropToCutline=True, dstNodata=0)

print('All done!')