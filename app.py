import streamlit as st, sqlite3, requests, math, datetime
import streamlit.components.v1 as components
import google.generativeai as genai

st.set_page_config(page_title="الأعطال 06", page_icon="⚡", layout="wide")

# === 1. كلمة السرية بتاعتك ===
ADMIN_SECRET = "shahd8499" # غيريها هنا لو عايزة

# === 2. ربط الذكاء الاصطناعي ===
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# === 3. قاعدة البيانات ===
conn = sqlite3.connect('shahd_alatal06.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, code TEXT, name TEXT, phone TEXT, size REAL, cost REAL, monthly REAL, status TEXT, date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, image TEXT)''')

# اضافة منتجات اول مرة بس
if c.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
    c.executemany("INSERT INTO products VALUES (?,?,?,?)", [
        (1,'لوح 550W Jinko أصلي',280,'https://i.imgur.com/8Km9tLL.png'),
        (2,'بطارية 48V 200Ah أصلي',900,'https://i.imgur.com/JqYeZQp.png'),
        (3,'انفرتر 5KW Hybrid أصلي',750,'https://i.imgur.com/3tV4kXG.png')
    ])
    conn.commit()

# === 4. شاشة الدخول ===
if 'role' not in st.session_state: st.session_state.role = None

if st.session_state.role == None:
    st.markdown("<h1 style='text-align:center; color:#FFD700;'>⚡ الأعطال 06 | المهندسة شهد</h1>", unsafe_allow_html=True)
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

# === 5. البوت الذكي ===
products = c.execute("SELECT name, price FROM products").fetchall()
context = "\n".join([f"- {p[0]}: ${p[1]}" for p in products])
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=f"انت بوت المهندسة شهد. رد بالسوداني. اسعارنا: {context}")

# === 6. لوحة الادمن ===
if st.session_state.role == "ادمن":
    st.header("👑 لوحة تحكم الادمن")
    pending = c.execute("SELECT * FROM projects WHERE status='pending'").fetchall()
    st.info(f"عندك {len(pending)} طلب معلق")

    for p in pending:
        with st.container(border=True):
            st.write(f"**رقم الطلب:** {p[1]}")
            st.write(f"**الاسم:** {p[2]} | **التلفون:** {p[3]}")
            st.write(f"**حجم المنظومة:** {p[4]} KW")
            st.write(f"**التكلفة:** ${p[5]} | **القسط:** ${p[6]:.2f}")
            col1, col2 = st.columns(2)
            if col1.button("✅ تاكيد الطلب", key=f"ok{p[0]}", use_container_width=True):
                c.execute("UPDATE projects SET status='active' WHERE id=?", (p[0],)); conn.commit(); st.success("تم التاكيد"); st.rerun()
            if col2.button("❌ رفض الطلب", key=f"no{p[0]}", use_container_width=True):
                c.execute("DELETE FROM projects WHERE id=?", (p[0],)); conn.commit(); st.warning("تم الرفض"); st.rerun()

# === 7. لوحة المهندس ===
else:
    tab1, tab2, tab3 = st.tabs(["💬 البوت الذكي", "⚡ حاسبة الطاقة", "🛒 المتجر"])

    with tab1:
        st.subheader("اسأل بوت الأعطال 06")
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
        monthly = (cost*1.2)/36 # قسط 3 سنوات

        st.metric("عدد الالواح 550W", panels)
        st.metric("التكلفة الكلية", f"${cost:.0f}")
        st.metric("القسط الشهري", f"${monthly:.2f}")

        with st.form("form"):
            name = st.text_input("اسم العميل")
            phone = st.text_input("رقم التلفون")
            if st.form_submit_button("📤 ارسال الطلب للادمن", use_container_width=True):
                code = f"ALAT{datetime.date.today().year}{c.execute('SELECT COUNT(*) FROM projects').fetchone()[0]+1}"
                c.execute("INSERT INTO projects VALUES (NULL,?,?,?,?,?)", (code,name,phone,size,cost,monthly,"pending",str(datetime.date.today())))
                conn.commit(); st.success(f"✅ تم ارسال الطلب رقم {code} للادمن")

    with tab3:
        st.header("🛒 متجر الأعطال 06")
        cols = st.columns(3)
        for i,p in enumerate(c.execute("SELECT * FROM products")):
            with cols[i%3]:
                st.image(p[3])
                st.write(f"**{p[1]}**")
                st.write(f"<h3 style='color:#FFD700;'>${p[2]}</h3>", unsafe_allow_html=True)
                if st.button("اضافة للسلة", key=p[0], use_container_width=True):
                    c.execute("INSERT INTO cart VALUES (NULL,?,1)", (p[0],)); conn.commit(); st.toast("تمت الاضافة")
