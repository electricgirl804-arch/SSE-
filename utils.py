import streamlit as st
import sqlite3
import hashlib

DB_NAME = "users.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, user_type TEXT)''')
    admin_pass = hash_password("shahd8499")
    c.execute("INSERT OR REPLACE INTO users (username, password, user_type) VALUES (?,?,?)", ("م شهد", admin_pass, "admin"))
    conn.commit()
    conn.close()
init_db()

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
            username = st.text_input("الاسم / رقم الهاتف / الايميل")
            password = st.text_input("كلمة السر", type="password")
            if st.button("دخول", use_container_width=True):
                conn = sqlite3.connect(DB_NAME); c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=? AND password=? AND user_type=?", (username, hash_password(password), user_type))
                user = c.fetchone(); conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_type = user_type
                    st.session_state.username = username
                    st.success(f"اهلا {username}")
                    st.rerun()
                else:
                    st.error("البيانات خطأ")

        with tab2:
            new_user = st.text_input("انشئ اسم مستخدم", key="newu")
            new_pass = st.text_input("انشئ كلمة سر", type="password", key="newp")
            if st.button("انشاء حساب"):
                if new_user and new_pass:
                    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
                    try:
                        c.execute("INSERT INTO users (username, password, user_type) VALUES (?,?,?)", (new_user, hash_password(new_pass), "client"))
                        conn.commit()
                        st.success("تم انشاء الحساب. امشي تبويب دخول")
                    except:
                        st.error("الاسم دا مستخدم قبل كدا")
                    conn.close()
                else:
                    st.error("املأ كل الحقول")
        st.stop()

def logout():
    if st.session_state.get('logged_in'):
        if st.sidebar.button("تسجيل الخروج"):
            for key in ['logged_in', 'user_type', 'username']:
                del st.session_state[key]
            st.rerun()
