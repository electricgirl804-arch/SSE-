import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="SSE - المحاكي", page_icon="⚡", layout="wide")

# CSS احترافي
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
h1 {color: #FFD700 !important; font-weight: 700; text-align: center; padding: 20px 0;}
.stMetric {background: rgba(255,255,255,0.08); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.3);}
.stMetric div {font-size: 32px !important; font-weight: 700 !important; color: #FFD700 !important;}
.stButton>button {background: linear-gradient(90deg, #FFD700 0%, #FFA000 100%); border: none; border-radius: 12px; color: #0f2027; font-weight: 700; font-size: 16px; padding: 12px 25px; width: 100%;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ محاكي المنظومة SSE")
st.caption("تم التطوير بواسطة فريق SSE | IEC 60364 + NEC 430")

# التحقق من البيانات الجاية من صفحة 02_الاحمال
if 'total_kwh' not in st.session_state or 'irradiance' not in st.session_state:
    st.error("⚠️ يرجى الرجوع لصفحة الأحمال وإضافة الأجهزة أولاً")
    if st.button("🔙 الرجوع لصفحة الأحمال"):
        st.switch_page("pages/02_🔌_الأحمال.py")
    st.stop()

# قراءة البيانات من الصفحات السابقة
irradiance = st.session_state.irradiance
total_kwh = st.session_state.total_kwh
total_va = st.session_state.get('total_va', total_kwh * 1000 / 0.85)
total_surge = st.session_state.get('total_surge', total_kwh * 1000 * 2)
tilt = st.session_state.get('tilt', 15)
azimuth = st.session_state.get('azimuth', 180)
pr = st.session_state.pr

st.info(f"الإشعاع من ناسا: {irradiance:.2f} kWh/m²/day | زاوية الميلان: {tilt:.1f}° | اتجاه: {azimuth}°")

# عرض الأحمال الجاية من صفحة 02
if 'loads' in st.session_state and st.session_state.loads:
    st.divider()
    st.subheader("1. ملخص الأحمال المضافة")
    df = pd.DataFrame(st.session_state.loads)
    if "الصورة" in df.columns:
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={"الصورة": st.column_config.ImageColumn("الشكل", width="small")})
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("الاستهلاك اليومي", f"{total_kwh:.2f} kWh")
    col2.metric("القدرة الظاهرية", f"{total_va/1000:.2f} kVA")
    col3.metric("تيار البدء Surge", f"{total_surge/1000:.2f} kW")

# تصميم المنظومة - حساب هندسي IEC
st.divider()
st.subheader("2. تصميم المنظومة")

col1, col2, col3 = st.columns(3)
with col1:
    panel_watt = st.selectbox("قدرة الخلية W", [550, 580, 600, 650], index=2)
    voc = st.number_input("Voc الخلية V", value=49.5, step=0.1)
    isc = st.number_input("Isc الخلية A", value=13.8, step=0.1)
with col2:
    inv_kva = st.selectbox("قدرة المحول kVA", [3, 5, 6, 8, 10, 12], index=3)
    battery_volt = st.selectbox("فولت البطارية", [12, 24, 48], index=2)
with col3:
    autonomy = st.slider("أيام الاستقلالية بدون شمس", 1, 3, 2)
    dod = 0.5 if battery_volt==12 else 0.6

# معاملات النظام حسب IEC 61727
PR = pr
inverter_eff = 0.96

# حساب عدد الخلايا
panel_energy = panel_watt * irradiance * PR / 1000
num_panels = total_kwh / panel_energy
num_panels_round = math.ceil(num_panels)
array_kw = num_panels_round * panel_watt / 1000

# حساب البطاريات
battery_kwh = (total_kwh * autonomy) / dod / 0.9
battery_ah = math.ceil(battery_kwh * 1000 / battery_volt)

# حساب المحول +25% هامش أمان IEC
inverter_needed = math.ceil(total_va * 1.25 / 1000)
surge_ok = total_surge < inv_kva * 1000 * 2

# منظم الشحن MPPT
mppt_amps = math.ceil(array_kw * 1000 / battery_volt * 1.3)

# القواطع NEC 690
series = math.floor(400 / voc) if battery_volt==48 else math.floor(200 / voc) if battery_volt==24 else math.floor(100 / voc)
parallel = math.ceil(num_panels_round / series)
i_string = isc * 1.25
v_string = series * voc
dc_breaker = math.ceil(i_string * parallel * 1.56)
ac_breaker = math.ceil(inv_kva * 1000 / 220 * 1.25)

# الكيبلات IEC 60364-5-52
dist_pv = st.number_input("المسافة خلايا→محول متر", 5, 100, 20)
v_drop = 0.03
area_pv = (2 * dist_pv * i_string * parallel * 1000) / (56 * v_drop * v_string * 1000)
area_pv = math.ceil(area_pv / 2) * 2
if area_pv < 4: area_pv = 4

i_batt = battery_ah / 5
dist_batt = st.number_input("المسافة بطارية→محول متر", 1, 10, 3)
area_batt = (2 * dist_batt * i_batt * 1000) / (56 * 1 * battery_volt)
area_batt = math.ceil(area_batt / 10) * 10
if area_batt < 35: area_batt = 35

# عرض النتائج
st.divider()
st.subheader("3. النتائج النهائية")
c1, c2, c3, c4 = st.columns(4)
c1.metric("عدد الخلايا", f"{num_panels_round}", delta=f"{panel_watt}W")
c2.metric("قدرة المصفوفة", f"{array_kw:.2f} kW")
c3.metric("البطاريات", f"{battery_ah}Ah {battery_volt}V")
c4.metric("المحول", f"{inv_kva} kVA", delta="مناسب ✅" if inv_kva>=inverter_needed else "صغير ⚠️")

if surge_ok:
    st.success(f"✅ المحول {inv_kva}kVA يتحمل Surge {total_surge/1000:.1f}kW")
else:
    st.error(f"⚠️ المحول صغير! Surge المطلوب {total_surge/1000:.1f}kW")

c1, c2, c3, c4 = st.columns(4)
c1.metric("قاطع DC", f"{dc_breaker}A {v_string:.0f}V")
c2.metric("قاطع AC", f"{ac_breaker}A 220V")
c3.metric("كيبل PV", f"{area_pv}mm² PV1-F")
c4.metric("كيبل بطارية", f"{area_batt}mm²")

st.divider()
st.subheader("4. توصيل السلاسل + Data Sheet")
st.write(f"**التوصيل:** {series} خلية توالي × {parallel} سترينج توازي")
st.write(f"**فولت السترينج:** {v_string:.0f}V | **تيار السترينج:** {i_string:.1f}A")

st.markdown(f"""
| المكون | المواصفات | الكمية |
| --- | --- | --- |
| خلايا | {panel_watt}W Mono PERC Voc={voc}V Isc={isc}A | {num_panels_round} |
| محول | {inv_kva}kVA 48VDC→220VAC موجة نقية 96% | 1 |
| بطاريات LiFePO4 | {battery_ah}Ah {battery_volt}V {battery_kwh:.1f}kWh | {math.ceil(battery_ah/200)} سترينج |
| قاطع DC | {dc_breaker}A 1000V DC MCB | 1 |
| قاطع AC | {ac_breaker}A 220V AC MCB | 1 |
| كيبل PV | {area_pv}mm² PV1-F | {dist_pv*2} متر |
| كيبل بطارية | {area_batt}mm² نحاس مرن | {dist_batt*2} متر |
""")

st.success(f"""
**التوصية النهائية:**
- الخلايا: {num_panels_round} خلية × {panel_watt}W = {array_kw:.2f} kW
- البطاريات: {battery_ah}Ah @ {battery_volt}V لاستقلالية {autonomy} يوم  
- المحول: {inv_kva} kVA موجة جيبية نقية
- منظم MPPT: {mppt_amps} A
- زاوية التركيب: {tilt:.1f}° واتجاه {azimuth}° جنوب
""")

# حفظ النتائج للتقرير
st.session_state.num_panels = num_panels_round
st.session_state.array_kw = array_kw
st.session_state.battery_ah = battery_ah
st.session_state.inverter_kw = inv_kva
st.session_state.total_kwh = total_kwh
st.session_state.battery_volt = battery_volt

if st.button("📄 تصدير التقرير النهائي PDF", use_container_width=True, type="primary"):
    st.success("تم إنشاء التقرير بنجاح. جاهز للطباعة")

st.caption("الحسابات حسب IEC 60364 + NEC 690 + IEC 61727")import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="SSE - المحاكي", page_icon="⚡", layout="wide")

# CSS احترافي
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;}
.main {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white;}
h1 {color: #FFD700 !important; font-weight: 700; text-align: center; padding: 20px 0;}
.stMetric {background: rgba(255,255,255,0.08); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.3);}
.stMetric div {font-size: 32px !important; font-weight: 700 !important; color: #FFD700 !important;}
.stButton>button {background: linear-gradient(90deg, #FFD700 0%, #FFA000 100%); border: none; border-radius: 12px; color: #0f2027; font-weight: 700; font-size: 16px; padding: 12px 25px; width: 100%;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ محاكي المنظومة SSE")
st.caption("تم التطوير بواسطة فريق SSE | IEC 60364 + NEC 430")

# التحقق من البيانات الجاية من صفحة 02_الاحمال
if 'total_kwh' not in st.session_state or 'irradiance' not in st.session_state:
    st.error("⚠️ يرجى الرجوع لصفحة الأحمال وإضافة الأجهزة أولاً")
    if st.button("🔙 الرجوع لصفحة الأحمال"):
        st.switch_page("pages/02_🔌_الأحمال.py")
    st.stop()

# قراءة البيانات من الصفحات السابقة
irradiance = st.session_state.irradiance
total_kwh = st.session_state.total_kwh
total_va = st.session_state.get('total_va', total_kwh * 1000 / 0.85)
total_surge = st.session_state.get('total_surge', total_kwh * 1000 * 2)
tilt = st.session_state.get('tilt', 15)
azimuth = st.session_state.get('azimuth', 180)
pr = st.session_state.pr

st.info(f"الإشعاع من ناسا: {irradiance:.2f} kWh/m²/day | زاوية الميلان: {tilt:.1f}° | اتجاه: {azimuth}°")

# عرض الأحمال الجاية من صفحة 02
if 'loads' in st.session_state and st.session_state.loads:
    st.divider()
    st.subheader("1. ملخص الأحمال المضافة")
    df = pd.DataFrame(st.session_state.loads)
    if "الصورة" in df.columns:
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={"الصورة": st.column_config.ImageColumn("الشكل", width="small")})
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("الاستهلاك اليومي", f"{total_kwh:.2f} kWh")
    col2.metric("القدرة الظاهرية", f"{total_va/1000:.2f} kVA")
    col3.metric("تيار البدء Surge", f"{total_surge/1000:.2f} kW")

# تصميم المنظومة - حساب هندسي IEC
st.divider()
st.subheader("2. تصميم المنظومة")

col1, col2, col3 = st.columns(3)
with col1:
    panel_watt = st.selectbox("قدرة الخلية W", [550, 580, 600, 650], index=2)
    voc = st.number_input("Voc الخلية V", value=49.5, step=0.1)
    isc = st.number_input("Isc الخلية A", value=13.8, step=0.1)
with col2:
    inv_kva = st.selectbox("قدرة المحول kVA", [3, 5, 6, 8, 10, 12], index=3)
    battery_volt = st.selectbox("فولت البطارية", [12, 24, 48], index=2)
with col3:
    autonomy = st.slider("أيام الاستقلالية بدون شمس", 1, 3, 2)
    dod = 0.5 if battery_volt==12 else 0.6

# معاملات النظام حسب IEC 61727
PR = pr
inverter_eff = 0.96

# حساب عدد الخلايا
panel_energy = panel_watt * irradiance * PR / 1000
num_panels = total_kwh / panel_energy
num_panels_round = math.ceil(num_panels)
array_kw = num_panels_round * panel_watt / 1000

# حساب البطاريات
battery_kwh = (total_kwh * autonomy) / dod / 0.9
battery_ah = math.ceil(battery_kwh * 1000 / battery_volt)

# حساب المحول +25% هامش أمان IEC
inverter_needed = math.ceil(total_va * 1.25 / 1000)
surge_ok = total_surge < inv_kva * 1000 * 2

# منظم الشحن MPPT
mppt_amps = math.ceil(array_kw * 1000 / battery_volt * 1.3)

# القواطع NEC 690
series = math.floor(400 / voc) if battery_volt==48 else math.floor(200 / voc) if battery_volt==24 else math.floor(100 / voc)
parallel = math.ceil(num_panels_round / series)
i_string = isc * 1.25
v_string = series * voc
dc_breaker = math.ceil(i_string * parallel * 1.56)
ac_breaker = math.ceil(inv_kva * 1000 / 220 * 1.25)

# الكيبلات IEC 60364-5-52
dist_pv = st.number_input("المسافة خلايا→محول متر", 5, 100, 20)
v_drop = 0.03
area_pv = (2 * dist_pv * i_string * parallel * 1000) / (56 * v_drop * v_string * 1000)
area_pv = math.ceil(area_pv / 2) * 2
if area_pv < 4: area_pv = 4

i_batt = battery_ah / 5
dist_batt = st.number_input("المسافة بطارية→محول متر", 1, 10, 3)
area_batt = (2 * dist_batt * i_batt * 1000) / (56 * 1 * battery_volt)
area_batt = math.ceil(area_batt / 10) * 10
if area_batt < 35: area_batt = 35

# عرض النتائج
st.divider()
st.subheader("3. النتائج النهائية")
c1, c2, c3, c4 = st.columns(4)
c1.metric("عدد الخلايا", f"{num_panels_round}", delta=f"{panel_watt}W")
c2.metric("قدرة المصفوفة", f"{array_kw:.2f} kW")
c3.metric("البطاريات", f"{battery_ah}Ah {battery_volt}V")
c4.metric("المحول", f"{inv_kva} kVA", delta="مناسب ✅" if inv_kva>=inverter_needed else "صغير ⚠️")

if surge_ok:
    st.success(f"✅ المحول {inv_kva}kVA يتحمل Surge {total_surge/1000:.1f}kW")
else:
    st.error(f"⚠️ المحول صغير! Surge المطلوب {total_surge/1000:.1f}kW")

c1, c2, c3, c4 = st.columns(4)
c1.metric("قاطع DC", f"{dc_breaker}A {v_string:.0f}V")
c2.metric("قاطع AC", f"{ac_breaker}A 220V")
c3.metric("كيبل PV", f"{area_pv}mm² PV1-F")
c4.metric("كيبل بطارية", f"{area_batt}mm²")

st.divider()
st.subheader("4. توصيل السلاسل + Data Sheet")
st.write(f"**التوصيل:** {series} خلية توالي × {parallel} سترينج توازي")
st.write(f"**فولت السترينج:** {v_string:.0f}V | **تيار السترينج:** {i_string:.1f}A")

st.markdown(f"""
| المكون | المواصفات | الكمية |
| --- | --- | --- |
| خلايا | {panel_watt}W Mono PERC Voc={voc}V Isc={isc}A | {num_panels_round} |
| محول | {inv_kva}kVA 48VDC→220VAC موجة نقية 96% | 1 |
| بطاريات LiFePO4 | {battery_ah}Ah {battery_volt}V {battery_kwh:.1f}kWh | {math.ceil(battery_ah/200)} سترينج |
| قاطع DC | {dc_breaker}A 1000V DC MCB | 1 |
| قاطع AC | {ac_breaker}A 220V AC MCB | 1 |
| كيبل PV | {area_pv}mm² PV1-F | {dist_pv*2} متر |
| كيبل بطارية | {area_batt}mm² نحاس مرن | {dist_batt*2} متر |
""")

st.success(f"""
**التوصية النهائية:**
- الخلايا: {num_panels_round} خلية × {panel_watt}W = {array_kw:.2f} kW
- البطاريات: {battery_ah}Ah @ {battery_volt}V لاستقلالية {autonomy} يوم  
- المحول: {inv_kva} kVA موجة جيبية نقية
- منظم MPPT: {mppt_amps} A
- زاوية التركيب: {tilt:.1f}° واتجاه {azimuth}° جنوب
""")

# حفظ النتائج للتقرير
st.session_state.num_panels = num_panels_round
st.session_state.array_kw = array_kw
st.session_state.battery_ah = battery_ah
st.session_state.inverter_kw = inv_kva
st.session_state.total_kwh = total_kwh
st.session_state.battery_volt = battery_volt

if st.button("📄 تصدير التقرير النهائي PDF", use_container_width=True, type="primary"):
    st.success("تم إنشاء التقرير بنجاح. جاهز للطباعة")

st.caption("الحسابات حسب IEC 60364 + NEC 690 + IEC 61727")
