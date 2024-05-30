# Preprocessing lightGBM을 이용한 데이터 전처리, 인공지능에 활용할 DataSet으로의 변환

## 전처리 과정 사용 파일
### 1. OutlierPredict.ipynb
#### lightGBM을 이용한 TRFFCVLM, SPD_AVG 예측
VDS 데이터셋에서 특정 콘존에 대해 일부 값이 결측되거나, 특정 콘존의 VDS 데이터가 전부 결측되어 있는 문제가 발생

결측치를 삭제할것인가, 예측할 것인가에 대한 고민을 하였는데, 결론은 '예측'


예측을 하지 않으면, VDS 데이터가 전부 결측되어 있는 상황에는 그 콘존으로는 그래프 탐색이 불가능해지기 때문

#### Case A : 특정 콘존에 대해 데이터가 전부 결측된 경우, 일일히 주변 콘존의 데이터를 찾아서 주변 콘존의 데이터로 결측치를 예측
![image](https://github.com/AI-based-ETA/Preprocessing/assets/62549045/0f00bf14-b10d-4bc5-a603-78852905ab9a)

#### Case B : 특정 콘존에 대해 일부의 데이터만 결측된 경우, 해당 콘존의 데이터를 이용하여 결측치를 예측
![image](https://github.com/AI-based-ETA/Preprocessing/assets/62549045/91e55786-2e02-4173-9b97-25391ae08f16)

### 2. PASNG_RUNTM_predict.ipynb
##### 예측 이후, 데이터셋에서 인공지능에 학습시킬 때 필요한 속성인 PASNG_RUNTM을 계산, 필요없는 속성은 제거


### 3. transform_sumhmin.py
##### 날짜 변환
인공지능에서 해당 데이터셋을 사용할 수 있도록 날짜와 시간 형식 변환이 필요함

한국도로공사에서 제공해 준 날짜 -> 150 = 1시 50분

인공지능에서 요구하는 날짜 형식 { YYYY-MM-DD hh:mm:ss }


### 4. coct.py 
##### COCT_CD(차로 유형 구분 코드)값에 따른 가중 평균 속도 데이터 구하기
![image](https://github.com/AI-based-ETA/Preprocessing/assets/47581536/95b41f78-8a71-4035-9501-3f155e070578)

한국도로공사에서 제공하는 데이터셋은 차로 유형 구분 코드에 따라 데이터를 구분해 놓아, 한 콘존에서 두 가지의 COCT_CD 값에 따른 데이터가 두 종류로 존재. 어떤 데이터는 차로 유형 구분 코드가 1개(2), 어떤 데이터는 2개(1, 2)
(1=버스차로, 2=승용차)

처리 방법 : COCT_CD값이 1일 때와 2일 때의 교통량의 비율을 구해 해당 콘존에서의 속도를 두 값의 비율 가중 평균 속도 데이터를 구함
![image](https://github.com/AI-based-ETA/Preprocessing/assets/47581536/cc9e722c-9e13-4b19-9aa9-105e0fb7953e)

### 5. relocation.py
##### 인공지능에서 활용할 수 있도록 속도 데이터셋 형식 변환
Graph-WaveNet 기반으로 한 인공지능 모델에서 요구하는 데이터셋은 한 노드에서의 속도 측정값

하지만, 한국도로공사에서 제공하는 데이터셋은 한 구간에서의 평균 속도를 나타냄.

즉, 노드에서가 아닌 간선에서의 속도이므로, 해당 값을 노드에서의 속도로 변환하는 과정이 필요
![image](https://github.com/AI-based-ETA/Preprocessing/assets/47581536/b083e939-6715-4238-b80a-d25af8fa46d2)
활용한 방식 : 원하는 노드에서의 속도 = 해당 노드가 출발점일 때를 기준으로 해당 간선의 속도를 노드의 속도로 대입

만약, 해당 노드가 여러 간선에서의 출발점이 되는 노드라면, 해당 간선들의 교통량을 비교해 비율 가중 평균 속도값으로 책정
![image](https://github.com/AI-based-ETA/Preprocessing/assets/47581536/683ae71c-54b4-4dea-babb-11f8bdf90caf)
