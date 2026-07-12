import streamlit as st
with open("../style.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.title("👤 تسجيل الدخول")
email = st.text_input("الايميل")
password = st.text_input("كلمة السر", type="password")
if st.button("دخول", type="primary"):
    if email == "electricgirl804@gmail.com" and password == "shahd8499":
        st.session_state.logged_in = True; st.session_state.user = email; st.rerun()
    else: st.error("بيانات خاطئة")
