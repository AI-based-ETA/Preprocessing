import pandas as pd

# CSV파일 호출 및 저장 경로 설정
file_path = "5m_dataset/complete_complete/4.11(5m)_complete_complete.csv"
save_filepath = "5m_dataset/tr_sumhmin/updated_data5(4.11).csv"
data = pd.read_csv(file_path)

# 날짜 형식 바꾸기 -> { YYYY-MM-DD hh:mm:ss }
def hhmm_to_datetime(hhmm):
    #데이터 원본 예시
    # 150 => 1시 50분
    hour = hhmm // 100  # 시간 추출
    minute = hhmm % 100  # 분 추출
    return pd.to_datetime(f'2024-04-11 {hour}:{minute}:00') #반환

# 바꾼 값 적용
data['DateTime'] = data['SUM_HMIN'].apply(hhmm_to_datetime)

# CSV파일 저장
data.to_csv(save_filepath, index=False)

# 저장된 예시 보기 (헤더부분)
print(data[['SUM_HMIN', 'DateTime']].head())