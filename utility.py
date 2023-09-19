# -*- coding:utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import requests

def load_lottieurl(url) -> dict:
    r = requests.get(url)
    if r.status_code != 200:
        return st.sidebar.error("Lottie 파일을 가져오는 데 문제가 발생했습니다.")
    return r.json()

def plot_line_chart(x, y):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, marker='o', linestyle='-')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('line Plot')
    plt.xticks(rotation=90)  # x 축 라벨을 45도 회전하여 보기 편하게 설정
    plt.tight_layout()
    st.pyplot(f)

def plot_bar_chart(x, y):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x, y)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('bar Plot')
    plt.xticks(rotation=90)  # x 축 라벨을 45도 회전하여 보기 편하게 설정
    plt.tight_layout()
    st.pyplot(f)

# Scatter 차트 그리는 함수
def plot_scatter_chart(x, y):
    f, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('Scatter Plot')
    plt.xticks(rotation=90)  # x 축 라벨을 45도 회전하여 보기 편하게 설정
    plt.tight_layout()
    st.pyplot(f)

# box 차트 그리는 함수
def plot_box_chart(x, y):
    f, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=x, y=y, ax=ax)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('Box Plot')
    plt.xticks(rotation=90)  # x 축 라벨을 45도 회전하여 보기 편하게 설정
    plt.tight_layout()
    st.pyplot(f)

# heatmap 차트 그리는 함수
def plot_heatmap_chart(data, target_column):

    f, ax = plt.subplots(figsize=(8, 6))
    corrmat = data.corr()
    k = 10
    cols = corrmat.nlargest(k, target_column)[target_column].index
    cm = np.corrcoef(data[cols].values.T)
    
    # Seaborn 라이브러리 폰트 설정
    sns.set(font_scale=1.25)

    # 상관 관계 히트맵 그리기
    hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f',
                     annot_kws={'size': 10}, yticklabels=cols.values,
                     xticklabels=cols.values)
    
    ax.set_title('Correlation Heatmap plot')
    
    plt.tight_layout()
    st.pyplot(f)

    # hm = sns.heatmap 사용 옵션 정리
    #   corrmat = data.corr() = 데이터프레임 내의 변수들 간의 상관 관계를 계산하여 상관 계수(correlation coefficient)를 행렬 형태로 저장
    #   cm: 상관 관계 행렬을 입력 데이터로 지정합니다.
    #   cbar=True: 컬러 바(색상 막대)를 표시합니다.
    #   annot=True: 각 셀에 숫자 값을 표시합니다.
    #   square=True: 히트맵을 정사각형 모양으로 표시합니다.
    #   fmt='.2f': 숫자 값의 형식을 소수점 두 자리까지 표시하도록 지정합니다.
    #   annot_kws={'size': 10}: 히트맵에 표시되는 숫자의 크기를 조절합니다.
    #   yticklabels=cols.values, xticklabels=cols.values: 히트맵의 축 라벨에 cols 변수에 저장된 컬럼명을 사용합니다.

    