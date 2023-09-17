# -*- coding:utf-8 -*-

import streamlit as st
import joblib
import os
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet

# 전역 변수 설정
selected_date = None
model_file_path = None
Data_path = './models'
File_name = None
loaded_model = None

# 예측 모델 불러오는 함수
def Model_data_load():

    # Prophet 모델 불러오기
    model_file_path = Data_path + File_name
    loaded_model = joblib.load(open(os.path.join(model_file_path), "rb"))
    return loaded_model

# 예측 모델 예측값 표기 함수
def make_ml_app():

    # Prophet 모델 불러오기
    loaded_model = Model_data_load()

    # st.write(loaded_model) >> 모델 이름 표기하니까 도움말이 자동으로 떠서 주석처리함

    # 미래 날짜 생성 (Prophet 모델의 예측 범위 내에서)
    future_dates = loaded_model.make_future_dataframe(periods=365 * 3)

    # 선택한 날짜에 대한 예측값 추출
    selected_date_prediction = loaded_model.predict(future_dates.iloc[[selected_date - 1]])

    # 예측값 출력
    return st.write(f"선택한 Date 값({selected_date})의 예측 가격: {selected_date_prediction['yhat'].values[0]}")

# 예측 모델 불러와서 옵션값에 따라 예측 가격 표시하기
def run_ml_app():

    with st.expander("ML_Predictions_Section", expanded=True):

        # 전역 변수로서 selected_date를 사용
        global selected_date
        global File_name

        # 레이아웃 구성
        tab1, tab2, tab3 = st.tabs(["ML to Apart", "ML to Officetel", "ML to Townhouse"])

        with tab1 :
            col1, col2 = st.columns(2)
            with col1:

                st.subheader("아파트 가격 예측")
                selected_date = st.select_slider("Option : Day", options=np.arange(1, 1096), key="ML_APT_Slider")
                selected_date_list = [selected_date]

            with col2:
                st.subheader("모델 결과 확인")

                # 아파트 예측모델 불러오기 위한 File_name 전역 변수화
                File_name = '/Prophet_model_230916_APT_.pkl'
                make_ml_app()

        with tab2 :
            col1, col2 = st.columns(2)
            with col1:

                st.subheader("오피스텔 가격 예측")
                selected_date = st.select_slider("Option : Day", options=np.arange(1, 1096), key="ML_OFC_Slider")
                selected_date_list = [selected_date]

            with col2:
                st.subheader("모델 결과 확인")

                # 아파트 예측모델 불러오기 위한 File_name 전역 변수화
                File_name = '/Prophet_model_230916_OFC_.pkl'
                make_ml_app()

        with tab3 :
            col1, col2 = st.columns(2)
            with col1:
                

                st.subheader("타운하우스 가격 예측")
                selected_date = st.select_slider("Option : Day", options=np.arange(1, 1096), key="ML_TWN_Slider")
                selected_date_list = [selected_date]

            with col2:
                st.subheader("모델 결과 확인")

                # 아파트 예측모델 불러오기 위한 File_name 전역 변수화
                File_name = '/Prophet_model_230916_TWN_.pkl'
                make_ml_app()

# Visualize_Predictions = 예측 시각화
# def make_VP_app():

def load_Model_df():
    # 데이터 프레임 Check
    loaded_model = Model_data_load()

    # 미래 날짜 생성 (Prophet 모델의 예측 범위 내에서)
    future_dates = loaded_model.make_future_dataframe(periods=365 * 3)
    
    # 데이터 all_predictions 함수에 불러와서 데이터 프레임화 시키기
    all_predictions = loaded_model.predict(future_dates)
    all_predictions_df = pd.DataFrame(all_predictions)

    # 데이터 출력
    st.write(all_predictions_df)

def Model_data_Visualization():
    loaded_model = Model_data_load()

    # 미래 날짜 생성 (Prophet 모델의 예측 범위 내에서)
    future_dates = loaded_model.make_future_dataframe(periods=365 * 3)

    # 데이터 all_predictions 함수에 불러와서 데이터 프레임화 시키기
    all_predictions = loaded_model.predict(future_dates)
    all_predictions_df = pd.DataFrame(all_predictions)

    # "Date" 열을 날짜 및 시간 형식으로 변환합니다 (만약 이미 날짜 형식이 아닌 경우에만).
    all_predictions_df['ds'] = pd.to_datetime(all_predictions_df['ds'])

    # "Date" 열에서 일(day)이 1일 (월의 첫 번째 날)인 행(row)들만 추출합니다.
    all_predictions_df = all_predictions_df[all_predictions_df['ds'].dt.day == 1]

    # Plot Setting
    f, ax = plt.subplots(figsize=(60, 40))
    ax.plot(all_predictions_df['ds'], all_predictions_df['yhat'], linewidth=10)
    ax.set_xlabel('Date', fontsize=48)
    ax.set_ylabel('Predicte Price', fontsize=48)
    ax.set_title('Predicted Price Over Time', fontsize=48)
    ax.tick_params(axis='x', rotation=45)

    # x-축의 눈금(틱)을 월별 시작일을 1일 간격으로 설정
    monthly_ticks = pd.date_range(start=all_predictions_df['ds'].min(), end=all_predictions_df['ds'].max(), freq='MS')
    plt.xticks(monthly_ticks, [date.strftime('%Y-%m-%d') for date in monthly_ticks], rotation=45)

    # 4개월, 8개월, 12개월 이동평균 계산
    for monthly_ticks in [4, 8, 12]:

        # monthly_ticks 단위로 이동평균 컬럼 만들기
        ma_column = f'ma_{monthly_ticks}'
        all_predictions_df[ma_column] = ta.sma(all_predictions_df['yhat'], length=monthly_ticks)

    # 추세선 및 이동평균선 그리기
    ax.plot(all_predictions_df['ds'], all_predictions_df['trend'], linewidth=4, linestyle='--', color='red', label='Trend')
    ax.plot(all_predictions_df['ds'], all_predictions_df['ma_4'], linewidth=4, linestyle='--', color='green', label='ma_120')
    ax.plot(all_predictions_df['ds'], all_predictions_df['ma_8'], linewidth=4, linestyle='--', color='orange', label='ma_240')
    ax.plot(all_predictions_df['ds'], all_predictions_df['ma_12'], linewidth=4, linestyle='--', color='purple', label='ma_360')

    # 출력
    ax.legend(loc=2, fontsize=52) # 1=좌상단, 2=우상단, 3=좌하단, 4=우하단
    ax.grid(True)
    st.pyplot(f)

