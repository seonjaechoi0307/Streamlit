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
import joblib

df = pd.read_csv('./data/Address_Filter.csv')
address = "대학로1길 34-12"

# OpenCage Geocoding API 키 // 일일 제한횟수 : 2500회
api_key = "9b234a70713041749b360493fc572fb7"

# API 호출 // API 발급 사이트 : https://opencagedata.com/api#rate-limiting
url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}&language=ko"
response = requests.get(url)

# 응답 처리
if response.status_code == 200:
    data = response.json()
    if data.get("results"):
        location = data["results"][0]["geometry"]
        lat, lng = location["lat"], location["lng"]
        print(f"주소: {address}")
        print(f"위도: {lat}")
        print(f"경도: {lng}")

        full_address = data["results"][0].get("formatted", "주소를 찾을 수 없습니다.")
        print(f"주소: {full_address}")
        
        # 받아온 주소 값에서 "동" 텍스트를 찾아 OO동 값 받아오기
        match = re.search(r"(\w+동)", full_address)

        if match:
            # Found_Name = OO동(Legal_Name)
            Found_Name = match.group()  # 일치하는 문자열 추출
            print(Found_Name)  # "OO동" 출력
        else:
            print("일치하는 동 이름을 찾을 수 없습니다.")

        # 찾은 OO동 기준 자치구 파악하기
        # Region_Name = df[df["Legal_Name"] == Found_Name]["Region_Name"].iloc[0]
        # print(Region_Name)
