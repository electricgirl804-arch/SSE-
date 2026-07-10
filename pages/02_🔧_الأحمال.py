import streamlit as st, pandas as pd
from utils import check_login, load_css
from database import save_to_sheet
check_login(); load_css()
st.title("🔌 حاسبة الاحمال الذكية")
name = st.text_input("اسم العميل"); phone = st.text_input("رقم الواتساب")
if 'loads' not in st.session_state: st.session_state.loads = []
device = st.selectbox("اختار الجهاز", ["مكيف 1 حصان","ثلاجة 12 قدم","شاشة 43","مروحة سقف","لمبة LED"])
power = st.number_input("قدرة الجهاز بالواط", 100, 5000, 200); hours = st.number_input("عدد ساعات التشغيل", 1.0, 24.0, 5.0)
if st.button("➕ اضافة للجدول"): st.session_state.loads.append({"الجهاز":device, "الواط":power, "الساعات":hours, "الاستهلاك_Wh":power*hours})
df = pd.DataFrame(st.session_state.loads)
if len(df)>0: st.dataframe(df); st.session_state.total_kwh = df["الاستهلاك_Wh"].sum()/1000; st.metric("اجمالي الاستهلاك اليومي", f"{st.session_state.total_kwh:.2f} kWh")
if st.button("💾 حفظ وانتقل للمحاكي"):
    save_to_sheet({"الاسم":name, "الرقم":phone, "الاستهلاك_kWh":st.session_state.total_kwh}, "Customer")
    st.success("تم الحفظ ✅"); st.switch_page("pages/03_⚡_المحاكي_العالمي.py")
