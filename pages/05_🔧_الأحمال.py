import streamlit as st

st.title("🔧 إدارة الأحمال التفصيلية")

st.markdown("أضف الأجهزة واحد تلو الآخر لحساب أدق")

if 'loads' not in st.session_state:
    st.session_state.loads = []

with st.form("add_load"):
    col1, col2, col3 = st.columns(3)
    with col1:
        device_name = st.text_input("اسم الجهاز")
    with col2:
        power = st.number_input("القدرة بالواط", min_value=10, value=100)
    with col3:
        hours = st.number_input("ساعات التشغيل", min_value=1, value=5)
    
    submitted = st.form_submit_button("إضافة الجهاز")
    if submitted and device_name:
        st.session_state.loads.append({"الجهاز": device_name, "القدرة W": power, "الساعات": hours, "الاستهلاك Wh": power*hours})

if st.session_state.loads:
    df = st.DataFrame(st.session_state.loads)
    st.dataframe(df, use_container_width=True, hide_index=True)
    total = sum([i["الاستهلاك Wh"] for i in st.session_state.loads])
    st.metric("إجمالي الاستهلاك اليومي", f"{total/1000:.2f} kWh")
else:
    st.info("لم تتم إضافة أي أجهزة بعد")
