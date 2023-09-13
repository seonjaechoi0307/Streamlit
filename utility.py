import streamlit as st
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

# Font
import os
import matplotlib.font_manager as fm

# 한글 폰트 경로 설정 (설치한 폰트의 경로를 지정)
fpath = os.path.join(os.getcwd(), "Fonts/NanumGothic-Bold.ttf")
prop = fm.FontProperties(fname=fpath)
plt.rc('font', family=prop.get_name())

def load_lottieurl(url) -> dict:

    r = requests.get(url)
    if r.status_code != 200:
        return st.sidebar.error("Lottie 파일을 가져오는 데 문제가 발생했습니다.")
    return r.json()

def plot_line_chart(x, y, x_label, y_label, title):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, marker='o', linestyle='-')
    ax.set_xlabel(x_label, fontproperties=prop)
    ax.set_ylabel(y_label, fontproperties=prop)
    ax.set_title(title, fontproperties=prop)
    return f

def plot_bar_chart(x, y, x_label, y_label, title):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x, y)
    ax.set_xlabel(x_label, fontproperties=prop)
    ax.set_ylabel(y_label, fontproperties=prop)
    ax.set_title(title, fontproperties=prop)
    ax.set_xticks(x)
    ax.set_xticklabels(x_label)
    return f

def plot_moving_average(data, x_column, y_column, window_length):
    data = data[[x_column, y_column]]
    data['이동평균'] = ta.sma(data[y_column], length=window_length)
    return data

'''def plot_moving_average(data, x_column, y_column, window_length):

    """
    이동평균 그래프를 생성하는 함수

    Parameters:
        data : 데이터프레임
        x_column (str): x 축으로 사용할 컬럼 이름
        y_column (str): y 축으로 사용할 컬럼 이름
        window_length (int): 이동평균 창 길이

    Returns:
        None (그래프를 표시)
    """

    # 데이터프레임에서 필요한 컬럼 선택
    data = data[[x_column, y_column]]

    # 이동평균 계산
    data['이동평균'] = ta.sma(data[y_column], length=window_length)

    # 그래프 그리기
    f, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data[y_column], label=y_column, marker='o')
    ax.plot(data.index, data['이동평균'], label=f'{window_length}일 이동평균', linestyle='--')
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f'{y_column} 및 {window_length}일 이동평균 그래프')
    ax.legend()
    ax.grid(True)
    return f, ax'''