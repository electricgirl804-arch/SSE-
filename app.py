import streamlit as st

st.set_page_config(page_title="SSE", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a192f 0%, #112240 100%); }
h1 { color: #64ffda!important; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("☀️ شركة SSE للطاقة الشمسية")
st.markdown("### مرحباً بك في منصة الحسابات")

st.divider()

# المستخدم يختار طريقة الدخول
login_type = st.radio(
    "اختر طريقة تسجيل الدخول:",
    ["🔑 الدخول بالايميل", "🔢 الدخول بالرقم", "🏢 دخول الشركة"],
    horizontal=True
)

if login_type == "🔑 الدخول بالايميل":
    st.switch_page("pages/01_🔐_تسجيل_الدخول.py")

elif login_type == "🔢 الدخول بالرقم":
    st.switch_page("pages/02_🔢_الدخول_بالرقم.py") # غيري الاسم حسب ملفك

elif login_type == "🏢 دخول الشركة":
    st.switch_page("pages/03_🏢_دخول_الشركة.py") # اعملي صفحة للشركة

st.caption("💡 اختاري الطريقة المناسبة واضغطي")
