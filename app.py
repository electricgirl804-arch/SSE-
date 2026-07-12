import streamlit as st
st.set_page_config(page_title="SSE", layout="wide", page_icon="☀️")
with open("style.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in: st.switch_page("pages/01_👤_تسجيل_الدخول.py")
else: st.switch_page("pages/00_🏠_الرئيسية.py")
