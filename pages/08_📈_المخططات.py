import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from utils import check_login, logout, load_css

check_login(); logout(); load_css()

st.title("📈 المخطات والتحليلات")
st.caption("تحليل التكاليف والانتاج الشهري للنظام")

# ===== CSS =====
st.markdown("""
<style>
.metric-card { background: #112240; padding: 20px; border-radius: 15px; 
               border-left: 5px solid #64ffda; }
.chart-card { background: #112240; padding: 25px; border-radius: 15px; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

if 'num_panels' in st.session_state and 'total_kwh' in st.session_state:
    st.success("✅ تم تحميل بيانات النظام بنجاح")
    
    tab1, tab2 = st.tabs(["💰 تحليل التكاليف", "⚡ تحليل الانتاج"])

    # ===== TAB 1: التكاليف =====
    with tab1:
        # Sidebar الاسعار
        with st.sidebar:
            st.header("⚙️ تعديل الاسعار $")
            price_panel = st.number_input("سعر اللوح 550W", value=85, min_value=50, key="p1")
            price_battery = st.number_input("سعر البطارية 100Ah", value=280, min_value=100, key="p2")
            price_inverter = st.number_input("سعر الانفرتر للكيلو", value=450, min_value=200, key="p3")
            price_cable = st.number_input("سعر الكيبل للوح", value=12, min_value=5, key="p4")
            price_install = st.number_input("سعر التركيب للوح", value=15, min_value=10, key="p5")
        
        # حساب التكاليف
        num_batt = st.session_state.get('battery_ah', 400) / 100
        cost_panels = st.session_state.num_panels * price_panel
        cost_batteries = num_batt * price_battery
        cost_inverter = st.session_state.inverter_kw * price_inverter
        cost_cables = st.session_state.num_panels * price_cable
        cost_installation = st.session_state.num_panels * price_install
        total = cost_panels + cost_batteries + cost_inverter + cost_cables + cost_installation
        
        data = {
            "المكون": ["الألواح الشمسية", "البطاريات", "الانفرتر", "الكيبل والحمايات", "التركيب"],
            "التكلفة": [cost_panels, cost_batteries, cost_inverter, cost_cables, cost_installation],
            "الكمية": [
                f"{st.session_state.num_panels} لوح",
                f"{int(num_batt)} بطارية",
                f"{st.session_state.inverter_kw} kW",
                f"{st.session_state.num_panels} طقم",
                "شامل"
            ]
        }
        df = pd.DataFrame(data)
        
        # كروت الملخص
        st.subheader("الملخص السريع")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"<div class='metric-card'><h4>عدد الألواح</h4><h2>{st.session_state.num_panels}</h2></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='metric-card'><h4>البطاريات</h4><h2>{int(num_batt)}</h2></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='metric-card'><h4>الانفرتر</h4><h2>{st.session_state.inverter_kw} kW</h2></div>", unsafe_allow_html=True)
        with col4: st.markdown(f"<div class='metric-card'><h4>الإجمالي</h4><h2 style='color:#64ffda;'>${total:,.0f}</h2></div>", unsafe_allow_html=True)
        
        # مخط الأعمدة
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("توزيع التكاليف حسب المكون")
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        fig1.patch.set_facecolor('#112240')
        ax1.set_facecolor('#112240')
        bars = ax1.bar(df["المكون"], df["التكلفة"], color=["#64ffda", "#4CAF50", "#FFD700", "#FFA500", "#FF4B4B"])
        ax1.set_ylabel("التكلفة بالدولار $", color='white')
        ax1.tick_params(colors='white')
        ax1.bar_label(bars, fmt='$%.0f', color='white', fontweight='bold')
        plt.xticks(rotation=20, color='white')
        st.pyplot(fig1)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # مخط دائري
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("النسبة المئوية لكل مكون")
        fig2 = px.pie(df, values='التكلفة', names='المكون', 
                      title=f'الإجمالي الكلي: ${total:,.0f}',
                      color_discrete_sequence=["#64ffda", "#4CAF50", "#FFD700", "#FFA500", "#FF4B4B"])
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(paper_bgcolor='#112240', font_color='white', template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ===== TAB 2: الانتاج =====
    with tab2:
        st.subheader("توقع الانتاج الشهري")
        months = ['يناير','فبراير','مارس','ابريل','مايو','يونيو','يوليو','اغسطس','سبتمبر','اكتوبر','نوفمبر','ديسمبر']
        # محاكاة: الصيف اعلى والشتاء اقل. معامل 1.2 للصيف و 0.8 للشتاء
        base = st.session_state.total_kwh * 30
        production = [base * (0.8 + 0.4*abs(6-i)/6) for i in range(12)]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=months, y=production, name="الانتاج kWh", marker_color='#64ffda'))
        fig3.update_layout(template="plotly_dark", title="الانتاج الشهري المتوقع", paper_bgcolor='#112240', plot_bgcolor='#112240')
        st.plotly_chart(fig3, use_container_width=True)

        c1,c2,c3 = st.columns(3)
        c1.metric("اجمالي الانتاج السنوي", f"{sum(production):,.0f} kWh")
        c2.metric("متوسط شهري", f"{sum(production)/12:.0f} kWh")
        c3.metric("متوسط يومي", f"{sum(production)/365:.1f} kWh")

        # التحليل المالي
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("التحليل المالي")
        energy_year = sum(production)
        saving_yearly = energy_year * 0.15 # نفترض سعر الكيلو 0.15$
        payback = total / saving_yearly if saving_yearly > 0 else 0
        col1, col2 = st.columns(2)
        with col1: st.metric("التوفير السنوي", f"${saving_yearly:,.0f}")
        with col2: st.metric("فترة الاسترجاع", f"{payback:.1f} سنة")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ ارجع لصفحة الحاسبة لإدخال بيانات الأحمال أولاً")
    if st.button("العودة للحاسبة", type="primary"):
        st.switch_page("pages/02_📊_الأحمال.py")
