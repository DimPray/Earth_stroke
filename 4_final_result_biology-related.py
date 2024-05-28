# 对每月提取的GSW统计值进行年合成
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

input_path = 'I:/nc_task/4_biology-related/'
output_path = 'I:/nc_task/4_biology-related/'

HR_path = 'I:/nc_task/statistics/RHWH_buffer_5km/'

# ---------------------------------> 1.AGPP <------------------------------

AGPP_input_path = input_path + 'AGPP_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 2.CLCD <------------------------------

CLCD_input_path = input_path + 'CLCD_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 3.NDVI <------------------------------

NDVI_input_path = input_path + 'NDVI_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 4.RTSIF <------------------------------

RTSIF_input_path = input_path + 'RTSIF_13-20_WGS84_UTM_50N_yearly_zonal_csv/'


for i in range(0, len(os.listdir(AGPP_input_path))):

    biology_related = pd.DataFrame()
    Hospitalization_rate = pd.read_excel(HR_path + os.listdir(HR_path)[i + 1])

    # for AGPP
    AGPP_raw = pd.read_csv(AGPP_input_path + os.listdir(AGPP_input_path)[i], index_col='id')

    # for CLCD -- cropland, forest, grassland, impervious, water
    CLCD_cropland_raw = pd.read_csv(CLCD_input_path + 'cropland/' + os.listdir(CLCD_input_path + 'cropland/')[i],
                                    index_col='id')
    CLCD_forest_raw = pd.read_csv(CLCD_input_path + 'forest/' + os.listdir(CLCD_input_path + 'forest/')[i],
                                    index_col='id')
    CLCD_grassland_raw = pd.read_csv(CLCD_input_path + 'grassland/' + os.listdir(CLCD_input_path + 'grassland/')[i],
                                    index_col='id')
    CLCD_impervious_raw = pd.read_csv(CLCD_input_path + 'impervious/' + os.listdir(CLCD_input_path + 'impervious/')[i],
                                    index_col='id')
    CLCD_water_raw = pd.read_csv(CLCD_input_path + 'water/' + os.listdir(CLCD_input_path + 'water/')[i],
                                    index_col='id')
    CLCD_cropland_raw.replace('--', '0.0', inplace=True)
    CLCD_forest_raw.replace('--', '0.0', inplace=True)
    CLCD_grassland_raw.replace('--', '0.0', inplace=True)
    CLCD_impervious_raw.replace('--', '0.0', inplace=True)
    CLCD_water_raw.replace('--', '0.0', inplace=True)

    # for NDVI
    NDVI_mean_raw = pd.read_csv(NDVI_input_path + 'mean/' + os.listdir(NDVI_input_path + 'mean/')[i], index_col='id')
    # NDVI_mean_raw.replace('0j', '0.0 + 0j', inplace=True)
    NDVI_max_raw = pd.read_csv(NDVI_input_path + 'max/' + os.listdir(NDVI_input_path + 'max/')[i], index_col='id')
    # NDVI_max_raw.replace('0j', '0.0 + 0j', inplace=True)

    # for RTSIF
    RTSIF_mean_raw = pd.read_csv(RTSIF_input_path + 'mean/' + os.listdir(RTSIF_input_path + 'mean/')[i], index_col='id')
    # RTSIF_mean_raw.replace('0j', '0.0 + 0j', inplace=True)
    RTSIF_max_raw = pd.read_csv(RTSIF_input_path + 'max/' + os.listdir(RTSIF_input_path + 'max/')[i], index_col='id')

    # start integration
    biology_related = biology_related.append(Hospitalization_rate['FID'])  # FID
    biology_related = biology_related.append(Hospitalization_rate['HR'])  # HR
    biology_related = biology_related.append(AGPP_raw['mean'])  # AGPP_mean
    biology_related = biology_related.append(AGPP_raw['max'])  # AGPP_max
    biology_related = biology_related.append(CLCD_cropland_raw['sum'])  # CLCD_cropland_sum
    biology_related = biology_related.append(CLCD_forest_raw['sum'])  # CLCD_forest_sum
    biology_related = biology_related.append(CLCD_grassland_raw['sum'])  # CLCD_grassland_sum
    biology_related = biology_related.append(CLCD_impervious_raw['sum'])  # CLCD_impervious_sum
    biology_related = biology_related.append(CLCD_water_raw['sum'])  # CLCD_water_sum

    mean_col_NDVI = []
    max_col_NDVI = []
    mean_col_RTSIF = []
    max_col_RTSIF = []
    mean_raw_NDVI = NDVI_mean_raw['mean']
    max_raw_NDVI = NDVI_max_raw['max']
    mean_raw_RTSIF = RTSIF_mean_raw['mean']
    max_raw_RTSIF = RTSIF_max_raw['max']

    count = 0
    for j in range(0, len(mean_raw_NDVI)):
        mean_col_f_NDVI = float(mean_raw_NDVI.iloc[j].split('+')[0].split('(')[1])
        max_col_f_NDVI = float(max_raw_NDVI.iloc[j].split('+')[0].split('(')[1])
        mean_col_f_RTSIF = float(mean_raw_RTSIF.iloc[j].split('+')[0].split('(')[1])
        max_col_f_RTSIF = float(max_raw_RTSIF.iloc[j].split('+')[0].split('(')[1])
        mean_col_NDVI.append(mean_col_f_NDVI)
        max_col_NDVI.append(max_col_f_NDVI)
        mean_col_RTSIF.append(mean_col_f_RTSIF)
        max_col_RTSIF.append(max_col_f_RTSIF)

    NDVI_mean = pd.DataFrame(mean_col_NDVI, columns=['mean_ndvi'])
    NDVI_max = pd.DataFrame(max_col_NDVI, columns=['max_ndvi'])
    RTSIF_mean = pd.DataFrame(mean_col_RTSIF, columns=['mean_rtsif'])
    RTSIF_max = pd.DataFrame(max_col_RTSIF, columns=['max_rtsif'])

    biology_related = biology_related.append(NDVI_mean.T)  # NDVI_mean
    biology_related = biology_related.append(NDVI_max.T)  # NDVI_max
    biology_related = biology_related.append(RTSIF_mean.T)  # RTSIF_mean
    biology_related = biology_related.append(RTSIF_max.T)  # RTSIF_max

    biology_related.index = ['FID', 'HR', 'AGPP_mean', 'AGPP_max', 'CLCD_cropland', 'CLCD_forest', 'CLCD_grassland',
                             'CLCD_impervious', 'CLCD_water', 'NDVI_mean', 'NDVI_max', 'RTSIF_mean', 'RTSIF_max']
    result = biology_related.T
    result.to_excel(output_path + str(2013 + i) + '_biology-related_statistics.xlsx', index=False)
print('All done!')
