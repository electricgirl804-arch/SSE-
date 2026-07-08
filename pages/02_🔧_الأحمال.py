import streamlit as st
import pandas as pd

st.set_page_config(page_title="محاكي المنظومة", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    html, body,.main {direction: rtl; text-align: right;}
    h1 {text-align: center!important; color: #FFD700!important;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ محاكي المنظومة SSE")
st.caption("تم التطوير بواسطة فريق SSE | IEC 60364 + NEC 430")

# === نشيك لو في أحمال ولا لا ===
if 'loads' not in st.session_state or len(st.session_state.loads) == 0:
    st.warning("⚠️ يرجى الرجوع لصفحة الأحمال وإضافة الأجهزة أولاً")
    if st.button("⬅️ الرجوع لصفحة الأحمال", use_container_width=True):
        # دا التعديل المهم: لازم الاسم يطابق اسم الملف بالضبط
        st.switch_page("pages/02_🔧_الأحمال.py")
    st.stop()

# === باقي كود المحاكي بتاعك ===
st.success("تم تحميل الأحمال بنجاح")

df = pd.DataFrame(st.session_state.loads)
st.dataframe(df, use_container_width=True)

total_kw = df['power'].sum()
st.metric("إجمالي الحمل", f"{total_kw:.2f} KW")

# هنا كملي باقي حسابات المحاكي حقتك
st.info("كملي باقي اكواد المحاكي تحت هنا")
