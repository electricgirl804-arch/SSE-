import streamlit as st, sqlite3, requests, math, datetime, json
import streamlit.components.v1 as components
import google.generativeai as genai

st.set_page_config(page_title="الأعطال 06", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# === دا البقفل زر الصفحات ويظبط اليمين ===
st.markdown("""
<style>
    /* 1. نقفل الشريط الجانبي وزر ≡ نهائي */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}

    /* 2. نخلي كل شي يمين عشان العربي */
    html, body,.main {
        direction: rtl;
        text-align: right;
    }

    /* 3. نظبط التابات ما تتداخل في الجوال */
   .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        overflow-x: auto;
        justify-content: flex-start;
    }
   .stTabs [data-baseweb="tab"] {
        flex-shrink: 0;
    }

    /* 4. نظبط العنوان */
    h1 {
        text-align: center!important;
        color: #FFD700!important;
        font-size: 28px!important;
    }
</style>
""", unsafe_allow_html=True)

# === 1. نقرا ملف products.json ===
@st.cache_data
def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)

products_json = load_products()

# === 2. كلمة السرية ===
ADMIN_SECRET = "shahd8499"

# === 3. ربط الذكاء الاصطناعي بدون ما يوقع ===
AI_ENABLED = False
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    AI_ENABLED = True
except:
    pass

# === 4. قاعدة البيانات ===
conn = sqlite3.connect('shahd_alatal06.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, code TEXT, name TEXT, phone TEXT, size REAL, cost REAL, monthly REAL, status TEXT, date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY, code TEXT, name TEXT, phone TEXT, items TEXT, total REAL, status TEXT, date TEXT)''')
conn.commit()

# === 5. شاشة الدخول ===
if 'role' not in st.session_state: st.session_state.role = None

if st.session_state.role == None:
    st.markdown("<h1>⚡ الأعطال 06 | المهندسة شهد</h1>", unsafe_allow_html=True)
    role = st.radio("اختار نوع الدخول", ["ادمن", "مهندس"], horizontal=True)

    if role == "ادمن":
        password = st.text_input("دخل كلمة سر الادمن", type="password")
        if st.button("دخول", use_container_width=True):
            if password == ADMIN_SECRET:
                st.session_state.role = "ادمن"; st.rerun()
            else:
                st.error("❌ كلمة السر غلط")

    if role == "مهندس":
        if st.button("دخول كمهندس", use_container_width=True):
            st.session_state.role = "مهندس"; st.rerun()
    st.stop()

st.sidebar.success(f"مرحبا: {st.session_state.role}")
if st.sidebar.button("تسجيل خروج"): st.session_state.role = None; st.rerun()

# === 6. البوت الذكي ===
if AI_ENABLED:
    prod_list = [f"{p['brand']} {p['watt']}W: ${p['price']}" for p in products_json["panels"]]
    context = "\n".join(prod_list)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=f"انت بوت المهندسة شهد. رد بالسوداني. اسعارنا: {context}")
else:
    model = None
    st.sidebar.warning("⚠️ البوت معطل. اضف GOOGLE_API_KEY في Secrets")

