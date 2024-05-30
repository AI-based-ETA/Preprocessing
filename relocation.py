import pandas as pd
import numpy as np

# 데이터셋 호출
updated_data = pd.read_csv('5m_dataset/tr_sumhmin/updated_data5(4.11).csv')
save_filepath = "5m_dataset/relocation/4.11relocation.csv" # 저장 데이터셋 경로 설정
# 교통량에 따른 데이터셋 가중치 설정 -> 평균 속도를 노드에서의 교통량을 비교해 가중 평균
node_speed_data = updated_data.groupby(['ST_ND_ID', 'DateTime']).apply(
    lambda x: np.average(x['WEIGHTED_SPD_AVG'], weights=x['WEIGHTED_TRFFCVLM'])
).reset_index(name='Weighted_Avg_Spd')

# 컬럼 이름 재설정
node_speed_data.columns = ['Node_ID', 'DateTime', 'Weighted_Avg_Spd']

# 컬럼(날짜 & 시간), 노드 번호에 대한 속도 값 배치
node_speed_pivoted = node_speed_data.pivot(index='DateTime', columns='Node_ID', values='Weighted_Avg_Spd')

# 앞에서 설정한 경로로 csv로 저장

node_speed_pivoted.to_csv(save_filepath)