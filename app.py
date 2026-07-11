import streamlit as st
from utils import load_css
st.set_page_config(page_title="SSE للطاقة الشمسية", layout="wide", page_icon="☀️")
load_css()

st.title("☀️ SSE للطاقة الشمسية الذكية")
st.markdown("### بيع + تأجير + موردين في مكان واحد")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/06_🛒_السلة_والمتجر.py", label="🛒 ادخل المتجر")
with col2:
    st.page_link("pages/15_📊_لوحة_الادمن.py", label="📊 لوحة الادمن")

st.info("📱 للدفع: حول على الرقم 0110560222 و رسل الاشعار واتساب")
