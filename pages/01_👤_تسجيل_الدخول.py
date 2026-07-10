import streamlit as st
from utils import load_css
from config import ADMIN_PASSWORD
load_css()
st.title("👤 تسجيل الدخول")
role = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True)
name = st.text_input("الاسم")
password = st.text_input("كلمة السر", type="password")
if st.button("دخول"):
    if role == "ادمن" and password == ADMIN_PASSWORD:
        st.session_state.user = {"name": name, "role": "admin"}; st.success("مرحباً م. شهد"); st.switch_page("pages/18_🔒_لوحة_الادمن.py")
    elif role == "عميل":
        st.session_state.user = {"name": name, "role": "customer"}; st.success(f"اهلا {name}"); st.switch_page("pages/02_🔌_الأحمال.py")
    else: st.error("كلمة السر خطأ")
