import streamlit as st
import qrcode
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="SSE - المهندس الأمين", layout="centered")

# 2. الهوية البصرية (ضعي رابط شعارك هنا)
st.image("https://i.imgur.com/your_logo_here.png", width=150)
st.title("🛡️ SSE - المهندس الرقمي المتكامل")

# 3. قاعدة بيانات الأجهزة
devices = {
    "مصباح (20W)": 20, "مروحة (80W)": 80, 
    "تلفاز (100W)": 100, "ثلاجة (150W)": 150
}

# 4. الترحيب والأفاتار
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "أهلاً بكِ يا بشمهندسة! أنا مساعدكِ الرقمي الموثوق. كيف يمكنني مساعدتكِ في حساب أحمالكِ اليوم؟"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# 5. التفاعل الهندسي
selected = st.multiselect("اختاري الأجهزة:", list(devices.keys()))
dist = st.number_input("المسافة (متر):", min_value=1, value=10)

if st.button("تحليل المنظومة"):
    if selected:
        total = sum([devices[d] for d in selected])
        current = total / 220
        breaker = current * 1.25
        batt_ah = ((total * 6) / 0.2) / 12
        cable = (current * dist * 0.0175) / (220 * 0.03)
        
        report = f"""
        ### 📊 نتائج التصميم الهندسي:
        - **الحمل الكلي:** {total} وات
        - **القاطع المناسب:** {breaker:.1f} أمبير
        - **البطارية:** {int(batt_ah)} أمبير/ساعة
        - **مقطع السلك:** {cable:.2f} مم²
        """
        
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(report)
            st.session_state.messages.append({"role": "assistant", "content": report})
            
            # ذكاء تفاعلي: نصيحة إضافية
            if total > 500:
                st.warning("💡 **نصيحة المهندس:** حملكِ مرتفع، هل تريدين حساب تكلفة التبريد؟")
    else:
        st.warning("يرجى اختيار جهاز واحد على الأقل.")

# 6. التوثيق الشخصي
st.sidebar.subheader("للتواصل والتوثيق")
st.sidebar.write("📧 electricgirl804@gmail.com")
qr = qrcode.make("Verified SSE - Contact: electricgirl804@gmail.com")
buffer = BytesIO()
qr.save(buffer, format="PNG")
st.sidebar.image(buffer.getvalue(), caption="باركود التحقق")
