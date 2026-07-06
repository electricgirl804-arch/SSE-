import streamlit as st
import pandas as pd

st.set_page_config(page_title="SSE - جدول التشغيل", page_icon="🕐")
st.title("🕐 جدول التشغيل الذكي")
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v1.2")

battery_kwh = st.number_input("سعة البطارية kWh", 5, 50, 15)
load_w = st.number_input("قدرة المكيف وات", 500, 3000, 1200)

hours = list(range(6, 22))
data = []
for h in hours:
    solar = max(0, 800 * np.sin((h-6)*np.pi/12)) # محاكاة انتاج شمسي
    net = solar - load_w
    data.append({"الساعة": f"{h}:00", "الطاقة الشمسية وات": solar, "الحالة": "شغل" if net > 0 else "انتظر"})

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)
st.success("أفضل وقت: 10ص - 3م وقت الذروة الشمسية")
