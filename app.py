import streamlit as st

st.set_page_config(page_title="SSE", layout="wide")

# CSS بسيط
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a192f 0%, #112240 100%); }
h1 { color: #64ffda!important; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("☀️ شركة SSE للطاقة الشمسية")
st.markdown("### مرحباً بك في منصة الحسابات")
st.caption("اختر طريقة الدخول")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔑 تسجيل الدخول", use_container_width=True):
        st.switch_page("pages/01_🔐_تسجيل_الدخول.py")

with col2:
    if st.button("🔢 الدخول بالرقم", use_container_width=True):
        st.switch_page("pages/02_🔢_الدخول_بالرقم.py") # غيري الاسم حسب اسم ملفك

with col3:
    if st.button("🏠 الرئيسية مباشر", use_container_width=True):
        st.switch_page("pages/00_🏠_الرئيسية.py")

st.divider()
st.info("💡 لو واجهتك مشكلة سجل دخول اول عشان باقي الصفحات تفتح معاك")
