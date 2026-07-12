import streamlit as st; import math
with open("../style.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.title("📊 حاسبة النظام الهندسية 100%")
if 'devices_db' not in st.session_state: st.session_state.devices_db = {"🏠 منزل": {"💡 لمبة": [10, 1, 5]}, "🏥 مركز صحي": {"🧊 تلاجة ادوية": [300, 2.5, 24]}}
if 'loads_db' not in st.session_state: st.session_state.loads_db = {p:{} for p in st.session_state.devices_db.keys()}
calc_type = st.radio("طريقة الحساب", ["⚡ بالأحمال", "💰 بالفاتورة"], horizontal=True)
place_type = st.selectbox("اختار المنشأة", list(st.session_state.devices_db.keys()))
with st.expander("➕ اضافة جهاز"): d_name = st.text_input("اسم الجهاز"); d_watt = st.number_input("الواط", 1, 10000, 100); d_start = st.selectbox("الحمل", [1, 2.5, 3]); d_hours = st.number_input("الساعات", 1, 24, 8)
if st.button("اضافة"): st.session_state.devices_db[place_type][d_name] = [d_watt, d_start, d_hours]; st.session_state.loads_db[place_type][d_name] = 0; st.rerun()
total_kwh = 0; peak_kw = 0
if calc_type == "⚡ بالأحمال":
    for d, data in st.session_state.devices_db[place_type].items():
        w, s, h = data; qty = st.number_input(d, 0, 50, st.session_state.loads_db[place_type].get(d,0), key=f"{place_type}_{d}")
        st.session_state.loads_db[place_type][d]=qty; total_kwh += qty*w*h/1000; peak_kw = max(peak_kw, qty*w*s/1000)
    system_kw = (total_kwh / 5.5) / 0.77
else:
    monthly_kwh = st.number_input("kWh شهري", 100, 50000, 500); total_kwh = monthly_kwh/30; system_kw = (total_kwh / 5.5) / 0.77
st.divider()
if total_kwh > 0:
    inv_kw = math.ceil(peak_kw * 1.1); panels = math.ceil((system_kw*1000)/(550*0.77)); batteries = math.ceil(system_kw*2)
    c1,c2,c3 = st.columns(3); c1.metric("الانفرتر", f"{inv_kw} KW"); c2.metric("الالواح", f"{panels} لوح"); c3.metric("البطاريات", f"{batteries} بطارية")
    st.success(f"النظام: {system_kw:.2f} KW")
