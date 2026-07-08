import streamlit as st
import qrcode
from PIL import Image
import io
import base64

st.set_page_config(page_title="SSE - عن المنصة", page_icon="logo.png", layout="wide")

# ===== 1. الخلفية الزرقاء برا =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}
h1, h2, h3 { color: #FFD700!important; font-weight: 800; }
.about-card {
    background: rgba(255,255,255,0.98);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    border-right: 5px solid #FFD700;
    margin: 20px 0;
}
.sidebar-logo { text-align: center; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ===== 2. اللوجو في الـ sidebar برا =====
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>", unsafe_allow_html=True)
    try:
        st.image("logo.png", width=200)
    except:
        st.error("الرجاء رفع logo.png في المشروع")
    st.markdown("### Smart Solar Engineering")
    st.caption("SSE v2.7")
    st.markdown("</div>", unsafe_allow_html=True)

# ===== 3. المحتوى جوا الكرت الابيض =====
st.markdown("<h1 style='text-align:center'>ℹ️ عن Smart Solar Engineering</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white'>منصة متخصصة في تصميم أنظمة الطاقة الشمسية</p>", unsafe_allow_html=True)

st.markdown("<div class='about-card'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        img = Image.open("logo.png").convert("RGBA")
        st.image(img, width=280)
    except:
        st.error("الرجاء رفع logo.png في فولدر المشروع")

st.markdown("---")
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("من نحن")
    st.markdown("**Smart Solar Engineering** منصة سودانية تهدف لتبسيط تصميم أنظمة الطاقة الشمسية للجميع")
    st.success("**الإيميل:** electricgirl804@gmail.com")
    st.success("**الواتساب:** 0110560222")
    st.info("**المطور:** المهندسة شهد")
    st.caption("**الإصدار:** v2.7 - أبريل 2026")

with col2:
    st.subheader("📱 تواصل معنا عبر واتساب")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data("https://wa.me/249110560222")
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="#FF8C00", back_color="white")
    buf = io.BytesIO()
    img_qr.save(buf, format='PNG')
    st.image(buf.getvalue(), width=200)
    st.caption("امسح الكود للتواصل المباشر")

st.markdown("</div>", unsafe_allow_html=True)  # قفل الكرت الابيض

st.page_link("app.py", label="العودة للرئيسية", icon="🏠")
