import streamlit as st

st.title("⚙️ إعدادات المنصة")

st.header("أسعار المكونات")
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.price_panel = st.number_input("سعر اللوح 550W", value=85, key="p1")
with col2:
    st.session_state.price_battery = st.number_input("سعر البطارية 48V", value=280, key="b1")
with col3:
    st.session_state.price_inverter = st.number_input("سعر الانفرتر", value=450, key="i1")

st.divider()
st.header("معاملات الحساب")
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.system_eff = st.slider("كفاءة النظام %", 70, 95, 85)
with col2:
    st.session_state.dod = st.slider("عمق التفريغ %", 50, 90, 80)
with col3:
    st.session_state.inverter_eff = st.slider("كفاءة الانفرتر %", 90, 98, 95)

st.success("تم حفظ الإعدادات. ارجع للصفحة الرئيسية لإعادة الحساب")
