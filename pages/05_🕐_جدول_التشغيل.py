import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SSE - جدول التشغيل الذكي", page_icon="🕐", layout="wide")

# ===== CSS للشكل البريميوم =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
h1 {color: #FFD700!important; font-weight: 700; text-align: center; margin-bottom: 10px;}
.stDataFrame {border-radius: 10px; overflow: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🕐 جدول التشغيل الذكي")
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v1.4")

# ===== 1. قائمة الأجهزة الجاهزة =====
devices = {
    "اختار جهازك": 0,
    "مكيف 12 وحدة - 1200 واط": 1200,
    "مكيف 18 وحدة - 1800 واط": 1800,
    "تلاجة 14 قدم - 150 واط": 150,
    "سخان موية 50 لتر - 2000 واط": 2000,
    "غسالة 7 كيلو - 800 واط": 800,
    "موتور موية 1 حصان - 750 واط": 750,
    "مايكروويف - 1000 واط": 1000,
    "جهاز آخر - أدخل الواط يدوياً": -1
}

col1, col2 = st.columns(2)
with col1:
    battery_kwh = st.number_input("سعة البطارية بالكيلو واط ساعة", 5, 50, 15, help="مكتوبة في الاستيكر حق البطارية")
with col2:
    device_choice = st.selectbox("اختار الجهاز", list(devices.keys()))

if devices[device_choice] == -1:
    load_w = st.number_input("أدخل قدرة الجهاز بالواط يدوياً", 50, 5000, 1200)
else:
    load_w = devices[device_choice]

if load_w == 0:
    st.info("👆 اختاري جهاز من القائمة عشان نبدأ الحساب")
    st.stop()

# ===== 2. محاكاة الشمس من 6 صباحاً لـ 10 مساءً =====
hours = list(range(6, 22))
data = []
for h in hours:
    solar = max(0, 800 * np.sin((h-6)*np.pi/12)) # معادلة الإشعاع الشمسي
    net = solar - load_w
    status = "✅ شغلي الجهاز" if net > 0 else "⏳ انتظري الشمس"
    data.append({
        "الساعة": f"{h}:00",
        "الطاقة الشمسية واط": int(solar),
        "استهلاك الجهاز واط": load_w,
        "الفائض/العجز واط": int(net),
        "الحالة": status
    })

df = pd.DataFrame(data)

# ===== 3. تلوين الجدول أخضر/أحمر =====
def color_rows(row):
    if "شغلي" in row.الحالة:
        return ['background-color: rgba(0,255,0,0.2)'] * len(row)
    else:
        return ['background-color: rgba(255,0,0,0.1)'] * len(row)

st.divider()
st.subheader("متى يتم تشغيل الجهاز لتوفير البطارية؟")
st.dataframe(df.style.apply(color_rows, axis=1), use_container_width=True, height=420)

# ===== 4. أفضل وقت + حساب الألواح الناقصة + التوفير =====
best_hours = df[df['الفائض/العجز واط'] > 0]['الساعة'].tolist()
st.divider()

if best_hours:
    st.success(f"🔋 أفضل فترة للتشغيل: من {best_hours[0]} إلى {best_hours[-1]} وقت ذروة الإشعاع الشمسي")
    st.info(f"البطارية بسعة {battery_kwh} كيلو واط ساعة تكفي لمدة {battery_kwh*1000/load_w:.1f} ساعة بعد المغرب")

    # حساب التوفير بالجنيه
    saving_kwh = (len(best_hours) * load_w) / 1000
    saving_money = saving_kwh * 47 # سعر الكيلو 47 جنيه
    col1, col2 = st.columns(2)
    col1.metric("التوفير اليومي", f"{saving_money:.0f} جنيه")
    col2.metric("التوفير الشهري", f"{saving_money*30:.0f} جنيه")
else:
    st.error("⚠️ قدرة الجهاز أعلى من إنتاج الألواح الشمسية الحالية")
    panels_needed = int(load_w / 550) + 2 # اللوح 550 واط
    battery_needed = (load_w * 8) / 1000 # 8 ساعات بالليل
    st.warning(f"الحل: محتاجة {panels_needed} لوح 550 واط + بطارية {battery_needed:.1f} كيلو واط ساعة عشان الجهاز يشتغل نهار كامل")

st.divider()
if st.button("⬅️ العودة للقائمة الرئيسية"):
    st.switch_page("app.py")
