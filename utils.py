import streamlit as st
from database import load_from_sheet, save_to_sheet

def load_css():
    st.markdown("""<style>.stApp { direction: rtl; text-align: right; }</style>""", unsafe_allow_html=True)

def show_logo_as_cover():
    pass

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("تسجيل الدخول 👤")
        tab1, tab2 = st.tabs(["دخول", "تسجيل جديد"])

        with tab1:
            user_type = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True)
            username = st.text_input("الاسم")
            password = st.text_input("كلمة السر", type="password")
            if st.button("دخول", use_container_width=True):

                # الادمن الثابت
                if user_type == "admin" and username == "م شهد" and password == "shahd8499":
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.session_state.username = username
                    st.success(f"اهلا {username}")
                    st.rerun()

                # العملاء من الشيت
                else:
                    users = load_from_sheet("users")
                    for user in users:
                        if user['username'] == username and user['password'] == password and user['user_type'] == user_type:
                            st.session_state.logged_in = True
                            st.session_state.user_type = user_type
                            st.session_state.username = username
                            st.success(f"اهلا {username}")
                            st.rerun()
                    st.error("البيانات خطأ")

        with tab2: # تسجيل جديد للعملاء
            new_user = st.text_input("انشئ اسم مستخدم", key="newu")
            new_pass = st.text_input("انشئ كلمة سر", type="password", key="newp")
            if st.button("انشاء حساب"):
                if new_user and new_pass:
                    data = {"username": new_user, "password": new_pass, "user_type": "client"}
                    save_to_sheet(data, "users") # بنحفظ في ورقة users
                    st.success("تم انشاء الحساب. امشي تبويب دخول")
                else:
                    st.error("املأ كل الحقول")
        st.stop()

def logout():
    if st.session_state.get('logged_in'):
        if st.sidebar.button("تسجيل الخروج"):
            for key in ['logged_in', 'user_type', 'username']:
                del st.session_state[key]
            st.rerun()
