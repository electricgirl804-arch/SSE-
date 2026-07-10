import streamlit as st
from PIL import Image

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True
    if not st.session_state.logged_in:
        st.warning("⚠️ الرجاء تسجيل الدخول اولا")
        st.stop()

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; }
   .stApp { direction: rtl; }
   .block-container {padding-top: 2rem;}
    </style>
    """, unsafe_allow_html=True)

def show_logo_as_cover():
    """الدالة دي كانت ناقصة"""
    try:
        logo = Image.open("assets/logo.png")
        st.image(logo, use_container_width=True)
    except:
        st.title("Smart Solara Engineer")
