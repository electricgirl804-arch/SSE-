import streamlit as st
import google.generativeai as genai
from google.generativeai import protos # دي الجديدة
from utils import check_login, logout, load_css
from database import load_products
import json

check_login(); logout(); load_css()

st.title("🤖 بوت SSE الذكي")
st.caption("بجيب ليك المعلومات من النت + من المتجر. اسأل اي شي")

# 1. المفتاح
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)

    # 2. اهم شي: نفعل البحث في قوقل
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        tools=[protos.Tool(google_search=protos.GoogleSearch())] # بفتش في النت
    )
except:
    st.error("⚠️ المفتاح ما موجود. امشي Settings > Secrets")
    st.stop()

# 3. نجيب منتجاتك
products = load_products()
products_text = json.dumps(products, ensure_ascii=False, indent=2)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحبا بيك ☀️ \nانا بفتش في النت وبشوف اسعارنا. اسألني اي شي"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("مثلا: كم سعر الدولار اليوم في السودان؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("بفتش ليك في النت..."):
            full_prompt = f"""
            انت موظف SSE للطاقة الشمسية في السودان.
            دي منتجاتنا واسعارنا: {products_text}

            القوانين:
            1. رد بالسوداني.
            2. لو سأل عن منتجنا جيب السعر من القائمة الفوق.
            3. لو سأل عن سعر دولار، اخبار، او اي شي برا متجرنا: فتش في النت وجيب اخر تحديث.
            4. اذكر المصدر لو جبتو من النت.

            سؤال العميل: {prompt}
            """
            response = model.generate_content(full_prompt)
            st.markdown(response.text)

            # بنوريه جاب المعلومات من وين
            if response.candidates[0].grounding_metadata:
                st.caption("المصدر: بحث قوقل")

    st.session_state.messages.append({"role": "assistant", "content": response.text})
