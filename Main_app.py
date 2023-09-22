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
import requests
import utility
from streamlit_lottie import st_lottie
import lightgbm as lgb

# 다른 어플에서 함수 호출하기
# 어플만 호출해도 함수는 사용 가능하다 하지만 유지보수 및 모든 함수 및 객체를 갖고오면 네임스페이스가 혼란스러워질 수 있다함(in Chat GPT)
from EDA_app import run_eda_app
from EDA_app import run_eda_app2
from Home_app import Create_Map
from Home_app import Regional_Infrastructure
from Test_ml_app import run_ml_app
from Test_ml_app import run_VP_app
from ML_app import layout_ml_LightGBM_app

# folium 관련 경고 무시
import warnings
from folium import folium

# Folium의 FutureWarning 경고 무시
warnings.simplefilter(action="ignore", category=FutureWarning)

# Font 관련 라이브러리
import matplotlib.font_manager as fm
import os

# Matplotlib에서 한글 폰트 설정
# 그래프에서 마이너스 폰트 깨지는 현상 방지
plt.rcParams['axes.unicode_minus'] = False

@st.cache_data()
def set_custom_font():
    # Custom Fonts 디렉토리 경로 설정
    font_dir = os.path.join(os.getcwd(), "Fonts")

    # Custom Fonts 디렉토리 내의 모든 폰트 파일 경로 가져오기
    font_files = fm.findSystemFonts(fontpaths=[font_dir])

    if font_files:
        # 첫 번째 폰트 파일을 사용하거나 다른 원하는 폰트를 선택하세요.
        selected_font_path = font_files[0]
        font_name = fm.FontProperties(fname=selected_font_path).get_name()

        # 폰트 매니저에 선택한 폰트 추가
        fm.fontManager.addfont(selected_font_path)

        # Matplotlib 폰트 설정
        plt.rcParams['font.family'] = font_name
        plt.rcParams['font.size'] = 12
        plt.rcParams['font.weight'] = 'semibold'

        print(f"한글 폰트 '{font_name}'이 설정되었습니다.")
    else:
        print("Fonts 디렉토리에서 사용 가능한 폰트 파일을 찾을 수 없습니다.")

# 한글 폰트 설정 함수 호출
set_custom_font()

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
        menu = ["🏛️ 홈페이지", "📊 데이터 분석", "⚙️ 전세가격 예측", "임시메뉴", "🥇 서비스 제공자"]
        choice = st.sidebar.selectbox("Menu", menu)

    if choice == ("🏛️ 홈페이지"):
        Create_Map()
        Regional_Infrastructure()
        run_eda_app2()
            
    elif choice == "📊 데이터 분석" :
        run_eda_app()

    elif choice == "⚙️ 전세가격 예측" :
        st.subheader("머신 러닝 페이지")
        run_ml_app()
        run_VP_app()

    elif choice == "임시메뉴" :
        st.write("<h4>Light GBM 알고리즘을 활용한 전세가격 예측모델</h4>", unsafe_allow_html=True)
        layout_ml_LightGBM_app()

    elif choice == "🥇 서비스 제공자" :
        st.image("./image/Service_Provider.png")

    else :
        pass

# 메인
if __name__ == "__main__" :
    main()