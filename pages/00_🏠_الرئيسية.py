import streamlit as st
from utils import check_login, logout, load_css

check_login()
logout()
load_css()

st.title("🏠 الرئيسية - منصة SSE")
st.success("مرحبا بك في منصة الطاقة الشمسية الذكية الاولى في السودان")

c1, c2, c3 = st.columns(3)
c1.page_link("pages/02_📊_الأحمال.py", label="📊 ابدأ الحسابات")
c2.page_link("pages/03_⚡_المحاكي.py", label="⚡ المحاكي الهندسي")
c3.page_link("pages/14_🤖_بوت_Gemini.py", label="🤖 اسأل البوت")

st.divider()
st.info("منصة متكاملة لحساب وتصميم وبيع انظمة الطاقة الشمسية حسب IEC و NEC")
