import streamlit as st
from reportlab.pdfgen import canvas
from utils import check_login, load_css
from config import COMPANY_NAME, ENGINEER_NAME, WARRANTY_YEARS
check_login(); load_css()
st.title("📄 التقرير الهندسي والعقد الرسمي")
st.caption("PDF معتمد ومختوم")

if st.button("📥 انشاء التقرير PDF", use_container_width=True, type="primary"):
    c = canvas.Canvas("SSE_Report.pdf")
    c.setFont("Helvetica-Bold", 20); c.drawString(100, 800, f"{COMPANY_NAME}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"المهندس المسؤول: {ENGINEER_NAME}")
    c.drawString(100, 750, f"حجم النظام: {st.session_state.get('array_kw',0):.2f} kW")
    c.drawString(100, 730, f"عدد الالواح: {st.session_state.get('num_panels',0)}")
    c.drawString(100, 710, f"البطاريات: {st.session_state.get('battery_ah',0)}Ah")
    c.drawString(100, 690, f"الضمان: {WARRANTY_YEARS} سنوات شامل")
    c.drawString(100, 650, "التوقيع: ___________________")
    c.save()
    with open("SSE_Report.pdf", "rb") as f: st.download_button("نزل التقرير المعتمد", f, file_name="SSE_Report.pdf")
