import streamlit as st

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Cairo', sans-serif;
            direction: rtl;
        }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div style="background: linear-gradient(90deg, #0056b3, #007bff); padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <h1 style="color:white; text-align:center; margin:0; font-size:28px;">🌞 SSE - Smart Solara Engineer</h1>
            <p style="color:white; text-align:center; margin:5px 0 0 0; font-size:16px;">مطور</p>
            <p style="color:#cce5ff; text-align:center; margin:0; font-size:14px;">بيع + تأجير + موردين في مكان واحد</p>
        </div>
    """, unsafe_allow_html=True)

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        st.warning("يجب تسجيل الدخول اولا")
        st.stop()

def logout():
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
