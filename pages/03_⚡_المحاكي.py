import streamlit as st
import pandas as pd

st.set_page_config(page_title="SSE - الأحمال", page_icon="⚡", layout="wide")
st.title("⚡ محاكي الأحمال الذكي SSE")
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v1.2")

st.markdown("احسب استهلاكك الشهري وعدد الألواح والبطاريات المطلوبة")
st.divider()

# إدخال الأجهزة
st.subheader("1. أضف الأجهزة الكهربائية")

if 'loads' not in st.session_state:
    st.session_state.loads = pd.DataFrame(columns=["الجهاز", "العدد", "الوات", "ساعات التشغيل", "الطاقة Wh"])

with st.form("add_load", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        device = st.text_input("اسم الجهاز", placeholder="مكيف، لمبة، شاشة")
    with col2:
        qty = st.number_input("العدد", 1, 20, 1)
    with col3:
        watt = st.number_input("القدرة بالواط", 10, 5000, 100)
    with col4:
        hours = st.number_input("ساعات التشغيل/اليوم", 0.5, 24.0, 5.0, 0.5)

    submitted = st.form_submit_button("➕ إضافة الجهاز")
    if submitted and device:
        energy = qty * watt * hours
        new_row = pd.DataFrame([[device, qty, watt, hours, energy]],
                                columns=["الجهاز", "العدد", "الوات", "ساعات التشغيل", "الطاقة Wh"])
        st.session_state.loads = pd.concat([st.session_state.loads, new_row], ignore_index=True)
        st.success(f"تمت إضافة {device}")

# عرض الأجهزة المضافة
st.divider()
if not st.session_state.loads.empty:
    st.subheader("2. الأجهزة المضافة")
    st.dataframe(st.session_state.loads, use_container_width=True, hide_index=True)
    
    total_wh = st.session_state.loads["الطاقة Wh"].sum()
    total_watt = st.session_state.loads["الوات"].sum()
    total_kwh = total_wh / 1000
    
    col1, col2, col3 = st.columns(3)
    col1.success(f"إجمالي القدرة: {total_watt:,} واط")
    col2.success(f"الاستهلاك اليومي: {total_kwh:.2f} كيلو واط/ساعة")
    col3.info(f"الاستهلاك الشهري: {total_kwh * 30:.2f} كيلو واط/ساعة")
    
    # اقتراح المنظومة
    st.divider()
    st.subheader("3. المنظومة المقترحة")
    panels = int(total_watt / 550) + 1  # لوح 550 واط
    battery_ah = int(total_kwh * 2 * 1000 / 48)  # بطاريات 48V تكفي يومين
    
    col1, col2 = st.columns(2)
    col1.metric("عدد الألواح 550W", f"{panels} لوح")
    col2.metric("سعة البطاريات 48V", f"~{battery_ah} أمبير")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 اطلب عرض سعر"):
            st.switch_page("pages/SSE_12_ℹ️_عن_المنصة.py")
    with col2:
        if st.button("🗑️ مسح كل الأحمال"):
            st.session_state.loads = pd.DataFrame(columns=["الجهاز", "العدد", "الوات", "ساعات التشغيل", "الطاقة Wh"])
            st.rerun()
else:
    st.info("أضف أول جهاز عشان يتم الحساب")

st.divider()
if st.button("🔙 الرجوع للرئيسية"):
    st.switch_page("pages/SSE_01_🏠_الرئيسية.py")
