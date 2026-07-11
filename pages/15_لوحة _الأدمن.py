import streamlit as st
import pandas as pd
from utils import check_login, logout
from database import load_from_sheet

st.set_page_config(page_title="لوحة الادمن", layout="wide")

check_login()
logout()

# حماية: بس الادمن يقدر يشوف الصفحة دي
if st.session_state.get('user_type') != "admin":
    st.error("⛔ الصفحة دي للادمن فقط")
    st.stop()

st.title("لوحة تحكم الادمن 👑")
st.markdown("هنا بتشوفي كل طلبات العملاء الجات من حاسبة الاحمال")

# نسحب البيانات من قوقل شيت ورقة requests
try:
    data = load_from_sheet("requests")
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"خطأ في جلب البيانات من الشيت: {e}")
    st.stop()

if df.empty:
    st.warning("لسه ما في اي طلبات")
else:
    st.success(f"عدد الطلبات الكلي: {len(df)}")
    
    # عرض الجدول
    st.dataframe(df, use_container_width=True)
    
    # زر تحميل البيانات
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تحميل البيانات Excel",
        data=csv,
        file_name="طلبات_SSE.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()
st.caption("© SSE 2026")
