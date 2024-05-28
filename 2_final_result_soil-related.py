# 对每月提取的GSW统计值进行年合成
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

input_path = 'I:/nc_task/2_soil-related/'
output_path = 'I:/nc_task/2_soil-related/'

HR_path = 'I:/nc_task/statistics/RHWH_buffer_5km/'

# ---------------------------------> 1.SMCI <-----------------------------

SMCI_input_path = input_path + 'SMCI_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 2.SSM <------------------------------

SSM_input_path = input_path + 'SSM_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

for i in range(0, len(os.listdir(SSM_input_path))):

    soil_related = pd.DataFrame()
    Hospitalization_rate = pd.read_excel(HR_path + os.listdir(HR_path)[i + 1])

    # for SSM
    SSM_mean_raw = pd.read_csv(SSM_input_path + os.listdir(SSM_input_path)[i], index_col='id')
    SSM_mean_raw.replace('0j', '(0.0+0j)', inplace=True)
    SSM_mean_raw.replace('--', '(0.0+0j)', inplace=True)

    # for SMCI
    SMCI_mean_raw = pd.read_csv(SMCI_input_path + 'mean/' + os.listdir(SMCI_input_path + 'mean/')[i], index_col='id')
    SMCI_max_raw = pd.read_csv(SMCI_input_path + 'max/' + os.listdir(SMCI_input_path + 'max/')[i], index_col='id')

    # start integration
    soil_related = soil_related.append(Hospitalization_rate['FID'])  # FID
    soil_related = soil_related.append(Hospitalization_rate['HR'])  # HR

    mean_col_SMCI = []
    max_col_SMCI = []
    mean_col_SSM = []
    mean_raw_SMCI = SMCI_mean_raw['mean']
    max_raw_SMCI = SMCI_max_raw['max']
    mean_raw_SSM = SSM_mean_raw['mean']

    for j in range(0, len(mean_raw_SMCI)):
        mean_col_f_SSM = float(mean_raw_SSM.iloc[j].split('+')[0].split('(')[1])
        mean_col_f_SMCI = float(mean_raw_SMCI.iloc[j].split('+')[0].split('(')[1])
        max_col_f_SMCI = float(max_raw_SMCI.iloc[j].split('+')[0].split('(')[1])
        mean_col_SSM.append(mean_col_f_SSM)
        mean_col_SMCI.append(mean_col_f_SMCI)
        max_col_SMCI.append(max_col_f_SMCI)

    SSM_mean = pd.DataFrame(mean_col_SSM, columns=['mean_ssm'])
    SMCI_mean = pd.DataFrame(mean_col_SMCI, columns=['mean'])
    SMCI_max = pd.DataFrame(max_col_SMCI, columns=['max'])

    soil_related = soil_related.append(SSM_mean.T)  # SSM_mean
    soil_related = soil_related.append(SMCI_mean.T)  # SMCI_mean
    soil_related = soil_related.append(SMCI_max.T)  # SMCI_max

    soil_related.index = ['FID', 'HR', 'SSM_mean', 'SMCI_mean', 'SMCI_max']
    result = soil_related.T
    result.to_excel(output_path + str(2013 + i) + '_soil-related_statistics.xlsx', index=False)
print('All done!')
