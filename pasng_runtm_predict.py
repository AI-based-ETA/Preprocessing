# -*- coding: utf-8 -*-
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

traffic_data_path = '/content/drive/My Drive/4_12_updated_lightGBM.csv'
traffic_data = pd.read_csv(traffic_data_path)

zone_distance_path = '/content/drive/My Drive/zone_distance.csv'
zone_distance_data = pd.read_csv(zone_distance_path)

columns_to_keep = [
    'SUM_YRMTHDAT', 'SUM_HMIN', 'CZN_CD', 'COCT_CD', 'TRFFCVLM', 'SPD_AVG',
    'PASNG_RUNTM_MINS', 'NMLT_CSCNT', 'REVISN_CSCNT', 'PSTM_STDV',
    'PASNG_TG_CAHNGE_CFFCN', 'MAX_PASNG_TM_MINS', 'MEDIAN_PASNG_TM_MINS',
    'MINM_PASNG_TM_MINS', 'F15T85_PASNG_RUNTM_QNTL'
]

merged_data = pd.merge(traffic_data, zone_distance_data[['CZN_CD', 'CZN_LENGTH']], on='CZN_CD', how='left')

condition = merged_data['PASNG_RUNTM_MINS'] == 0
merged_data.loc[condition, 'PASNG_RUNTM_MINS'] = (
    (merged_data['CZN_LENGTH'] / (merged_data['SPD_AVG'] * 1000 / 3600))
    .where(condition)
    .fillna(0)  # 계산 불가능한 경우를 대비하여 NaN 값을 0으로 채움
    .astype(int)  # 결과를 정수형으로 변환
)

updated_file_path = '/content/drive/My Drive/4_12_complete.csv'
merged_data = merged_data.drop(columns=[col for col in merged_data.columns if col not in columns_to_keep])
merged_data.to_csv(updated_file_path, index=False, encoding='utf-8')
