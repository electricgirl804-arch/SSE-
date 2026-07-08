import streamlit as st

st.set_page_config(
    page_title="الأعطال 06",
    page_icon="⚡",
    layout="wide"
)

# === CSS خارق يمسح اي تداخل ===
st.markdown("""
<style>
    /* اهم شي: نجبر الكل يمين */
    * {
        direction: rtl !important;
        text-align: right !important;
    }

    /* نمسح الهيدر كلو ونبني واحد جديد */
    header[data-testid="stHeader"] {
        display: none !important;
    }
   .block-container {
        padding-top: 1rem!important;
    }

    /* العنوان */
    h1 {
        text-align: center!important;
        color: #FFD700!important;
        font-size: 30px!important;
    }
</style>
""", unsafe_allow_html=True)

st.switch_page("pages/01_🏠_الرئيسية.py")
