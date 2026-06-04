import streamlit as st
import qrcode
from io import BytesIO
from streamlit_webrtc import webrtc_streamer

# 1. إعدادات الصفحة
st.set_page_config(page_title="SSE - المهندس الرقمي", layout="centered")

# 2. التنسيق الحركي والخلفية (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%); }
    .footer { text-align: center; margin-top: 50px; padding: 20px; font-size: 0.9em; color: #333; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .main-container { animation: fadeIn 1.5s; }
    </style>
    <div class="main-container">
    """, unsafe_allow_html=True)

# 3. الترحيب بالأفاتار
st.title("🛡️ المهندس الرقمي المتكامل (SSE)")
col1, col2 = st.columns([1, 3])
with col1:
    st.image("1000224141.jpg", width=100)
with col2:
    st.markdown("### 👩‍💻 أهلاً بك في عالم الطاقة الذكية!")
    st.write("أنا مساعدك الرقمي من **SSE**. سأرافقك لتصميم منظومتك وحمايتها.")

# 4. اختيار المدينة والأجهزة
cities = ["الدامر", "عطبرة", "شندي", "بربر", "مروي", "بورتسودان", "الخرطوم"]
selected_city = st.selectbox("اختر مدينتك (لتخصيص الأداء حسب المناخ):", cities)

devices = {
    "إضاءة LED (10W)": 10, "ثلاجة (150W)": 150, "غسالة (500W)": 500,
    "موتور مياه (750W)": 750, "مكيف 18 ألف (2200W)": 2200, "هيتر (2000W)": 2000
}
selected = st.multiselect("اختاري الأجهزة:", list(devices.keys()))

# 5. تحليل المنظومة مع نظام الإنذار
if st.button("تحليل المنظومة 🚀"):
    if selected:
        total = sum([devices[d] for d in selected])
        st.write(f"📊 إجمالي الحمل: {total} وات")
        
        # نظام الإنذار الهندسي
        if total > 4000:
            st.error("🚨 إنذار أحمر: حمل خطر جداً! قد يؤدي لتلف المنظومة، يرجى التواصل معي فوراً.")
        elif total > 2000:
            st.warning("⚠️ تحذير: حمل مرتفع، تأكدي من جودة الأسلاك والتهوية.")
        else:
            st.success("✅ منظومة آمنة ومستقرة.")
    else:
        st.warning("يرجى اختيار جهاز واحد على الأقل.")

# 6. قسم الكاميرا (التحقق)
st.divider()
st.subheader("📸 كاشف المنتجات الأصلية")
webrtc_streamer(key="product-check")

# 7. التذييل
st.markdown("<div class='footer'>🛡️ SSE - المهندس الرقمي المتكامل | جميع الحقوق محفوظة</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

