import streamlit as st
import pandas as pd
from utils import CSS, check_session, init_session_state

st.set_page_config(page_title="SSE الأحمال", page_icon="⚡", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
init_session_state()
check_session(['irradiance', 'pr', 'cell_temp'])

st.title("🔧 إدارة الأحمال - حسابات عالمية")
st.markdown("حساب الأحمال الحثية والمقاومية + خسائر النظام كاملة")

if 'loads' not in st.session_state:
    st.session_state.loads = []

location_type = st.selectbox("نوع المكان IEC 60364", ["منزل سكني", "شقة/عمارة", "مؤسسة/مكتب", "مصنع صغير", "ورشة", "مزرعة", "محل تجاري"])
div_factor = {"منزل سكني": 0.6, "شقة/عمارة": 0.5, "مؤسسة/مكتب": 0.7, "مصنع صغير": 0.8, "ورشة": 0.9, "مزرعة": 0.75, "محل تجاري": 0.7}[location_type]

# إضافة جهاز
with st.expander("➕ إضافة جهاز جديد"):
    col1, col2, col3, col4, col5 = st.columns(5)
    new_name = col1.text_input("اسم الجهاز")
    new_power = col2.number_input("القدرة الاسمية W", 1, 50000, 100)
    new_hours = col3.number_input("ساعات التشغيل/يوم", 0.5, 24.0, 5.0, 0.5)
    new_type = col4.selectbox("نوع الحمل", ["مقاومي", "حثي", "إلكتروني"])
    new_eff = col5.selectbox("كفاءة الجهاز", [0.98, 0.95, 0.9, 0.85, 0.8], format_func=lambda x: f"{x*100:.0f}%")
    
    if st.button("إضافة"):
        if new_name:
            pf = 1.0 if new_type=="مقاومي" else 0.8 if new_type=="حثي" else 0.9
            surge = new_power * 1.0 if new_type=="مقاومي" else new_power * 6.0
            actual_power = new_power / new_eff
            st.session_state.loads.append({
                "الجهاز": new_name, "القدرة W": new_power, "الساعات": new_hours, "النوع": new_type,
                "PF": pf, "الكفاءة": new_eff, "القدرة الفعلية W": actual_power,
                "Surge W": surge, "الاستهلاك Wh": actual_power * new_hours
            })
            st.rerun()

if st.session_state.loads:
    df = pd.DataFrame(st.session_state.loads)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor_final")
    
    for i in range(len(edited_df)):
        pf = 1.0 if "مقاومي" in edited_df.loc[i, "النوع"] else 0.8 if "حثي" in edited_df.loc[i, "النوع"] else 0.9
        surge_factor = 1.0 if "مقاومي" in edited_df.loc[i, "النوع"] else 6.0
        eff = edited_df.loc[i, "الكفاءة"]
        p_nom = edited_df.loc[i, "القدرة W"]
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
    
    # خسائر النظام
    cable_loss = 0.03
    inverter_loss = 0.04
    battery_loss = 0.08 if st.session_state.get('system_type', 'off-grid') == 'off-grid' else 0.02
    temp_loss = abs(st.session_state.get('temp_loss', -12)) / 100
    
    total_system_loss = cable_loss + inverter_loss + battery_loss + temp_loss
    watt_with_loss = adjusted_watt / (1 - total_system_loss)
    va_with_loss = watt_with_loss / avg_pf
    
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("الاستهلاك اليومي", f"{total_wh/1000:.2f} kWh")
    col2.metric("القدرة بعد Diversity", f"{adjusted_watt/1000:.2f} kW")
    col3.metric("القدرة مع الخسائر", f"{watt_with_loss/1000:.2f} kW")
    col4.metric("القدرة الظاهرية", f"{va_with_loss/1000:.2f} kVA")
    
    st.metric("تيار البدء", f"{adjusted_surge/1000:.2f} kW")
    
    st.session_state.total_kwh = total_wh / 1000
    st.session_state.total_watt = watt_with_loss
    st.session_state.total_va = va_with_loss
    st.session_state.total_surge = adjusted_surge
    st.session_state.pf = avg_pf
    
    if st.button("التالي → المحاكي 24 ساعة", use_container_width=True, type="primary"):
        st.switch_page("pages/03_المحاكي.py")

st.caption("IEC 60364 + NEC 430 + IEC 61727")
