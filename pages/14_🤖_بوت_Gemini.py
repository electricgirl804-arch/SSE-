import streamlit as st
import google.generativeai as genai
from utils import check_login, logout, load_css

check_login(); logout(); load_css()

st.title("🤖 بوت SSE الذكي")
st.caption("اسألني عن الاحمال, البطاريات, الاسعار, اي شي في الطاقة الشمسية")

# 1. نجيب المفتاح من الخزنة السرية Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ المفتاح ما موجود. امشي Settings > Secrets وضيفي GEMINI_API_KEY")
    st.stop()

# 2. ذاكرة المحادثة عشان يتذكر كلامك
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحبا بيك في SSE ☀️ \nانا البوت الذكي. عايز تحسب احمال ولا تعرف سعر منظومة؟"}
    ]

# 3. نعرض المحادثة القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. مكان الكتابة
if prompt := st.chat_input("مثلا: داير منظومة تشغل مكيف وتلاجة..."):
    # نضيف سؤالك
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): 
        st.markdown(prompt)

    # نجاوب
    with st.chat_message("assistant"):
        with st.spinner("بفكر ليك..."):
            # بنعلمو انو خبير SSE وبرد بالسوداني
            full_prompt = f"""
            انت موظف في شركة SSE للطاقة الشمسية في السودان.
            مهمتك ترد على العملاء باللهجة السودانية وبطريقة بسيطة ومقنعة.
            لو الزول سأل عن سعر قوليهو راجع المتجر.
            السؤال: {prompt}
            """
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
    
    # نحفظ الاجابة
    st.session_state.messages.append({"role": "assistant", "content": response.text})
