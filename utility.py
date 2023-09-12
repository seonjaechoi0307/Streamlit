import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import plotly
import requests
import utility
from streamlit_folium import st_folium
from streamlit_lottie import st_lottie

def load_lottieurl(url) -> dict:

    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()