import streamlit as st
from utils import check_login, load_css
check_login(); load_css()
st.title("📊 لوحة المعايير الفنية")
c1,c2,c3 = st.columns(3)
c1.metric("نسبة الفقد", "12%"); c2.metric("كفاءة الانفيرتر", "96%"); c3.metric("درجة الحرارة", "45°C")
st.info("دي المعايير البنحسب عليها النظام")
if st.button("التالي"): st.switch_page("pages/06_🛒_السلة_والمتجر.py")
