import streamlit as st
import json
import pandas as pd
from utils import check_login, logout, load_css
from database import load_orders, load_suppliers, load_users, save_file

check_login(); logout(); load_css()

if st.session_state.get('user_type')!= 'admin':
    st.error("🚫 للادمن فقط"); st.stop()

st.title("📊 لوحة الادمن 15.1")

orders = load_orders(); suppliers = load_suppliers(); users = load_users()

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 الطلبات", len(orders))
c2.metric("🏭 الموردين", len(suppliers))
c3.metric("👥 العملاء", len(users))
c4.metric("⏳ معلقين", len([s for s in suppliers if s['status']=="معلق"]))
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📦 الطلبات", "🏭 الموردين", "👥 العملاء", "💾 نسخ احتياطي"])

# تبويب 1: الطلبات
with tab1:
    st.subheader("ادارة الطلبات")
    if orders:
        بحث = st.text_input("🔍 بحث بالاسم او رقم الطلب")

        for order in orders:
            if بحث and بحث.lower() not in str(order).lower(): continue

            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2,2,2,2])
                c1.markdown(f"**رقم:** {order['id']}\n**العميل:** {order['customer']}")
                c2.markdown(f"**المبلغ:** {order['total']} $")
                c3.markdown(f"**الحالة الحالية:** `{order['status']}`")

                # زرار تغيير الحالة
                حالة_جديدة = c4.selectbox(
                    "تغيير الحالة",
                    ["في انتظار الدفع", "تم الدفع", "قيد التجهيز", "تم الشحن", "مكتمل", "ملغي"],
                    index=0, key=f"status{order['id']}"
                )
                if c4.button("تحديث", key=f"btn{order['id']}"):
                    order['status'] = حالة_جديدة
                    save_file("orders.json", orders)
                    st.success(f"تم تحديث طلب {order['id']}"); st.rerun()
    else: st.info("لا يوجد طلبات بعد")

# تبويب 2: الموردين
with tab2:
    st.subheader("ادارة الموردين")
    if suppliers:
        for i, s in enumerate(suppliers):
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3,2,2,1])
                c1.markdown(f"**{s['brand']}** \n `{s['category']}`")
                c2.markdown(f"**السعر:** {s.get('price','')} $")
                c3.markdown(f"**الحالة:** {s['status']}")
                if s['status'] == "معلق":
                    if c4.button("✅ تفعيل", key=f"app{i}"):
                        suppliers[i]['status'] = "مفعل"
                        save_file("suppliers.json", suppliers); st.rerun()
    else: st.info("لا يوجد موردين بعد")

# تبويب 3 و 4 زي ما هم
with tab3:
    if users: st.dataframe(pd.DataFrame(users), use_container_width=True)
    else: st.info("لا يوجد عملاء بعد")

with tab4:
    st.download_button("📥 orders.json", json.dumps(orders,ensure_ascii=False,indent=2), "orders.json")
    st.download_button("📥 suppliers.json", json.dumps(suppliers,ensure_ascii=False,indent=2), "suppliers.json")
    st.download_button("📥 users.json", json.dumps(users,ensure_ascii=False,indent=2), "users.json")
