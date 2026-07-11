import streamlit as st
from database import load_from_sheet, save_to_sheet

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

   .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(180deg, #F0F8FF 0%, #FFFFFF 100%);
    }

    h1, h2, h3 {
        color: #0A3D62;
        font-weight: 700;
    }

   .stButton>button {
        background-color: #F39C12;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        padding: 10px 20px;
        width: 100%;
    }
   .stButton>button:hover {
        background-color: #E67E22;
        color: white;
    }

   .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #D6EAF8;
    }

    [data-testid="stSidebar"] {
        background-color: #0A3D62;
        color: white;
    }

   .stAlert {
        border-radius: 10px;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D6EAF8;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

def show_logo_as_cover():
    st.image("https://via.placeholder.com/1200x300/0A3D62/FFFFFF?text=SSE+الطاقة+الشمسية+الذكية", use_column_width=True)

def check_login():
    load_css() # شغلنا الاستايل هنا
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if not st.session_state.logged_in:
        st.title("تسجيل الدخول 👤")
        tab1, tab2 = st.tabs(["دخول", "تسجيل جديد"])
        with tab1:
            user_type = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True)
            username = st.text_input("الاسم")
            password = st.text_input("كلمة السر", type="password")
            if st.button("دخول", use_container_width=True):
                if user_type == "admin" and username == "م شهد" and password == "shahd8499":
                    st.session_state.logged_in = True; st.session_state.user_type = "admin"; st.session_state.username = username; st.success(f"اهلا {username}"); st.rerun()
                else:
                    users = load_from_sheet("users")
                    for user in users:
                        if user['username'] == username and user['password'] == password and user['user_type'] == user_type:
                            st.session_state.logged_in = True; st.session_state.user_type = user_type; st.session_state.username = username; st.success(f"اهلا {username}"); st.rerun()
                    st.error("البيانات خطأ")
        with tab2:
            new_user = st.text_input("انشئ اسم مستخدم", key="newu"); new_pass = st.text_input("انشئ كلمة سر", type="password", key="newp")
            if st.button("انشاء حساب"):
                if new_user and new_pass:
                    save_to_sheet({"username": new_user, "password": new_pass, "user_type": "client"}, "users")
                    st.success("تم انشاء الحساب. امشي تبويب دخول")
                else: st.error("املأ كل الحقول")
        st.stop()

def logout():
    if st.session_state.get('logged_in'):
        if st.sidebar.button("تسجيل الخروج"):
            for key in ['logged_in', 'user_type', 'username']: del st.session_state[key]
            st.rerun()
