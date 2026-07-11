import streamlit as st
from utils import load_css, show_logo_as_cover, check_login, logout

COMPANY_NAME = "SSE - الطاقة الشمسية الذكية"
FOOTER = "© 2026 SSE. جميع الحقوق محفوظة"

st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="☀️", initial_sidebar_state="expanded")

load_css()
show_logo_as_cover()
check_login()
logout()

st.markdown(f"<h1 style='text-align: center;'>{COMPANY_NAME}</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>اول منصة ذكية متكاملة للطاقة الشمسية في السودان</h3>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("السرعة", "3 دقايق", "لحساب نظامك")
col2.metric("الضمان", "10 سنوات", "على التركيب")
col3.metric("الدعم", "24/7", "واتساب مباشر")

st.info("ابدأ من القائمة الجانبية > اختار الصفحة العايزها")
if st.session_state.get('user_type') == 'admin':
    st.success("انت داخل كـ ادمن. امشي صفحة '15_لوحة_الادمن' من القائمة")
st.markdown(f"<center>{FOOTER}</center>", unsafe_allow_html=True)
