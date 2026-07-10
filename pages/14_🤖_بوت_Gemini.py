import streamlit as st
from utils import check_login, load_css
from ai_bot import ask_gemini
check_login(); load_css()
st.title("🤖 بوت SSE الذكي - اسأل م. شهد")
if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])
if prompt := st.chat_input("اسألني عن الطاقة الشمسية..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = ask_gemini(prompt); st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
