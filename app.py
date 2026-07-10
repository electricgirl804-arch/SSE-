import streamlit as st
from utils import load_css, show_logo_as_cover
from config import COMPANY_NAME, FOOTER

st.set_page_config(
    page_title=COMPANY_NAME, 
    layout="wide", 
    page_icon="logo.ico",  # ايقونة البرنامج "الضوءة"
    initial_sidebar_state="collapsed" # القائمة مقفولة
)

load_css() 
show_logo_as_cover() # بعرض logo.png الكبير كغلاف

st.markdown(f"<h1 style='text-align: center; color: #FFC107;'>{COMPANY_NAME}</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>اول منصة ذكية متكاملة للطاقة الشمسية في السودان</h3>", unsafe_allow_html=True)
st.divider()

c1, c2, c3 = st.columns(3)
c1.metric("السرعة", "3 دقايق", "لحساب نظامك")
c2.metric("الضمان", "10 سنوات", "على التركيب")
c3.metric("الدعم", "24/7", "واتساب مباشر")

st.info("👈 ابدئي من القائمة الجانبية > تسجيل الدخول")
st.markdown(f"---\n{FOOTER}")