# === 7. لوحة المهندس ===
if st.session_state.role == "مهندس":
    tab1, tab2, tab3 = st.tabs(["💬 البوت الذكي", "⚡ حاسبة الطاقة", "🛒 المتجر"])

    with tab1:
        st.subheader("اسأل بوت الأعطال 06")
        if not AI_ENABLED:
            st.error("البوت ما شغال لانو مافي مفتاح Google AI")
        else:
            if "chat" not in st.session_state: st.session_state.chat = []
            for m in st.session_state.chat: st.chat_message(m["role"]).write(m["content"])
            if q := st.chat_input("مثلا: داير اشغل 2 مكيف"):
                st.session_state.chat.append({"role":"user","content":q}); st.chat_message("user").write(q)
                r = model.generate_content(q).text; st.session_state.chat.append({"role":"assistant","content":r}); st.chat_message("assistant").write(r)

    with tab2:
        st.subheader("1. جيب بيانات الشمس")
        if st.button("📡 جيب موقعي تلقائي"):
            components.html("<script>navigator.geolocation.getCurrentPosition(p=>window.parent.postMessage({type:'streamlit:setComponentValue',key:'gps',value:[p.coords.latitude,p.coords.longitude]},'*'))</script>",height=0)
        gps = st.session_state.get("gps", [15.5007, 32.5599])
        lat = st.number_input("خط العرض", value=float(gps[0])); lon = st.number_input("خط الطول", value=float(gps[1]))

        try:
            url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start=20221231&end=20221231&latitude={lat}&longitude={lon}&parameters=ALLSKY_SFC_SW_DWN&format=JSON"
            ghi = requests.get(url, timeout=10).json()["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["20221231"]
            st.metric("☀️ متوسط الاشعاع", f"{ghi:.2f} kWh/m²")
        except:
            ghi = 5.5; st.warning("ماقدرت اجيب بيانات ناسا. استخدمت 5.5")

        st.subheader("2. احسب منظومتك")
        load = st.number_input("الحمل بالكيلو واط KW", 2.0)
        hours = st.number_input("عدد ساعات التشغيل", 8)

        panels = math.ceil((load*hours) / (ghi * 0.55 * 0.85))
        size = panels * 0.55
        cost = size * 1000
        monthly = (cost*1.2)/36

        st.metric("عدد الالواح 550W", panels)
        st.metric("التكلفة الكلية", f"${cost:.0f}")
        st.metric("القسط الشهري", f"${monthly:.2f}")

    with tab3:
        st.markdown("""
        <style>
  .product-card {background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 4px solid #FFD700; margin-bottom: 20px; height: 380px; display: flex; flex-direction: column; justify-content: space-between;}
  .product-title {color: #1e3c72; font-weight: 800; font-size: 18px; margin-bottom: 10px;}
  .product-price {color: #FF8C00; font-weight: 700; font-size: 22px;}
  .stButton>button {background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; border-radius: 10px; font-weight: 700; border: none; width: 100%;}
        </style>
        """, unsafe_allow_html=True)

        st.subheader("🛒 اختار المكونات")
        if "cart" not in st.session_state: st.session_state.cart = []
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown("<div class='product-title'>☀️ الألواح الشمسية</div>", unsafe_allow_html=True)
            panel_options = [f"{p['brand']} {p['watt']}W" for p in products_json["panels"]]
            selected_panel = st.selectbox("اختار", panel_options, key="panel", label_visibility="collapsed")
            panel_data = products_json["panels"][panel_options.index(selected_panel)]
            st.markdown(f"<div class='product-price'>${panel_data['price']}</div>", unsafe_allow_html=True)
            if st.button("➕ اضافة للسلة", key="add_panel"):
                st.session_state.cart.append({"item": selected_panel, "price": panel_data['price'], "type": "لوح", "qty": 1})
                st.toast(f"تمت اضافة {selected_panel} للسلة ✅")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown("<div class='product-title'>⚡ الانفيرتر</div>", unsafe_allow_html=True)
            inv_options = [f"{i['brand']} {i['kw']}KW" for i in products_json["inverters"]]
            selected_inv = st.selectbox("اختار", inv_options, key="inv", label_visibility="collapsed")
            inv_data = products_json["inverters"][inv_options.index(selected_inv)]
            st.markdown(f"<div class='product-price'>${inv_data['price']}</div>", unsafe_allow_html=True)
            if st.button("➕ اضافة للسلة", key="add_inv"):
                st.session_state.cart.append({"item": selected_inv, "price": inv_data['price'], "type": "انفيرتر", "qty": 1})
                st.toast(f"تمت اضافة {selected_inv} للسلة ✅")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown("<div class='product-title'>🔋 البطاريات</div>", unsafe_allow_html=True)
            bat_options = [f"{b['brand']} {b['ah']}Ah" for b in products_json["batteries"]]
            selected_bat = st.selectbox("اختار", bat_options, key="bat", label_visibility="collapsed")
            bat_data = products_json["batteries"][bat_options.index(selected_bat)]
            st.markdown(f"<div class='product-price'>${bat_data['price']}</div>", unsafe_allow_html=True)
            if st.button("➕ اضافة للسلة", key="add_bat"):
                st.session_state.cart.append({"item": selected_bat, "price": bat_data['price'], "type": "بطارية", "qty": 1})
                st.toast(f"تمت اضافة {selected_bat} للسلة ✅")
            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.cart:
            st.subheader("🛍️ سلة المشتريات")
            total_cart = 0
            for i, item in enumerate(st.session_state.cart):
                with st.container(border=True):
                    col_a, col_b, col_c, col_d = st.columns([3,1,1,1])
                    col_a.markdown(f"**{item['type']}**<br>{item['item']}", unsafe_allow_html=True)
                    col_b.markdown(f"<h3 style='color:#FF8C00'>${item['price']}</h3>", unsafe_allow_html=True)
                    qty = col_c.number_input("الكمية", min_value=1, value=item.get('qty', 1), key=f"qty{i}", label_visibility="collapsed")
                    st.session_state.cart[i]['qty'] = qty
                    if col_d.button("🗑️", key=f"del{i}", use_container_width=True):
                        st.session_state.cart.pop(i); st.rerun()
                    total_cart += item['price'] * qty
            st.markdown("---")
            st.success(f"**الاجمالي الكلي: {total_cart}$**")
            with st.form("order_form"):
                name = st.text_input("اسمك")
                phone = st.text_input("رقم تلفونك")
                if st.form_submit_button("📤 ارسال الطلب للادمن", use_container_width=True):
                    if name and phone:
                        code = f"SSE{datetime.date.today().year}{c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]+1}"
                        items_str = ", ".join([f"{x['qty']}x {x['type']}: {x['item']}" for x in st.session_state.cart])
                        c.execute("INSERT INTO orders VALUES (NULL,?,?,?,?,?,?,?)", (code, name, phone, items_str, total_cart, "pending", str(datetime.date.today())))
                        conn.commit()
                        st.success(f"✅ تم ارسال الطلب رقم {code} للادمن")
                        st.session_state.cart = []; st.rerun()
                    else: st.error("دخل الاسم والتلفون")
        else:
            st.info("السلة فاضية. اضف منتجات من فوق 👆")

# === 8. لوحة الادمن ===
else:
    st.header("👑 لوحة تحكم الادمن")
    orders = c.execute("SELECT * FROM orders WHERE status='pending'").fetchall()
    st.info(f"عندك {len(orders)} طلب معلق")
    for o in orders:
        with st.container(border=True):
            st.write(f"**رقم الطلب:** {o[1]}")
            st.write(f"**الاسم:** {o[2]} | **التلفون:** {o[3]}")
            st.write(f"**المنتجات:** {o[4]}")
            st.write(f"**الاجمالي:** {o[5]}$")
            col1, col2 = st.columns(2)
            if col1.button("✅ تاكيد الطلب", key=f"ok{o[0]}", use_container_width=True):
                c.execute("UPDATE orders SET status='active' WHERE id=?", (o[0],)); conn.commit(); st.success("تم التاكيد"); st.rerun()
            if col2.button("❌ رفض الطلب", key=f"no{o[0]}", use_container_width=True):
                c.execute("DELETE FROM orders WHERE id=?", (o[0],)); conn.commit(); st.warning("تم الرفض"); st.rerun()
