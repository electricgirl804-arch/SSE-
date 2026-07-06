import streamlit as st

st.set_page_config(page_title="دخول SSE", page_icon="🔐")
st.title("🔐 دخول منصة SSE التعليمية")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

phone = st.text_input("رقم التلفون *", placeholder="09xxxxxxxx", max_chars=12)
email = st.text_input("الايميل - اختياري")
name = st.text_input("الاسم")

if st.button("🚀 دخول المنصة"):
    if phone == "":
        st.error("رقم التلفون مطلوب")
    elif len(phone) < 10:
        st.error("رقم التلفون غير صحيح")
    else:
        st.session_state.logged_in = True
        st.session_state.user_phone = phone
        st.session_state.user_email = email
        st.session_state.user_name = name if name else "مستخدم"
        st.success(f"مرحباً {st.session_state.user_name} ✅ تم تسجيل الدخول")
        st.switch_page("pages/05_🎓_معمل_الطالب.py")

st.caption("رقم التلفون هو كلمة المرور")
