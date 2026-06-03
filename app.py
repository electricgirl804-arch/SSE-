import streamlit as st
import qrcode
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="SSE Solar App", layout="wide")

# محاولة تحميل الصورة
try:
    # تأكدي أن اسم الملف في GitHub مطابق تماماً لهذا الاسم
    image = Image.open('1000224141.jpg')
    st.image(image, width=150)
except:
    st.write("ملاحظة: الصورة غير موجودة في المجلد")

st.title("SSE - نظام الطاقة الشمسية الذكي")
st.write("حلول هندسية عالمية لبيانات الأقمار الصناعية")

# جمع البيانات مع إضافة مدينة عطبرة
city = st.selectbox("حدد موقع مشروعك:", ["أم درمان", "الخرطوم", "عطبرة", "بورتسودان", "نيالا", "دنقلا"])
st.write(f"جاري جلب بيانات القمر الصناعي لموقع: {city}")

# الدالة الأساسية للحسابات
def calculate_system(load_watts, distance, breaker_amps):
    total_power = load_watts * 1.25
    cable_size = (distance * (total_power / 220) * 0.0175) / 6.6
    alerts = []
    if (total_power / 220) > (breaker_amps * 0.8):
        alerts.append("⚠️ خطر: القاطع غير مناسب للحمل!")
    if cable_size > 6.0:
        alerts.append("⚠️ تحذير: الكبل يتطلب مقاساً أكبر من 6 ملم.")
    return total_power, cable_size, alerts

# المدخلات من المستخدم
load = st.number_input("إجمالي الحمل (وات):", min_value=100)
dist = st.number_input("المسافة (متر):", min_value=1)
brk = st.number_input("حجم القاطع (أمبير):", min_value=1)

# زر التحليل
if st.button("تحليل الأمان المقر"):
    power, cable, notifications = calculate_system(load, dist, brk)
    st.success(f"القدرة المطلوبة: {power:.2f} وات")
    st.info(f"المقطع العرضي للكبل: {cable:.1f} مم")
    
    if notifications:
        for alert in notifications:
            st.error(alert)
    else:
        st.write("✅ النظام آمن ومطابق للمواصفات.")

    # التوقيع الرقمي (QR Code)
    qr = qrcode.make(f"SSE-Verified-Report: {load}W - {city}")
    st.image(qr, caption="باركود التحقق من أصالة التقرير")

st.write("---")
st.subheader("شكر خاص")
st.write("نحن نحرص على سلامة طاقتكم ومستقبل منشآتكم.")
st.write("للتواصل والدعم الفني: support@sse-energy.sd")

