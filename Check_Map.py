# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd
import folium
import numpy as np
import requests
from streamlit_folium import st_folium
import os
import requests
import json
import re
from math import radians, sin, cos, sqrt, atan2
import datetime
import lightgbm as lgb
import joblib

# 전역변수 세팅파트

# 자치구 필터링할 데이터 프레임 불러오기
School_df = pd.read_csv('./data/School.csv')
University_df = pd.read_csv('./data/University.csv')
Subway_df = pd.read_csv('./data/서울지하철주소종합.csv')

# 함수관련 세팅파트

# Function to calculate Haversine distance = Haversine 공식에 따라 두 좌표간의 최단거리를 구하는 함수
def haversine_distance(lat1, lon1, lat2, lon2):

    """
    lat1 및 lon1: 첫 번째 지점의 위도와 경도입니다.
    lat2 및 lon2: 두 번째 지점의 위도와 경도입니다.
    R: 지구의 반지름 (평균 반지름 6,371,000 미터)
    phi1 및 phi2: 위도를 라디안 단위로 변환한 값입니다.
    delta_phi 및 delta_lambda: 위도와 경도의 차이를 라디안 단위로 표현한 값입니다.

    1. 두 지점의 위도 및 경도를 라디안 단위로 변환
    2. 위도와 경도의 차이를 계산
    3. Haversine 공식을 사용하여 위도와 경도 차이에 기반한 중간 값 'a' 계산
    4. 중간 값 'a'를 사용하여 최단거리 'a'를 계산합니다.
    """

    R = 6371000  # Radius of Earth in meters
    phi1 = radians(lat1)
    phi2 = radians(lat2)

    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi / 2) * sin(delta_phi / 2) + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) * sin(delta_lambda / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # Distance in meters
    return distance

# 기준 좌표(위도,경도)를 기준으로 데이터 프레임에서 가장 가까운 위도, 경도값을 구하는 함수
def Find_Nearest_distance(data, lat, lng):

    # 초기 최단거리와 인덱스 설정
    min_distance = float('inf')  # 초기 최단거리를 무한대로 설정
    closest_index = -1

    # 기준 위도 경도를 주소 입력한 위도, 경도값으로 맞춰놓기
    Reference_latitude = lat
    Reference_longitude = lng

    # 반복문을 통해 데이터 프레임의 row[위도, 경도] 불러와서 최단거리 찾기
    for index, row in data.iterrows():
        infra_latitude = row['위도']
        infra_longitude = row['경도']

         # 기준 좌표(위도, 경도)와 현재 인프라(위도, 경도) 사이의 최단거리 계산
        distance = haversine_distance(Reference_latitude, Reference_longitude, infra_latitude, infra_longitude)

        # 현재의 거리가 지금까지 계산된 거리 보다 작은지 확인합니다.
        if distance < min_distance:
            
            # 최단거리 업데이트
            min_distance = distance

            # 최단거리의 인덱스 업데이트
            closest_index = index

    # 가장 가까운 위도, 경도 값
    closest_coordinates = data.iloc[closest_index]   # 가장 가까운 좌표(위도, 경도)
    closest_latitude = closest_coordinates['위도']   # 가장 가까운 위도
    closest_longitude = closest_coordinates['경도']  # 가장 가까운 경도

    return closest_latitude, closest_longitude

# 기준 좌표(위도,경도)와 가장 가까운 좌표(위도,경도)의 최단거리를 구하는 함수
def calculate_shortest_distance(data, lat, lng):

    # 가장 가까운 위도 경도 찾는 함수 불러오기 clat = 가장 가까운 위도, clng = 가장 가까운 경도
    clat, clng = Find_Nearest_distance(data, lat, lng)

    # 최단 거리 계산하는 함수를 통해 최단거리 계산 =>>> 기준 좌표를 기준으로 최단 거리 좌표와의 최단 거리 계산하기
    shortest_distance = haversine_distance(lat, lng, clat, clng)

    # 최단 거리 값 반환
    return shortest_distance

# 선택된 년, 월을 기준으로 데이터 프레임을 필터링하는 함수
def Filter_df_by_date(data, column_list, select_year, select_month):
    
    # 모델을 데이터프레임으로 변환
    df = pd.DataFrame(data)

    # 선택한 연도와 월 값으로 year와 month 컬럼의 값과 일치하는 행을 필터링
    filter_df = df[(df['Year'] == select_year) & (df['Month'] == select_month)]
    
    # 필터된 데이터 프레임에서 특정 컬럼 리스트 값들만 추출하기
    selected_columns_df = filter_df[column_list]

    # 필터된 데이터 프레임 반환
    return selected_columns_df

# 레이아웃 관련파트

# 머신러닝 모델 레이아웃을 배치하는 함수
def layout_ml_LightGBM_app():

    with st.expander("Light GBM ML Section", expanded=True):
        
        st.write("<h4>사용 방법 안내</h4>", unsafe_allow_html=True)
        st.write("<h5>1. 좌측에 조건 값을 입력하세요.</h5>", unsafe_allow_html=True)
        st.write("<h5>2. 조건 값 입력 후 엔터를 누르세요.</h5>", unsafe_allow_html=True)
        st.write("<h5>3. 조건 값 전체 입력 시 우측에 예측 결과 값이 나옵니다.</h5>", unsafe_allow_html=True)
        st.markdown('---')

        col1, col2 = st.columns([1, 2])
        
        with col1 :

            # 변수 설정
            data_point = {}
            Found_Name = None

            # 컬럼 리스트 = 데이터 프레임에서 특정 컬럼만 갖고올 때 사용함
            column_list = ['IR', 'Population', 'LC_index', 'TC_index', 'SDT_index', 'Crime_Rates']
            
            # 사용자에게 예측값 Input 받기
            # 주소 입력
            address = st.text_input("주변 인프라를 확인할 기준 도로명 주소를 입력하고 엔터를 누르세요.", key='LightGBM_address')
            # address = "서울역"

            # 날짜 입력
            input_date = st.date_input("예측하고 싶은 날짜를 선택하세요.", datetime.date(2023, 10, 1), key='LightGBM_date')
            if input_date:
                year = input_date.year
                month = input_date.month
                # ml_df = Filter_df_by_date(Test_df, column_list, year, month)
            else:
                # 사용자가 날짜를 선택하지 않았을 때 처리
                st.write("날짜를 선택하지 않았습니다.")

            # 임의 값 입력
            Building_Age_option = st.number_input("건물 연식을 입력하세요", key='LightGBM_Building_Age', step=1)
            JS_Price_option = st.number_input("계약하시는 물건의 전세 가격을 입력하세요.", key='LightGBM_JS_Price', step=1)
            JS_BA_option = st.number_input("임대 면적을 입력하세요. (단위 : 제곱미터)", key='LightGBM_JS_BA', step=1)
            Sell_Price_option = st.number_input("평균적인 매매 가격을 입력하세요.", key='LightGBM_Sell_Price', step=1)

            

            if (address != "") :
                # Google Geocoding API 키, 분당 사용량 제한 : 100회, 일일 사용량 제한 : 1000회, 도로명 주소로 검색해야할듯.. 지번주소랑 위도 경도값 차이남
                api_key = "AIzaSyCrhAVjetsFGeMQExKGnfFhOdUyb9LQQSs"

                # API 호출
                url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}&language=ko"
                response = requests.get(url)

                # 응답 처리
                if response.status_code == 200:
                    data = response.json()
                    if data.get("results"):
                        location = data["results"][0]["geometry"]["location"]
                        lat, lng = location["lat"], location["lng"]
                        # print(f"주소: {address}")
                        # print(f"위도: {lat}")
                        # print(f"경도: {lng}")

                        full_address = data["results"][0].get("formatted_address", "주소를 찾을 수 없습니다.")
                        # print(f"주소: {full_address}")
                        
                        # 받아온 주소 값에서 "구" 텍스트를 찾아 OO구 값 받아오기
                        match = re.search(r"(\w+구)", full_address)

                        if match:

                            Found_Name = match.group()
                        
                        else:
                            print("일치하는 자치구 이름을 찾을 수 없습니다.")

                    # 검색한 주소와 가장 가까운 주변 지하철 인프라와의 최단거리
                    SD_to_Subway = calculate_shortest_distance(Subway_df, lat, lng)
                    SD_to_University = calculate_shortest_distance(University_df, lat, lng)
                    SD_to_School = calculate_shortest_distance(School_df, lat, lng)
                    
                    # 데이터 포인트 생성
                    data_point = {
                        'Building_Age': Building_Age_option,
                        'JS_BA': JS_BA_option,
                        'Sell_Price': Sell_Price_option,
                        'Year': year,
                        'Month': month,
                        # ↓ ↓ ↓ 임의 지정값 ↓ ↓ ↓ #
                        'IR': 3.5,
                        'Population': 4000000,
                        'LC_index': 100,
                        'TC_index': 100,
                        'SDT_index': 100,
                        'Crime_Rates': 1400,
                        # ↑ ↑ ↑ 임의 지정값 ↑ ↑ ↑ #
                        '위도': lat,
                        '경도': lng,
                        'Region_강남구': 1 if Found_Name == '강남구' else 0,
                        'Region_강동구': 1 if Found_Name == '강동구' else 0,
                        'Region_강북구': 1 if Found_Name == '강북구' else 0,
                        'Region_강서구': 1 if Found_Name == '강서구' else 0,
                        'Region_관악구': 1 if Found_Name == '관악구' else 0,
                        'Region_광진구': 1 if Found_Name == '광진구' else 0,
                        'Region_구로구': 1 if Found_Name == '구로구' else 0,
                        'Region_금천구': 1 if Found_Name == '금천구' else 0,
                        'Region_노원구': 1 if Found_Name == '노원구' else 0,
                        'Region_도봉구': 1 if Found_Name == '도봉구' else 0,
                        'Region_동대문구': 1 if Found_Name == '동대문구' else 0,
                        'Region_동작구': 1 if Found_Name == '동작구' else 0,
                        'Region_마포구': 1 if Found_Name == '마포구' else 0,
                        'Region_서대문구': 1 if Found_Name == '서대문구' else 0,
                        'Region_서초구': 1 if Found_Name == '서초구' else 0,
                        'Region_성동구': 1 if Found_Name == '성동구' else 0,
                        'Region_성북구': 1 if Found_Name == '성북구' else 0,
                        'Region_송파구': 1 if Found_Name == '송파구' else 0,
                        'Region_양천구': 1 if Found_Name == '양천구' else 0,
                        'Region_영등포구': 1 if Found_Name == '영등포구' else 0,
                        'Region_용산구': 1 if Found_Name == '용산구' else 0,
                        'Region_은평구': 1 if Found_Name == '은평구' else 0,
                        'Region_종로구': 1 if Found_Name == '종로구' else 0,
                        'Region_중구': 1 if Found_Name == '중구' else 0,
                        'Region_중랑구': 1 if Found_Name == '중랑구' else 0,
                        'Shortest_Distance_to_Subway': SD_to_Subway,
                        'Shortest_Distance_to_University': SD_to_University,
                        'Shortest_Distance_to_School': SD_to_School
                    }

                    # st.write(data_point) 딕셔너리 형태 및 값 파악하는 코드

            with col2 :
                if (address != ""):
                    # 사용자 입력값 리스트 생성
                    user_input_values = [Building_Age_option, JS_Price_option, JS_BA_option, Sell_Price_option]

                    # 딕셔너리 값들이 전부 None 이 아닐 경우와 입력값이 0이 아닐 경우 조건 통과
                    if all(value is not None for value in data_point.values()) and \
                           all(value != 0 for value in user_input_values):

                        # LightGBM 모델 로드
                        model = joblib.load('./models/Test.pkl')

                        # 데이터 포인트를 LightGBM 모델에 입력하여 예측값 얻기
                        data_array = np.array(list(data_point.values()))

                        # 2D 배열로 변환 >>> data_array = [[5, 2, 200000, 2023, ... , 500, 1000, 800]]
                        data_array = data_array.reshape(1, -1)  

                        # 변환된 배열, 데이터 포인트로 예측값 불러오기
                        predicted_value = np.round(model.predict(data_array), 2)

                        # 예측 결과 출력
                        st.write(f'<h4>예측 결과 값 : {predicted_value} 만원</h4>', unsafe_allow_html=True)

                        # Folium 지도 생성
                        m = folium.Map(location=[lat, lng], zoom_start=16)  # 해당 주소의 위도, 경도 값을 기준으로 지도 생성
                        m.add_child(folium.LatLngPopup())  # 마커 클릭 시 위도와 경도 표시
                        map = st_folium(m, height=440, width=850)

                    else:
                        st.write('<h5>값을 전부 입력 안하셨으므로 예측이 불가합니다.</h5>', unsafe_allow_html=True)
                else:
                    st.write('<h5>주소를 입력하지 않으셨습니다. 도로명 주소를 입력해주세요.</h5>', unsafe_allow_html=True)