def Model_data_RSI():
    loaded_model = Model_data_load()

    # 미래 날짜 생성 (Prophet 모델의 예측 범위 내에서)
    future_dates = loaded_model.make_future_dataframe(periods=365 * 3)

    # 데이터 all_predictions 함수에 불러와서 데이터 프레임화 시키기
    all_predictions = loaded_model.predict(future_dates)
    all_predictions_df = pd.DataFrame(all_predictions)

    # "Date" 열을 날짜 및 시간 형식으로 변환합니다 (만약 이미 날짜 형식이 아닌 경우에만).
    all_predictions_df['ds'] = pd.to_datetime(all_predictions_df['ds'])

    # "Date" 열에서 일(day)이 1일 (월의 첫 번째 날)인 행(row)들만 추출합니다.
    all_predictions_df = all_predictions_df[all_predictions_df['ds'].dt.day == 1]

    # Plot Setting
    f, ax = plt.subplots(figsize=(10, 4))
    ax.plot(all_predictions_df['rsi_14'])
    ax.axhline(y=40, color='r', linestyle='--', label='RSI 40')
    ax.axhline(y=60, color='g', linestyle='--', label='RSI 60')
    ax.axhline(y=all_predictions_df['rsi_14'].mean(), color='b', linestyle='--', label='RSI Mean')

    # x-축의 눈금(틱)을 월별 시작일을 1일 간격으로 설정
    monthly_ticks = pd.date_range(start=all_predictions_df['ds'].min(), end=all_predictions_df['ds'].max(), freq='MS')
    plt.xticks(monthly_ticks, [date.strftime('%Y-%m-%d') for date in monthly_ticks], rotation=45)

    # 상대강도지수 (RSI) 지표 계산
    all_predictions_df['rsi_14'] = ta.rsi(monthly_ticks, length=1)

    ax.set_title('상대강도지수 (RSI) 지표 계산')
    ax.set_xlabel('Date')
    ax.set_ylabel('RSI Value')

    # 출력
    ax.legend(loc=1, fontsize=12) # 1=좌상단, 2=우상단, 3=좌하단, 4=우하단
    ax.grid(True)
    st.pyplot(f)


def run_VP_app():

    with st.expander("Model_DataFrame_Section", expanded=False):
        
        # 전역변수 설정
        global File_name, selected_date

        # 레이아웃 구성
        tab1, tab2, tab3 = st.tabs(["ML to Apart_DF", "ML to Officetel_DF", "ML to Townhouse_DF"])

        with tab1 :
            File_name = '/Prophet_model_230916_APT_.pkl'
            load_Model_df()

        with tab2 :
            File_name = '/Prophet_model_230916_OFC_.pkl'
            load_Model_df()

        with tab3 :
            File_name = '/Prophet_model_230916_TWN_.pkl'
            load_Model_df()
        
    with st.expander("Visualize_Predictions_Section", expanded=False):
        
        # 레이아웃 구성
        tab1, tab2, tab3 = st.tabs(["Apart Plot", "Officetel Plot", "Townhouse Plot"])

        with tab1 :
            st.write("아파트 가격 예측 시각화")
            File_name = '/Prophet_model_230916_APT_.pkl'
            Model_data_load()
            Model_data_Visualization()

        with tab2 :
            st.write("오피스텔 가격 예측 시각화")
            File_name = '/Prophet_model_230916_OFC_.pkl'
            Model_data_load()
            Model_data_Visualization()


        with tab3 :
            st.write("타운하우스 가격 예측 시각화")
            File_name = '/Prophet_model_230916_TWN_.pkl'
            Model_data_load()
            Model_data_Visualization()

def RSI():
    with st.expander("Predictions_RSI_Section", expanded=False):
        
        # 레이아웃 구성
        tab1, tab2, tab3 = st.tabs(["Apart Plot", "Officetel Plot", "Townhouse Plot"])

        with tab1 :
            st.write("아파트 가격 예측 시각화")
            File_name = '/Prophet_model_230916_APT_.pkl'
            Model_data_load()

        with tab2 :
            st.write("오피스텔 가격 예측 시각화")
            File_name = '/Prophet_model_230916_OFC_.pkl'
            Model_data_load()


        with tab3 :
            st.write("타운하우스 가격 예측 시각화")
            File_name = '/Prophet_model_230916_TWN_.pkl'
            Model_data_load()

