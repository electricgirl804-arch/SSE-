import streamlit as st
import folium
import requests
import pandas as pd
import plotly.express as px
from utils import load_css, check_login, logout
from streamlit_folium import st_folium

st.set_page_config(page_title="الخريطة - SSE", layout="wide")
load_css()
check_login()
logout()

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a192f 0%, #112240 100%); }
h1, h2, h3 { color: #64ffda!important; font-weight: 800; text-align: center; }
.info-card { background: #112240; padding: 20px; border-radius: 15px; border-left: 5px solid #64ffda; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 خريطة الموقع وبيانات NASA")
st.caption("مستخدمين موقع الخرطوم افتراضي. بعدين بنرجع الـ GPS")

def get_nasa_solar_data(lat, lon):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M",
        "community": "RE", "longitude": lon, "latitude": lat, "format": "JSON"
    }
    try:
        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()
        ghi_monthly = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        temp_monthly = data['properties']['parameter']['T2M']
        df = pd.DataFrame({
            'الشهر': ['يناير','فبراير','مارس','ابريل','مايو','يونيو','يوليو','اغسطس','سبتمبر','اكتوبر','نوفمبر','ديسمبر'],
            'GHI': [ghi_monthly[k] for k in ghi_monthly.keys()],
            'الحرارة': [(temp_monthly[k] - 273.15) for k in temp_monthly.keys()]
        })
        df
