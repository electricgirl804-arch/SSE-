import streamlit as st

# CSS موحد
CSS = """
<style>
   .main-header { font-size: 2.5rem; font-weight: bold; color: #FFA500; }
   .card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
"""

def init_session_state():
    keys = ['cart', 'user', 'irradiance', 'pr', 'cell_temp', 'page']
    for key in keys:
        if key not in st.session_state:
            if key == 'cart': st.session_state[key] = []
            elif key == 'pr': st.session_state[key] = 0.8
            elif key == 'cell_temp': st.session_state[key] = 45
            elif key == 'irradiance': st.session_state[key] = 1000
            else: st.session_state[key] = None

def check_session(required_keys=[]):
    init_session_state()
    # نتأكد انو كل المفاتيح المطلوبة موجودة
    for key in required_keys:
        if key not in st.session_state:
            st.session_state[key] = 0
