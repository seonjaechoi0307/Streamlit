# -*- coding:utf-8 -*-

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

# Font 관련 라이브러리
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Matplotlib에서 한글 폰트 설정
# 그래프에서 마이너스 폰트 깨지는 현상 방지
plt.rcParams['axes.unicode_minus'] = False

# Font Path Set
script_dir = os.path.dirname(__file__)
font_path = os.path.join(script_dir, "Fonts", "NanumGothic-Bold.ttf")

if os.path.isfile(font_path):
    font_name = fm.FontProperties(fname=font_path).get_name()
    # weight(폰트 굵기 종류) = 'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'.
    plt.rc('font', family=font_name, size=14, weight='semibold')
    print(f"한글 폰트 '{font_name}'이 설정되었습니다.")
else:
    print("폰트 파일을 찾을 수 없습니다.")

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