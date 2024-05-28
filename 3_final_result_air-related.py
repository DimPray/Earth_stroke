# 对每月提取的GSW统计值进行年合成
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

input_path = 'I:/nc_task/3_air-related/'
output_path = 'I:/nc_task/3_air-related/'

HR_path = 'I:/nc_task/statistics/RHWH_buffer_5km/'

# ---------------------------------> 1.HiTIC <---------------------------

HiTIC_input_path = input_path + 'HiTIC_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 2.ODIAC <------------------------------

ODIAC_input_path = input_path + 'ODIAC_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 3.PM10 <------------------------------

PM10_input_path = input_path + 'PM10_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

# ---------------------------------> 4.PM25 <------------------------------

PM25_input_path = input_path + 'PM25_13-20_WGS84_UTM_50N_yearly_zonal_csv/'

for i in range(0, len(os.listdir(ODIAC_input_path + 'mean/'))):

    air_related = pd.DataFrame()
    Hospitalization_rate = pd.read_excel(HR_path + os.listdir(HR_path)[i + 1])

    # for HiTIC -- 'ATin', 'ATout', 'DI', 'ET', 'HI', 'HMI', 'MDI', 'NET', 'SAT', 'sWBGT', 'WBT', 'WCT'
    HiTIC_mean_rasters = [raster for raster in os.listdir(HiTIC_input_path + 'mean/') if raster.startswith(str(2013+i))]
    HiTIC_max_rasters = [raster for raster in os.listdir(HiTIC_input_path + 'max/') if raster.startswith(str(2013+i))]

    HiTIC_mean_ATin_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[0], index_col='id')
    HiTIC_mean_ATout_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[1], index_col='id')
    HiTIC_mean_DI_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[2], index_col='id')
    HiTIC_mean_ET_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[3], index_col='id')
    HiTIC_mean_HI_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[4], index_col='id')
    HiTIC_mean_HMI_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[5], index_col='id')
    HiTIC_mean_MDI_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[6], index_col='id')
    HiTIC_mean_NET_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[7], index_col='id')
    HiTIC_mean_SAT_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[8], index_col='id')
    HiTIC_mean_sWBGT_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[9], index_col='id')
    HiTIC_mean_WBT_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[10], index_col='id')
    HiTIC_mean_WCT_raw = pd.read_csv(HiTIC_input_path + 'mean/' + HiTIC_mean_rasters[11], index_col='id')

    HiTIC_max_ATin_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[0], index_col='id')
    HiTIC_max_ATout_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[1], index_col='id')
    HiTIC_max_DI_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[2], index_col='id')
    HiTIC_max_ET_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[3], index_col='id')
    HiTIC_max_HI_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[4], index_col='id')
    HiTIC_max_HMI_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[5], index_col='id')
    HiTIC_max_MDI_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[6], index_col='id')
    HiTIC_max_NET_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[7], index_col='id')
    HiTIC_max_SAT_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[8], index_col='id')
    HiTIC_max_sWBGT_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[9], index_col='id')
    HiTIC_max_WBT_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[10], index_col='id')
    HiTIC_max_WCT_raw = pd.read_csv(HiTIC_input_path + 'max/' + HiTIC_max_rasters[11], index_col='id')

    # for ODIAC
    ODIAC_mean_raw = pd.read_csv(ODIAC_input_path + 'mean/' + os.listdir(ODIAC_input_path + 'mean/')[i], index_col='id')
    ODIAC_max_raw = pd.read_csv(ODIAC_input_path + 'max/' + os.listdir(ODIAC_input_path + 'max/')[i], index_col='id')
    ODIAC_mean_raw.replace('0j', '(0.0+0j)', inplace=True)
    ODIAC_max_raw.replace('0j', '(0.0+0j)', inplace=True)
    # for PM10
    PM10_mean_raw = pd.read_csv(PM10_input_path + 'mean/' + os.listdir(PM10_input_path + 'mean/')[i], index_col='id')
    PM10_max_raw = pd.read_csv(PM10_input_path + 'max/' + os.listdir(PM10_input_path + 'max/')[i], index_col='id')

    # for PM25
    PM25_mean_raw = pd.read_csv(PM25_input_path + 'mean/' + os.listdir(PM25_input_path + 'mean/')[i], index_col='id')
    PM25_max_raw = pd.read_csv(PM25_input_path + 'max/' + os.listdir(PM25_input_path + 'max/')[i], index_col='id')

    # start integration
    air_related = air_related.append(Hospitalization_rate['FID'])  # FID
    air_related = air_related.append(Hospitalization_rate['HR'])  # HR

    # 'ATin', 'ATout', 'DI', 'ET', 'HI', 'HMI', 'MDI', 'NET', 'SAT', 'sWBGT', 'WBT', 'WCT'
    air_related = air_related.append(HiTIC_mean_ATin_raw['mean'])  # ATin_mean
    air_related = air_related.append(HiTIC_mean_ATout_raw['mean'])  # ATout_mean
    air_related = air_related.append(HiTIC_mean_DI_raw['mean'])  # DI_mean
    air_related = air_related.append(HiTIC_mean_ET_raw['mean'])  # ET_mean
    air_related = air_related.append(HiTIC_mean_HI_raw['mean'])  # HI_mean
    air_related = air_related.append(HiTIC_mean_HMI_raw['mean'])  # HMI_mean
    air_related = air_related.append(HiTIC_mean_MDI_raw['mean'])  # MDI_mean
    air_related = air_related.append(HiTIC_mean_NET_raw['mean'])  # NET_mean
    air_related = air_related.append(HiTIC_mean_SAT_raw['mean'])  # SAT_mean
    air_related = air_related.append(HiTIC_mean_sWBGT_raw['mean'])  # sWBGT_mean
    air_related = air_related.append(HiTIC_mean_WBT_raw['mean'])  # WBT_mean
    air_related = air_related.append(HiTIC_mean_WCT_raw['mean'])  # WCT_mean

    max_col_ATin = []
    max_col_ATout = []
    max_col_DI = []
    max_col_ET = []
    max_col_HI = []
    max_col_HMI = []
    max_col_MDI = []
    max_col_NET = []
    max_col_SAT = []
    max_col_sWBGT = []
    max_col_WBT = []
    max_col_WCT = []

    max_raw_ATin = HiTIC_max_ATin_raw['max']
    max_raw_ATout = HiTIC_max_ATout_raw['max']
    max_raw_DI = HiTIC_max_DI_raw['max']
    max_raw_ET = HiTIC_max_ET_raw['max']
    max_raw_HI = HiTIC_max_HI_raw['max']
    max_raw_HMI = HiTIC_max_HMI_raw['max']
    max_raw_MDI = HiTIC_max_MDI_raw['max']
    max_raw_NET = HiTIC_max_NET_raw['max']
    max_raw_SAT = HiTIC_max_SAT_raw['max']
    max_raw_sWBGT = HiTIC_max_sWBGT_raw['max']
    max_raw_WBT = HiTIC_max_WBT_raw['max']
    max_raw_WCT = HiTIC_max_WCT_raw['max']

    # 'ATin', 'ATout', 'DI', 'ET', 'HI', 'HMI', 'MDI', 'NET', 'SAT', 'sWBGT', 'WBT', 'WCT'
    for j in range(0, len(max_raw_ATin)):
        # print(len(max_raw_ATin))

        max_col_f_ATin = float(max_raw_ATin.iloc[j].split('+')[0].split('(')[1])
        max_col_f_ATout = float(max_raw_ATout.iloc[j].split('+')[0].split('(')[1])
        max_col_f_DI = float(max_raw_DI.iloc[j].split('+')[0].split('(')[1])
        max_col_f_ET = float(max_raw_ET.iloc[j].split('+')[0].split('(')[1])
        max_col_f_HI = float(max_raw_HI.iloc[j].split('+')[0].split('(')[1])
        max_col_f_HMI = float(max_raw_HMI.iloc[j].split('+')[0].split('(')[1])
        max_col_f_MDI = float(max_raw_MDI.iloc[j].split('+')[0].split('(')[1])
        max_col_f_NET = float(max_raw_NET.iloc[j].split('+')[0].split('(')[1])
        max_col_f_SAT = float(max_raw_SAT.iloc[j].split('+')[0].split('(')[1])
        max_col_f_sWBGT = float(max_raw_sWBGT.iloc[j].split('+')[0].split('(')[1])
        max_col_f_WBT = float(max_raw_WBT.iloc[j].split('+')[0].split('(')[1])
        max_col_f_WCT = float(max_raw_WCT.iloc[j].split('+')[0].split('(')[1])
        max_col_ATin.append(max_col_f_ATin)
        max_col_ATout.append(max_col_f_ATout)
        max_col_DI.append(max_col_f_DI)
        max_col_ET.append(max_col_f_ET)
        max_col_HI.append(max_col_f_HI)
        max_col_HMI.append(max_col_f_HMI)
        max_col_MDI.append(max_col_f_MDI)
        max_col_NET.append(max_col_f_NET)
        max_col_SAT.append(max_col_f_SAT)
        max_col_sWBGT.append(max_col_f_sWBGT)
        max_col_WBT.append(max_col_f_WBT)
        max_col_WCT.append(max_col_f_WCT)

    ATin_max = pd.DataFrame(max_col_ATin, columns=['ATin_max'])
    air_related = air_related.append(ATin_max.T)  # HiTIC_ATin_max
    ATout_max = pd.DataFrame(max_col_ATout, columns=['ATout_max'])
    air_related = air_related.append(ATout_max.T)  # HiTIC_ATout_max
    DI_max = pd.DataFrame(max_col_DI, columns=['DI_max'])
    air_related = air_related.append(DI_max.T)  # HiTIC_DI_max
    ET_max = pd.DataFrame(max_col_ET, columns=['ET_max'])
    air_related = air_related.append(ET_max.T)  # HiTIC_ET_max
    HI_max = pd.DataFrame(max_col_HI, columns=['HI_max'])
    air_related = air_related.append(HI_max.T)  # HiTIC_HI_max
    HMI_max = pd.DataFrame(max_col_HMI, columns=['HMI_max'])
    air_related = air_related.append(HMI_max.T)  # HiTIC_HMI_max
    MDI_max = pd.DataFrame(max_col_MDI, columns=['MDI_max'])
    air_related = air_related.append(MDI_max.T)  # HiTIC_MDI_max
    NET_max = pd.DataFrame(max_col_NET, columns=['NET_max'])
    air_related = air_related.append(NET_max.T)  # HiTIC_NET_max
    SAT_max = pd.DataFrame(max_col_SAT, columns=['SAT_max'])
    air_related = air_related.append(SAT_max.T)  # HiTIC_SAT_max
    sWBGT_max = pd.DataFrame(max_col_sWBGT, columns=['sWBGT_max'])
    air_related = air_related.append(sWBGT_max.T)  # HiTIC_sWBGT_max
    WBT_max = pd.DataFrame(max_col_WBT, columns=['WBT_max'])
    air_related = air_related.append(WBT_max.T)  # HiTIC_WBT_max
    WCT_max = pd.DataFrame(max_col_WCT, columns=['WCT_max'])
    air_related = air_related.append(WCT_max.T)  # HiTIC_WCT_max

    mean_col_ODIAC = []
    max_col_ODIAC = []
    mean_col_PM10 = []
    max_col_PM10 = []
    mean_col_PM25 = []
    max_col_PM25 = []
    mean_raw_ODIAC = ODIAC_mean_raw['mean']
    max_raw_ODIAC = ODIAC_max_raw['max']
    mean_raw_PM10 = PM10_mean_raw['mean']
    max_raw_PM10 = PM10_max_raw['max']
    mean_raw_PM25 = PM25_mean_raw['mean']
    max_raw_PM25 = PM25_max_raw['max']

    for j in range(0, len(mean_raw_ODIAC)):

        mean_col_f_ODIAC = float(mean_raw_ODIAC.iloc[j].split('+')[0].split('(')[1])
        max_col_f_ODIAC = float(max_raw_ODIAC.iloc[j].split('+')[0].split('(')[1])
        mean_col_f_PM10 = float(mean_raw_PM10.iloc[j].split('+')[0].split('(')[1])
        max_col_f_PM10 = float(max_raw_PM10.iloc[j].split('+')[0].split('(')[1])
        mean_col_f_PM25 = float(mean_raw_PM25.iloc[j].split('+')[0].split('(')[1])
        max_col_f_PM25 = float(max_raw_PM25.iloc[j].split('+')[0].split('(')[1])

        mean_col_ODIAC.append(mean_col_f_ODIAC)
        max_col_ODIAC.append(max_col_f_ODIAC)
        mean_col_PM10.append(mean_col_f_PM10)
        max_col_PM10.append(max_col_f_PM10)
        mean_col_PM25.append(mean_col_f_PM25)
        max_col_PM25.append(max_col_f_PM25)

    ODIAC_mean = pd.DataFrame(mean_col_ODIAC, columns=['mean_odiac'])
    ODIAC_max = pd.DataFrame(max_col_ODIAC, columns=['max_odiac'])
    PM10_mean = pd.DataFrame(mean_col_PM10, columns=['mean_pm10'])
    PM10_max = pd.DataFrame(max_col_PM10, columns=['max_pm10'])
    PM25_mean = pd.DataFrame(mean_col_PM25, columns=['mean_pm25'])
    PM25_max = pd.DataFrame(max_col_PM25, columns=['max_pm25'])

    air_related = air_related.append(ODIAC_mean.T)  # ODIAC_mean
    air_related = air_related.append(ODIAC_max.T)  # ODIAC_max
    air_related = air_related.append(PM10_mean.T)  # PM10_mean
    air_related = air_related.append(PM10_max.T)  # PM10_max
    air_related = air_related.append(PM25_mean.T)  # PM25_mean
    air_related = air_related.append(PM25_max.T)  # PM25_max

    air_related.index = ['FID', 'HR', 'HiTIC_ATin_mean', 'HiTIC_ATout_mean', 'HiTIC_DI_mean', 'HiTIC_ET_mean',
                         'HiTIC_HI_mean', 'HiTIC_HMI_mean', 'HiTIC_MDI_mean', 'HiTIC_NET_mean', 'HiTIC_SAT_mean',
                         'HiTIC_sWBGT_mean', 'HiTIC_WBT_mean', 'HiTIC_WCT_mean', 'HiTIC_ATin_max', 'HiTIC_ATout_max',
                         'HiTIC_DI_max', 'HiTIC_ET_max', 'HiTIC_HI_max', 'HiTIC_HMI_max', 'HiTIC_MDI_max',
                         'HiTIC_NET_max', 'HiTIC_SAT_max', 'HiTIC_sWBGT_max', 'HiTIC_WBT_max', 'HiTIC_WCT_max',
                         'ODIAC_mean', 'ODIAC_max', 'PM10_mean', 'PM10_max', 'PM25_mean', 'PM25_max']
    result = air_related.T
    result.to_excel(output_path + str(2013 + i) + '_air-related_statistics.xlsx', index=False)
print('All done!')
