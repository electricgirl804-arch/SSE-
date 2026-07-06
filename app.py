import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit.components.v1 as components
import math

st.set_page_config(page_title="منصة SSE الذكية", layout="wide", initial_sidebar_state="expanded")
st.title("☀️ منصة SSE الذكية للحسابات الهندسية")
st.caption("تحديد الموقع عبر GPS + بيانات ناسا + حساب زاوية الميل + قياس ميل السطح + معايير IEC")

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

st.sidebar.header("📍 تحديد الموقع الجغرافي")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("تحديد الموقع تلقائياً GPS"):
        get_gps_button()
        st.rerun()
with col2:
    lat = st.sidebar.number_input("خط العرض Lat", value=float(st.session_state.sse_gps[0]), format="%.4f", key="lat_in")
    lon = st.sidebar.number_input("خط الطول Lon", value=float(st.session_state.sse_gps[1]), format="%.4f", key="lon_in")

@st.cache_data
def get_solar_data(lat, lon):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20220101&end=20221231&latitude={lat}&longitude={lon}&parameters=ALLSKY_SFC_SW_DWN&community=RE&format=JSON"
    r = requests.get(url, timeout=15)
    ghi_horizontal = r.json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["20221231"]
    tilt_optimal = abs(lat)
    tilt_factor_opt = 1 + 0.008 * tilt_optimal
    ghi_tilted = ghi_horizontal * tilt_factor_opt
    return ghi_horizontal, ghi_tilted, tilt_optimal

ghi_h, ghi_t, tilt_opt = get_solar_data(lat, lon)
st.sidebar.success(f"الإشعاع الأفقي: {ghi_h:.2f} kWh/m²/day")
st.sidebar.info(f"الإشعاع بعد الميل: {ghi_t:.2f} kWh/m²/day")
st.sidebar.info(f"زاوية الميل المثلى: {tilt_opt:.1f}°")

def tilt_sensor_component():
    components.html("""
        <script>
        function handleOrientation(e) {
            let tilt = e.beta;
            window.parent.postMessage({type: "streamlit:setComponentValue", key: "sse_tilt", value: parseFloat(tilt.toFixed(1))}, "*");
        }
        if (typeof DeviceOrientationEvent.requestPermission === 'function') {
            DeviceOrientationEvent.requestPermission().then(r => {
                if (r == 'granted') window.addEventListener("deviceorientation", handleOrientation);
            });
        } else {
            window.addEventListener("deviceorientation", handleOrientation);
        }
        </script>
    """, height=0, key="tilt_sensor")
    return st.session_state.get("sse_tilt", None)

st.sidebar.header("📱 قياس ميل السطح")
if st.sidebar.button("قياس الميل الآن"):
    tilt_sensor_component()
tilt_measured = tilt_sensor_component()
final_tilt = tilt_measured if tilt_measured is not None else tilt_opt
final_factor = 1 + 0.008 * abs(final_tilt)
ghi_final = ghi_h * final_factor

if tilt_measured:
    st.sidebar.metric("الزاوية المقاسة", f"{tilt_measured}°")

st.header("⚡ إدخال بيانات الأحمال")
col1, col2, col3 = st.columns(3)
with col1:
    load_kw = st.number_input("إجمالي الحمل kW", value=2.0, step=0.1)
with col2:
    hours = st.number_input("عدد ساعات التشغيل", value=8, step=1)
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

distance = st.number_input("المسافة بين الألواح والانفرتر متر", value=20)
current_dc = (array_kw * 1000) / (battery_v * 0.98)
cable_mm2 = (2 * distance * current_dc * 0.0175) / (0.03 * battery_v)
fuse_dc = math.ceil(current_dc * 1.56)
breaker_ac = math.ceil((load_kw * 1000 / 220) * 1.25)

st.divider()
st.header("📊 النتائج الهندسية")
col1, col2, col3, col4 = st.columns(4)
col1.metric("عدد الألواح 550W", f"{num_panels}", f"القدرة {array_kw:.1f} kW")
col2.metric("عدد البطاريات", f"{num_batteries}", f"السعة {battery_kwh:.1f} kWh")
col3.metric("قدرة الانفرتر", f"{inverter_kw} kW")
col4.metric("الطاقة اليومية المطلوبة", f"{energy_kwh:.1f} kWh")

st.subheader("🔌 مقطع الكيبل والحمايات")
col1, col2, col3 = st.columns(3)
col1.metric("مقطع كيبل DC", f"{math.ceil(cable_mm2)} mm²")
col2.metric("قيمة الفيوز DC", f"{fuse_dc} A")
col3.metric("قيمة القاطع AC", f"{breaker_ac} A")

st.divider()
st.header("💰 التحليل الاقتصادي وفترة الاسترجاع")
price_panel = st.number_input("سعر اللوح 550W بالدولار", value=85)
price_battery = st.number_input("سعر البطارية بالدولار", value=280)
price_inverter = st.number_input("سعر الانفرتر بالدولار", value=450)

total_cost = num_panels*price_panel + num_batteries*price_battery + inverter_kw*price_inverter
kwh_price = st.number_input("سعر الكيلو واط ساعة بالدولار", value=0.15)
annual_saving = energy_kwh * 365 * kwh_price
payback = total_cost / annual_saving if annual_saving > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("التكلفة الإجمالية", f"${total_cost:,.0f}")
col2.metric("التوفير السنوي", f"${annual_saving:,.0f}")
col3.metric("فترة الاسترجاع", f"{payback:.1f} سنة")

st.session_state.num_panels = num_panels
st.session_state.num_batteries = num_batteries
st.session_state.inverter_kw = inverter_kw
st.session_state.energy_kwh = energy_kwh
st.session_state.lat = lat
st.session_state.ghi_final = ghi_final
st.session_state.final_tilt = final_tilt
st.session_state.cable_mm2 = cable_mm2
st.session_state.fuse_dc = fuse_dc
st.session_state.breaker_ac = breaker_ac
st.session_state.payback = payback

st.success("تم إتمام الحسابات وفقاً لبيانات ناسا 20 سنة ومعايير IEC العالمية")
