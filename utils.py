import streamlit as st
def check_login():
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if not st.session_state.logged_in: st.switch_page("pages/01_👤_تسجيل_الدخول.py")
def logout():
    if st.sidebar.button("🚪 تسجيل الخروج"): st.session_state.logged_in=False; st.rerun()
def load_css():
    with open("style.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
