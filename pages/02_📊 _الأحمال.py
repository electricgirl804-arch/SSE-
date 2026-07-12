import streamlit as st; import math
from utils import check_login, logout, load_css
check_login(); logout(); load_css()
st.title("📊 حاسبة النظام الهندسية 100%")

if 'devices_db' not in st.session_state: 
    st.session_state.devices_db = {"🏠 منزل": {"💡 لمبة ليد": [10, 1, 5], "🌀 مروحة": [70, 1.5, 8]}, "🏥 مركز صحي": {"🧊 تلاجة ادوية": [300, 2.5, 24]}}
if 'loads' not in st.session_state: st.session_state.loads = []

calc_type = st.radio("طريقة الحساب", ["⚡ بالأحمال", "💰 بالفاتورة"], horizontal=True)
place_type = st.selectbox("اختار المنشأة", list(st.session_state.devices_db.keys()))

with st.expander("➕ اضافة جهاز جديد"):
    d_name = st.text_input("اسم الجهاز")
    d_watt = st.number_input("الواط", 1, 10000, 100)
    d_start = st.selectbox("معامل البدء", [1, 2.5, 3])
    d_hours = st.number_input("عدد الساعات", 1, 24, 8)
if st.button("اضافة للجدول"):
    st.session_state.loads.append({"الجهاز":d_name, "العدد":1, "الواط":d_watt, "الساعات":d_hours, "kWh/يوم":d_watt*d_hours/1000})

total_kwh = sum([i['kWh/يوم'] for i in st.session_state.loads])
peak_kw = sum([i['الواط']*i['العدد'] for i in st.session_state.loads])/1000 * 2.5
system_kw = (total_kwh / 5.5) / 0.77

st.divider()
if total_kwh > 0:
    st.dataframe(st.session_state.loads, use_container_width=True, hide_index=True)
    inv_kw = math.ceil(peak_kw * 1.1); panels = math.ceil((system_kw*1000)/(550*0.77)); batteries = math.ceil(system_kw*2)
    c1,c2,c3 = st.columns(3); c1.metric("الانفرتر", f"{inv_kw} KW"); c2.metric("الواح", f"{panels} لوح"); c3.metric("البطاريات", f"{batteries} بطارية")
    st.success(f"النظام المقترح: {system_kw:.2f} KW")

# ===== حفظ البيانات للمحاكي =====
    st.session_state.total_kwh = total_kwh
    st.session_state.total_va = peak_kw * 1000 
    st.session_state.total_surge = peak_kw * 1000 * 2.5
    st.session_state.irradiance = 5.5
    st.session_state.tilt = 15
    st.session_state.azimuth = 180
    if st.button("الذهاب للمحاكي الهندسي ➡️", type="primary"):
        st.switch_page("pages/03_⚡_المحاكي.py")
