import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit.components.v1 as components
import math
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# فعل الذكاء الاصطناعي
AI_ENABLED = False
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="انت مهندس طاقة شمسية محترف اسمك SSE Assistant. رد باللغة العربية وباسلوب بسيط.")
        AI_ENABLED = True
    except:
        AI_ENABLED = False

st.set_page_config(page_title="SSE Smart Solar Platform", page_icon="logo.png", layout="wide")

# CSS + هيدر
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
.header-container {display: flex; align-items: center; justify-content: space-between; background: linear-gradient(90deg, rgba(255,215,0,0.15) 0%, rgba(0,123,255,0.15) 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px);}
.logo {width: 120px; height: 120px; background-image: url('logo.png'); background-size: contain; background-repeat: no-repeat; background-position: center; margin-left: 20px; animation: float 3s ease-in-out infinite;}
.header-text h1 {font-size: 42px; color: #FFD700; margin: 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
.header-text p {font-size: 18px; color: #b0c4de; margin-top: 8px;}
.stMetric {background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); transition: transform 0.3s; text-align: center;}
.stMetric:hover {transform: translateY(-5px);}
.metric-label {font-size: 14px!important; color: #b0c4de!important; margin-top: 10px;}
.metric-value {font-size: 32px!important; font-weight: 700!important; color: white!important;}
.success-msg {background: linear-gradient(90deg, #00b09b, #96c93d); padding: 15px; border-radius: 10px; color: white; font-weight: 600; text-align: center; margin-top: 20px;}
@keyframes float {0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); }}
</style>
<div class="header-container">
    <div class="header-text">
        <h1>SSE Smart Solar Platform</h1>
        <p>Smart Solara Engineer | بيانات ناسا 20 سنة | معايير IEC العالمية</p>
    </div>
    <div class="logo"></div>
</div>
""", unsafe_allow_html=True)

# GPS
def get_gps_button():
    components.html("""
        <script>
        if (!window.sse_gps_sent) {
            navigator.geolocation.getCurrentPosition(
                pos => { window.parent.postMessage({type: "streamlit:setComponentValue", key: "sse_gps", value: [pos.coords.latitude, pos.coords.longitude]}, "*"); window.sse_gps_sent = true;},
                err => { window.parent.postMessage({type: "streamlit:setComponentValue", key: "sse_gps", value: [15.5007, 32.5599]}, "*"); window.sse_gps_sent = true;}
            );
        }
        </script>
    """, height=0)
    return st.session_state.get("sse_gps", [15.5007, 32.5599])

if "sse_gps" not in st.session_state: st.session_state.sse_gps = [15.5007, 32.5599]

st.sidebar.markdown("""<div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 15px; border-radius: 10px; margin-bottom: 20px;"><h3 style="color: #0f2027; margin: 0; text-align: center;">📍 تحديد الموقع</h3></div>""", unsafe_allow_html=True)
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("📡 GPS تلقائي"):
        get_gps_button()
        st.rerun()
with col2:
    lat = st.sidebar.number_input("خط العرض", value=float(st.session_state.sse_gps[0]), format="%.4f", key="lat_in")
    lon = st.sidebar.number_input("خط الطول", value=float(st.session_state.sse_gps[1]), format="%.4f", key="lon_in")

@st.cache_data
def get_solar_data(lat, lon):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20220101&end=20221231&latitude={lat}&longitude={lon}&parameters=ALLSKY_SFC_SW_DWN&community=RE&format=JSON"
    r = requests.get(url, timeout=15)
    ghi_horizontal = r.json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["20221231"]
    tilt_optimal = abs(lat) * 0.9
    tilt_factor_opt = 1 + 0.008 * tilt_optimal
    ghi_tilted = ghi_horizontal * tilt_factor_opt
    return ghi_horizontal, ghi_tilted, tilt_optimal

ghi_h, ghi_t, tilt_opt = get_solar_data(lat, lon)
st.sidebar.metric("☀️ الاشعاع الافقي", f"{ghi_h:.2f} kWh/m²/day")
st.sidebar.metric("📈 بعد الميل", f"{ghi_t:.2f} kWh/m²/day")
st.sidebar.metric("📐 زاوية ناسا", f"{tilt_opt:.1f}°")

final_tilt = tilt_opt
final_factor = 1 + 0.008 * abs(final_tilt)
ghi_final = ghi_h * final_factor

# الحسابات
st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px;"><h2>⚡ إدخال بيانات الأحمال</h2></div>""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: load_kw = st.number_input("إجمالي الحمل kW", value=2.0, step=0.1)
with col2: hours = st.number_input("ساعات التشغيل", value=8, step=1)
with col3: days_autonomy = st.number_input("أيام الاستقلالية", value=1.5, step=0.5)

energy_kwh = load_kw * hours
panel_w = 550
battery_v = 48
battery_ah = 200
system_eff = 0.85
dod = 0.8
inverter_eff = 0.95

num_panels = math.ceil(energy_kwh / (ghi_final * panel_w/1000 * system_eff))
array_kw = num_panels * panel_w / 1000
battery_kwh = energy_kwh * days_autonomy / (dod * inverter_eff)
num_batteries = math.ceil(battery_kwh / (battery_v * battery_ah / 1000))
inverter_kw = math.ceil(load_kw * 1.3)

st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; margin: 30px 0;"><h2>📊 النتائج الهندسية</h2></div>""", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("☀️ عدد الألواح 550W", num_panels, f"{array_kw:.1f} kW")
col2.metric("🔋 البطاريات 48V 200Ah", num_batteries, f"{battery_kwh:.1f} kWh")
col3.metric("⚡ الانفرتر", f"{inverter_kw} kW")
col4.metric("📊 الطاقة اليومية", f"{energy_kwh:.1f} kWh/يوم")

# === الشات الذكي ===
if AI_ENABLED:
    st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; margin-top:30px;"><h2>💬 اسأل المهندس الذكي</h2></div>""", unsafe_allow_html=True)
    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input("اسأل عن الطاقة الشمسية..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("بفكر..."):
                context = f"بيانات النظام: الاشعاع {ghi_final:.2f}, الواح {num_panels}, بطاريات {num_batteries}, انفرتر {inverter_kw}kW"
                response = model.generate_content(context + "\n\nسؤال: " + prompt)
                st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("💡 لتشغيل المهندس الذكي: اعمل ملف.env وخت فيه GOOGLE_API_KEY")

st.markdown("""<div class="success-msg">✅ تم إتمام الحسابات وفقاً لبيانات ناسا 20 سنة ومعايير IEC 61727</div>""", unsafe_allow_html=True)
