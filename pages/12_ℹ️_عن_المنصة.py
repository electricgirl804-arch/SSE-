import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="SSE - عن المنصة", page_icon="ℹ️", layout="wide")
st.title("ℹ️ عن Smart Solar Engineering")
st.caption("Smart Solar Engineering | SSE v1.2")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        img = Image.open("logo.png").convert("RGBA")
        txt = Image.new('RGBA', img.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        draw.rectangle([50, 120, 350, 160], fill="white")
        draw.text((70, 125), "Smart Solar Engineering", fill="#1E3A8A", font=font)
        combined = Image.alpha_composite(img, txt)
        st.image(combined, width=280)
    except:
        st.error("ارفعي logo.png في فولدر المشروع")

st.markdown("---")
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("عن SSE")
    st.markdown("**Smart Solar Engineering** منصة سودانية لتصميم أنظمة الطاقة الشمسية")
    st.success("الإيميل: electricgirl804@gmail.com")
    st.success("الواتساب: 0110560222")
    st.info("المطور: المهندسة شهد")
    st.caption("الإصدار: v1.2 - أبريل 2026")

with col2:
    st.subheader("📱 تواصل واتساب")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data("https://wa.me/249110560222")
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="#FF8C00", back_color="white")
    buf = io.BytesIO()
    img_qr.save(buf, format='PNG')
    st.image(buf.getvalue(), width=200)
    st.caption("امسحي الباركود")
