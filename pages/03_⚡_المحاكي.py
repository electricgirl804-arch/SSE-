import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="SSE - محاكي الأحمال", page_icon="⚡", layout="wide")

# CSS عام احترافي
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
h1 {color: #FFD700 !important; font-weight: 700; text-align: center; padding: 20px 0;}
h3 {color: #4FC3F7 !important; border-right: 4px solid #FFD700; padding-right: 15px; margin-top: 30px;}
.stMetric {background: rgba(255,255,255,0.08); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.3);}
.stMetric:hover {transform: translateY(-5px); border-color: #FFD700;}
.stMetric div {font-size: 32px !important; font-weight: 700 !important; color: #FFD700 !important;}
.stButton>button {background: linear-gradient(90deg, #FFD700 0%, #FFA000 100%); border: none; border-radius: 12px; color: #0f2027; font-weight: 700; font-size: 16px; padding: 12px 25px;}
.stDataFrame {border-radius: 15px; overflow: hidden; border: 2px solid rgba(255,215,0,0.2);}
</style>
""", unsafe_allow_html=True)

st.title("⚡ محاكي الأحمال الذكي SSE")
st.caption("تم التطوير بواسطة فريق SSE | الإصدار v2.1")

# التحقق من القيم الجاية من الصفحة الرئيسية
if 'irradiance' not in st.session_state:
    st.error("⚠️ يرجى الرجوع للصفحة الرئيسية وتحديد الموقع GPS أولاً")
    if st.button("🔙 الرجوع للصفحة الرئيسية"):
        st.switch_page("pages/SSE_01_🏠_الرئيسية.py")
    st.stop()

irradiance = st.session_state.irradiance
tilt = st.session_state.tilt
azimuth = st.session_state.azimuth

st.info(f"الإشعاع الشمسي من ناسا: {irradiance:.2f} kWh/m²/day | زاوية الميلان: {tilt:.1f}° | اتجاه التركيب: {azimuth}°")
st.divider()

# إدخال الأجهزة
st.subheader("1. إضافة الأجهزة الكهربائية")

if 'loads' not in st.session_state:
    st.session_state.loads = pd.DataFrame(columns=["الجهاز", "العدد", "القدرة W", "ساعات التشغيل", "الطاقة Wh/يوم"])

with st.form("add_load", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        device = st.text_input("اسم الجهاز", placeholder="مثال: مكيف، لمبة، شاشة")
    with col2:
        qty = st.number_input("العدد", 1, 50, 1)
    with col3:
        watt = st.number_input("القدرة بالواط", 1, 5000, 100)
    with col4:
        hours = st.number_input("ساعات التشغيل/اليوم", 0.5, 24.0, 5.0, 0.5)

    submitted = st.form_submit_button("➕ إضافة الجهاز", type="primary")
    if submitted:
        if not device:
            st.warning("يرجى إدخال اسم الجهاز")
        else:
            energy = qty * watt * hours
            new_row = pd.DataFrame([[device, qty, watt, hours, energy]],
                                    columns=["الجهاز", "العدد", "القدرة W", "ساعات التشغيل", "الطاقة Wh/يوم"])
            st.session_state.loads = pd.concat([st.session_state.loads, new_row], ignore_index=True)
            st.success(f"تمت إضافة {device} بنجاح")
            st.rerun()

# عرض الأجهزة المضافة
st.divider()
if not st.session_state.loads.empty:
    st.subheader("2. ملخص الأحمال المضافة")
    st.dataframe(st.session_state.loads, use_container_width=True, hide_index=True)
    
    total_wh = st.session_state.loads["الطاقة Wh/يوم"].sum()
    total_watt = st.session_state.loads["القدرة W"].sum()
    total_kwh = total_wh / 1000
    
    col1, col2, col3 = st.columns(3)
    col1.metric("القدرة اللحظية الكلية", f"{total_watt:,} واط")
    col2.metric("الاستهلاك اليومي", f"{total_kwh:.2f} kWh")
    col3.metric("الاستهلاك الشهري", f"{total_kwh * 30:.2f} kWh")
    
    # اقتراح المنظومة - حساب هندسي
    st.divider()
    st.subheader("3. النظام المقترح")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        panel_watt = st.selectbox("قدرة اللوح الشمسي W", [450, 550, 580, 600], index=1)
    with col2:
        dod = st.slider("عمق التفريغ DoD %", 50, 80, 70) / 100
    with col3:
        days = st.number_input("أيام الاستقلالية بدون شمس", 1, 5, 2)
    
    # معاملات النظام حسب IEC
    PR = 0.82  # Performance Ratio
    inverter_eff = 0.96
    
    # حساب عدد الألواح
    panel_energy = panel_watt * irradiance * PR / 1000  # kWh من لوح واحد
    num_panels = total_kwh / panel_energy
    num_panels_round = math.ceil(num_panels)
    array_kw = num_panels_round * panel_watt / 1000
    
    # حساب البطاريات
    battery_wh = (total_kwh * 1000 * days) / (dod * inverter_eff)
    battery_ah = battery_wh / 48
    
    # حساب الانفرتر +30% هامش أمان
    inverter_kw = total_watt * 1.3 / 1000
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("طاقة اللوح الواحد", f"{panel_energy:.2f} kWh/يوم")
    col2.metric("عدد الألواح المطلوبة", f"{num_panels:.1f}", delta=f"≈ {num_panels_round} لوح")
    col3.metric("قدرة المصفوفة الكلية", f"{array_kw:.2f} kW")
    col4.metric("الانفرتر المقترح", f"{inverter_kw:.2f} kW")
    
    col1, col2 = st.columns(2)
    col1.metric("سعة البطاريات 48V", f"{battery_ah:.0f} Ah")
    col2.metric("الاستهلاك اليومي المغطى", f"{total_kwh:.2f} kWh")
    
    st.success(f"""
    **التوصية النهائية للنظام:**
    - الألواح: {num_panels_round} لوح × {panel_watt}W = {array_kw:.2f} kW
    - البطاريات: {battery_ah:.0f}Ah @ 48V لاستقلالية {days} يوم
    - الانفرتر: {inverter_kw:.2f} kW موجة جيبية نقية
    - زاوية التركيب المثلى: {tilt:.1f}° واتجاه {azimuth}° جنوب
    """)
    
    # حفظ النتائج للتقرير
    st.session_state.num_panels = num_panels_round
    st.session_state.array_kw = array_kw
    st.session_state.battery_ah = battery_ah
    st.session_state.inverter_kw = inverter_kw
    st.session_state.total_kwh =
