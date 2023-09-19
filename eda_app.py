# -*- utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

# utility.py에서 함수 갖고오기
from utility import plot_line_chart
from utility import plot_bar_chart
from utility import plot_scatter_chart
from utility import plot_box_chart
from utility import plot_heatmap_chart

def run_eda_app():

    st.subheader("탐색적 자료 분석 페이지")
    data = pd.read_csv("./data/month_at.csv")

    tab1, tab2, tab3 = st.tabs(["📈 Chart", "📘 Data", "📄 ETC"])

    with tab1 :
        with st.expander("Option Select Section", expanded=True) :
            col1, col2 = st.columns([1, 2])

            with col1 :
                st.markdown("<h4>옵션 선택</h4>", unsafe_allow_html=True)
                
                # 데이터 프레임의 컬럼 목록을 옵션으로 사용
                # key = 고유 세션값 (셀렉박스 연속 구현 시 오류를 방지하기 위한 고유 세션값 주기)
                options1 = data.columns.tolist()
                selected_option1 = st.selectbox("Y 컬럼을 선택하세요 : ", options1, key="SelectBox_1")

                options2 = data.columns.tolist()
                selected_option2 = st.selectbox("X 컬럼을 선택하세요 : ", options2, key="SelectBox_2")

                options3 = ['plot_line_chart', 'plot_bar_chart', 'plot_scatter_chart', 'plot_box_chart', 'plot_heatmap_chart']
                selected_option3 = st.selectbox("시각화 종류를 선택하세요 : ", options3, key="SelectBox_3")
            
            with col2 :
                st.markdown("<h4>시각화</h4>", unsafe_allow_html=True)

                # Select options to Graph Setting
                y = data[selected_option1]
                x = data[selected_option2]

                if (selected_option1 == selected_option2) :
                    st.write("X와 Y의 값이 같습니다.")

                elif (selected_option3 == 'plot_line_chart'):
                    plot_line_chart(x, y)

                elif (selected_option3 == 'plot_bar_chart'):
                    plot_bar_chart(x, y)

                elif (selected_option3 == 'plot_scatter_chart'):
                    plot_scatter_chart(x, y)

                elif (selected_option3 == 'plot_box_chart'):
                    plot_box_chart(x, y)

                elif (selected_option3 == 'plot_heatmap_chart'):
                    target_column = selected_option1
                    plot_heatmap_chart(data, target_column)

                else:
                    pass

    with tab2 :
        st.dataframe(data, height=500)
        with st.expander("Column List", expanded=False) :
            st.write("해당 데이터 프레임의 컬럼 리스트")
            st.write(data.columns.tolist())

    with tab3 :
        # 선택한 옵션을 기반으로 데이터프레임 필터링
        # filtered_column = pd.concat([data[selected_option1], data[selected_option2]], axis=1)

        # 선택한 옵션과 열 데이터를 목록으로 출력
        st.write("선택한 옵션:", selected_option1)
        st.write("열 데이터 목록:")
        st.write(data[selected_option1])

def make_chart_EGR_IR(df):
    
    # Economic Growth and Interest Rates : 경제성장률 and 금리
    # 전처리 데이터 이름 >>> df = pd.read_csv('lr_uer_merged.csv')
    
    # 년, 월 컬럼값 정수로 변환 및 날짜라는 컬럼에 년, 월 데이터 합친 값 넣기
    df['년'] = df['년'].astype(int)
    df['월'] = df['월'].astype(int)
    df['날짜'] = df['년'].astype(str) + '.' + df['월'].astype(str)

    plt.figure(figsize=(30, 16))
    plt.plot(df['날짜'], df['금리'], marker='o', label='금리', linestyle='-')
    plt.plot(df['날짜'], df['실업률'], marker='o', label='실업률', linestyle='-')

    plt.title('금리와 실업률')
    plt.xlabel('날짜')
    plt.grid()
    plt.xticks(rotation=45)

    plt.xlim(['2011.1', '2023.7'])
    plt.legend()
    st.pyplot(plt)

def make_chart_ECI(df):

    # Economic Composite Index : 경제 종합 지수
    # 전처리 데이터 이름 >>> df = pd.read_csv('경기종합지리_전처리완료.csv')

    # 년, 월 컬럼값 정수로 변환 및 날짜라는 컬럼에 년, 월 데이터 합친 값 넣기
    df['날짜'] = df['년'].astype(str) + '.' + df['월'].astype(str)

    plt.figure(figsize=(30, 16))
    plt.plot(df['날짜'], df['선행종합지수(2020=100)'], marker='o', label='선행종합지수', linestyle='-')  # 선 그래프 그리기
    plt.plot(df['날짜'], df['동행종합지수(2020=100)'], marker='o', label='동행종합지수', linestyle='-')
    plt.plot(df['날짜'], df['후행종합지수(2020=100)'], marker='o', label='후행종합지수', linestyle='-')

    plt.title('경기종합지수')
    plt.xlabel('날짜')

    plt.grid(True)
    plt.xticks(rotation=45)

    plt.xlim(['2011.1', '2023.7'])
    plt.legend()
    st.pyplot(plt)

