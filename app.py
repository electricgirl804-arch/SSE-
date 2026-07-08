import streamlit as st
import sqlite3
import requests
import streamlit.components.v1 as components
import math
import io
import qrcode
import smtplib
import pdfkit
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="الأعطال 06", page_icon="⚡", layout="wide")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
EMAIL = st.secrets["EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
MY_WHATSAPP = "249110560222"
ADMIN_PASSWORD = "shahd8499"

conn = sqlite3.connect('alatal06.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, code TEXT, customer_name TEXT, phone TEXT, email TEXT, size REAL, cost REAL, monthly REAL, status TEXT, date TEXT)''')
conn.commit()

def check_login():
    if 'role' not in st.session_state:
        st.session_state.role = None
    if st.session_state.role == None:
        st.title("⚡ دخول الأعطال 06")
        user_type = st.radio("نوع الدخول", ["ادمن", "مهندس"])
        password = st.text_input("كلمة السر", type="password")
        if st.button("دخول"):
            if user_type == "ادمن" and password == ADMIN_PASSWORD:
                st.session_state.role = "ادمن"
                st.rerun()
            elif user_type == "مهندس":
                st.session_state.role = "مهندس"
                st.rerun()
            else:
                st.error("كلمة السر غلط")
        st.stop()

check_login()

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="انت الأعطال 06 بوت ذكاء اصطناعي متخصص في الطاقة الشمسية. رد بالعربي السوداني البسيط.")

def translate_text(text):
    trans_model = genai.GenerativeModel('gemini-1.5-flash')
    result = trans_model.generate_content(f"Translate this to English: {text}")
    return result.text

def generate_pdf(data):
    html = f"<h1 style='text-align:center'>تقرير الأعطال 06</h1><hr><p>رقم المشروع: {data['code']}</p><p>العميل: {data['name']}</p><p>حجم المنظومة: {data['size']} KW</p><p>القسط الشهري: {data['monthly']} $</p>"
    path = f"{data['code']}.pdf"
    pdfkit.from_string(html, path)
    return path

def send_pdf_email(to_email, pdf_path, project_code, customer_name):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"تقرير مشروع رقم {project_code} - الأعطال 06"
        body = f"مرحبا\nتم تاكيد مشروع جديد\nرقم المشروع: {project_code}\nاسم العميل: {customer_name}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        with open(pdf_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header('Content-Disposition', 'attachment', filename=f"ALATAL06_{project_code}.pdf")
            msg.attach(attach)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except:
        pass

def send_whatsapp_notification(customer_name, project_code, phone):
    API_KEY = st.secrets["CALLMEBOT_KEY"]
    message = f"⚡ *الأعطال 06 - طلب جديد* ⚡%0Aاسم الزبون: {customer_name}%0Aرقم المشروع: {project_code}%0Aالحالة: في انتظار تاكيد الادمن"
    url = f"https://api.callmebot.com/whatsapp.php?phone={MY_WHATSAPP}&text={message}&apikey={API_KEY}"
    requests.get(url)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ الأعطال 06")
st.caption("منصة ذكاء الطاقة الشمسية - ايجار 3 سنوات")
st.sidebar.success(f"مسجل دخول كـ: {st.session_state.role}")
if st.sidebar.button("تسجيل خروج"):
    st.session_state.role = None
    st.rerun()

if st.session_state.role == "ادمن":
    st.header("لوحة تحكم الادمن")
    pending = c.execute("SELECT * FROM projects WHERE status='pending'").fetchall()
    st.subheader(f"طلبات معلقة: {len(pending)}")
    if len(pending) == 0:
        st.info("مافي طلبات جديدة")
    for p in pending:
        with st.container(border=True):
            st.write(f"**رقم:** {p[1]} | **الاسم:** {p[2]} | **التلفون:** {p[3]}")
            st.write(f"**الحجم:** {p[5]} KW | **التكلفة:** {p[6]}$ | **القسط:** {p[7]:.2f}$")
            col1, col2 = st.columns(2)
            if col1.button("✅ تاكيد", key=f"ok{p[0]}"):
                c.execute("UPDATE projects SET status='active' WHERE id=?", (p[0],))
                conn.commit()
                pdf = generate_pdf({'code':p[1],'name':p[2],'size':p[5],'monthly':p[7]})
                send_pdf_email(EMAIL, pdf, p[1], p[2])
                st.success("تم التاكيد واترسل الايميل")
                st.rerun()
            if col2.button("❌ رفض", key=f"no{p[0]}"):
                c.execute("DELETE FROM projects WHERE id=?", (p[0],))
                conn.commit()
                st.warning("تم الرفض")
                st.rerun()

elif st.session_state.role == "مهندس":
    tab1, tab2 = st.tabs(["بوت الذكاء", "حساب + تسجيل مشروع"])

    with tab1:
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and st.button("🌐 ترجم للانجليزي", key=message["id"]):
                    st.info(f"**English:** {translate_text(message['content'])}")
        if prompt := st.chat_input("اسأل الأعطال 06"):
            st.session_state.messages.append({"role": "user", "content": prompt, "id": len(st.session_state.messages)})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                response = model.generate_content(prompt).text
                st.markdown(response)
                if st.button("🌐 ترجم للانجليزي", key=len(st.session_state.messages)):
                    st.info(f"**English:** {translate_text(response)}")
            st.session_state.messages.append({"role": "assistant", "content": response, "id": len(st.session_state.messages)})

    with tab2:
        st.subheader("حساب المنظومة")
        col1, col2, col3 = st.columns(3)
        with col1: load_kw = st.number_input("إجمالي الحمل kW", value=2.0, step=0.1)
        with col2: hours = st.number_input("ساعات التشغيل", value=8, step=1)
        with col3: days_autonomy = st.number_input("أيام الاستقلالية", value=1.5, step=0.5)

        lat = 15.5007
        lon = 32.5599
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20221231&end=20221231&latitude={lat}&longitude={lon}&parameters=ALLSKY_SFC_SW_DWN&community=RE&format=JSON"
        r = requests.get(url, timeout=15)
        ghi_h = r.json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["20221231"]
        tilt_opt = abs(lat) * 0.9
        final_factor = 1 + 0.008 * abs(tilt_opt)
        ghi_final = ghi_h * final_factor

        energy_kwh = load_kw * hours
        panel_w = 550
        system_eff = 0.85
        num_panels = math.ceil(energy_kwh / (ghi_final * panel_w/1000 * system_eff))
        array_kw = num_panels * panel_w / 1000
        cost = array_kw * 1000
        months = 36
        monthly = ((cost * 1.2) / months)

        st.metric("☀️ عدد الألواح 550W", num_panels, f"{array_kw:.1f} kW")
        st.metric("💰 التكلفة التقديرية", f"${cost:.0f}")
        st.metric("📅 القسط الشهري 3 سنوات", f"${monthly:.2f}")

        st.subheader("تسجيل الطلب")
        with st.form("project"):
            name = st.text_input("اسم الزبون")
            phone = st.text_input("تلفون الزبون")
            email = st.text_input("ايميل الزبون")
            if st.form_submit_button("ارسال الطلب للادمن"):
                code = f"ALAT2026{c.execute('SELECT COUNT(*) FROM projects').fetchone()[0]+1}"
                c.execute("INSERT INTO projects VALUES (NULL,?,?,?,?,?)",(code,name,phone,email,array_kw,cost,monthly,"pending",str(st.date.today())))
                conn.commit()
                send_whatsapp_notification(name, code, phone)
                st.success(f"✅ تم ارسال الطلب {code} للادمن")
