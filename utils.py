import streamlit as st
import base64
from pathlib import Path

def check_login():
    if 'user' not in st.session_state:
        st.warning("⚠️ لازم تسجل دخول اول")
        st.stop()

def load_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {font-family: 'Cairo', sans-serif; direction: rtl;}
    body {background: linear-gradient(135deg, #0D47A1 0%, #1A1A1A 100%); color: white;}
  .stButton>button {background: linear-gradient(90deg, #FFC107, #FFA000); color: black; border-radius: 15px; border: none; padding: 12px 25px; font-weight: bold; width: 100%;}
    h1, h2, h3 {color: #FFC107!important; text-align: center;}
    [data-testid="stSidebar"] {display: none!important;}
    [data-testid="collapsedControl"] {display: none!important;}
    </style>""", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f: data = f.read()
    return base64.b64encode(data).decode()

def show_logo_as_cover():
    logo_path = Path("assets/logo.png")
    if not logo_path.exists(): logo_path = Path("logo.png")
    if logo_path.exists():
        img_base64 = get_base64_of_bin_file(logo_path)
        st.markdown(f'<div style="text-align: center; padding-top: 20px;"><img src="data:image/png;base64,{img_base64}" width="300"></div>', unsafe_allow_html=True)
