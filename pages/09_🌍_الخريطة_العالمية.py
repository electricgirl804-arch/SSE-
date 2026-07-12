import streamlit as st
import folium
import requests
import pandas as pd
import plotly.express as px
from utils import load_css, check_login, logout
from streamlit_geolocator import geolocator
from streamlit_folium import st_folium

st.set_page_config(page_title="الخريطة - SSE", layout="wide")
load_css()
check_login()
logout()

# ===== CSS موحد مع المنصة =====
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a192f 0%, #112240 100%); }
h1, h2, h3 { color: #64ffda!important; font-weight: 800; text-align: center; }
.stCaption { color: #ccd6f6!important; text-align: center; }
.info-card { background: #112240; padding: 20px; border-radius: 15px;
             border-left: 5px solid #64ffda; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 خريطة الموقع وبيانات NASA بالـ GPS")
st.caption("اضغط على الزر لتفعيل الـ GPS وجلب بيانات الاشعاع الشمسي من ناسا لموقعك")

def get_nasa_solar_data(lat, lon):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M", # GHI + الحرارة
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON"
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
            'الحرارة': [(temp_monthly[k] - 273.15) for k in temp_monthly.keys()] # من كلفن لسليزيوس
        })
        df['GHI'] = df['GHI'].round(2)
        df['الحرارة'] = df['الحرارة'].round(1)
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال بناسا: {e}")
        return None

# ===== جلب الـ GPS =====
location = geolocator("📍 اضغط هنا لتفعيل الـ GPS وجلب موقعك")

if location:
    lat = location['latitude']
    lon = location['longitude']
    st.session_state.lat = lat
    st.session_state.lon = lon
    st.success(f"✅ تم تحديد موقعك: خط العرض {lat:.4f}, خط الطول {lon:.4f}")
else:
    lat = st.session_state.get('lat', 15.5007) # الخرطوم افتراضي
    lon = st.session_state.get('lon', 32.5599)
    st.warning("⚠️ لم يتم تحديد الموقع. سيتم استخدام موقع الخرطوم كافتراضي")

with st.spinner("⏳ جاري جلب بيانات ناسا لموقعك..."):
    df_nasa = get_nasa_solar_data(lat, lon)

if df_nasa is not None:
    ghi_avg = df_nasa['GHI'].mean()
    temp_avg = df_nasa['الحرارة'].mean()
    st.session_state.ghi_final = ghi_avg # بنرسلها للحاسبة
    st.session_state.final_tilt = abs(lat) # زاوية الميل

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("موقع المشروع")
        m = folium.Map(location=[lat, lon], zoom_start=14, tiles="CartoDB positron")
        folium.Marker([lat, lon], popup=f"GHI: {ghi_avg:.2f}", tooltip="موقعك", icon=folium.Icon(color="red", icon="map-marker")).add_to(m)
        folium.Circle([lat, lon], radius=500, color="#64ffda", fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, height=400, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("📊 ملخص بيانات NASA")
        st.metric("متوسط GHI السنوي", f"{ghi_avg:.2f} kWh/m²/day")
        st.metric("متوسط الحرارة", f"{temp_avg:.1f} °C")
        st.metric("زاوية الميل المقترحة", f"{abs(lat):.1f}°")
        if ghi_avg > 5.5: st.success("☀️ ممتاز جداً للطاقة الشمسية")
        elif ghi_avg > 4.5: st.info("👍 جيد")
        else: st.warning("⚠️ متوسط")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.subheader("📈 الاشعاع الشمسي خلال 12 شهر")
    fig = px.bar(df_nasa, x='الشهر', y='GHI', color='GHI', color_continuous_scale='YlOrRd', text='GHI')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(paper_bgcolor='#112240', plot_bgcolor='#112240', font_color='white')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.page_link("app.py", label="🏠 الرجوع للرئيسية")
st.caption("المصدر: NASA POWER | شركة SSE للطاقة الشمسية")
