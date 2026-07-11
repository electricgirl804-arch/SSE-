import streamlit as st
from database import load_from_sheet, save_to_sheet

def load_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }}

.stApp {{
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }}
.header {{ display:flex; align-items:center; gap:20px; padding:20px; background:rgba(255,255,255,0.97); border-radius:15px; margin-bottom:20px; box-shadow:0 4px 15px rgba(0,0,0,0.1); }}
.header h1 {{ color: #1e3c72; margin: 0; font-size: 24px; }}
.header h3 {{ color: #FF8C00; margin: 0; font-size: 15px; }}

   h1, h2, h3 {{ color: #0A3D62; font-weight: 700; }}
.stButton>button {{ background: #F39C12; color: white; border-radius: 12px; border: none; font-weight: bold; padding: 10px 20px; width: 100%; }}
.stButton>button:hover {{ background-color: #E67E22; color: white; }}
.stTextInput>div>div>input {{ border-radius: 10px; border: 2px solid #D6EAF8; }}
   [data-testid="stSidebar"] {{ background-color: #0A3D62; color: white; }}
.stAlert {{ border-radius: 10px; }}
   div[data-testid="stMetric"] {{ background-color: #FFFFFF; border: 1px solid #D6EAF8; padding: 15px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }}
.product-card {{ background: rgba(255,255,255,0.95); padding: 15px; border-radius: 15px; margin: 10px 0; color: #0A3D62; border: 1px solid #D6EAF8; }}
    </style>
    """, unsafe_allow_html=True)

def show_header():
    col1, col2 = st.columns([1,5])
    with col1:
        st.image("logo.png", width=75)
    with col2:
        st.markdown("<h1>SSE - Smart Solara Engineer</h1>", unsafe_allow_html=True)
        st.markdown("<h3>شركة شهد للطاقة الشمسية الذكية</h3>", unsafe_allow_html=True)

def check_login():
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("تسجيل الدخول 👤")
        show_header()
        tab1, tab2 = st.tabs(["دخول", "تسجيل جديد"])

        with tab1:
            user_type = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True)
            username = st.text_input("الاسم")
            password = st.text_input("كلمة السر", type="password")
            if st.button("دخول", use_container_width=True):
                if user_type == "ادمن" and username == "م شهد" and password == "shahd8499":
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.session_state.username = username
                    st.success(f"اهلا {username}")
                    st.rerun()
                else:
                    users = load_from_sheet("users")
                    found = False
                    for user in users:
                        if user['username'] == username and user['password'] == password and user['user_type'] == user_type:
                            st.session_state.logged_in = True
                            st.session_state.user_type = user_type
                            st.session_state.username = username
                            st.success(f"اهلا {username}")
                            st.rerun()
                            found = True
                            break
                    if not found: st.error("البيانات خطأ")

        with tab2:
            new_user = st.text_input("انشئ اسم مستخدم", key="newu")
            new_pass = st.text_input("انشئ كلمة سر", type="password", key="newp")
            if st.button("انشاء حساب"):
                if new_user and new_pass:
                    save_to_sheet({"username": new_user, "password": new_pass, "user_type": "عميل"}, "users")
                    st.success("تم انشاء الحساب. امشي تبويب دخول")
                else: st.error("املأ كل الحقول")
        st.stop()

def logout():
    with st.sidebar:
        if st.session_state.get('logged_in'):
            st.write(f"مرحبا {st.session_state.get('username')}")
        if st.button("🚪 تسجيل الخروج"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
