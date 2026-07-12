import streamlit as st
import plotly.graph_objects as go
from utils import check_login, logout, load_css

check_login(); logout(); load_css()

st.title("📊 لوحة المعايير الفنية IEC")
st.caption("كل المعايير المحسوب عليها النظام - متوافق مع IEC 60364 + NEC 690")

# 4 مؤشرات اساسية
c1,c2,c3,c4 = st.columns(4)
c1.metric("نسبة الفقد PR", f"{st.session_state.get('pr', 0.8)*100:.0f}%")
c2.metric("كفاءة الانفيرتر", "96%")
c3.metric("متوسط حرارة الخلية", f"{st.session_state.get('cell_temp', 45):.0f}°C")
c4.metric("معامل الأمان", "1.25")

st.divider()

col1, col2 = st.columns(2)
with col1:
    # مقياس كفاءة النظام
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", 
        value = 94.5,
        title = {'text': "كفاءة النظام الكلية %", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, 100]}, 
            'bar': {'color': "#FFD700"},
            'steps': [
                {'range': [0, 70], 'color': "rgba(255,0,0,0.3)"},
                {'range': [70, 85], 'color': "rgba(255,255,0,0.3)"},
                {'range': [85, 100], 'color': "rgba(0,255,0,0.3)"}
            ]
        }))
    fig.update_layout(height=300, margin=dict(t=50,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # تفصيل الفقد
    st.subheader("تفصيل نسب الفقد")
    losses = {
        "الغبار والاتساخ": 3,
        "الحرارة": 8,
        "الكابلات DC": 2,
        "عدم تطابق الالواح": 2,
        "الانفيرتر": 4,
        "الظل": st.session_state.get('shading_loss', 1)
    }
    total_loss = sum(losses.values())
    st.write(f"**اجمالي الفقد: {total_loss}%**")
    for k,v in losses.items():
        st.progress(100-v, text=f"{k}: {v}%")

st.divider()

# جدول المعايير
st.subheader("المعايير المستخدمة في التصميم")
st.markdown("""
| الكود | الوصف | الاستخدام في المنصة |
| --- | --- | --- |
| **IEC 60364-7-712** | التركيبات الكهربائية - انظمة PV | تصميم الكيبلات والقواطع |
| **NEC 690** | الكود الامريكي للطاقة الشمسية | حساب القواطع DC + التأريض |
| **IEC 61727** | خصائص ربط PV مع الشبكة | كفاءة الانفيرتر PR |
| **IEC 61683** | كفاءة انظمة PV | حساب كفاءة الانفيرتر 96% |
| **IEC 61215** | اختبار الالواح الشمسية | ضمان جودة الالواح 25 سنة |
""")

st.info("💡 كل هذه المعايير مطبقة تلقائيا في حاسبة الاحمال والمحاكي")

# زر التنقل
if st.button("التالي: المتجر 🛒", type="primary", use_container_width=True): 
    st.switch_page("pages/06_🛒_السلة_والمتجر.py")
