import streamlit as st
from utils import load_css, show_logo_as_cover

COMPANY_NAME = "SSE - الطاقة الشمسية الذكية"
FOOTER = "© 2026 SSE. جميع الحقوق محفوظة"

st.set_page_config(
    page_title=COMPANY_NAME, 
    layout="wide", 
    page_icon="☀️",
    initial_sidebar_state="collapsed"
)

load_css()
show_logo_as_cover()

st.markdown(f"<h1 style='text-align: center;'>{COMPANY_NAME}</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>اول منصة ذكية متكاملة للطاقة الشمسية في السودان</h3>", unsafe_allow_html=True)
st.divider()

c1, c2, c3 = st.columns(3)
c1.metric("السرعة", "3 دقايق", "لحساب نظامك")
c2.metric("الضمان", "10 سنوات", "على التركيب")
c3.metric("الدعم", "24/7", "واتساب مباشر")

st.info("ابدأ من القائمة الجانبية > تسجيل الدخول")  # شلت الايموجي

st.markdown(f"<center>{FOOTER}</center>", unsafe_allow_html=True)
