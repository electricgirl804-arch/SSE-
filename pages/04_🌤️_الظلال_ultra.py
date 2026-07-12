import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, time
import pvlib
import math
from utils import check_login, logout, load_css

check_login(); logout(); load_css()

st.set_page_config(page_title="SSE - محاكي الظلال", page_icon="🌤️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
h1 {color: #FFD700!important; font-weight: 700; text-align: center;}
.stMetric {background: rgba(255,255,255,0.08); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.3);}
.stMetric div {font-size: 28px!important; font-weight: 700!important; color: #FFD700!important;}
</style>
""", unsafe_allow_html=True)

st.title("🌤️ محاكي الظلال ثلاثي الأبعاد SSE")
st.caption("تم التطوير بواسطة المهندس/ة شهد | IEC 61724")

# قراءة الموقع من صفحة 01
if 'lat' in st.session_state and 'lon' in st.session_state:
    lat = st.session_state.lat
    lon = st.session_state.lon
    st.success(f"📍 الموقع: {lat:.4f}°N, {lon:.4f}°E")
else:
    st.warning("⚠️ الرجوع للصفحة الرئيسية وتحديد الموقع GPS أولاً")
    lat = st.number_input("خط العرض", 10.0, 23.0, 15.5, 0.1)
    lon = st.number_input("خط الطول", 20.0, 40.0, 32.5, 0.1)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🏗️ بيانات العوائق")
    obstacle_h = st.slider("ارتفاع العمود/الشجرة بالمتر", 1, 15, 6)
    obstacle_dist = st.slider("المسافة من الألواح بالمتر", 1, 20, 5)
    row_spacing = st.slider("المسافة بين الصفوف متر", 1, 10, 3)

with col2:
    st.subheader("📅 الزمن")
    date = st.date_input("التاريخ", datetime.now())
    hour = st.slider("الساعة", 6, 18, 12)

# حساب لحظي سريع
times = pd.DatetimeIndex([datetime.combine(date, time(hour, 0))])
solpos = pvlib.solarposition.get_solarposition(times, lat, lon, method='nrel_numpy')
azimuth = solpos['azimuth'].values[0]
elevation = solpos['elevation'].values[0]

shadow_length = obstacle_h / np.tan(np.radians(elevation)) if elevation > 0 else 20
shadow_on_array = max(0, shadow_length - obstacle_dist)
panel_height = 2.0
shading_loss = min(100, (shadow_on_array / panel_height) * 100) if elevation > 10 else 0

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("ارتفاع الشمس", f"{elevation:.1f}°")
c2.metric("سمت الشمس", f"{azimuth:.1f}°")
c3.metric("طول الظل", f"{shadow_length:.1f} متر")
c4.metric("نسبة الفقد", f"{shading_loss:.0f}%", delta="خطير" if shading_loss>30 else "مقبول")

if shading_loss > 30:
    st.error("⚠️ الظل يغطي أكثر من 30% حسب IEC 61727")
elif shading_loss > 10:
    st.warning("⚠️ فقد 10-30% يجب مراجعة التباعد")
else:
    st.success("✅ التباعد مناسب")

# ===== حساب الفقد السنوي =====
@st.cache_data
def calculate_annual_shading(lat, lon, obstacle_h, obstacle_dist, year):
    """حساب الفقد السنوي - 8760 ساعة"""
    hours = pd.date_range(f"{year}-01-01 06:00", f"{year}-12-31 18:00", freq="H")
    solpos = pvlib.solarposition.get_solarposition(hours, lat, lon, method='nrel_numpy')

    shadow_lengths = obstacle_h / np.tan(np.radians(solpos['elevation']))
    shadow_lengths[solpos['elevation'] <= 10] = 0

    shading_hours = (shadow_lengths > obstacle_dist).sum()
    annual_loss = (shading_hours / len(hours)) * 100

    return shading_hours, annual_loss

st.divider()
st.subheader("حساب الفقد السنوي بسبب الظل")

if st.button("احسب الفقد السنوي", type="primary", use_container_width=True):
    with st.spinner("⏳ جاري حساب 8760 ساعة في السنة... 5 ثواني"):
        shading_hours, annual_loss = calculate_annual_shading(lat, lon, obstacle_h, obstacle_dist, date.year)

    st.success("✅ تم الحساب وحفظ النتيجة")
    col1, col2 = st.columns(2)
    col1.metric("ساعات التظليل في السنة", f"{shading_hours:,} ساعة")
    col2.metric("الفقد السنوي المتوقع", f"{annual_loss:.1f}%")

    if annual_loss > 5:
        st.error(f"⚠️ الفقد {annual_loss:.1f}% عالي! يجب إبعاد العائق أو زيادة ارتفاع الصفوف")
        st.info(f"المسافة الآمنة حسب IEC: {obstacle_h * 2.5:.1f} متر")
    else:
        st.success(f"✅ الفقد {annual_loss:.1f}% مقبول حسب المعايير")

    # تخزين النتيجة للتقرير النهائي
    st.session_state.shading_loss = annual_loss

# رسم 3D
st.divider()
st.subheader("رسم الظل ثلاثي الأبعاد")

fig = go.Figure()
for i in range(3):
    x0 = i * row_spacing
    fig.add_trace(go.Mesh3d(
        x=[x0, x0+1, x0+1, x0],
        y=[0, 0, 2, 2],
        z=[0, 0, 0, 0],
        color='blue', opacity=0.6, name=f'صف {i+1}'
    ))

fig.add_trace(go.Mesh3d(
    x=[obstacle_dist, obstacle_dist+0.5, obstacle_dist+0.5, obstacle_dist],
    y=[0, 0, 0.5, 0.5],
    z=[0, 0, obstacle_h, obstacle_h],
    color='gray', opacity=0.8, name='العائق'
))

if elevation > 0:
    shadow_x = obstacle_dist + shadow_length
    fig.add_trace(go.Mesh3d(
        x=[obstacle_dist, shadow_x, shadow_x, obstacle_dist],
        y=[-1, -1, 1, 1],
        z=[0, 0, 0, 0],
        color='black', opacity=0.4, name='الظل'
    ))

fig.update_layout(
    scene=dict(xaxis_title='المسافة متر', yaxis_title='العرض متر', zaxis_title='الارتفاع متر'),
    height=450, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

if st.button("التالي: المعايير 📊"):
    st.switch_page("pages/05_📚_المعايير.py")
