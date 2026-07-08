import streamlit as st

# CSS موحد
CSS = """
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #FFA500; }
    .card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
"""

def init_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

def check_session():
    init_session_state()
    if 'user' not in st.session_state:
        st.session_state.user = None
