import google.generativeai as genai
import streamlit as st
from config import COMPANY_NAME, ENGINEER_NAME
GEMINI_API_KEY = "PASTE_YOUR_GEMINI_API_KEY"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except: model = None

def ask_gemini(question):
    if not model: return "الرجاء اضافة مفتاح Gemini في ai_bot.py"
    prompt = f"انت بوت ذكاء اصطناعي لشركة {COMPANY_NAME} والمهندس {ENGINEER_NAME}. تخصصك الطاقة الشمسية في السودان. رد مختصر باللهجة السودانية: {question}"
    response = model.generate_content(prompt)
    return response.text
