import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, time
import pvlib
from shapely.geometry import Polygon, Point

st.set_page_config(page_title="SSE - محاكي الظلال", page_icon="🌤️", layout="wide")

st.title("🌤️ محاكي الظلال ثلاثي الأبعاد")
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v1.2")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 بيانات الموقع")
    lat = st.number_input("خط العرض", 10.0, 23.0, 15.5, 0.1)
    lon = st.number_input("خط الطول", 20.0, 40.0, 32.5, 0.1)

    st.subheader("🏗️ بيانات العوائق")
    obstacle_h = st.slider("ارتفاع العمود/الشجرة بالمتر", 1, 15, 6)
    obstacle_dist = st.slider("المسافة من الألواح بالمتر", 1, 20, 5)

with col2:
    st.subheader("📅 الزمن")
    date = st.date_input("التاريخ", datetime.now())
    hour = st.slider("الساعة", 6, 18, 12)

# حساب موقع الشمس
times = pd.DatetimeIndex([datetime.combine(date, time(hour, 0))])
solpos = pvlib.solarposition.get_solarposition(times, lat, lon)
azimuth = solpos['azimuth'].values[0]
elevation = solpos['elevation'].values[0]

# حساب طول الظل
shadow_length = obstacle_h / np.tan(np.radians(elevation)) if elevation > 0 else 20

st.metric("طول الظل المتوقع", f"{shadow_length:.1f} متر")
st.metric("زاوية الشمس", f"{elevation:.1f}°")

# رسم الظل
fig = go.Figure()
fig.add_shape(type="rect", x0=0, y0=0, x1=10, y1=10, fillcolor="blue", opacity=0.3)
fig.add_shape(type="rect", x0=obstacle_dist, y0=0, x1=obstacle_dist+2, y1=obstacle_h, fillcolor="gray")
st.plotly_chart(fig, use_container_width=True)
