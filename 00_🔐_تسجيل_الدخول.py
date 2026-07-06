import streamlit as st
st.title("🔐 دخول منصة SSE التعليمية")
phone = st.text_input("رقم التلفون *", placeholder="09xxxxxxxx")
email = st.text_input("الايميل - اختياري")
name = st.text_input("الاسم")
if st.button("🚀 دخول المنصة"):
    if phone == "":
        st.error("لازم تدخلي رقم التلفون")
    else:
        st.session_state.logged_in = True
        st.session_state.user_phone = phone
        st.session_state.user_email = email
        st.session_state.user_name = name
        st.success(f"مرحباً {name} ✅")
        st.switch_page("pages/05_🎓_معمل_الطالب.py")
st.caption("رقم التلفون هو كلمة السر حقتك")
