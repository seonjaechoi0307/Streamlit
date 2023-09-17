# -*- utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from utility import plot_line_chart

def run_eda_app() :
    st.subheader("탐색적 자료 분석 페이지")
    estate_df = pd.read_csv("./data/month_at.csv")

    tab1, tab2, tab3 = st.tabs(["📈 Chart", "📘 Data", "📄 ETC"])

    with tab1 :
        with st.expander("Option Select Section", expanded=True) :
            col1, col2 = st.columns(2)

            with col1 :
                st.markdown("<h4>옵션 선택</h4>", unsafe_allow_html=True)
                # 데이터 프레임의 컬럼 목록을 옵션으로 사용
                # key = 고유 세션값 (셀렉박스 연속 구현 시 오류를 방지하기 위한 고유 세션값 주기)
                options1 = estate_df.columns.tolist()
                selected_option1 = st.selectbox("X 컬럼을 선택하세요 : ", options1, key="SelectBox_1")
                options2 = estate_df.columns.tolist()
                selected_option2 = st.selectbox("Y 컬럼을 선택하세요 : ", options2, key="SelectBox_2")
                options3 = estate_df.columns.tolist()
                selected_option3 = st.selectbox("컬럼을 선택하세요 : ", options3, key="SelectBox_3")
                options4 = estate_df.columns.tolist()
                selected_option4 = st.selectbox("컬럼을 선택하세요 : ", options4, key="SelectBox_4")
                options5 = estate_df.columns.tolist()
                selected_option5 = st.selectbox("컬럼을 선택하세요 : ", options5, key="SelectBox_5")
            
            with col2 :
                st.write("선택한 옵션의 그래프가 표시됩니다.")
                # Select options to Graph Setting
                x = estate_df[selected_option1]
                y = estate_df[selected_option2]
                x_label = "X축"
                y_label = "Y축"
                title = selected_option1 + "-" + selected_option2
                f = plot_line_chart(x, y, x_label, y_label, title)

                if (selected_option1 == selected_option2) :
                    st.write("X와 Y의 값이 같습니다.")
                else :
                    st.pyplot(f)

    with tab2 :
        st.dataframe(estate_df, height=500)
        with st.expander("Column List", expanded=False) :
            st.write("해당 데이터 프레임의 컬럼 리스트")
            st.write(estate_df.columns.tolist())

    with tab3 :
        # 선택한 옵션을 기반으로 데이터프레임 필터링
        # filtered_column = pd.concat([estate_df[selected_option1], estate_df[selected_option2]], axis=1)

        # 선택한 옵션과 열 데이터를 목록으로 출력
        st.write("선택한 옵션:", selected_option1)
        st.write("열 데이터 목록:")
        st.write(estate_df[selected_option1])