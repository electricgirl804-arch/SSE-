import streamlit as st
import pandas as pd
from utils import CSS, check_session, init_session_state

st.set_page_config(page_title="SSE الأحمال", page_icon="⚡", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
init_session_state()
check_session(['irradiance', 'pr', 'cell_temp'])

st.title("🔧 إدارة الأحمال - أيقونات حقيقية")
st.markdown(f"الإشعاع: {st.session_state.irradiance:.2f} kWh/m² | حرارة الخلية: {st.session_state.cell_temp:.1f}°C")

def get_device_image(name):
    name = name.lower()
    base = "https://cdn-icons-png.flaticon.com/128/"
    if "لمبة" in name or "إضاءة" in name: return f"{base}702/702814.png"
    elif "مكيف" in name or "تكييف" in name: return f"{base}483/483103.png"
    elif "ثلاجة" in name or "فريزر" in name: return f"{base}891/891419.png"
    elif "مروحة" in name: return f"{base}727/727269.png"
    elif "تلفزيون" in name or "شاشة" in name: return f"{base}2972/2972185.png"
    elif "كمبيوتر" in name or "لابتوب" in name: return f"{base}686/686136.png"
    elif "غسالة" in name: return f"{base}2987/2987892.png"
    elif "سخان" in name: return f"{base}3050/3050521.png"
    elif "موتور" in name or "ماكينة" in name: return f"{base}809/809957.png"
    elif "طابعة" in name: return f"{base}1263/1263975.png"
    elif "لحام" in name: return f"{base}2945/2945571.png"
    elif "صاروخ" in name or "جلخ" in name: return f"{base}2917/2917996.png"
    elif "كمبروسر" in name: return f"{base}727/727269.png"
    else: return f"{base}2991/2991148.png"

if 'loads' not in st.session_state:
    st.session_state.loads = []

location_type = st.selectbox("نوع المكان IEC 60364", ["منزل سكني", "شقة/عمارة", "مؤسسة/مكتب", "مصنع صغير", "ورشة", "مزرعة", "محل تجاري"])
div_factor = {"منزل سكني": 0.6, "شقة/عمارة": 0.5, "مؤسسة/مكتب": 0.7, "مصنع صغير": 0.8, "ورشة": 0.9, "مزرعة": 0.75, "محل تجاري": 0.7}[location_type]

col1, col2 = st.columns([3,1])
with col1:
    if st.button(f"📋 تحميل قالب {location_type}"):
        templates = {
            "منزل سكني": [["لمبة LED",12,6,"مقاومي",0.95], ["مروحة سقف",70,10,"حثي",0.85], ["ثلاجة 14 قدم",150,24,"حثي",0.85], ["مكيف 1.5 حصان",1200,8,"حثي",0.9]],
            "ورشة": [["ماكينة لحام",3000,3,"حثي",0.85], ["صاروخ جلخ",2200,2,"حثي",0.85], ["كمبروسر هواء",2200,4,"حثي",0.85], ["لمبة ورشة",100,10,"مقاومي",0.95]],
            "مصنع صغير": [["موتور 3 فاز 5 حصان",3700,8,"حثي",0.88], ["كمبروسر 2 حصان",1500,4,"حثي",0.85], ["إضاءة LED",100,10,"مقاومي",0.95]]
        }
        if location_type in templates:
            st.session_state.loads = []
            for name, p, h, typ, eff in templates[location_type]:
                pf = 1.0 if typ=="مقاومي" else 0.8 if typ=="حثي" else 0.9
                surge = p * 1.0 if typ=="مقاومي" else p * 6.0
                actual_p = p / eff
                img = get_device_image(name)
                st.session_state.loads.append({
                    "الصورة": img,
                    "الجهاز": name,
                    "القدرة W": p, "الساعات": h, "النوع": typ,
                    "PF": pf, "الكفاءة": eff, "القدرة الفعلية W": actual_p,
                    "Surge W": surge, "الاستهلاك Wh": actual_p * h
                })
            st.rerun()
with col2:
    if st.button("🗑️ مسح الكل"):
        st.session_state.loads = []
        st.rerun()

with st.expander("➕ إضافة جهاز جديد"):
    col1, col2, col3, col4, col5 = st.columns(5)
    new_name = col1.text_input("اسم الجهاز")
    new_power = col2.number_input("القدرة الاسمية W", 1, 50000, 100)
    new_hours = col3.number_input("ساعات التشغيل/يوم", 0.5, 24.0, 5.0, 0.5)
    new_type = col4.selectbox("نوع الحمل", ["مقاومي", "حثي", "إلكتروني"])
    new_eff = col5.selectbox("كفاءة الجهاز", [0.98, 0.95, 0.9, 0.85, 0.8], format_func=lambda x: f"{x*100:.0f}%")
    
    if st.button("إضافة الجهاز"):
        if new_name:
            pf = 1.0 if new_type=="مقاومي" else 0.8 if new_type=="حثي" else 0.9
            surge = new_power * 1.0 if new_type=="مقاومي" else new_power * 6.0
            actual_power = new_power / new_eff
            img = get_device_image(new_name)
            st.session_state.loads.append({
                "الصورة": img,
                "الجهاز": new_name,
                "القدرة W": new_power, "الساعات": new_hours, "النوع": new_type,
                "PF": pf, "الكفاءة": new_eff, "القدرة الفعلية W": actual_power,
                "Surge W": surge, "الاستهلاك Wh": actual_power * new_hours
            })
            st.rerun()

if st.session_state.loads:
    df = pd.DataFrame(st.session_state.loads)
    
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor_images",
                               column_config={
                                   "الصورة": st.column_config.ImageColumn("الشكل", width="small"),
                                   "الجهاز": st.column_config.TextColumn("اسم الجهاز", width="medium"),
                                   "PF": st.column_config.NumberColumn(format="%.2f", disabled=True),
                                   "القدرة الفعلية W": st.column_config.NumberColumn(format="%.0f", disabled=True),
                                   "الاستهلاك Wh": st.column_config.NumberColumn(format="%.0f", disabled=True)
                               })
    
    for i in range(len(edited_df)):
        typ = edited_df.loc[i, "النوع"]
        pf = 1.0 if "مقاومي" in typ else 0.8 if "حثي" in typ else 0.9
        surge_factor = 1.0 if "مقاومي" in typ else 6.0
        eff = edited_df.loc[i, "الكفاءة"]
        p_nom = edited_df.loc[i, "القدرة W"]
        img = get_device_image(edited_df.loc[i, "الجهاز"])
        edited_df.loc[i, "الصورة"] = img
        edited_df.loc[i, "PF"] = pf
        edited_df.loc[i, "القدرة الفعلية W"] = p_nom / eff
        edited_df.loc[i, "Surge W"] = p_nom * surge_factor
        edited_df.loc[i, "الاستهلاك Wh"] = edited_df.loc[i, "القدرة الفعلية W"] * edited_df.loc[i, "الساعات"]
    
    st.session_state.loads = edited_df.to_dict('records')
    
    total_wh = edited_df["الاستهلاك Wh"].sum()
    total_watt_actual = edited_df["القدرة الفعلية W"].sum()
    
    max_surge_idx = edited_df["Surge W"].idxmax() if len(edited_df) > 0 else 0
    max_surge = edited_df.loc[max_surge_idx, "Surge W"] if len(edited_df) > 0 else 0
    rest_watt = total_watt_actual - edited_df.loc[max_surge_idx, "القدرة الفعلية W"] if len(edited_df) > 0 else 0
    total_surge_nec = max_surge + rest_watt * 1.25
    
    adjusted_watt = total_watt_actual * div_factor
    adjusted_surge = total_surge_nec * div_factor
    
    avg_pf = sum([pf * w for pf, w in zip(edited_df["PF"], edited_df["القدرة الفعلية W"])]) / total_watt_actual if total_watt_actual > 0 else 0.85
    apparent_power_va = adjusted_watt / avg_pf
    
    cable_loss = 0.03
    inverter_loss = 0.04
    battery_loss = 0.08 if st.session_state.get('system_type', 'off-grid') == 'off-grid' else 0.02
    temp_loss = abs(st.session_state.get('temp_loss', -12)) / 100
    
    total_system_loss = cable_loss + inverter_loss + battery_loss + temp_loss
    watt_with_loss = adjusted_watt / (1 - total_system_loss)
    va_with_loss = watt_with_loss / avg_pf
    
    st.divider()
    st.markdown("### 📊 النتائج النهائية")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("الاستهلاك اليومي", f"{total_wh/1000:.2f} kWh")
    c2.metric("القدرة بعد Diversity", f"{adjusted_watt/1000:.2f} kW")
    c3.metric("القدرة مع الخسائر", f"{watt_with_loss/1000:.2f} kW")
    c4.metric("القدرة الظاهرية kVA", f"{va_with_loss/1000:.2f}")
    
    st.metric("تيار البدء Surge", f"{adjusted_surge/1000:.2f} kW")
    
    st.session_state.total_kwh = total_wh / 1000
    st.session_state.total_watt = watt_with_loss
    st.session_state.total_va = va_with_loss
    st.session_state.total_surge = adjusted_surge
    st.session_state.pf = avg_pf
    
    if st.button("التالي → المحاكي 24 ساعة", use_container_width=True, type="primary"):
        st.switch_page("pages/03_المحاكي.py")
else:
    st.info("اضغط تحميل قالب أو أضف جهاز. حتشوف أيقونات ملونة حقيقية")

st.caption("IEC 60364 + NEC 430 + IEC 61727")
