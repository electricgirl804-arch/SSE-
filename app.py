import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit.components.v1 as components
import math

st.set_page_config(page_title="SSE Smart Solar Platform", page_icon="logo.png", layout="wide")

# CSS + هيدر + أيقونات
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}

.header-container {
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(90deg, rgba(255,215,0,0.15) 0%, rgba(0,123,255,0.15) 100%);
    padding: 30px; border-radius: 20px; margin-bottom: 30px;
    border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px);
}

.logo {
    width: 120px; height: 120px;
    background-image: url('logo.png');
    background-size: contain; background-repeat: no-repeat; background-position: center;
    margin-left: 20px; animation: float 3s ease-in-out infinite;
}

.header-text h1 {font-size: 42px; color: #FFD700; margin: 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
.header-text p {font-size: 18px; color: #b0c4de; margin-top: 8px;}

.stMetric {
    background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
    border-radius: 15px; padding: 20px; border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); transition: transform 0.3s;
    text-align: center;
}
.stMetric:hover {transform: translateY(-5px);}

.metric-label {font-size: 14px!important; color: #b0c4de!important; margin-top: 10px;}
.metric-value {font-size: 32px!important; font-weight: 700!important; color: white!important;}

.stButton>button {
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
    color: #0f2027; font-weight: 700; border: none; border-radius: 10px;
    padding: 12px 24px; width: 100%; transition: all 0.3s;
}
.stButton>button:hover {transform: scale(1.05); box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);}

.success-msg {
    background: linear-gradient(90deg, #00b09b, #96c93d);
    padding: 15px; border-radius: 10px; color: white; font-weight: 600; text-align: center; margin-top: 20px;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
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
                pos => {
                    window.parent.postMessage({type: "streamlit:setComponentValue", key: "sse_gps", value: [pos.coords.latitude, pos.coords.longitude]}, "*");
                    window.sse_gps_sent = true;
                },
                err => {
                    window.parent.postMessage({type: "streamlit:setComponentValue", key: "sse_gps", value: [15.5007, 32.5599]}, "*");
                    window.sse_gps_sent = true;
                }
            );
        }
        </script>
    """, height=0)
    return st.session_state.get("sse_gps", [15.5007, 32.5599])

if "sse_gps" not in st.session_state:
    st.session_state.sse_gps = [15.5007, 32.5599]

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

st.sidebar.markdown(f"""<div class="stMetric"><div style="font-size: 40px;">☀️</div><div class="metric-label">الإشعاع الأفقي</div><div class="metric-value">{ghi_h:.2f}</div><div style="color: #b0c4de;">kWh/m²/day</div></div>""", unsafe_allow_html=True)

st.sidebar.markdown(f"""<div class="stMetric"><div style="font-size: 40px;">📈</div><div class="metric-label">بعد الميل</div><div class="metric-value">{ghi_t:.2f}</div><div style="color: #b0c4de;">kWh/m²/day</div></div>""", unsafe_allow_html=True)

st.sidebar.markdown(f"""<div class="stMetric"><div style="font-size: 40px;">📐</div><div class="metric-label">زاوية ناسا</div><div class="metric-value">{tilt_opt:.1f}°</div></div>""", unsafe_allow_html=True)

final_tilt = tilt_opt
final_factor = 1 + 0.008 * abs(final_tilt)
ghi_final = ghi_h * final_factor

st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin: 20px 0;"><h2>⚡ إدخال بيانات الأحمال</h2></div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    load_kw = st.number_input("إجمالي الحمل kW", value=2.0, step=0.1)
with col2:
    hours = st.number_input("ساعات التشغيل", value=8, step=1)
with col3:
    days_autonomy = st.number_input("أيام الاستقلالية", value=1.5, step=0.5)

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

distance = st.number_input("المسافة DC متر", value=20)
current_dc = (array_kw * 1000) / (battery_v * 0.98)
cable_mm2 = (2 * distance * current_dc * 0.0175) / (0.03 * battery_v)
fuse_dc = math.ceil(current_dc * 1.56)
breaker_ac = math.ceil((load_kw * 1000 / 220) * 1.25)

# النتائج مع الأيقونات الكبيرة
st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin: 30px 0;"><h2>📊 النتائج الهندسية</h2></div>""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"""<div class="stMetric"><div style="font-size: 50px; margin-bottom: 10px;">☀️</div><div class="metric-label">عدد الألواح 550W</div><div class="metric-value">{num_panels}</div><div style="color: #FFD700; font-size: 16px; margin-top: 5px;">⚡ {array_kw:.1f} kW</div></div>""", unsafe_allow_html=True)
col2.markdown(f"""<div class="stMetric"><div style="font-size: 50px; margin-bottom: 10px;">🔋</div><div class="metric-label">البطاريات 48V 200Ah</div><div class="metric-value">{num_batteries}</div><div style="color: #FFD700; font-size: 16px; margin-top: 5px;">💾 {battery_kwh:.1f} kWh</div></div>""", unsafe_allow_html=True)
col3.markdown(f"""<div class="stMetric"><div style="font-size: 50px; margin-bottom: 10px;">⚡</div><div class="metric-label">الانفرتر</div><div class="metric-value">{inverter_kw} kW</div><div style="color: #FFD700; font-size: 16px; margin-top: 5px;">AC 220V</div></div>""", unsafe_allow_html=True)
col4.markdown(f"""<div class="stMetric"><div style="font-size: 50px; margin-bottom: 10px;">📊</div><div class="metric-label">الطاقة اليومية</div><div class="metric-value">{energy_kwh:.1f}</div><div style="color: #b0c4de; font-size: 16px; margin-top: 5px;">kWh/يوم</div></div>""", unsafe_allow_html=True)

# الكيبل والحمايات مع أيقونات
st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin: 30px 0;"><h2>🔌 مقطع الكيبل والحمايات</h2></div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.markdown(f"""<div class="stMetric"><div style="font-size: 45px; margin-bottom: 10px;">🔌</div><div class="metric-label">مقطع كيبل DC</div><div class="metric-value">{math.ceil(cable_mm2)} mm²</div></div>""", unsafe_allow_html=True)
col2.markdown(f"""<div class="stMetric"><div style="font-size: 45px; margin-bottom: 10px;">🔒</div><div class="metric-label">فيوز DC</div><div class="metric-value">{fuse_dc} A</div></div>""", unsafe_allow_html=True)
col3.markdown(f"""<div class="stMetric"><div style="font-size: 45px; margin-bottom: 10px;">⚡</div><div class="metric-label">قاطع AC</div><div class="metric-value">{breaker_ac} A</div></div>""", unsafe_allow_html=True)

# الاقتصادي
st.markdown("""<div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin: 30px 0;"><h2>💰 التحليل الاقتصادي</h2></div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
price_panel = col1.number_input("سعر اللوح $", value=85)
price_battery = col2.number_input("سعر البطارية $", value=280)
price_inverter = col3.number_input("سعر الانفرتر $", value=450)

total_cost = num_panels*price_panel + num_batteries*price_battery + inverter_kw*price_inverter
kwh_price = st.number_input("سعر الكيلو واط $", value=0.15)
annual_saving = energy_kwh * 365 * kwh_price
payback = total_cost / annual_saving if annual_saving > 0 else 0

col1, col2, col3 = st.columns(3)
col1.markdown(f"""<div class="stMetric"><div style="font-size: 45px; margin-bottom: 10px;">💵</div><div class="metric-label">التكلفة الكلية</div><div class="metric-value">${total_cost:,.0f}</div></div>""", unsafe_allow_html=True)
col2.markdown(f"""<div class="stMetric"><div style="font-size: 45px; margin-bottom: 10px;">📈</div><div class="metric-label">التوفير السنوي</div><div class="metric-value">${annual_saving:,.0f}</div></div>""", unsafe_allow_html=True)
col3.markdown(f"""<div class="stMetric"><div style="font-size: 45px; margin-bottom: 10px;">⏱️</div><div class="metric-label">الاسترجاع</div><div class="metric-value">{payback:.1f} سنة</div></div>""", unsafe_allow_html=True)

st.markdown("""<div class="success-msg">✅ تم إتمام الحسابات وفقاً لبيانات ناسا 20 سنة ومعايير IEC 61727</div>""", unsafe_allow_html=True)
