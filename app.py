import streamlit as st

st.set_page_config(page_title="الأعطال 06", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    header {visibility: hidden !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    * {direction: rtl !important; text-align: right !important;}
   .block-container {padding-top: 2rem!important;}
    h1 {text-align: center!important; color: #FFD700!important; font-size: 30px!important;}
</style>
""", unsafe_allow_html=True)

st.switch_page("pages/01_🏠_الرئيسية.py")
