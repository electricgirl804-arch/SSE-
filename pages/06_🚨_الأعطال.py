import streamlit as st

st.set_page_config(page_title="SSE - تشخيص الأعطال", page_icon="🚨")
st.title("🚨 التنبؤ بالأعطال")
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v1.2")

fault = st.selectbox("اختاري كود الخطأ", ["E01 - جهد منخفض", "E05 - حرارة عالية", "E09 - عطل بطارية"])

if fault.startswith("E01"):
    st.error("السبب: بطاريات ضعيفة أو كيبل رفيع")
    st.info("الحل: افصلي الأحمال الثقيلة + شيكي التوصيلات")
elif fault.startswith("E05"):
    st.warning("السبب: تهوية الانفرتر مسدودة")
    st.info("الحل: نظفي المراوح + خلي مسافة 30سم للتهوية")
else:
    st.error("السبب: بطارية تالفة")
    st.info("الحل: قيسي الجهد. لو أقل من 11V غيري البطارية")
