import streamlit as st
from utils import load_css

load_css() # بتحمل الالوان الزرقاء والبرتقالي

st.title("👤 تسجيل الدخول")
st.write("مرحبا بعودتك في نظام SSE")

email = st.text_input("الايميل")
password = st.text_input("كلمة السر", type="password")

if st.button("دخول", type="primary", use_container_width=True):
    if email == "electricgirl804@gmail.com" and password == "shahd8499":
        st.session_state.logged_in = True
        st.session_state.user = email
        st.success("تم تسجيل الدخول بنجاح!")
        st.switch_page("app.py") # بوديك للصفحة الرئيسية
        st.rerun()
    else: 
        st.error("❌ بيانات خاطئة. حاول مرة اخرى")
