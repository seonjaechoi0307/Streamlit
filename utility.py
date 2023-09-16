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