import streamlit as st
import sqlite3
import hashlib

DB_NAME = "users.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, user_type TEXT)''')
    
    admin_pass = hash_password("shahd8499")
    c.execute("UPDATE users SET password=?, user_type=? WHERE username=?", (admin_pass, "admin", "م شهد"))
    if c.rowcount == 0:
        c.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                  ("م شهد", admin_pass, "admin"))
    
    conn.commit()
    conn.close()

init_db()

# ضفنا ديل عشان app.py ما يضرب
def load_css():
    st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

def show_logo_as_cover():
    pass # خليها فاضية هسي

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None
    
    if not st.session_state.logged_in:
        st.set_page_config(page_title="تسجيل الدخول", layout="centered")
        st.title("تسجيل الدخول 👤")
        
        tab1, tab2 = st.tabs(["دخول", "تسجيل جديد"])
        
        with tab1:
            user_type = st.radio("سجل كـ", ["عميل", "ادمن"], horizontal=True, key="login_type")
            username = st.text_input("الاسم / رقم الهاتف / الايميل", key="login_user")
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
                    st.success(f"اهلا {username}")
                    st.rerun()
                else:
                    st.error("البيانات خطأ")
        
        with tab2:
            new_user = st.text_input("انشئ اسم مستخدم")
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
                        st.error("الاسم دا مستخدم قبل كدا")
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
