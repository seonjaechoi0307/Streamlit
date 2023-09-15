# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd
import folium
import numpy as np
import requests
from streamlit_folium import st_folium

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def get_pos(lat, lng) :
    return lat, lng

def Create_Map() :
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
                map = st_folium(m, height=350, width=700)
                
                # 사용자가 마커를 클릭한 경우 클릭한 위치의 위도, 경도 데이터를 보여줌
                if map.get("last_clicked") :
                    data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
            else:
                print("주소를 찾을 수 없습니다.")
        else:
            print("API 호출에 실패했습니다.")
    else:
        pass # 입력 주소가 없으므로 Pass
