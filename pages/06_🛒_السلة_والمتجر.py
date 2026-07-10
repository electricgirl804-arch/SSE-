import streamlit as st, pandas as pd
from utils import check_login, load_css
from database import save_to_sheet
from config import CURRENCY
check_login(); load_css()
st.title("🛒 المتجر الرسمي - SSE Store")
st.caption("اسعار جملة + ضمان 10 سنوات")

if 'cart' not in st.session_state: st.session_state.cart = []

products = {
    "لوح Jinko 550W Mono PERC": {"price": 280000, "warranty": "25 سنة"},
    "بطارية LiFePO4 200Ah 48V": {"price": 1850000, "warranty": "10 سنوات"},
    "انفيرتر Growatt 5KW": {"price": 1250000, "warranty": "5 سنوات"},
    "هيكل مجلفن 10 الواح": {"price": 400000, "warranty": "10 سنوات"},
    "كيبل PV 4mm PV1-F": {"price": 3500, "warranty": "25 سنة"}
}

for p, data in products.items():
    c1,c2,c3 = st.columns([3,1,1])
    c1.write(f"**{p}** | الضمان: {data['warranty']}")
    c2.metric("السعر", f"{data['price']:,} {CURRENCY}")
    if c3.button("اضافة", key=p): st.session_state.cart.append({"المنتج":p, "السعر":data['price']})

if st.session_state.cart:
    df = pd.DataFrame(st.session_state.cart)
    st.dataframe(df, use_container_width=True)
    total = df["السعر"].sum()
    st.metric("اجمالي الفاتورة", f"{total:,} {CURRENCY}")
    name = st.text_input("اسم العميل للفاتورة")
    if st.button("📧 ارسال الطلب", type="primary"):
        save_to_sheet({"العميل":name, "الاجمالي":total, "عدد_الاصناف":len(df)}, "Order")
        st.success("✅ تم ارسال الطلب. ح نتواصل معاك خلال ساعة")
if st.button("التالي"): st.switch_page("pages/07_📄_التقرير_والعقد.py")
