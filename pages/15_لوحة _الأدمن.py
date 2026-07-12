import streamlit as st
import json
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime
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
c4.metric("⏳ معلقين", len([s for s in suppliers if s.get('status')=="معلق"]))
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📦 الطلبات", "🏭 الموردين", "👥 العملاء", "💾 نسخ احتياطي"])

with tab1:
    st.subheader("ادارة الطلبات")
    if orders:
        بحث = st.text_input("🔍 بحث")
        for order in orders:
            if بحث and بحث.lower() not in str(order).lower(): continue
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2,2,2,2])
                c1.markdown(f"**رقم:** {order['id']}\n**العميل:** {order['customer']}")
                c2.markdown(f"**المبلغ:** {order['total']} $")
                c3.markdown(f"**الحالة:** `{order['status']}`")
                حالة_جديدة = c4.selectbox("تغيير الحالة",["في انتظار الدفع", "تم الدفع", "قيد التجهيز", "تم الشحن", "مكتمل", "ملغي"], key=f"status{order['id']}")
                if c4.button("تحديث", key=f"btn{order['id']}"):
                    order['status'] = حالة_جديدة
                    save_file("orders.json", orders); st.success("تم التحديث"); st.rerun()
    else: st.info("لا يوجد طلبات بعد")

with tab2:
    st.subheader("ادارة الموردين")
    if suppliers:
        for i, s in enumerate(suppliers):
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3,2,2,1])
                c1.markdown(f"**{s['brand']}** \n `{s['category']}`")
                c2.markdown(f"**السعر:** {s.get('price','')} $")
                c3.markdown(f"**الحالة:** {s.get('status','')}")
                if s.get('status') == "معلق":
                    if c4.button("✅ تفعيل", key=f"app{i}"):
                        suppliers[i]['status'] = "مفعل"
                        save_file("suppliers.json", suppliers); st.rerun()
    else: st.info("لا يوجد موردين بعد")

with tab3:
    st.subheader("بيانات العملاء")
    if users: st.dataframe(pd.DataFrame(users), use_container_width=True)
    if os.path.exists("customers.csv"):
        st.divider()
        st.subheader("طلبات المهندسين")
        df_c = pd.read_csv("customers.csv", encoding='utf-8-sig')
        st.dataframe(df_c, use_container_width=True)

with tab4:
    st.subheader("💾 نسخ احتياطي")
    st.warning("نزلي الملفات دي كل اسبوع عشان تضمنيها")

    def create_pdf(df, title):
        pdf = FPDF(orientation='L'); pdf.add_page()
        try: pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True); pdf.set_font('DejaVu', '', 8)
        except: pdf.set_font("Arial", size=8)
        pdf.cell(0, 10, txt=title, ln=True, align='C'); pdf.ln(5)
        if len(df) > 0:
            cw = pdf.w / (len(df.columns) + 1)
            for col in df.columns: pdf.cell(cw, 8, txt=str(col), border=1, align='C'); pdf.ln()
            for i in range(len(df)):
                for col in df.columns: pdf.cell(cw, 8, txt=str(df.iloc[i][col]), border=1, align='C'); pdf.ln()
        return pdf.output(dest='S').encode('latin-1')

    c1,c2,c3,c4 = st.columns(4)
    c1.download_button("📥 orders.json", json.dumps(orders,ensure_ascii=False,indent=2), "orders.json")
    c2.download_button("📥 suppliers.json", json.dumps(suppliers,ensure_ascii=False,indent=2), "suppliers.json")
    c3.download_button("📥 users.json", json.dumps(users,ensure_ascii=False,indent=2), "users.json")
    if os.path.exists("customers.csv"):
        df_c = pd.read_csv("customers.csv", encoding='utf-8-sig')
        c4.download_button("📊 customers.csv", df_c.to_csv(index=False, encoding='utf-8-sig'), "customers.csv")
        st.download_button("📄 PDF طلبات المهندسين", create_pdf(df_c, "تقرير SSE"), "report.pdf", "application/pdf")
