import streamlit as st, pandas as pd, numpy as np, datetime, pvlib, folium
from utils import check_login, logout
from database import load_products, save_to_sheet
from streamlit_geolocator import geolocator
from streamlit_folium import st_folium
from timezonefinder import TimezoneFinder
check_login(); logout()
st.title("الحاسبة الذكية بناسا ☀️")

p = load_products()
location = geolocator("حدد موقعك")
lat, lon = (location['latitude'], location['longitude']) if location else (15.5, 32.5)

m = folium.Map(location=[lat, lon], zoom_start=10)
folium.Marker([lat, lon]).add_to(m)
st_folium(m, width=700, height=300)

place_type = st.selectbox("نوع المكان", list(p['places'].keys()))
place_data = p['places'][place_type]

total_watt, total_energy = 0, 0
for device in p['devices'][place_type]:
    qty = st.number_input(f"عدد {device['name']}", 0, 100, device.get('qty',1), key=device['name'])
    if qty > 0: total_watt += device['watt'] * qty; total_energy += device['watt'] * qty * device['hours'] / 1000

system_kw = (total_watt * place_data['backup']) / 1000
tilt, azimuth = abs(lat), 180 if lat > 0 else 0
tf = TimezoneFinder(); tz = tf.timezone_at(lng=lon, lat=lat)
times = pd.date_range(start=f"{datetime.datetime.now().year}-01-01", periods=8760, freq='h', tz=tz)
weather = pvlib.iotools.get_psm3(lat, lon, api_key='YOUR_NREL_KEY', email='test@test.com')[0]
poa = pvlib.irradiance.get_total_irradiance(tilt, azimuth, pvlib.solarposition.get_solarposition(times, lat, lon)['zenith'], pvlib.solarposition.get_solarposition(times, lat, lon)['azimuth'], weather['DNI'], weather['GHI'], weather['DHI'])
energy_year = (system_kw * 1000 * (poa['poa_global'] / 1000) * 0.8).sum() / 1000

st.metric("الانتاج السنوي", f"{energy_year:.0f} KWh")

inv = st.selectbox("الانفرتر", p['inverters'], format_func=lambda x: f"{x['brand']}")
bat = st.selectbox("البطارية", p['batteries'], format_func=lambda x: f"{x['brand']}")

if total_watt > inv['kw']*1000: st.error("⚠️ الحمل اكبر من الانفرتر"); can_run=False
else: st.success("✅ النظام متوافق"); can_run=True

name, phone = st.text_input("اسمك"), st.text_input("رقمك")
if can_run and st.button("ارسال الطلب"):
    save_to_sheet({"name":name,"phone":phone,"type":place_type,"kw":system_kw,"energy":energy_year}, "requests")
    st.success("تم الارسال")
