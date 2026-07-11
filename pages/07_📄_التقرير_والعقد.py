import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from utils import check_login, logout, load_css
from config import COMPANY_NAME, ENGINEER_NAME, WARRANTY_YEARS
import io

check_login(); logout(); load_css()

st.title("📄 التقرير الهندسي والعقد الرسمي")
st.caption("PDF معتمد ومختوم")

# نسجل خط عربي - نزلي ملف Cairo-Regular.ttf وختيه مع المشروع
try:
    pdfmetrics.registerFont(TTFont('Cairo', 'Cairo-Regular.ttf'))
except:
    st.warning("نزلي خط Cairo-Regular.ttf عشان العربي يظهر في PDF")

def create_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # العنوان
    c.setFont("Cairo", 18)
    c.drawCentredString(width/2, height-50, f"{COMPANY_NAME}")
    c.setFont("Cairo", 12)
    c.drawCentredString(width/2, height-75, "التقرير الهندسي والعرض الفني لنظام الطاقة الشمسية")

    # بيانات
    y = height - 120
    c.drawRightString(width-50, y, f"المهندس المسؤول: {ENGINEER_NAME}")
    c.drawRightString(width-50, y-20, f"اسم العميل: {st.session_state.get('username', '---')}")
    c.drawRightString(width-50, y-40, f"تاريخ التقرير: {pd.Timestamp.now().strftime('%Y-%m-%d')}")

    # جدول المواصفات
    data = [
        ['المواصفة', 'القيمة'],
        ['قدرة النظام', f"{st.session_state.get('array_kw',0):.2f} kW"],
        ['عدد الألواح', f"{st.session_state.get('num_panels',0)} لوح"],
        ['قدرة الانفيرتر', f"{st.session_state.get('inverter_kw',0)} kVA"],
        ['سعة البطاريات', f"{st.session_state.get('battery_ah',0)}Ah {st.session_state.get('battery_volt',48)}V"],
        ['الاستهلاك اليومي', f"{st.session_state.get('total_kwh',0):.2f} kWh"],
        ['الضمان', f"{WARRANTY_YEARS} سنوات شامل"]
    ]
    table = Table(data, colWidths=[250, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A3D62')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,-1), 'Cairo'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, y-250)

    # الشروط
    c.setFont("Cairo", 10)
    c.drawRightString(width-50, 150, "1. الضمان شامل الالواح والانفيرتر والبطاريات")
    c.drawRightString(width-50, 130, "2. التركيب حسب مواصفات IEC 60364 + NEC 690")
    c.drawRightString(width-50, 110, "3. العرض ساري لمدة 30 يوم")

    # التوقيع
    c.drawRightString(width-50, 70, "التوقيع والختم: ___________________")

    c.save()
    buffer.seek(0)
    return buffer

if st.button("📥 انشاء التقرير PDF", use_container_width=True, type="primary"):
    pdf = create_pdf()
    st.download_button(
        label="📥 نزل التقرير المعتمد",
        data=pdf,
        file_name=f"SSE_Report_{st.session_state.get('username')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.success("تم انشاء التقرير بنجاح")
