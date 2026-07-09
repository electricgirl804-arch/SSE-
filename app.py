import streamlit as st
import os

st.set_page_config(
    page_title="محاكي المنظومة SSE", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {padding-top: 1rem!important; direction: rtl !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    [data-testid="stToolbar"] {zoom: 0.5 !important; opacity: 0.15 !important;}
    html, body {direction: rtl !important; text-align: center !important; font-family: 'Cairo', sans-serif !important;}
    h1 {color: #FFD700!important; font-size: 34px!important; font-weight: 700!important; margin-top: 10px!important;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ محاكي المنظومة SSE")
st.markdown("SSE | IEC 60364 + NEC 430")
st.warning("⚠️ يرجى الرجوع لصفحة الاحمال واضافة الاجهزة أولاً")

if st.button("⬅️ الرجوع لصفحة الاحمال"):
    st.switch_page("pages/الرئيسية.py") # <-- عدلتو هنا
