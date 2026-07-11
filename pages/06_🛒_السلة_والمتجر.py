import streamlit as st
from utils import check_login, logout, load_css
from database import load_products, save_to_sheet, load_suppliers
check_login(); logout(); load_css()

st.set_page_config(page_title="المتجر - SSE", layout="wide")
st.title("🛒 المتجر الذكي SSE")
st.caption("جميع مستلزمات الطاقة الشمسية - بيع + تأجير")

# ===== 1. اختيار طريقة الشراء والدولة =====
col1, col2 = st.columns(2)
with col1:
    mode = st.radio("طريقة الشراء:", ["شراء كاش", "تأجير 3 سنوات"], horizontal=True)
with col2:
    country = st.selectbox("🌍 الدولة", ["SA", "EG", "SD", "UAE", "USD"])
currency = {"SA":"ريال","EG":"جنيه","SD":"جنيه","UAE":"درهم","USD":"$"}[country]

if 'cart' not in st.session_state: st.session_state.cart = []
p = load_products()
st.session_state.supplier_products = load_suppliers()

# ===== 2. عرض المنتجات كلها =====
st.subheader("☀️ المنتجات")
tabs = st.tabs(["☀️ الواح", "⚡ انفرترات", "🔋 بطاريات", "🔌 كيبلات", "🛡️ حمايات", "🏭 موردين"])

with tabs[0]: # الواح
    for prod in p['panels']:
        price = prod[f'price_{country}']
        c1, c2, c3, c4 = st.columns([3,1,1,1])
        c1.write(f"**{prod['brand']}** - {prod['watt']}W")
        c2.write(f"المخزون: {prod['stock']}")
        c3.metric("السعر", f"{price} {currency}")
        if c4.button("➕ اضافة", key=f"panel_{prod['brand']}"):
            # لو المنتج موجود زيد الكمية
            found = False
            for item in st.session_state.cart:
                if item['name'] == prod['brand']:
                    item['qty'] += 1
                    found = True
            if not found:
                st.session_state.cart.append({"name": prod['brand'], "price": price, "qty": 1, "seller": "SSE"})
            st.rerun()

with tabs[1]: # انفرترات
    for prod in p['inverters']:
        price = prod[f'price_{country}']
        c1, c2, c3, c4 = st.columns([3,1,1,1])
        c1.write(f"**{prod['brand']}** - {prod['kw']}KW")
        c2.write(f"المخزون: {prod['stock']}")
        c3.metric("السعر", f"{price} {currency}")
        if c4.button("➕ اضافة", key=f"inv_{prod['brand']}"):
            found = False
            for item in st.session_state.cart:
                if item['name'] == prod['brand']: item['qty'] += 1; found = True
            if not found: st.session_state.cart.append({"name": prod['brand'], "price": price, "qty": 1, "seller": "SSE"})
            st.rerun()

with tabs[2]: # بطاريات
    for prod in p['batteries']:
        price = prod[f'price_{country}']
        c1, c2, c3, c4 = st.columns([3,1,1,1])
        c1.write(f"**{prod['brand']}** - {prod['ah']}AH")
        c2.write(f"المخزون: {prod['stock']}")
        c3.metric("السعر", f"{price} {currency}")
        if c4.button("➕ اضافة", key=f"bat_{prod['brand']}"):
            found = False
            for item in st.session_state.cart:
                if item['name'] == prod['brand']: item['qty'] += 1; found = True
            if not found: st.session_state.cart.append({"name": prod['brand'], "price": price, "qty": 1, "seller": "SSE"})
            st.rerun()

with tabs[3]: # كيبلات
    cables = [{"name": "كيبل 4mm", "price_USD": 1.5}, {"name": "كيبل 6mm", "price_USD": 2.2}, {"name": "كيبل 10mm", "price_USD": 3.5}]
    for prod in cables:
        price = prod['price_USD'] * {"SA":3.75,"EG":50,"SD":600,"UAE":3.67,"USD":1}[country]
        c1, c2, c3 = st.columns([3,1,1])
        c1.write(f"**{prod['name']}** - للمتر")
        c2.metric("السعر", f"{price:.2f} {currency}")
        if c3.button("➕ اضافة", key=f"cab_{prod['name']}"):
            found = False
            for item in st.session_state.cart:
                if item['name'] == prod['name']: item['qty'] += 1; found = True
            if not found: st.session_state.cart.append({"name": prod['name'], "price": price, "qty": 1, "seller": "SSE"})
            st.rerun()

