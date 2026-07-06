import streamlit as st
import pandas as pd
import numpy as np
import json
import requests

st.set_page_config(page_title="Solar BOM", layout="wide")
st.title("☀️ حاسبة الطاقة الشمسية - BOM + التكلفة")

# 1. مكتبة المعدات
with open("components.json", encoding="utf-8") as f:
    DB = json.load(f)

# 2. دالة حساب فترة الاسترجاع
def calc_roi(total_cost, kwh_per_day, electricity_price=0.15):
    yearly_saving = kwh_per_day * 365 * electricity_price
    payback_years = total_cost / yearly_saving if yearly_saving > 0 else 99
    lcoe = total_cost / (kwh_per_day * 365 * 25)  # على 25 سنة
    return round(payback_years, 1), round(lcoe, 3), round(yearly_saving)

# 3. دالة حساب الإشعاع من ناسا
@st.cache_data
def get_ghi(lat, lon):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20220101&end=20221231&latitude={lat}&longitude={lon}&community=RE&parameters=ALLSKY_SFC_SW_DWN&format=JSON"
    r = requests.get(url, timeout=10)
    return r.json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["20221231"]

# 4. دالة حساب الـ BOM
def calc_full_bom(load_w, hours, lat, lon, battery_days=2, dod=0.8, system_eff=0.85):
    ghi = get_ghi(lat, lon)
    daily_kwh = load_w * hours / 1000
    panel_w = 550
    panels = int(np.ceil(daily_kwh / (ghi * panel_w / 1000 * system_eff)))
    battery_wh = daily_kwh * 1000 * battery_days / dod
    battery_ah = battery_wh / 48
    num_batteries = int(np.ceil(battery_ah / 200))
    inverter_kw = load_w * 1.3 / 1000
    return {
        "daily_kwh": round(daily_kwh, 2),
        "panels": panels,
        "num_batteries": num_batteries,
        "inverter_kw": round(inverter_kw, 1),
        "total_kwh": daily_kwh,
        "ghi": round(ghi, 2)
    }

# 5. الواجهة
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("المدينة", "الخرطوم")
    lat = st.number_input("خط العرض", value=15.5)
    lon = st.number_input("خط الطول", value=32.5)
with col2:
    load = st.number_input("الحمل بالواط", value=2000)
    hours = st.number_input("ساعات التشغيل", value=8)

# 6. اختيار الماركات والأسعار
st.subheader("🛠️ اختاري الماركة والسعر")
panel = st.selectbox("اللوح الشمسي", DB["panels"], format_func=lambda x: f"{x['brand']} {x['watt']}W - ${x['price']}")
inverter = st.selectbox("الانفرتر", DB["inverters"], format_func=lambda x: f"{x['brand']} {x['kw']}kW - ${x['price']}")
battery = st.selectbox("البطارية", DB["batteries"], format_func=lambda x: f"{x['brand']} {x['ah']}Ah - ${x['price']}")

# 7. زرار الحساب + النتائج
if st.button("احسب", type="primary"):
    with st.spinner("بحسب ليك..."):
        bom = calc_full_bom(load, hours, lat, lon)
        
        # حساب التكلفة
        cost = bom["panels"]*panel["price"] + bom["num_batteries"]*battery["price"] + inverter["price"]
        payback, lcoe, saving = calc_roi(cost, bom["total_kwh"])
        
        st.success("تم الحساب بنجاح ✅")
        
        # عرض المواصفات
        st.subheader("📋 المواصفات المطلوبة")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("الاستهلاك اليومي", f"{bom['daily_kwh']} kWh")
        c2.metric("عدد الألواح", f"{bom['panels']} لوح")
        c3.metric("عدد البطاريات", f"{bom['num_batteries']} بطارية")
        c4.metric("الانفرتر", f"{bom['inverter_kw']} kW")
        
        # عرض التكلفة
        st.divider()
        st.subheader("💰 دراسة الجدوى المالية")
        col1, col2, col3 = st.columns(3)
        col1.metric("التكلفة الكلية", f"${cost:,}")
        col2.metric("فترة الاسترجاع", f"{payback} سنة")
        col3.metric("التوفير السنوي", f"${saving:,}")
        
        st.info(f"💡 تكلفة الكيلو واط مدى الحياة LCOE: ${lcoe}")
