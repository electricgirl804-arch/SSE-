import streamlit as st
from utils import load_css, show_header, logout

st.set_page_config(
    page_title="SSE - Smart Solara Engineer",
    page_icon="☀️",  # غيرتها من logo.png
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;} 
    </style>
    """, unsafe_allow_html=True)

load_css()
st.session_state.logged_in = True  # فتحنا الدخول مؤقتا
show_header()
logout()

st.image("logo.png", width=180) # ضفت اللوجو هنا
st.markdown("<h1 style='text-align:center; color:white;'>🌞 مرحبا بك في SSE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white;'>بيع + تأجير + موردين في مكان واحد</p>", unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/01_👤_تسجيل_الدخول.py", label="🔑 تسجيل الدخول")
    st.page_link("pages/02_🔧_الاحمال.py", label="📊 حساب الأحمال")
with col2:
    st.page_link("pages/09_🌍_الخريطة_العالمية.py", label="🌍 الخريطة + ناسا")
    st.page_link("pages/06_🛒_السلة_والمتجر.py", label="🛒 السلة والمتجر")
with col3:
    st.page_link("pages/14_🤖_بوت_Gemini.py", label="🤖 بوت Gemini")
    st.page_link("pages/15_لوحة_الادمن.py", label="⚙️ لوحة الأدمن")

st.divider()
st.info("📱 للدفع: حول على الرقم 0110560222 و رسل الاشعار واتساب")
