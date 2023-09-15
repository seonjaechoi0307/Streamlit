# -*- coding:utf-8 -*-

import streamlit as st
# wide mode로 페이지 설정
st.set_page_config(
    page_title = "3Team_Project",
    # 이모지 사이트 : https://www.emojiall.com/ko/emoji/
    page_icon = "🏦",
    initial_sidebar_state="expanded",
    layout="wide"
    )

import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import plotly
import requests
import utility
from streamlit_folium import st_folium
from streamlit_lottie import st_lottie

# 다른 어플에서 함수 호출하기
# 어플만 호출해도 함수는 사용 가능하다 하지만 유지보수 및 모든 함수 및 객체를 갖고오면 네임스페이스가 혼란스러워질 수 있다함(in Chat GPT)
from utility import plot_line_chart
from utility import plot_bar_chart
from eda_app import run_eda_app
from MapInfra import Create_Map

# 함수
def main():
    st.markdown("# 3Team Project : 부동산 전세가격 예측 및 전세가율 분석")
    # 구분선 추가
    st.markdown('---')

    with st.sidebar:
        # Sidebar animation
        lottie_url = "https://assets-v2.lottiefiles.com/a/f02fd2fc-1178-11ee-b799-df4a4787e702/cyDf6xxWfS.json"
        lottie_json = utility.load_lottieurl(lottie_url)
        st_lottie(lottie_json, speed=0.1, height=200, key="initial", quality="low")
        st.markdown(
            "<h2 style='text-align: center; color: Black;'>Team Name : 건물주 </h2>",
            unsafe_allow_html=True,
        )
        menu = ["Home", "EDA", "ML", "Chart", "서비스 제공자"]
        choice = st.sidebar.selectbox("Menu", menu)

    if choice == ("Home"):
        with st.expander("Create Map Section", expanded=True):
            col1, col2 = st.columns(2)

            with col1 :
                # 맵 생성
                Create_Map()

            with col2 :
                st.write("인프라 목록화 준비중...")

        # with = Python 컨텍스트 관리자(Context Managter), 작업의 시작과 끝 정의 및 리소스 할당 및 해제 관리하기 위해 사용
        with st.expander("Chart Section", expanded=False):
            # 두 개의 컬럼 생성
            col1, col2 = st.columns(2)

            # 첫 번째 컬럼에 차트 추가
            with col1 :
                st.markdown("<h4>OOO 차트</h4>", unsafe_allow_html=True)
                x = np.arange(0, 10, 0.1)
                y = np.cos(x)
                x_label = 'X 축'
                y_label = 'Y 축'
                title = '선 그래프'
                f1 = plot_line_chart(x, y, x_label, y_label, title)
                st.pyplot(f1)

            # 두 번째 컬럼에 차트 추가
            with col2 :
                st.markdown("<h4>OOO 차트</h4>", unsafe_allow_html=True)
                x = np.arange(5)
                y = [10, 15, 7, 12, 5]
                x_label = ['1차', '2차', '3차', '4차', '5차']
                y_label = 'Data Value'
                title = 'Second Bar Chart'
                f2 = plot_bar_chart(x, y, x_label, y_label, title)
                st.pyplot(f2)

        with st.expander("Stock Section", expanded=False):
            # 두 개의 컬럼 생성
            col1, col2 = st.columns(2)

            # 첫 번째 컬럼에 차트 추가
            with col1 :
                st.markdown("<h4>이동평균 차트</h4>", unsafe_allow_html=True)

                # 데이터 프레임 생성 (예제 데이터)
                data = pd.DataFrame({'Date': ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06'],
                                    'JS_Price': [100, 150, 140, 130, 120, 110, ]})

                # 이동평균 계산 함수
                def calculate_moving_average(data, window_size):
                    return data.rolling(window=window_size).mean()

                # 트렌드선 계산 함수
                def calculate_trend_line(data):
                    x = np.arange(len(data))
                    y = data.values
                    coefficients = np.polyfit(x, y, 1)
                    trend_line = np.poly1d(coefficients)
                    return trend_line(x)

                # 이동평균 윈도우 크기 선택
                window_size = st.slider('Select Moving Average Window Size:', 2, 20, 7)

                # 이동평균 계산
                data['MovingAverage'] = calculate_moving_average(data['JS_Price'], window_size)

                # 트렌드선 계산
                data['TrendLine'] = calculate_trend_line(data['JS_Price'])

                # 선 차트 그리기
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(data['Date'], data['JS_Price'], label='JS_Price', color='b')
                ax.plot(data['Date'], data['MovingAverage'], label=f'{window_size}-Day Moving Average', color='g')
                ax.plot(data['Date'], data['TrendLine'], label='Trend Line', color='r')
                ax.set_xlabel('Date 데이트')
                ax.set_ylabel('JS_Price 전세가격')
                ax.set_title('JS_Price Moving Average and Trend Line 전세가격 이동평균 트렌드 선 차트')
                ax.legend()
                st.pyplot(fig)

            # 두 번째 컬럼에 차트 추가
            with col2 :
                st.markdown("<h4>OOO 차트</h4>", unsafe_allow_html=True)
                x = np.arange(5)
                y = [10, 15, 7, 12, 5]
                x_label = ['1차', '2차', '3차', '4차', '5차']
                y_label = 'Data Value'
                title = 'Second Bar Chart'
                f2 = plot_bar_chart(x, y, x_label, y_label, title)
                st.pyplot(f2)

        with st.expander("ML Section", expanded=True) :
            st.subheader("머신러닝 예측 데이터")
            
    elif choice == "EDA" :
        run_eda_app()
    elif choice == "ML" :
        st.subheader("ML")
    elif choice == "Chart" :
        st.subheader("Chart")
    elif choice == "서비스 제공자" :
        st.image("./image/Service_Provider.png")
    else :
        pass

# 메인
if __name__ == "__main__" :
    main()