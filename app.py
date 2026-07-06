import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Solar BOM Pro", layout="wide")
st.title("☀️ حاسبة الطاقة الشمسية - GPS + BOM + حمايات")

# 1. مكتبة المعدات
with open("components.json", encoding="utf-8") as f:
    DB = json.load(f)

# 2. حساب فترة الاسترجاع
def calc_roi(total_cost, kwh_per_day, electricity_price=0.15):
    yearly_saving = kwh_per_day * 365 * electricity_price
    payback_years = total_cost / yearly_saving if yearly_saving > 0 else 99
    lcoe = total_cost / (kwh_per_day * 365 * 25)
    return round(payback_years, 1), round(lcoe, 3), round(yearly_saving)

# 3. حساب الإشعاع من ناسا
@st.cache_data
def get_ghi(lat, lon):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20220101&end=20221231&latitude={lat}&longitude={lon}&community=RE&parameters=ALLSKY_SFC_SW_DWN&format=JSON"
    r = requests.get(url, timeout=10)
    return r.json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["20221231"]

# 4. حساب الـ BOM الأساسي
def calc_full_bom(load_w, hours, lat, lon, battery_days=2, dod=0.8, system_eff=0.85):
    ghi = get_ghi(lat, lon)
    daily_kwh = load_w * hours / 1000
    panel_w = 550
    panels = int(np.ceil(daily_kwh / (ghi * panel_w / 1000 * system_eff)))
    battery_wh = daily_kwh * 1000 * battery_days / dod
    battery_ah = battery_wh / 48
    num_batteries = num_batteries = int(np.ceil(battery_ah / 200))
    inverter_kw = load_w * 1.3 / 1000
    return {
        "daily_kwh": round(daily_kwh, 2),
        "panels": panels,
        "num_batteries": num_batteries,
        "inverter_kw": round(inverter_kw, 1),
        "total_kwh": daily_kwh,
        "ghi": round(ghi, 2)
    }

# 5. حساب الحمايات والكيبلات
def calc_protections(bom, panel, inverter, distance_pv_to_inv):
    string_current = panel["imp"]
    panels_per_string = 10
    vmp_string = panel["vmp"] * panels_per_string
    cable_mm2 = (2 * distance_pv_to_inv * string_current * 0.017) / (0.03 * vmp_string)
    cable_size = int(np.ceil(cable_mm2 * 1.25))
    cable_size = 4 if cable_size <= 4 else 6 if cable_size <= 6 else 10 if cable_size <= 10 else 16
    fuse_dc = int(np.ceil(string_current * 1.56))
    ac_current = inverter["kw"] * 1000 / 220
    breaker_ac = int(np.ceil(ac_current * 1.25))
    return {
        "cable_pv_mm2": cable_size,
        "fuse_dc_A": fuse_dc,
        "breaker_ac_A": breaker_ac,
        "surge_protector": "Type 2 DC + AC"
    }

# 6. الواجهة + GPS
st.subheader("📍 تحديد الموقع")

if st.button("📡 حدد موقعي تلقائياً GPS"):
    components.html(
        """
        <script>
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                window.parent.postMessage({type: "streamlit:setComponentValue", value: {lat: lat, lon: lon}}, "*");
            },
            function(error) {
                alert("فشل في تحديد الموقع. فعلي الـ GPS واعملي Refresh");
            }
        );
        </script>
        """,
        height=0,
    )

col1, col2, col3 = st.columns(3)
with col1:
    lat = st.number_input("خط العرض Latitude", value=15.5, format="%.6f", key="lat")
with col2:
    lon = st.number_input("خط الطول Longitude", value=32.5, format="%.6f", key="lon")
with col3:
    distance = st.number_input("المسافة بالمتر", value=25, min_value=5)

# عرض بيانات ناسا طوالي
if lat and lon:
    ghi = get_ghi(lat, lon)
    st.success(f"✅ الموقع: {lat:.4f}, {lon:.4f} | GHI: {ghi:.2f} kWh/m²/day")

col1, col2 = st.columns(2)
with col1:
    load = st.number_input("الحمل بالواط", value=2000)
    hours = st.number_input("ساعات التشغيل", value=8)
with col2:
    st.info("💡 بعد تحددي الموقع بالـ GPS اضغطي احسب")

# 7. اختيار الماركات
st.subheader("🛠️ اختاري الماركة والسعر")
panel = st.selectbox("اللوح الشمسي", DB["panels"], format_func=lambda x: f"{x['brand']} {x['watt']}W - ${x['price']}")
inverter = st.selectbox("الانفرتر", DB["inverters"], format_func=lambda x: f"{x['brand']} {x['kw']}kW - ${x['price']}")
battery = st.selectbox("البطارية", DB["batteries"], format_func=lambda x: f"{x['brand']} {x['ah']}Ah - ${x['price']}")

# 8. زرار الحساب
if st.button("احسب", type="primary"):
    with st.spinner("بحسب من بيانات ناسا..."):
        bom = calc_full_bom(load, hours, lat, lon)
        protections = calc_protections(bom, panel, inverter, distance)
        cost = bom["panels"]*panel["price"] + bom["num_batteries"]*battery["price"] + inverter["price"]
        payback, lcoe, saving = calc_roi(cost, bom["total_kwh"])
        
        st.success("تم الحساب بنجاح ✅")
        
        # المواصفات
        st.subheader("📋 المواصفات المطلوبة")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("الاستهلاك اليومي", f"{bom['daily_kwh']} kWh")
        c2.metric("عدد الألواح", f"{bom['panels']} لوح")
        c3.metric("عدد البطاريات", f"{bom['num_batteries']} بطارية")
        c4.metric("الانفرتر", f"{bom['inverter_kw']} kW")
        
        # الحمايات
        st.divider()
        st.subheader("⚡ الحمايات والكيبلات")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("كيبل DC", f"{protections['cable_pv_mm2']} mm²")
        c2.metric("فيوز DC", f"{protections['fuse_dc_A']} A")
        c3.metric("قاطع AC", f"{protections['breaker_ac_A']} A")
        c4.metric("مانع صواعق", protections["surge_protector"])
        
        # التكلفة
        st.divider()
        st.subheader("💰 دراسة الجدوى المالية")
        col1, col2, col3 = st.columns(3)
        col1.metric("التكلفة الكلية", f"${cost:,}")
        col2.metric("فترة الاسترجاع", f"{payback} سنة")
        col3.metric("التوفير السنوي", f"${saving:,}")
        st.info(f"💡 LCOE: ${lcoe} /kWh")
        
        # الداتا شيت
        st.divider()
        st.subheader("📄 داتا شيت المعدات")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write(f"**{panel['brand']} {panel['watt']}W**")
            if "datasheet" in panel: st.link_button("📄 داتا شيت", panel["datasheet"])
        with c2:
            st.write(f"**{inverter['brand']} {inverter['kw']}kW**")
            if "datasheet" in inverter: st.link_button("📄 داتا شيت", inverter["datasheet"])
        with c3:
            st.write(f"**{battery['brand']} {battery['ah']}Ah**")
            if "datasheet" in battery: st.link_button("📄 داتا شيت", battery["datasheet"])
