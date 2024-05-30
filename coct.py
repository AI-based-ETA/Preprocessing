import pandas as pd


# 교통량과 콘존 데이터 호출
tr_data = pd.read_csv("5m_dataset/complete/4_12_complete.csv") #속도 데이터 셋 csv파일
final_csv_path_hmin = "5m_dataset/complete_complete/4.12(5m)_complete_complete.csv"#저장경로 설정
czn_data = pd.read_csv("from_to_cost(수정본csv).csv") #속도 데이터 셋에 관한 콘존 데이터 

# 두 데이터 병합 -> CZN_CD(콘존 ID)를 기준으로 해당 데이터에 맞게 병합
merged_data = pd.merge(tr_data, czn_data, on='CZN_CD', how='left')

# 교통량이 -1인 경우 예외 처리
merged_data['TRFFCVLM'] = merged_data['TRFFCVLM'].fillna(-1)

# 콘존ID에 맞게 병합
merged_data_sorted = merged_data.sort_values(by=['CZN_CD', 'SUM_HMIN'])

# COCT_CD(차로 유형 코드) 값의 총 교통량 합 (1=버스차로 2=승용차)
traffic_volume_total_sum_hmin = merged_data_sorted.groupby(['CZN_CD', 'SUM_HMIN'])['TRFFCVLM'].transform('sum')

# 두 차로에 관한 교통량 비율 조사
merged_data_sorted['TRFFCVLM_RATIO'] = merged_data_sorted['TRFFCVLM'] / traffic_volume_total_sum_hmin

# 가중 평균 계산 -> 교통량의 비율
merged_data_sorted['WEIGHTED_PASNG_RUNTM_MINS'] = merged_data_sorted['PASNG_RUNTM_MINS'] * merged_data_sorted['TRFFCVLM_RATIO']
merged_data_sorted['WEIGHTED_SPD_AVG'] = merged_data_sorted['SPD_AVG'] * merged_data_sorted['TRFFCVLM_RATIO']
merged_data_sorted['WEIGHTED_TRFFCVLM'] = merged_data_sorted['TRFFCVLM'] * merged_data_sorted['TRFFCVLM_RATIO']

# 콘존ID와 날짜&시간 에 맞게 비율 책정
final_weighted_metrics = merged_data_sorted.groupby(['CZN_CD', 'SUM_HMIN']).agg({
    'WEIGHTED_PASNG_RUNTM_MINS': 'sum',
    'WEIGHTED_SPD_AVG': 'sum',
    'WEIGHTED_TRFFCVLM': 'sum'
}).reset_index()

# 최종 병합된 데이터 준비
final_merged_data = merged_data_sorted[['CZN_CD', 'CZN_LENGTH', 'SUM_HMIN', 'ST_ND_ID', 'ST_ND_NM', 'END_ND_ID', 'END_ND_NM']].drop_duplicates()
final_merged_data = final_merged_data.merge(final_weighted_metrics, on=['CZN_CD', 'SUM_HMIN'], how='left')

# 설정한 경로로 저장
final_merged_data.to_csv(final_csv_path_hmin, index=False)