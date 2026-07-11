import streamlit as st
st.set_page_config(page_title="الرئيسية - SSE", layout="wide")

st.title("🌞 SSE للطاقة الشمسية")
st.caption("اختار الخدمة المناسبة")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/01_👤_تسجيل_الدخول.py", label="تسجيل الدخول")
    st.page_link("pages/02_🛠️_الأحمال.py", label="حساب الأحمال")
with col2:
    st.page_link("pages/09_🌍_الخريطة_العالمية.py", label="الخريطة وناسا")
    st.page_link("pages/06_🛒_السلة_والمتجر.py", label="المتجر")
with col3:
    st.page_link("pages/15_لوحة_الأدمن.py", label="لوحة الأدمن")
    st.page_link("pages/14_🤖_بوت_Gemini.py", label="بوت Gemini")
