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

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# 데이터 받아오기
infra_df = pd.read_csv('./data/Infra.csv')

def get_pos(lat, lng) :
    return lat, lng

# 기준 주소의 Nkm 반경의 인프라 목록을 구하는 함수
def filter_infra_by_distance(infra_df, base_lat, base_lng, radius_km):

    """
    Parameters:
        - infra_df (DataFrame): 인프라 데이터를 담고 있는 DataFrame.
        - base_lat (float): 기준 주소의 위도.
        - base_lng (float): 기준 주소의 경도.
        - radius_km (float): 반경 (킬로미터) 내에 있는 인프라를 검색할 거리.
        - distance (float): 기준 주소와 주변 인프라와의 거리

    Returns:
        - DataFrame: 반경 내에 있는 인프라 목록을 담은 DataFrame.
    """


    # 결과를 저장할 빈 리스트 설정
    infra_within_distance = []

    # 받아올 컬럼 설정
    selected_columns = ['Legion_Name', 'Name', 'Kind', 'Distance']

    # 반복문을 통한 반경 내 행값 가져오기
    for index, row in infra_df.iterrows():
        infra_lat, infra_lng = row['latitude'], row['longitude']

        # 기준 주소와 인프라의 위도, 경도를 사용하여 거리 계산
        distance = geodesic((base_lat, base_lng), (infra_lat, infra_lng)).meters

        # 거리가 반경 내에 있는 경우 결과 리스트에 추가
        if distance <= radius_km:
            row_with_distance = row.copy()
            row_with_distance['Distance'] = distance
            infra_within_distance.append(row_with_distance[selected_columns])

    # 반경 내에 인프라가 있는 경우에만 'Distance' 열을 포함한 데이터프레임을 생성
    if infra_within_distance:
        # 결과 리스트를 데이터프레임으로 변환하여 반환 // 거리를 기준으로 오름차순 정렬, 인덱스 값 초기화
        result_df = pd.DataFrame(infra_within_distance).sort_values(by='Distance').reset_index(drop=True)
        result_df['Distance'] = result_df['Distance'].round(2)
        
    elif not infra_within_distance:
        # 반경 내에 인프라가 없는 경우 빈 데이터프레임 반환
        result_df = None

    return result_df

def Create_Map():

    location = None  # location 변수 초기화

    with st.expander("Search Map & Infra index Section", expanded=True):
        col1, col2 = st.columns(2)

        with col1 :

            # 주소 입력
            address = st.text_input("주변 인프라를 확인할 기준 주소를 입력하고 엔터를 누르세요.")

            if (address != "") :
                # OpenCage Geocoding API 키 // 일일 제한횟수 : 2500회
                api_key = "9b234a70713041749b360493fc572fb7"

                # API 호출 // API 발급 사이트 : https://opencagedata.com/api#rate-limiting
                url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}"
                response = requests.get(url)

                # 응답 처리
                if response.status_code == 200:
                    data = response.json()
                    if data.get("results"):
                        location = data["results"][0]["geometry"]
                        lat, lng = location["lat"], location["lng"]
                        # print(f"주소: {address}")
                        # print(f"위도: {lat}")
                        # print(f"경도: {lng}")

                        # Folium 지도 생성
                        m = folium.Map(location=[lat, lng], zoom_start=16)  # 해당 주소의 위도, 경도 값을 기준으로 지도 생성
                        m.add_child(folium.LatLngPopup())  # 마커 클릭 시 위도와 경도 표시
                        map = st_folium(m, height=500, width=650)
                        
                        # 사용자가 마커를 클릭한 경우 클릭한 위치의 위도, 경도 데이터를 보여줌
                        if map.get("last_clicked") :
                            data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
                    else:
                        print("주소를 찾을 수 없습니다.")
                else:
                    print("API 호출에 실패했습니다.")
            else:
                pass # 입력 주소가 없으므로 Pass

        with col2 :

            # location이 None 아닐 시 아래 코드 실행
            if location is not None:

                # 기준 위도, 경도를 입력한 주소 기준으로 설정
                base_lat = location["lat"]
                base_lng = location["lng"]
            
                # 반경 3km 이내의 인프라 필터링
                Radius_meter = st.select_slider("인프라 검색 반경 (단위 : meter)", options=np.arange(1, 3001), key="Create_Map_Slider")
                infra_within_Nkm_df = filter_infra_by_distance(infra_df, base_lat, base_lng, Radius_meter)

                # 데이터 프레임 출력
                st.dataframe(infra_within_Nkm_df, width=650, height=500)
            else:
                st.write("입력 주소값이 없습니다.")

# 자치구별 인프라 맵 만들기
def Create_folium_map(data, condition):

    # 서울 행정구역 json raw파일(githubcontent)
    r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
    c = r.content
    seoul_geo = json.loads(c)

    # Legion_Name 밸류 카운트
    seoul_group_data = data[data["Class"] == condition]["Legion_Name"].value_counts()

    # Folium 맵 생성
    m = folium.Map(
        location=[37.559819, 126.963895],
        zoom_start=10,
        tiles='cartodbpositron'
    )

    # 지역구 경계 표시
    folium.GeoJson(
        seoul_geo,
        name='지역구'
    ).add_to(m)

    # Choropleth 레이어 추가
    m.choropleth(
        geo_data=seoul_geo,
        data=seoul_group_data,
        fill_color='YlOrRd',
        fill_opacity=0.5,
        line_opacity=0.2,
        key_on='properties.name',
        legend_name="지역구별 인프라 개수"
    )    

    # 지역구 내 인프라 위치 표시
    park_data = data[data['Class'] == condition]
    for index, row in park_data.iterrows():
        sub_lat, sub_lng = row['latitude'], row['longitude']

        # 아이콘 색상 설정
        icon_color = 'grey'
        radius = 200

        # 마커 생성 및 추가
        folium.CircleMarker(
            [sub_lat, sub_lng],
            radius=1,
            color=icon_color,
        ).add_to(m)

    return m

# Regional Infrastructure = 지역 인프라
def Regional_Infrastructure():

    # with = Python 컨텍스트 관리자(Context Managter), 작업의 시작과 끝 정의 및 리소스 할당 및 해제 관리하기 위해 사용
    with st.expander("Infra Map Section", expanded=True):
            
            # 각 탭 선택 옵션 리스트 만들기
            tabs = ["공원 위치정보", "대학 위치정보", "지하철 위치정보", "학교 위치정보"]

            # 확인할 인프라 탭을 선택하세요.
            selected_tab = st.selectbox("확인할 인프라 지도 탭을 선택하세요.", tabs)

            # 선택한 탭에 따라 데이터를 렌더링하고 지도를 표시
            if selected_tab == "공원 위치정보":

                data = infra_df
                condition = 'Park'
                m = Create_folium_map(data, condition)
                st_folium(m, height=500, width=700, key='map_1')
                
            elif selected_tab == "대학 위치정보":
                
                data = infra_df
                condition = 'College'
                m = Create_folium_map(data, condition)
                st_folium(m, height=500, width=700, key='map_2')
                
            elif selected_tab == "지하철 위치정보":
                
                data = infra_df
                condition = 'Subway'
                m = Create_folium_map(data, condition)
                st_folium(m, height=500, width=700, key='map_3')
                
            elif selected_tab == "학교 위치정보":
                
                data = infra_df
                condition = 'School'
                m = Create_folium_map(data, condition)
                st_folium(m, height=500, width=700, key='map_4')

# def View_Info_Visualization():