import streamlit as st
with open("../style.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.title("🏠 الرئيسية - منصة SSE")
st.success("مرحبا بك في منصة الطاقة الشمسية الذكية الاولى في السودان")
c1, c2, c3 = st.columns(3)
c1.page_link("pages/02_📊_الأحمال.py", label="📊 ابدأ الحسابات")
c2.page_link("pages/06_🛒_السلة_والمتجر.py", label="🛒 المتجر")
c3.page_link("pages/14_🤖_بوت_Gemini.py", label="🤖 اسأل البوت")
if st.button("🚪 تسجيل الخروج"): st.session_state.logged_in=False; st.rerun()
