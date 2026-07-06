import streamlit as st
import qrcode
from PIL import Image
import io

st.title("ℹ️ عن منصة SSE الذكية")

st.image("logo.png", width=250)

st.markdown("""
### من نحن
منصة SSE الذكية هي أول منصة عربية متكاملة لحسابات الطاقة الشمسية وفق المعايير العالمية IEC
""")

st.divider()
st.header("الدعم الفني والتواصل")

email = "electricgirl804@gmail.com"
phone = "0110560222"

col1, col2 = st.columns(2)

def create_qr_with_logo(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    logo = Image.open("logo.png")
    logo_size = 50
    logo = logo.resize((logo_size, logo_size))

    pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
    qr_img.paste(logo, pos)
    return qr_img

with col1:
    st.subheader("📧 البريد الإلكتروني")
    st.code(email)
    qr_email = create_qr_with_logo(f"mailto:{email}")
    buf = io.BytesIO()
    qr_email.save(buf, format="PNG")
    st.image(buf, caption="امسح الكود لإرسال إيميل", width=180)

with col2:
    st.subheader("📱 واتساب / اتصال")
    st.code(phone)
    qr_phone = create_qr_with_logo(f"tel:{phone}")
    buf2 = io.BytesIO()
    qr_phone.save(buf2, format="PNG")
    st.image(buf2, caption="امسح الكود للاتصال", width=180)

st.success("شكراً لاستخدام منصة SSE الذكية")
