# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/My Drive/4.12.csv'
data = pd.read_csv(file_path)

data['TRFFCVLM'] = data['TRFFCVLM'].replace(-1,np.nan)
data['SPD_AVG'] = data['SPD_AVG'].replace(0,np.nan)

def predict_missing_values_lgbm(df, feature_col, target_col, is_integer=False):
    # 학습 데이터와 예측해야 할 데이터 분리
    train_data = df[df[target_col].notnull()]
    predict_data = df[df[target_col].isnull()]

    # 모델 학습
    model = LGBMRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(train_data[[feature_col]], train_data[target_col])

    # 결측치 예측
    if not predict_data.empty:
        predicted_values = model.predict(predict_data[[feature_col]])

        # 결과 형식 조정
        if is_integer:
            predicted_values = np.round(predicted_values).astype(int)
        else:
            predicted_values = np.round(predicted_values, 2)

        # 결측치 대체
        df.loc[df[target_col].isnull(), target_col] = predicted_values

# 'SUM_HMIN'을 기준으로 'TRFFCVLM'과 'SPD_AVG'의 결측치 예측
predict_missing_values_lgbm(data, 'SUM_HMIN', 'TRFFCVLM', is_integer=True)
predict_missing_values_lgbm(data, 'SUM_HMIN', 'SPD_AVG', is_integer=False)

updated_file_path = '/content/drive/My Drive/4_12_updated_lightGBM.csv'
data.to_csv(updated_file_path, encoding='utf-8')
