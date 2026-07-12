import streamlit as st
from datetime import datetime
from utils import check_login, logout, load_css

check_login(); logout(); load_css()

st.title("🚨 تشخيص الأعطال الذكي")
st.caption("اختر كود الخطأ الظاهر على الانفرتر واحصل على السبب والحل فوراً")

# CSS موحد مع المنصة + اضافات الكروت
st.markdown("""
<style>
.info-card { background: #112240; padding: 25px; border-radius: 15px;
             border-left: 5px solid #64ffda; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
.danger { border-left: 5px solid #FF4B4B; }
.warning { border-left: 5px solid #FFA500; }
.success { border-left: 5px solid #4CAF50; }
.contact-box { background: #64ffda; color: #0a192f; padding: 15px; border-radius: 10px; 
               text-align: center; font-weight: bold; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# قاعدة بيانات الاعطال موسعة
ERRORS_DB = {
    "اختر الكود": {"سبب": "", "حل": "", "نوع": ""},
    "E01 - جهد البطارية منخفض": {"سبب": "ضعف في بطاريات التخزين او استخدام كابل DC بمقطع صغير", "حل": "1. فصل الاحمال الثقيلة مؤقتاً \n2. قياس جهد البطارية \n3. مراجعة سمك الكابل والتوصيلات", "نوع": "warning"},
    "E02 - جهد البطارية مرتفع": {"سبب": "عطل في منظم الشحن او زيادة عدد الالواح", "حل": "1. فصل الالواح فوراً \n2. فحص منظم الشحن MPPT \n3. التواصل مع الدعم الفني", "نوع": "danger"},
    "E04/E05 - ارتفاع حرارة الانفرتر": {"سبب": "انسداد فتحات التهوية او ارتفاع حرارة الجو", "حل": "1. تنظيف المراوح وازالة الاتربة \n2. توفير مسافة 30سم حول الانفرتر \n3. ابعاده من الشمس المباشرة", "نوع": "warning"},
    "E07/E15 - حمل زائد Overload": {"سبب": "تجاوز اجمالي الاحمال للقدرة القصوى للانفرتر", "حل": "1. فصل بعض الاجهزة فوراً \n2. تشغيل الاجهزة الثقيلة واحد واحد \n3. توزيع الاحمال على فترات", "نوع": "danger"},
    "E09 - عطل في البطارية": {"سبب": "تلف في احدى بطاريات المنظومة", "حل": "1. قياس جهد كل بطارية على حدة \n2. استبدال البطارية الاقل من 11V \n3. التاكد من تاريخ التصنيع", "نوع": "danger"},
    "E12 - دائرة قصر Short Circuit": {"سبب": "قصر في اسلاك 220V او عطل في احد الاجهزة", "حل": "1. فصل جميع الاحمال من الانفرتر \n2. اعادة التشغيل جهاز جهاز لتحديد المسبب \n3. فحص الاسلاك", "نوع": "danger"},
    "E21 - خطأ في الالواح PV Error": {"سبب": "قطع في كابل الالواح او ارتخاء في موصلات MC4", "حل": "1. مراجعة توصيلات الالواح \n2. قياس جهد الالواح يجب ان يكون > 200V \n3. فحص الفيوز", "نوع": "warning"},
    "E30/F01 - خطأ في الشبكة Grid Error": {"سبب": "ضعف او انقطاع التيار من الشبكة العامة", "حل": "1. التاكد من وجود كهرباء الشبكة \n2. فحص القاطع الرئيسي \n3. النظام سيحول تلقائي على البطاريات", "نوع": "warning"},
    "Normal": {"سبب": "النظام يعمل بشكل طبيعي", "حل": "لا توجد مشاكل ✅ كل شي تمام", "نوع": "success"}
}

col1, col2 = st.columns([1,2])

with col1:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.subheader("اختار كود الخطأ")
    error_code = st.selectbox("الاكواد الشائعة", list(ERRORS_DB.keys()))
    
    st.divider()
    st.subheader("لم تجد الكود؟")
    custom_issue = st.text_area("اوصف المشكلة", placeholder="مثال: الانفرتر بفصل بالليل")
    if st.button("🤖 ارسال للبوت الذكي", use_container_width=True):
        st.switch_page("pages/14_🤖_بوت_Gemini.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if error_code != "اختر الكود":
        data = ERRORS_DB[error_code]
        card_class = data['نوع']
        
        st.markdown(f"<div class='info-card {card_class}'>", unsafe_allow_html=True)
        st.subheader(f"نتيجة التشخيص: {error_code}")
        st.error(f"**السبب المحتمل:** {data['سبب']}")
        st.success(f"**الإجراء المقترح:** \n{data['حل']}")
        
        # زر تحميل التقرير
        report = f"SSE Fault Report\nالكود: {error_code}\nالوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nالسبب: {data['سبب']}"
        st.download_button("📄 تحميل تقرير العطل", data=report, file_name=f"fault_{error_code}.txt", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# فورم طلب مهندس
with st.expander("👷‍♂️ طلب مهندس موقع - تركيب او صيانة"):
    with st.form("engineer_request"):
        st.markdown('<div class="contact-box">للتواصل المباشر: 0110560222</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("الاسم *")
            phone = st.text_input("رقم الهاتف *")
        with col2:
            address = st.text_area("العنوان *")
            service_type = st.selectbox("نوع الخدمة", ["تركيب منظومة جديدة", "صيانة أعطال", "صيانة دورية"])
        
        details = st.text_area("وصف المشكلة او تفاصيل التركيب")
        
        if st.form_submit_button("📨 ارسال الطلب", type="primary", use_container_width=True):
            if name and phone and address:
                st.success(f"✅ تم استلام الطلب بنجاح! \nسيتم التواصل خلال ساعتين على الرقم {phone}")
            else:
                st.error("الرجاء ملء الحقول المطلوبة *")

st.divider()
col1, col2, col3 = st.columns(3)
with col1: st.page_link("pages/02_📊_الأحمال.py", label="🔙 الرجوع للحاسبة")
with col2: st.page_link("pages/09_🌍_الخريطة_العالمية.py", label="🌍 الخريطة")
with col3: st.page_link("app.py", label="🏠 الرئيسية")

st.caption("شركة SSE للطاقة الشمسية | الدعم الفني: 0110560222")
