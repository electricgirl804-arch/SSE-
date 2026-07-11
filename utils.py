import streamlit as st
import sqlite3
import hashlib

DB_NAME = "users.db"

# دالة تشفير كلمة السر
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# انشاء قاعدة البيانات والجداول
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, user_type TEXT)''')
    # نضيف الادمن تلقائي لو ما موجود
    c.execute("INSERT OR IGNORE INTO users (username, password, user_type) VALUES (?, ?, ?)",
              ("م.شهد", hash_password("shahd8499"), "admin"))
    conn.commit()
    conn.close()

init_db() # شغليها اول ما الملف يفتح

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None
    
    if not st.session_state.logged_in:
        st.set_page_config(page_title="تسجيل الدخول", layout="centered")
        st.title("تسجيل الدخول 👤")
        
        tab1, tab2 = st.tabs(["دخول", "تسجيل جديد"])
        
        with tab1: # تسجيل دخول
            user_type = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True, key="login_type")
            username = st.text_input("رقم الهاتف او الايميل", key="login_user")
            password = st.text_input("كلمة السر", type="password", key="login_pass")
            
            if st.button("دخول", use_container_width=True):
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=? AND password=? AND user_type=?",
                          (username, hash_password(password), user_type))
                user = c.fetchone()
                conn.close()
                
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_type = user_type
                    st.session_state.username = username
                    st.success("تم تسجيل الدخول")
                    st.rerun()
                else:
                    st.error("البيانات خطأ")
        
        with tab2: # تسجيل جديد للعملاء فقط
            new_user = st.text_input("رقم الهاتف او الايميل الجديد")
            new_pass = st.text_input("انشئ كلمة سر", type="password")
            if st.button("انشاء حساب"):
                if new_user and new_pass:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    try:
                        c.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                                  (new_user, hash_password(new_pass), "client"))
                        conn.commit()
                        st.success("تم انشاء الحساب. امشي تبويب دخول")
                    except:
                        st.error("الرقم او الايميل دا مستخدم قبل كدا")
                    conn.close()
                else:
                    st.error("املأ كل الحقول")
        st.stop()

def logout():
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None
        st.rerun()

# الدوال القديمة عشان ما يضرب ايرور
def load_css():
    st.markdown("""<style>.stButton>button {width: 100%;}</style>""", unsafe_allow_html=True)

def show_logo_as_cover():
    st.image("https://via.placeholder.com/800x200.png?text=Your+Logo", use_container_width=True)
