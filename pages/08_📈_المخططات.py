import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utils import check_login, logout, load_css

check_login(); logout(); load_css()

st.set_page_config(page_title="المخططات - SSE", layout="wide")

# ===== CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif; direction: rtl; text-align: right;}
.stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
h1, h2, h3 { color: #FFD700!important; font-weight: 800; }
.metric-card { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; 
               box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-left: 5px solid #FFD700; color: #0A3D62; }
.chart-card { background: rgba(255,255,255,0.98); padding: 25px; border-radius: 15px; 
              margin: 20px 0; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📈 المخططات والرسوم البيانية - التكاليف</h1>", unsafe_allow_html=True)
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v2.3")

if 'num_panels' in st.session_state:
    st.success("✅ تم تحميل بيانات التكاليف بنجاح")
    
    # ===== Sidebar اسعار =====
    with st.sidebar:
        st.markdown("<h2 style='color: #FFD700;'>⚙️ تعديل الاسعار $</h2>", unsafe_allow_html=True)
        price_panel = st.number_input("سعر اللوح 550W", value=85)
        price_battery = st.number_input("سعر البطارية 48V", value=280)
        price_inverter = st.number_input("سعر الانفرتر", value=450)
        price_cable = st.number_input("سعر الكيبل للوح", value=12)
        price_install = st.number_input("سعر التركيب للوح", value=15)
    
    # ===== حساب التكاليف =====
    cost_panels = st.session_state.num_panels * price_panel
    cost_batteries = st.session_state.get('num_batteries', 4) * price_battery
    cost_inverter = st.session_state.get('inverter_kw', 5) * price_inverter
    cost_cables = st.session_state.num_panels * price_cable
    cost_installation = st.session_state.num_panels * price_install
    total = cost_panels + cost_batteries + cost_inverter + cost_cables + cost_installation
    
    data = {
        "المكون": ["الألواح الشمسية", "البطاريات", "الانفرتر", "الكيبل والحمايات", "التركيب"],
        "التكلفة": [cost_panels, cost_batteries, cost_inverter, cost_cables, cost_installation],
        "الكمية": [
            f"{st.session_state.num_panels} لوح",
            f"{st.session_state.get('num_batteries', 4)} بطارية",
            f"{st.session_state.get('inverter_kw', 5)} kW",
            f"{st.session_state.num_panels} طقم",
            "شامل"
        ]
    }
    df = pd.DataFrame(data)
    
    # ===== 1. كروت الملخص =====
    st.markdown("### الملخص السريع")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h4>عدد الألواح</h4><h2>{st.session_state.num_panels}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h4>عدد البطاريات</h4><h2>{st.session_state.get('num_batteries', 4)}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h4>قدرة الانفرتر</h4><h2>{st.session_state.get('inverter_kw', 5)} kW</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><h4>الإجمالي</h4><h2 style='color:#FF4B4B;'>${total:,.0f}</h2></div>", unsafe_allow_html=True)
    
    # ===== 2. مخطط الأعمدة =====
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### 1. توزيع التكاليف حسب المكون")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    fig1.patch.set_facecolor('white')
    bars = ax1.bar(df["المكون"], df["التكلفة"], color=["#1e3c72", "#2a5298", "#FFD700", "#FFA500", "#FF4B4B"])
    ax1.set_ylabel("التكلفة بالدولار $", fontweight='bold')
    ax1.bar_label(bars, fmt='$%.0f', fontweight='bold')
    plt.xticks(rotation=20)
    st.pyplot(fig1)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ===== 3. مخطط دائري =====
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### 2. النسبة المئوية لكل مكون")
    fig2 = px.pie(df, values='التكلفة', names='المكون', 
                  title=f'الإجمالي الكلي: ${total:,.0f}',
                  color_discrete_sequence=["#1e3c72", "#2a5298", "#FFD700", "#FFA500", "#FF4B4B"])
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(paper_bgcolor='white', font_family="Cairo")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ===== 4. الجدول =====
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### 3. جدول تفصيلي للتكاليف")
    df_display = df.copy()
    df_display["التكلفة $"] = df_display["التكلفة"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(df_display[["المكون", "الكمية", "التكلفة $"]], 
                 use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ===== 5. التحليل المالي =====
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### 4. التحليل المالي")
    col1, col2 = st.columns(2)
    energy_year = st.session_state.get('energy_year', 8000)
    saving_yearly = energy_year * 0.15
    payback = total / saving_yearly if saving_yearly > 0 else 0
    
    with col1:
        st.metric("التكلفة الكلية", f"${total:,.0f}")
        st.metric("الانتاج السنوي", f"{energy_year:.0f} kWh")
    with col2:
        st.metric("فترة الاسترجاع", f"{payback:.1f} سنة")
        st.metric("التوفير السنوي", f"${saving_yearly:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ ارجع لصفحة المحاكي لإدخال بيانات الأحمال أولاً")
    if st.button("العودة للمحاكي"):
        st.switch_page("pages/03_⚡_المحاكي.py")

st.markdown("---")
st.caption("شركة SSE للطاقة الشمسية | المهندسة: م شهد")
