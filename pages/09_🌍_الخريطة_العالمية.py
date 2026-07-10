import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.set_page_config(page_title="الخريطة - SSE", layout="wide")

# ===== CSS =====
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
    h1, h2 { color: #FFD700!important; font-weight: 800; text-align: center; }
.stCaption { color: #FFFFFF!important; text-align: center; }
.info-card { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; 
             box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-left: 5px solid #FFD700; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌍 خريطة الموقع والإشعاع الشمسي</h1>", unsafe_allow_html=True)
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v2.4")

if 'lat' in st.session_state:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### موقع المشروع على الخريطة")
        
        # انشاء الخريطة
        m = folium.Map(
            location=[st.session_state.lat, st.session_state.lon], 
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        
        # اضافة Marker للموقع
        folium.Marker(
            [st.session_state.lat, st.session_state.lon],
            popup=folium.Popup(f"""
                <b>موقع المشروع</b><br>
                الإحداثيات: {st.session_state.lat:.4f}, {st.session_state.lon:.4f}<br>
                الإشعاع: {st.session_state.ghi_final:.2f} kWh/m²/day
            """, max_width=300),
            tooltip="📍 موقع المشروع",
            icon=folium.Icon(color="red", icon="sun", prefix="fa")
        ).add_to(m)
        
        # اضافة دائرة حول الموقع
        folium.Circle(
            location=[st.session_state.lat, st.session_state.lon],
            radius=1000,
            color="#FFD700",
            fill=True,
            fill_opacity=0.2,
            popup="نطاق 1 كيلومتر"
        ).add_to(m)
        
        st_folium(m, width=700, height=500)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 بيانات الموقع")
        
        st.metric("خط العرض", f"{st.session_state.lat:.4f}°")
        st.metric("خط الطول", f"{st.session_state.lon:.4f}°")
        st.metric("الإشعاع GHI", f"{st.session_state.ghi_final:.2f} kWh/m²/day")
        st.metric("زاوية الميل المثلى", f"{st.session_state.final_tilt:.1f}°")
        
        st.divider()
        st.markdown("### 💡 ملاحظة")
        st.info(f"الموقع دا مناسب جداً للطاقة الشمسية. \nمتوسط الإشعاع {st.session_state.ghi_final:.2f} يعتبر ممتاز")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### توصيات التركيب حسب الموقع")
    st.write(f"1. **زاوية الميل المثلى**: {st.session_state.final_tilt:.1f}° باتجاه الجنوب")
    st.write(f"2. **نوع الألواح المقترح**: Mono PERC 550W - مناسب للإشعاع {st.session_state.ghi_final:.2f}")
    st.write("3. **التنظيف**: يوصى بالتنظيف كل شهرين بسبب الأتربة")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ لم يتم تحديد الموقع بعد")
    st.info("ارجع للصفحة الرئيسية وحدد موقعك من الخريطة")
    st.page_link("app.py", label="العودة للصفحة الرئيسية", icon="🏠")

st.markdown("---")
st.caption("شركة SSE للطاقة الشمسية | الدعم الفني: 0110560222")
