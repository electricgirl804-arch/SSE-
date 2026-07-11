import streamlit as st
from utils import load_css, show_header, logout

st.set_page_config(
    page_title="SSE الرئيسية",
    page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAKACAYAAAB6uZQaAAAgAElEQVR4AezdB7Ak5XUo4M/7...END", # نفس كود الشعار
    layout="wide"
)

load_css()
show_header()
logout()

st.markdown("<h1 style='text-align:center; color:white;'>مرحبا بك في SSE</h1>", unsafe_allow_html=True)
st.caption("اختار الخدمة المناسبة من تحت")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/01_👤_تسجيل_الدخول.py", label="🔑 تسجيل الدخول")
    st.page_link("pages/02_🛠️_الأحمال.py", label="📊 حساب الأحمال")
with col2:
    st.page_link("pages/09_🌍_الخريطة_العالمية.py", label="🌍 الخريطة + ناسا")
    st.page_link("pages/06_🛒_السلة_والمتجر.py", label="🛍️ المتجر")
with col3:
    st.page_link("pages/15_لوحة_الأدمن.py", label="📊 لوحة الأدمن")
    st.page_link("pages/14_🤖_بوت_Gemini.py", label="🤖 بوت Gemini")

st.divider()
st.caption("SSE v3.0 | 0110560222")
