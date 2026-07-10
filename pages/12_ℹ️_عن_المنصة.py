import streamlit as st
import qrcode
from PIL import Image
import io
from utils import check_login, load_css
from config import ADMIN_WHATSAPP, ADMIN_PHONE

check_login(); load_css()

st.set_page_config(page_title="SSE - مركز المعلومات", page_icon="logo.png", layout="wide")

# ===== CSS الموحد =====
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
h1, h2, h3 { color: #FFD700!important; font-weight: 800; }
.info-card {
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

# ===== اللوجو في الـ sidebar =====
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>", unsafe_allow_html=True)
    try:
        st.image("logo.png", width=200)
    except:
        st.warning("⚠️ ارفع logo.png في المشروع")
    st.markdown("### Smart Solar Engineering")
    st.caption("SSE v2.7")
    st.markdown("</div>", unsafe_allow_html=True)

st.title("ℹ️ مركز معلومات SSE")

tab1, tab2, tab3 = st.tabs(["📞 الدعم الفني", "ℹ️ عن المنصة", "🔧 فاحص الباركود"])

with tab1:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.subheader("مركز الدعم الفني 24/7")
    c1,c2 = st.columns(2)
    c1.markdown(f"### [📱 واتساب مباشر]({ADMIN_WHATSAPP})")
    c2.metric("رقم الطوارئ", ADMIN_PHONE)
    st.success("متوسط زمن الرد: 5 دقائق")
    st.info("للبلاغات الفورية: اتصل 0110560222")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center'>عن Smart Solar Engineering</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>منصة متخصصة في تصميم أنظمة الطاقة الشمسية</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            img = Image.open("logo.png").convert("RGBA")
            st.image(img, width=280)
        except:
            st.error("الرجاء رفع logo.png في
