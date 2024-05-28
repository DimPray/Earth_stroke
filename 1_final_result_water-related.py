# 对每月提取的GSW统计值进行年合成
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

input_path = 'I:/nc_task/1_water-related/'
output_path = 'I:/nc_task/1_water-related/'

HR_path = 'I:/nc_task/statistics/RHWH_buffer_5km/'

# ---------------------------------> 1.GSW <-------------------------------

GSW_input_path = input_path + 'GSW_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 2.PREC <------------------------------

PREC_input_path = input_path + 'PREC_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

for i in range(0, len(os.listdir(GSW_input_path))):

    water_related = pd.DataFrame()
    Hospitalization_rate = pd.read_excel(HR_path + os.listdir(HR_path)[i + 1])

    # for GSW
    GSW_raw = pd.read_csv(GSW_input_path + os.listdir(GSW_input_path)[i], index_col='id')

    # for PREC
    PREC_mean_raw = pd.read_csv(PREC_input_path + 'mean/' + os.listdir(PREC_input_path + 'mean/')[i], index_col='id')
    PREC_max_raw = pd.read_csv(PREC_input_path + 'max/' + os.listdir(PREC_input_path + 'max/')[i], index_col='id')

    # start integration
    water_related = water_related.append(Hospitalization_rate['FID'])  # FID
    water_related = water_related.append(Hospitalization_rate['HR'])  # HR
    water_related = water_related.append(GSW_raw['count'])  # GSW_sum

    mean_col_PREC = []
    max_col_PREC = []
    mean_raw_PREC = PREC_mean_raw['mean']
    max_raw_PREC = PREC_max_raw['max']
    for j in range(0, len(mean_raw_PREC)):
        mean_col_f_PREC = float(mean_raw_PREC.iloc[j].split('+')[0].split('(')[1])
        max_col_f_PREC = float(max_raw_PREC.iloc[j].split('+')[0].split('(')[1])
        mean_col_PREC.append(mean_col_f_PREC)
        max_col_PREC.append(max_col_f_PREC)
    PREC_mean = pd.DataFrame(mean_col_PREC, columns=['mean'])
    PREC_max = pd.DataFrame(max_col_PREC, columns=['max'])

    water_related = water_related.append(PREC_mean.T)  # PREC_mean
    water_related = water_related.append(PREC_max.T)  # PREC_max

    water_related.index = ['FID', 'HR', 'GSW_sum', 'PREC_mean', 'PREC_max']
    result = water_related.T
    result.to_excel(output_path + str(2013 + i) + '_water-related_statistics.xlsx', index=False)
print('All done!')
