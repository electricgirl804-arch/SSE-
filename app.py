import streamlit as st
import sqlite3

st.set_page_config(page_title="الأعطال 06", page_icon="⚡", layout="wide")

# === تنسيق RTL للعربي ===
st.markdown("""
<style>
    html, body,.main {
        direction: rtl;
        text-align: right;
    }
    h1 {
        text-align: center!important;
        color: #FFD700!important;
        font-size: 32px!important;
    }
   .stButton>button {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        font-weight: 700;
        border: none;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# === كلمة سر الادمن ===
ADMIN_SECRET = "shahd8499"

# === قاعدة البيانات ===
conn = sqlite3.connect('shahd_alatal06.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, code TEXT, name TEXT, phone TEXT, items TEXT, total REAL, status TEXT, date TEXT)''')
conn.commit()

# === نظام الدخول ===
if 'role' not in st.session_state:
    st.session_state.role = None

if st.session_state.role == None:
    st.markdown("<h1>⚡ الأعطال 06 | المهندسة شهد</h1>", unsafe_allow_html=True)
    st.write("---")

    role = st.radio("اختار نوع الدخول", ["مهندس", "ادمن"], horizontal=True)

    if role == "ادمن":
        password = st.text_input("دخل كلمة سر الادمن", type="password")
        if st.button("دخول", use_container_width=True):
            if password == ADMIN_SECRET:
                st.session_state.role = "ادمن"; st.rerun()
            else:
                st.error("❌ كلمة السر غلط")

    if role == "مهندس":
        if st.button("دخول كمهندس", use_container_width=True):
            st.session_state.role = "مهندس"; st.rerun()
    st.stop()

# === الشريط الجانبي ===
st.sidebar.success(f"مرحبا: {st.session_state.role}")
if st.sidebar.button("تسجيل خروج"):
    st.session_state.role = None; st.rerun()

# === لوحة الادمن ===
if st.session_state.role == "ادمن":
    st.header("👑 لوحة تحكم الادمن")
    orders = c.execute("SELECT * FROM orders WHERE status='pending'").fetchall()
    st.info(f"عندك {len(orders)} طلب معلق")

    if len(orders) == 0:
        st.write("مافي طلبات جديدة حاليا")

    for o in orders:
        with st.container(border=True):
            st.write(f"**رقم الطلب:** {o[1]}")
            st.write(f"**الاسم:** {o[2]} | **التلفون:** {o[3]}")
            st.write(f"**المنتجات:** {o[4]}")
            st.write(f"**الاجمالي:** ${o[5]}")
            col1, col2 = st.columns(2)
            if col1.button("✅ تاكيد الطلب", key=f"ok{o[0]}", use_container_width=True):
                c.execute("UPDATE orders SET status='active' WHERE id=?", (o[0],)); conn.commit(); st.success("تم التاكيد"); st.rerun()
            if col2.button("❌ رفض الطلب", key=f"no{o[0]}", use_container_width=True):
                c.execute("DELETE FROM orders WHERE id=?", (o[0],)); conn.commit(); st.warning("تم الرفض"); st.rerun()

# === صفحة المهندس الرئيسية ===
else:
    st.markdown("<h1>⚡ الأعطال 06 | المهندسة شهد</h1>", unsafe_allow_html=True)
    st.success("تم تسجيل الدخول بنجاح")
    st.write("اختاري الصفحة الدايراها من الشريط الجانبي ←")

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("البوت الذكي", "شغال")
    with col2: st.metric("حاسبة الطاقة", "شغالة")
    with col3: st.metric("المتجر", "شغال")

    st.info("جديد: تمت اضافة البوت الذكي والمتجر وحاسبة الطاقة. بتلقيهم في الشريط الجانبي")
