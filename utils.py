import streamlit as st
import os

def check_login():
    if 'logged_in' not in st.session_state: 
        st.session_state.logged_in = False
    if not st.session_state.logged_in: 
        st.switch_page("pages/01_👤_تسجيل_الدخول.py")

def logout():
    if st.sidebar.button("🚪 تسجيل الخروج"): 
        st.session_state.logged_in = False
        st.rerun()

def load_css():
    """بتفتش على style.css في الجذر او جوه pages"""
    possible_paths = ["style.css", "../style.css"]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f: 
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            return
    # لو ما لقاه ما بعمل شي وما بضرب
