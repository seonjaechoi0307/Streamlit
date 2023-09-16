import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
from prophet import Prophet

def run_ml_app():
    st.subheader("머신 러닝 페이지")

    # 레이아웃 구성
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("날짜를 선택하세요.")
        selected_date = st.select_slider("날짜", options=np.arange(1, 1096))
        selected_date_list = [selected_date]
        st.write(selected_date_list)

    with col2:
        st.subheader("모델 결과 확인")

        # Prophet 모델 불러오기
        model_file_path = "./models/Prophet_model_230916.pkl"
        loaded_model = joblib.load(open(os.path.join(model_file_path), "rb"))
        # st.write(loaded_model)

        # 도움말 숨기기
        # st.help(loaded_model)

        # 미래 날짜 생성 (Prophet 모델의 예측 범위 내에서)
        future_dates = loaded_model.make_future_dataframe(periods=365 * 3)

        # 선택한 날짜에 대한 예측값 추출
        selected_date_prediction = loaded_model.predict(future_dates.iloc[[selected_date - 1]])

        # 예측값 출력
        st.write(f"선택한 날짜({selected_date})의 예측 가격: {selected_date_prediction['yhat'].values[0]}")