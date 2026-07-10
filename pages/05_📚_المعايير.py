import streamlit as st, plotly.graph_objects as go
from utils import check_login, load_css
check_login(); load_css()
st.title("📊 لوحة المعايير الفنية IEC")
st.caption("كل المعايير المحسوب عليها النظام")

c1,c2,c3,c4 = st.columns(4)
c1.metric("نسبة الفقد PR", "75%"); c2.metric("كفاءة الانفيرتر", "96%")
c3.metric("درجة الحرارة", "45°C"); c4.metric("معامل الأمان", "1.25")

st.divider()
fig = go.Figure(go.Indicator(
    mode = "gauge+number", value = 94.5,
    title = {'text': "كفاءة النظام الكلية %"},
    gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#FFD700"}}))
st.plotly_chart(fig, use_container_width=True)

st.info("الحسابات حسب: IEC 60364 + NEC 690 + IEC 61727 + IEC 61683")
if st.button("التالي: المتجر", type="primary"): st.switch_page("pages/06_🛒_السلة_والمتجر.py")
