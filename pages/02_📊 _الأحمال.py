import streamlit as st
import math
import pandas as pd
from utils import check_login, logout, load_css

check_login()
logout()
load_css()

st.title("📊 حاسبة تصميم النظام الشمسي")
st.caption("اختر الاجهزة الكهربائية لحساب حجم النظام المناسب لك")

# ===== CSS للكروت =====
st.markdown("""
<style>
.device-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; }
.device-card button {
    background-color: #112240 !important;
    border: 2px solid #233554 !important;
    border-radius: 15px !important;
    padding: 20px 10px !important;
    text-align: center !important;
    width: 100% !important;
    height: 130px !important;
    color: white !important;
    font-weight: 600 !important;
}
.device-card button:hover {
    border-color: #64ffda !important;
    background-color: #1a365d !important;
    transform: scale(1.03);
}
.device-icon { font-size: 35px; display: block; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# ===== 1. قاعدة بيانات الاجهزة العامة =====
if 'devices_db' not in st.session_state: 
    st.session_state.devices_db = {
        "منزل سكني": {
            "💡": ["إضاءة LED", 10, 1, 5], 
            "🌀": ["مروحة سقف", 70, 1.5, 8], 
            "📺": ["تلفزيون", 120, 1, 6],
            "❄️": ["مكيف اسبلت 1.5 حصان", 1500, 3, 8],
            "🧊": ["ثلاجة منزلية", 200, 2.5, 24],
            "📱": ["شواحن ورواتر", 50, 1, 24]
        },
        "مركز صحي": {
            "🧊": ["ثلاجة أدوية", 300, 2.5, 24], 
            "💡": ["إضاءة", 40, 1, 12],
            "🖥️": ["جهاز كمبيوتر", 250, 1, 8],
            "🩺": ["جهاز طبي صغير", 150, 1.5, 6]
        },
        "مكتب / محل": {
            "💻": ["لابتوب", 65, 1, 8], 
            "🖨️": ["طابعة", 400, 2, 3],
            "💡": ["إضاءة مكتب", 20, 1, 10],
            "❄️": ["مكيف شباك", 1200, 3, 8]
        },
        "مزرعة": {
            "💧": ["مضخة مياه 1 حصان", 750, 3, 4],
            "💡": ["إضاءة خارجية", 100, 1, 12],
            "🌀": ["شفاط", 200, 1.5, 10]
        }
    }
if 'loads' not in st.session_state: 
    st.session_state.loads = []

place_type = st.selectbox("📍 نوع المنشأة", list(st.session_state.devices_db.keys()))

# ===== 2. عرض الاجهزة ككروت =====
st.subheader("اختر الاجهزة")
st.markdown('<div class="device-grid">', unsafe_allow_html=True)
devices = st.session_state.devices_db[place_type]

cols = st.columns(4)
for i, (icon, data) in enumerate(devices.items()):
    name, watt, start, hours = data
    with cols[i % 4]:
        st.markdown('<div class="device-card">', unsafe_allow_html=True)
        if st.button(f"{icon}\n{name}\n{watt} واط", key=f"btn_{icon}_{name}"):
            kwh_day = watt * hours / 1000
            found = False
            for item in st.session_state.loads:
                if item["الجهاز"] == name:
                    item["العدد"] += 1
                    item["kWh/يوم"] = round(item["العدد"] * watt * hours / 1000, 2)
                    found = True
                    break
            if not found:
                st.session_state.loads.append({
                    "الجهاز": name, "العدد": 1, "الواط": watt, "الساعات": hours, "kWh/يوم": round(kwh_day, 2)
                })
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ===== 3. الجدول والنتائج =====
if len(st.session_state.loads) > 0:
    st.subheader("📋 ملخص الاحمال")
    df = pd.DataFrame(st.session_state.loads)
    st.dataframe(df, use_container_width=True, hide_index=True)

    total_kwh = df['kWh/يوم'].sum()
    peak_w = sum([row['الواط'] * row['العدد'] for _, row in df.iterrows()])
    peak_kw = peak_w / 1000 * 2.5

    # معادلات التصميم المعتمدة
    irradiance = 5.5  # متوسط ساعات الذروة
    system_eff = 0.77
    system_kw = (total_kwh / irradiance) / system_eff

    inv_kw = math.ceil(peak_kw * 1.2)
    panels = math.ceil((system_kw * 1000) / (550 * system_eff))
    batteries = math.ceil((total_kwh * 1.5) / (48 * 0.8))

    st.subheader("📈 التوصية الفنية")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("الاستهلاك اليومي", f"{total_kwh:.2f} كيلو واط ساعة")
    c2.metric("قدرة الانفرتر", f"{inv_kw} كيلو فولت امبير")
    c3.metric("عدد الالواح", f"{panels} لوح 550W")
    c4.metric("البطاريات", f"{batteries} بطارية 100Ah")

    st.success(f"**القدرة المقترحة للنظام: {system_kw:.2f} كيلو واط**")

    # حفظ البيانات للصفحات الاخرى
    st.session_state.total_kwh = round(total_kwh, 2)
    st.session_state.array_kw = round(system_kw, 2)
    st.session_state.num_panels = panels
    st.session_state.inverter_kw = inv_kw
    st.session_state.battery_ah = batteries * 100
    st.session_state.battery_volt = 48

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚡ الذهاب للمحاكي", type="primary", use_container_width=True):
            st.switch_page("pages/03_⚡_المحاكي.py")
    with col2:
        if st.button("📄 انشاء التقرير", use_container_width=True):
            st.switch_page("pages/07_📄_التقرير_والعقد.py")
else:
    st.info("👆 اضغط على اي جهاز لاضافته الى جدول الاحمال")
