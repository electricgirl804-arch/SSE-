import streamlit as st
import folium
import requests
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium

st.set_page_config(page_title="الخريطة - SSE", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
h1, h2, h3 { color: #FFD700!important; font-weight: 800; text-align: center; }
.stCaption { color: #FFFFFF!important; text-align: center; }
.info-card { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;
             box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-left: 5px solid #FFD700; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌍 خريطة الموقع والإشعاع الشمسي</h1>", unsafe_allow_html=True)
st.caption("البيانات من NASA POWER | SSE v2.5")

def get_nasa_solar_data(lat, lon):
    """يجيب بيانات الاشعاع الشهرية من NASA POWER"""
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON"
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        data = res.json()
        ghi_monthly = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        temp_monthly = data['properties']['parameter']['T2M']

        df = pd.DataFrame({
            'الشهر': ['يناير','فبراير','مارس','ابريل','مايو','يونيو','يوليو','اغسطس','سبتمبر','اكتوبر','نوفمبر','ديسمبر'],
            'GHI': [ghi_monthly[k] for k in ghi_monthly.keys()],
            'الحرارة': [(temp_monthly[k] - 273.15) for k in temp_monthly.keys()]
        })
        df['GHI'] = df['GHI'].round(2)
        df['الحرارة'] = df['الحرارة'].round(1)
        return df
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")
        return None

if 'lat' in st.session_state and 'lon' in st.session_state:

    with st.spinner("⏳ جاري جلب بيانات ناسا..."):
        df_nasa = get_nasa_solar_data(st.session_state.lat, st.session_state.lon)

    if df_nasa is not None:
        ghi_avg = df_nasa['GHI'].mean()
        st.session_state.ghi_final = ghi_avg
        st.session_state.final_tilt = abs(st.session_state.lat)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("### موقع المشروع على الخريطة")
            m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12, tiles="CartoDB positron")
            folium.Marker(
                [st.session_state.lat, st.session_state.lon],
                popup=f"GHI المتوسط: {ghi_avg:.2f} kWh/m²/day",
                icon=folium.Icon(color="red", icon="solar-panel", prefix="fa")
            ).add_to(m)
            folium.Circle([st.session_state.lat, st.session_state.lon], radius=1000, color="#FFD700", fill=True, fill_opacity=0.2).add_to(m)
            st_folium(m, width=None, height=400, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 ملخص البيانات")
            st.metric("متوسط GHI السنوي", f"{ghi_avg:.2f} kWh/m²/day")
            st.metric("اعلى شهر", f"{df_nasa.loc[df_nasa['GHI'].idxmax(), 'الشهر']} - {df_nasa['GHI'].max()} ")
            st.metric("اقل شهر", f"{df_nasa.loc[df_nasa['GHI'].idxmin(), 'الشهر']} - {df_nasa['GHI'].min()} ")
            st.metric("زاوية الميل", f"{st.session_state.final_tilt:.1f}°")
            if ghi_avg > 5.5: st.success("ممتاز للطاقة الشمسية ☀️")
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        # الرسم البياني
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 الاشعاع الشمسي خلال 12 شهر")

        fig = px.bar(df_nasa, x='الشهر', y='GHI',
                     title='متوسط الاشعاع الشمسي اليومي',
                     labels={'GHI': 'kWh/m²/day', 'الشهر': ''},
                     color='GHI', color_continuous_scale='YlOrRd',
                     text='GHI')
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(title_font_size=18, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ لم يتم تحديد الموقع بعد")
    st.page_link("01_🏠_الرئيسية.py", label="العودة للصفحة الرئيسية", icon="🏠")

st.markdown("---")
st.caption("شركة SSE للطاقة الشمسية | الدعم الفني: 0110560222")
