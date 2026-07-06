import streamlit as st

st.set_page_config(page_title="محاكي الأحمال", page_icon="⚡")

st.title("⚡ محاكي الأحمال الذكي SSE")
st.markdown("احسب استهلاكك الشهري وعدد الألواح والبطاريات المطلوبة")

st.divider()

# إدخال الأجهزة
st.subheader("1. أضف أجهزتك الكهربائية")

col1, col2, col3 = st.columns(3)
device_name = col1.text_input("اسم الجهاز", placeholder="مكيف، لمبة، شاشة")
power = col2.number_input("القدرة بالواط", min_value=1, value=100)
hours = col3.number_input("ساعات التشغيل/اليوم", min_value=0.5, value=5.0)

if st.button("➕ أضف الجهاز"):
    if "devices" not in st.session_state:
        st.session_state.devices = []
    st.session_state.devices.append({"name": device_name, "watt": power, "hours": hours})
    st.rerun()

# عرض الأجهزة المضافة
if "devices" in st.session_state and st.session_state.devices:
    st.divider()
    st.subheader("2. الأجهزة المضافة")
    
    total_watt = 0
    total_kwh = 0
    
    for i, d in enumerate(st.session_state.devices):
        daily_kwh = (d["watt"] * d["hours"]) / 1000
        total_watt += d["watt"]
        total_kwh += daily_kwh
        st.write(f"**{d['name']}**: {d['watt']}W × {d['hours']} ساعة = {daily_kwh:.2f} كيلو/يوم")
    
    st.divider()
    st.success(f"**إجمالي القدرة:** {total_watt} واط")
    st.success(f"**الاستهلاك اليومي:** {total_kwh:.2f} كيلو واط/ساعة")
    st.info(f"**الاستهلاك الشهري:** {total_kwh * 30:.2f} كيلو واط/ساعة")
    
    # اقتراح المنظومة
    st.divider()
    st.subheader("3. المنظومة المقترحة")
    panels = int(total_watt / 550) + 1  # لوح 550 واط
    battery = int(total_kwh * 2)  # بطاريات تكفي يومين
    
    col1, col2 = st.columns(2)
    col1.metric("عدد الألواح 550W", f"{panels} لوح")
    col2.metric("سعة البطاريات", f"~{battery} أمبير")
    
    if st.button("📞 اطلب عرض سعر"):
        st.switch_page("pages/12_📞_الدعم_الفني.py")
else:
    st.info("أضف أول جهاز عشان نحسب ليك المنظومة")

if st.button("🔙 الرجوع للرئيسية"):
    st.switch_page("pages/01_🏠_الرئيسية.py")