with tabs[4]: # حمايات
    protections = [{"name": "قاطع DC 32A"}, {"name": "مانع صواعق"}, {"name": "صندوق تجميع"}]
    for prod in protections:
        price = 20 * {"SA":3.75,"EG":50,"SD":600,"UAE":3.67,"USD":1}[country]
        c1, c2, c3 = st.columns([3,1,1])
        c1.write(f"**{prod['name']}**")
        c2.metric("السعر", f"{price:.2f} {currency}")
        if c3.button("➕ اضافة", key=f"pro_{prod['name']}"):
            found = False
            for item in st.session_state.cart:
                if item['name'] == prod['name']: item['qty'] += 1; found = True
            if not found: st.session_state.cart.append({"name": prod['name'], "price": price, "qty": 1, "seller": "SSE"})
            st.rerun()

with tabs[5]: # موردين
    with st.expander("➕ سجل كمورد وارفع منتجاتك"):
        new_brand = st.text_input("اسم المنتج")
        new_price = st.number_input("السعر بالدولار $", 0.0)
        if st.button("رفع المنتج"):
            save_to_sheet({"brand": new_brand, "price": new_price, "status": "معلق"}, "suppliers")
            st.success("تم استلام طلبك. سيتم مراجعته خلال 24 ساعة")
            st.rerun()

    for prod in st.session_state.supplier_products:
        if prod['status'] == "مفعل":
            price = prod['price'] * {"SA":3.75,"EG":50,"SD":600,"UAE":3.67,"USD":1}[country]
            c1, c2, c3 = st.columns([3,1,1])
            c1.write(f"**{prod['brand']}** - مورد معتمد")
            c2.metric("السعر", f"{price:.2f} {currency}")
            if c3.button("➕ اضافة", key=f"sup_{prod['brand']}"):
                found = False
                for item in st.session_state.cart:
                    if item['name'] == prod['brand']: item['qty'] += 1; found = True
                if not found: st.session_state.cart.append({"name": prod['brand'], "price": price, "qty": 1, "seller": "مورد"})
                st.rerun()

st.divider()

# ===== 3. السلة مع اختيار وحذف =====
st.subheader("🧺 سلة المشتريات")
if st.session_state.cart:
    total = 0
    for i, item in enumerate(st.session_state.cart):
        c1, c2, c3, c4 = st.columns([3,1,1,1])
        c1.write(f"**{item['name']}** - {item['seller']}")
        item['qty'] = c2.number_input("الكمية", 1, 100, item['qty'], key=f"qty_{i}")
        item_total = item['price'] * item['qty']
        c3.write(f"{item_total:.2f} {currency}")
        if c4.button("🗑️", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()
        total += item_total

    if mode == "شراء كاش":
        tax = total * p['tax'][country]
        shipping = p['shipping'][country]
        grand_total = total + tax + shipping
        st.metric("الاجمالي شامل الضريبة والشحن", f"{grand_total:.2f} {currency}")
    else:
        profit = total * 0.25
        grand_total = total + profit
        monthly = grand_total / 36
        st.metric("القسط الشهري", f"{monthly:.2f} {currency}")
        st.metric("الاجمالي بعد 36 شهر", f"{grand_total:.2f} {currency}")
        st.info("تنتقل ملكية المنظومة للعميل بعد سداد 36 قسط")

    name = st.text_input("الاسم الكامل")
    phone = st.text_input("رقم الواتساب")

    if st.button("✅ تأكيد الطلب", type="primary"):
        save_to_sheet({"name":name, "phone":phone, "items":str(st.session_state.cart), "total":grand_total, "mode":mode}, "orders")
        st.success("✅ تم استلام طلبك بنجاح")
        st.markdown(f"""
        <div style='background: #FFD700; padding: 20px; border-radius: 15px; color: #0A3D62;'>
        <h3>📱 خطوات الدفع</h3>
        <p>1. حول المبلغ: <b>{grand_total:.2f} {currency}</b></p>
        <p>2. على الرقم: <b>0110560222</b></p>
        <p>3. ارسل اشعار التحويل على واتساب</p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.cart = []
else:
    st.info("السلة فارغة. اضف منتجات للمتابعة")
