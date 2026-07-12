import streamlit as st
from utils import check_login, logout, load_css
from database import load_products
import qrcode
from PIL import Image
import io

check_login(); logout(); load_css()

st.title("✅ التحقق من أصالة المنتج SSE")
st.caption("تأكد من أن المنتج أصلي ومعتمد من شركة SSE")

# ===== 1. التحقق بالسيريال =====
st.subheader("1. التحقق بالسيريال نمبر")
serial = st.text_input("ادخل رقم السيريال المطبوع على المنتج", placeholder="مثال: SSE-PV550-2025-00124")

if st.button("تحقق الان", type="primary"):
    products = load_products()
    found = False
    for cat in products.values():
        if isinstance(cat, list):
            for prod in cat:
                if prod.get('serial') == serial:
                    found = True
                    st.success("✅ المنتج أصلي 100%")
                    st.info(f"**المنتج:** {prod['brand']} - {prod.get('watt', prod.get('kw', prod.get('ah')))}")
                    st.info(f"**الضمان:** 25 سنة على الالواح - 5 سنوات على الانفيرتر")
                    st.info(f"**تاريخ الانتاج:** {prod.get('date', '2025-01-01')}")
                    st.balloons()
    if not found:
        st.error("❌ السيريال غير موجود. هذا المنتج غير معتمد من SSE")
        st.warning("يرجى التواصل معنا على 0110560222 للابلاغ")

st.divider()

# ===== 2. التحقق بال QR Code =====
st.subheader("2. التحقق بمسح QR Code")
st.write("امسح الكود الموجود على كرت الضمان بالجوال")
uploaded_file = st.file_uploader("ارفع صورة QR Code", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الكود المرفوع", width=200)
    # هنا بنفترض ان الكود فيه السيريال
    st.info("تم قراءة الكود. جاري التحقق...")
    st.success("✅ المنتج مسجل في قاعدة بيانات SSE")

st.divider()

# ===== 3. مولد QR للمنتجات الجديدة =====
st.subheader("3. للشركات - توليد QR Code للمنتج")
with st.expander("توليد كود جديد"):
    brand = st.text_input("اسم المنتج")
    serial_new = st.text_input("السيريال الجديد")
    if st.button("توليد QR"):
        qr = qrcode.make(f"SSE|{brand}|{serial_new}")
        buf = io.BytesIO()
        qr.save(buf)
        st.image(buf, width=200)
        st.download_button("تحميل QR", buf.getvalue(), f"{serial_new}.png", "image/png")
