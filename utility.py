# -*- coding:utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import requests

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
        plt.rcParams['font.size'] = 14
        plt.rcParams['font.weight'] = 'semibold'

        print(f"한글 폰트 '{font_name}'이 설정되었습니다.")
    else:
        print("Custom Fonts 디렉토리에서 사용 가능한 폰트 파일을 찾을 수 없습니다.")

# 한글 폰트 설정 함수 호출
set_custom_font()

def load_lottieurl(url) -> dict:
    r = requests.get(url)
    if r.status_code != 200:
        return st.sidebar.error("Lottie 파일을 가져오는 데 문제가 발생했습니다.")
    return r.json()

def plot_line_chart(x, y, x_label, y_label, title):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, marker='o', linestyle='-')
    ax.set_xlabel(x_label)#, fontproperties=font_prop
    ax.set_ylabel(y_label)
    ax.set_title(title)
    return f

def plot_bar_chart(x, y, x_label, y_label, title):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_label)
    return f