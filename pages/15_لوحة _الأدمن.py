import streamlit as st
import pandas as pd
from utils import check_login, logout, load_css
from database import load_from_sheet

st.set_page_config(page_title="لوحة الادمن", layout="wide", page_icon="👑")
load_css() # نشغل الاستايل
check_login(); logout()

if st.session_state.get('user_type')!= "admin":
    st.error("⛔ الصفحة دي للادمن فقط"); st.stop()

st.title("لوحة تحكم الادمن 👑")
st.markdown("### هنا بتشوفي كل طلبات العملاء الجات من حاسبة الاحمال")

data = load_from_sheet("requests")
df = pd.DataFrame(data)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("عدد الطلبات الكلي", len(df))
with col2:
    if not df.empty:
        st.metric("متوسط الاحمال", f"{df['total_watt'].astype(float).mean():.0f} واط")
with col3:
    st.metric("اخر تحديث", "الان")

st.divider()

if df.empty:
    st.warning("📭 لسه ما في اي طلبات")
else:
    st.success(f"تم جلب {len(df)} طلب بنجاح")
    
    # فلتر بالاسم
    search = st.text_input("🔍 ابحثي باسم العميل او الرقم")
    if search:
        df = df[df.apply(lambda row: search in str(row).lower(), axis=1)]
    
    st.dataframe(df, use_container_width=True, height=400)
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تحميل كل البيانات Excel",
        data=csv,
        file_name="طلبات_SSE.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()
st.caption("© SSE 2026 - لوحة تحكم سرية")
