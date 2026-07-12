import streamlit as st
from utils import load_css, show_header, check_login, logout

st.set_page_config(
    page_title="SSE - Smart Solara Engineer",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()
check_login()
show_header()
logout()

st.markdown("<h1 style='text-align:center; color:white;'>🌞 مرحبا بك في SSE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white;'>بيع + تأجير + موردين في مكان واحد</p>", unsafe_allow_html=True)

st.divider()
st.info("📱 للدفع: حول على الرقم 0110560222 و رسل الاشعار واتساب")
st.caption("SSE v3.0 | مطور")
