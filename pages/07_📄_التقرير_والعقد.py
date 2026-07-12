import streamlit as st
import pandas as pd
from fpdf import FPDF
from utils import check_login, logout, load_css
import io
import requests
import os

check_login()
logout()
load_css()

st.title("📄 التقرير الهندسي والعرض الفني")
st.caption("تقرير معتمد بصيغة PDF")

# ====== بيانات الشركة ======
COMPANY_NAME = "SSE Smart Solar Energy"
WARRANTY_YEARS = 5
EMAIL = "electricgirl804@gmail.com"
PHONE = "0110560222"
LOGO_PATH = "logo.png"

@st.cache_data # عشان الخط ما ينزل كل مرة
def get_font():
    font_path = "Cairo.ttf"
    if not os.path.exists(font_path):
        font_url = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Regular.ttf"
        r = requests.get(font_url)
        with open(font_path, "wb") as f: f.write(r.content)
    return font_path

class PDF(FPDF):
    def __init__(self, font_path):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.font_path = font_path
        self.add_font("Cairo", "", self.font_path, uni=True)
        self.add_font("Cairo", "B", self.font_path, uni=True)

    def header(self):
        # اللوغو
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, 10, 8, 35)

        self.set_font("Cairo", "B", 16)
        self.set_text_color(100, 255, 218)
        self.cell(0, 8, COMPANY_NAME, 0, 1, "R")

        self.set_font("Cairo", "", 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, f"البريد: {EMAIL}", 0, 1, "R")
        self.cell(0, 6, f"الهاتف: {PHONE}", 0, 1, "R")
        self.ln(3)
        self.set_draw_color(100, 255, 218)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Cairo", "", 8)
        self.set_text_color(100, 255, 218)
        self.cell(0, 10, f"صفحة {self.page_no()} | {COMPANY_NAME}", 0, 0, "C")

def create_pdf(font_path):
    pdf = PDF(font_path)
    pdf.add_page()

    # عنوان
    pdf.set_font("Cairo", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "التقرير الهندسي والعرض الفني لنظام الطاقة الشمسية", 0, 1, "C")
    pdf.ln(5)

    # بيانات
    pdf.set_font("Cairo", "", 11)
    pdf.cell(0, 8, f"التاريخ: {pd.Timestamp.now().strftime('%Y-%m-%d')}", 0, 1, "R")
    pdf.cell(0, 8, f"اسم العميل: {st.session_state.get('user', 'عميل كريم')}", 0, 1, "R")
    pdf.ln(5)

    # جدول
    pdf.set_fill_color(100, 255, 218)
    pdf.set_text_color(10, 25, 47)
    pdf.cell(90, 10, "المواصفة", 1, 0, "C", 1)
    pdf.cell(90, 10, "القيمة", 1, 1, "C", 1)

    pdf.set_fill_color(17, 34, 64)
    pdf.set_text_color(255, 255, 255)

    data = [
        ["القدرة الاجمالية للنظام", f"{st.session_state.get('array_kw',0):.2f} KW"],
        ["عدد الالواح الشمسية", f"{st.session_state.get('num_panels',0)} لوح 550W"],
        ["قدرة الانفرتر", f"{st.session_state.get('inverter_kw',0)} KVA"],
        ["سعة بنك البطاريات", f"{st.session_state.get('battery_ah',0)} Ah - 48V"],
        ["متوسط الاستهلاك اليومي", f"{st.session_state.get('total_kwh',0):.2f} KWh"],
        ["مدة الضمان", f"{WARRANTY_YEARS} سنوات"]
    ]
    for row in data:
        pdf.cell(90, 10, row[0], 1, 0, "C", 1)
        pdf.cell(90, 10, row[1], 1, 1, "C", 1)

    pdf.ln(10)
    # الشروط
    pdf.set_font("Cairo", "B", 12)
    pdf.cell(0, 8, "الشروط والاحكام", 0, 1, "R")
    pdf.set_font("Cairo", "", 10)
    pdf.cell(0, 7, "1. الضمان شامل الالواح والانفرتر والبطاريات", 0, 1, "R")
    pdf.cell(0, 7, "2. التركيب وفقا لمواصفات IEC 60364 و NEC 690", 0, 1, "R")
    pdf.cell(0, 7, "3. العرض ساري لمدة 30 يوم من تاريخه", 0, 1, "R")
    pdf.ln(15)
    pdf.cell(0, 10, "التوقيع والختم: ___________________", 0, 1, "R")

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# ====== الواجهة ======
font_path = get_font()

if st.button("📥 انشاء التقرير PDF", use_container_width=True, type="primary"):
    if not os.path.exists(LOGO_PATH):
        st.warning("⚠️ لم يتم العثور على logo.png. سيتم انشاء التقرير بدون شعار")

    with st.spinner("جاري انشاء التقرير..."):
        pdf = create_pdf(font_path)
        st.download_button(
            label="📥 تحميل التقرير المعتمد",
            data=pdf,
            file_name=f"SSE_Report_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    st.success("تم انشاء التقرير بنجاح ✅")
