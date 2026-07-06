import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🌍 خريطة الموقع والإشعاع")

if 'lat' in st.session_state:
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=10)
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        popup=f"الإشعاع: {st.session_state.ghi_final:.2f} kWh/m²/day",
        tooltip="موقع المشروع"
    ).add_to(m)
    st_folium(m, width=700, height=400)
    st.metric("الإحداثيات", f"{st.session_state.lat:.4f}, {st.session_state.lon:.4f}")
else:
    st.warning("حدد الموقع من الصفحة الرئيسية أولاً")
