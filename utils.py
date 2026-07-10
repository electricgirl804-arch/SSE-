import streamlit as st

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None
    
    if not st.session_state.logged_in:
        st.set_page_config(page_title="تسجيل الدخول", layout="centered")
        st.title("تسجيل الدخول 👤")
        
        user_type = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True)
        st.write("---")
        
        if user_type == "ادمن":
            username = st.text_input("الاسم")
            password = st.text_input("كلمة السر", type="password")
            
            if st.button("دخول", use_container_width=True):
                # بيانات الادمن
                if username == "م.شهد" and password == "shahd8499":
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.session_state.username = username
                    st.success("تم
