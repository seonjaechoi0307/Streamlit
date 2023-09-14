# Font 관련 라이브러리
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import streamlit as st


@st.cache(allow_output_mutation=True)
def set_custom_font():
    # Custom Fonts 디렉토리 경로 설정
    font_dir = os.path.join(os.getcwd(), "customFonts")

    # Custom Fonts 디렉토리 내의 모든 폰트 파일 경로 가져오기
    font_files = fm.findSystemFonts(fontpaths=[font_dir])

    if font_files:
        # 첫 번째 폰트 파일을 사용하거나 다른 원하는 폰트를 선택하세요.
        selected_font_path = font_files[0]
        print(selected_font_path)
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