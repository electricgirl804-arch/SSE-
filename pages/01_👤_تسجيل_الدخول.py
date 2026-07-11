import streamlit as st
st.set_page_config(page_title="تسجيل الدخول", layout="wide")
st.title("تسجيل الدخول SSE")
email = st.text_input("الايميل")
password = st.text_input("كلمة السر", type="password")
if st.button("دخول"): st.session_state.logged_in = True; st.switch_page("pages/02_⚡_الأحمال.py")
