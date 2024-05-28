# 对每月提取的GSW统计值进行年合成
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

input_path = 'I:/nc_task/5_human-related/'
output_path = 'I:/nc_task/5_human-related/'

HR_path = 'I:/nc_task/statistics/RHWH_buffer_5km/'

# ---------------------------------> 1.LNTL <-------------------------------------

LNTL_input_path = input_path + 'LNTL_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 2.POPC <-------------------------------------

# POPC_input_path = input_path + 'POPC_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

for i in range(0, len(os.listdir(LNTL_input_path))):

    human_related = pd.DataFrame()
    Hospitalization_rate = pd.read_excel(HR_path + os.listdir(HR_path)[i + 1])

    # for LNTL
    LNTL_raw = pd.read_csv(LNTL_input_path + os.listdir(LNTL_input_path)[i], index_col='id')

    # for POPC
    # POPC_raw = pd.read_csv(POPC_input_path + os.listdir(POPC_input_path)[i], index_col='id')

    # start integration
    human_related = human_related.append(Hospitalization_rate['FID'])  # FID
    human_related = human_related.append(Hospitalization_rate['HR'])  # HR
    human_related = human_related.append(LNTL_raw['mean'])  # LNTL_mean
    human_related = human_related.append(LNTL_raw['max'])  # LNTL_max
    # human_related = human_related.append(POPC_raw['mean'])  # POPC_mean
    # human_related = human_related.append(POPC_raw['max'])  # POPC_max

    human_related.index = ['FID', 'HR', 'LNTL_mean', 'LNTL_max']
    result = human_related.T
    result.to_excel(output_path + str(2013 + i) + '_human-related_statistics.xlsx', index=False)
print('All done!')
