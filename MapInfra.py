# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd
import folium
import numpy as np
import requests
from streamlit_folium import st_folium
import os

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# 현재 스크립트 파일의 디렉토리 경로를 가져옵니다.
current_directory = os.path.dirname(__file__)

# 데이터 파일의 경로를 결정합니다. 현재 스크립트 파일의 디렉토리와 'data' 디렉토리를 연결합니다.
data_file_path = os.path.join(current_directory, 'data', 'infra.csv')

# 데이터 받아오기
infra_df = pd.read_csv(data_file_path)

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
        distance = geodesic((base_lat, base_lng), (infra_lat, infra_lng)).kilometers

        # 거리가 반경 내에 있는 경우 결과 리스트에 추가
        if distance <= radius_km:
            
            # 거리값 거리 컬럼에 넣기
            row['Distance'] = distance
            infra_within_distance.append(row[selected_columns])
        
    # 결과 리스트를 데이터프레임으로 변환하여 반환 // 거리를 기준으로 오름차순 정렬, 인덱스 값 초기화
    result_df = pd.DataFrame(infra_within_distance).sort_values(by='Distance').reset_index(drop=True)
    result_df['Distance'] = result_df['Distance'].round(2)
    return result_df

def Create_Map() :
    location = None  # location 변수 초기화

    with st.expander("Create Map Section", expanded=True):
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
            
                # 반경 5km 이내의 인프라 필터링
                Radius_km = st.select_slider("인프라 검색 반경 (Km)", options=np.arange(1, 6), key="Create_Map_Slider")
                infra_within_Nkm_df = filter_infra_by_distance(infra_df, base_lat, base_lng, Radius_km)

                # 데이터 프레임 출력
                st.dataframe(infra_within_Nkm_df, width=650, height=500)
            else:
                st.write("입력 주소값이 없습니다.")
