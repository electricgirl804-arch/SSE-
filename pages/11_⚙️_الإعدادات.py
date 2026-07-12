import streamlit as st
from utils import check_login, logout, load_css

check_login(); logout(); load_css()
st.title("⚙️ الإعدادات العامة")
st.caption("تحكم في بيانات الشركة واعدادات التصميم الافتراضية")

st.markdown("""
<style>
.info-card { background: #112240; padding: 20px; border-radius: 15px;
             border-left: 5px solid #64ffda; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='info-card'>", unsafe_allow_html=True)
st.subheader("بيانات الشركة")
col1, col2 = st.columns(2)
with col1:
    COMPANY_NAME = st.text_input("اسم الشركة", st.session_state.get('company_name', "SSE Smart Solar Energy"))
    EMAIL = st.text_input("البريد الالكتروني", st.session_state.get('email', "electricgirl804@gmail.com"))
with col2:
    PHONE = st.text_input("رقم الهاتف", st.session_state.get('phone', "0110560222"))
    WARRANTY = st.number_input("سنوات الضمان", value=st.session_state.get('warranty', 5), min_value=1, max_value=25)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='info-card'>", unsafe_allow_html=True)
st.subheader("اعدادات التصميم الهندسي")
col1, col2 = st.columns(2)
with col1:
    IRRADIANCE = st.slider("متوسط ساعات الذروة اليومية GHI", 4.0, 7.0, st.session_state.get('irradiance', 5.5), 0.1)
    st.caption("السودان المتوسط: 5.5 - 6.5")
with col2:
    SYSTEM_EFF = st.slider("كفاءة النظام الكلية %", 70, 85, int(st.session_state.get('eff', 77)))
    st.caption("تشمل الفقد في الاسلاك والانفرتر والبطاريات")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("💾 حفظ الاعدادات", type="primary", use_container_width=True):
    st.session_state.company_name = COMPANY_NAME
    st.session_state.email = EMAIL
    st.session_state.phone = PHONE
    st.session_state.warranty = WARRANTY
    st.session_state.irradiance = IRRADIANCE
    st.session_state.eff = SYSTEM_EFF
    st.success("✅ تم حفظ الاعدادات بنجاح")
    st.rerun() # عشان تتطبق طوالي
