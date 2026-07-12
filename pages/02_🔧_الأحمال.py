import streamlit as st
from utils import load_css, show_header, check_login, logout

st.set_page_config(page_title="حساب الأحمال", page_icon="🔧", layout="wide")

st.markdown("""
    <style>
    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()
check_login()
show_header()
logout()

st.title("🔧 حساب الأحمال الكهربائية")
st.caption("احسب استهلاكك اليومي وعدد الألواح والبطاريات المطلوبة")

# تهيئة الجلسة
if 'loads' not in st.session_state:
    st.session_state['loads'] = []

with st.form("add_device"):
    st.subheader("اضافة جهاز")
    col1, col2, col3 = st.columns(3)
    with col1:
        device_name = st.text_input("اسم الجهاز", placeholder="مثال: ثلاجة")
    with col2:
        power = st.number_input("القدرة بالوات W", min_value=1, value=100)
    with col3:
        hours = st.number_input("ساعات التشغيل / اليوم", min_value=0.5, step=0.5, value=8.0)
    
    add_btn = st.form_submit_button("➕ اضافة للجدول")

if add_btn and device_name:
    kwh = (power * hours) / 1000
    st.session_state['loads'].append({
        "device": device_name,
        "power": power,
        "hours": hours,
        "kwh": kwh
    })
    st.success(f"تم اضافة {device_name}")
    st.rerun()

st.divider()

if st.session_state['loads']:
    st.subheader("📋 جدول الأجهزة")
    
    total_kwh = 0
    for i, item in enumerate(st.session_state['loads']):
        col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])
        col1.write(f"**{item['device']}**")
        col2.write(f"{item['power']} W")
        col3.write(f"{item['hours']} ساعة")
        col4.write(f"{item['kwh']:.2f} kWh")
        if col5.button("🗑️", key=i):
            st.session_state['loads'].pop(i)
            st.rerun()
        total_kwh += item['kwh']
    
    st.metric("اجمالي الاستهلاك اليومي", f"{total_kwh:.2f} kWh/يوم")
    
    st.divider()
    st.subheader("⚡ التوصيات")
    
    # حساب تقريبي للالواح والبطاريات
    sun_hours = 5  # متوسط ساعات الشمس
    system_loss = 1.3
    
    panel_watt = 550
    battery_ah = 200
    battery_volt = 12
    
    required_panel = (total_kwh * 1000 * system_loss) / sun_hours
    panels_needed = int(required_panel / panel_watt) + 1
    
    battery_kwh = total_kwh * 2  # يومين
    battery_needed = int((battery_kwh * 1000) / (battery_ah * battery_volt)) + 1
    
    col1, col2 = st.columns(2)
    col1.metric("عدد الألواح 550W المقترح", panels_needed)
    col2.metric("عدد البطاريات 200Ah المقترح", battery_needed)
    
    if st.button("🛒 اضافة للسلة"):
        st.session_state['total_load'] = total_kwh
        st.success("تم حفظ الاستهلاك. امشي المتجر")
        st.page_link("pages/06_🛒_السلة_والمتجر.py", label="انتقل للمتجر")
    
    if st.button("مسح الكل"):
        st.session_state['loads'] = []
        st.rerun()
else:
    st.info("لم تضف اي اجهزة بعد")

st.divider()
st.page_link("app.py", label="🏠 الرجوع للرئيسية")
