import streamlit as st

st.set_page_config(
    page_title="محاكي المنظومة SSE", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# العلاج: نهرب من الشريط + نجبر RTL + خط عربي
st.markdown("""
<style>
    /* 1. نهرب من شريط Streamlit بي 160px */
   .block-container {
        padding-top: 160px!important; 
        direction: rtl !important;
    }
    
    /* 2. نجبر كل شي يمين */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* 3. خط عربي نضيف */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* 4. العنوان */
    h1 {
        text-align: center!important; 
        color: #FFD700!important; 
        font-size: 34px!important;
        font-weight: 700!important;
    }
    
    /* 5. نخفي الفوتر */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.switch_page("pages/01_🏠_الرئيسية.py")