def make_chart_CR(df):
    
    # Crime Rate : 범죄율
    # 전처리 데이터 이름 >>> df = pd.read_csv('서울시5대범죄전처리완료.csv')

    df_must = df[["년도", "자치구별", "범죄율"]]

    x = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구",
        "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구",  "금천구",
        "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

    y1 = df_must[df_must["년도"] == 2014]["범죄율"]
    y2 = df_must[df_must["년도"] == 2015]["범죄율"]
    y3 = df_must[df_must["년도"] == 2016]["범죄율"]
    y4 = df_must[df_must["년도"] == 2017]["범죄율"]
    y5 = df_must[df_must["년도"] == 2018]["범죄율"]
    y6 = df_must[df_must["년도"] == 2019]["범죄율"]
    y7 = df_must[df_must["년도"] == 2020]["범죄율"]
    y8 = df_must[df_must["년도"] == 2021]["범죄율"]


    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(x, y1, label='2014')
    plt.plot(x, y2, label='2015')
    plt.plot(x, y3, label='2016')
    plt.plot(x, y4, label='2017')
    plt.plot(x, y5, label='2018')
    plt.plot(x, y6, label='2019')
    plt.plot(x, y7, label='2020')
    plt.plot(x, y8, label='2021')

    plt.title('자치구별 범죄율')
    plt.xticks(rotation=80, ha='right')

    plt.xlim(['종로구', '강동구'])
    plt.ylim([500, 4000])

    plt.legend()
    plt.grid()
    st.pyplot(fig)

def make_chart_PBA(df):
    
    # Population by age : 연령별 인구수
    # 전처리 데이터 이름 >>> df = pd.read_csv('서울_연령별_인구수_전처리.csv')

    x = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구",
        "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구",  "금천구",
        "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

    y1 = df[(df["시점"] == 2014) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y2 = df[(df["시점"] == 2015) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y3 = df[(df["시점"] == 2016) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y4 = df[(df["시점"] == 2017) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y5 = df[(df["시점"] == 2018) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y6 = df[(df["시점"] == 2019) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y7 = df[(df["시점"] == 2020) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y8 = df[(df["시점"] == 2021) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]
    y9 = df[(df["시점"] == 2022) & (df["행정구역(시군구)별"] != "서울특별시")]["계"]


    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(x, y1, label='2014')
    plt.plot(x, y2, label='2015')
    plt.plot(x, y3, label='2016')
    plt.plot(x, y4, label='2017')
    plt.plot(x, y5, label='2018')
    plt.plot(x, y6, label='2019')
    plt.plot(x, y7, label='2020')
    plt.plot(x, y8, label='2021')
    plt.plot(x, y9, label='2022')

    plt.title("서울시 인구수")
    plt.xticks(rotation=80, ha='right')
    plt.xlim(['종로구', '강동구'])
    plt.legend()
    plt.grid()
    st.pyplot(fig)

def make_chart_HR(df):
    
    # Housing Redevelopment : 주택 재개발
    # 전처리 데이터 이름 >>> df = pd.read_csv('서울주택재개발_전처리완료.csv')

    # 컬럼 분류값 만들기
    df['건립가구 (가구)_완료'] = np.where(df['건립가구 (가구)_완료'] == 0, np.nan, df['건립가구 (가구)_완료'])
    
    x = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구",
        "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구",  "금천구",
        "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

    y1 = df[df["년"] == 2014]["건립가구 (가구)_완료"]
    y2 = df[df["년"] == 2015]["건립가구 (가구)_완료"]
    y3 = df[df["년"] == 2016]["건립가구 (가구)_완료"]
    y4 = df[df["년"] == 2017]["건립가구 (가구)_완료"]
    y5 = df[df["년"] == 2018]["건립가구 (가구)_완료"]
    y6 = df[df["년"] == 2019]["건립가구 (가구)_완료"]
    y7 = df[df["년"] == 2020]["건립가구 (가구)_완료"]
    y8 = df[df["년"] == 2021]["건립가구 (가구)_완료"]
    y9 = df[df["년"] == 2022]["건립가구 (가구)_완료"]


    fig, ax = plt.subplots(figsize=(10, 6))
    plt.scatter(x, y1, label='2014')
    plt.scatter(x, y2, label='2015')
    plt.scatter(x, y3, label='2016')
    plt.scatter(x, y4, label='2017')
    plt.scatter(x, y5, label='2018')
    plt.scatter(x, y6, label='2019')
    plt.scatter(x, y7, label='2020')
    plt.scatter(x, y8, label='2021')
    # plt.scatter(x, y9, label='2022')

    plt.xticks(rotation=80, ha='right')
    plt.legend()
    plt.grid()
    st.pyplot(fig)

def run_eda_app2():
    with st.expander("Trend in Economic Fluctuations Section", expanded=True):

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["경제성장률 및 금리 변동추이", "경기종합지수 변동추이", "범죄율 변동추이", "연령별 인구수 변동추이", "재개발 횟수 변동추이"])

        with tab1:
            # 경제성장률 및 금리
            df = pd.read_csv('./data/lr_uer_merged.csv')
            make_chart_EGR_IR(df)

        with tab2:
            # 경기종합지수
            df = pd.read_csv('./data/경기종합지리_전처리완료.csv')
            make_chart_ECI(df)

        with tab3:
            # 범죄율
            df = pd.read_csv('./data/서울시5대범죄전처리완료.csv')
            make_chart_CR(df)

        with tab4:
            # 연령별 인구수
            df = pd.read_csv('./data/서울_연령별_인구수_전처리.csv')
            make_chart_PBA(df)

        with tab5:
            # 재개발
            df = pd.read_csv('./data/서울주택재개발_전처리완료.csv')
            make_chart_HR(df)