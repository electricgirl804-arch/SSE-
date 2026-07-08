import streamlit as st
from datetime import datetime

st.set_page_config(page_title="SSE - تشخيص الأعطال", page_icon="🚨", layout="centered")

# ===== CSS =====
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
    h1 { color: #FFD700!important; text-align: center; font-weight: 800; }
.stCaption { text-align: center!important; color: #FFFFFF!important; }
.fault-card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-left: 5px solid #FFD700; margin: 20px 0; }
.stButton>button { background: linear-gradient(90deg, #FFD700, #FFA500); color: #1e3c72; font-weight: bold; border-radius: 10px; }
.contact-box { background: #FFD700; color: #1e3c72; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚨 نظام التنبؤ وتشخيص الأعطال</h1>", unsafe_allow_html=True)
st.caption("تم التطوير بواسطة المهندسة شهد | SSE v1.9")

st.markdown("---")

fault = st.selectbox(
    "الرجاء اختيار كود الخطأ الظاهر على الانفرتر", # تم التعديل
    [
        "E01 - جهد البطارية منخفض Low Voltage",
        "E02 - جهد البطارية مرتفع Over Voltage", 
        "E05 - ارتفاع حرارة الانفرتر Over Temp",
        "E09 - عطل في البطارية Battery Fault",
        "E12 - دائرة قصر في المخرج Short Circuit",
        "E15 - حمل زائد Overload",
        "E21 - خطأ في توصيل الألواح الشمسية PV Error",
        "E30 - خطأ في شبكة الكهرباء Grid Error"
    ]
)

st.markdown("---")

# عرض العطل داخل كرت
with st.container():
    st.markdown('<div class="fault-card">', unsafe_allow_html=True)
    
    if fault.startswith("E01"):
        st.error("**السبب المحتمل:** ضعف في بطاريات التخزين أو استخدام كابل DC بمقطع صغير أو وجود ارتخاء في التوصيلات")
        st.info("**الإجراء المقترح:** 1. فصل الأحمال الثقيلة مؤقتاً 2. قياس جهد البطارية 3. مراجعة سمك الكابل والتأكد من إحكام التوصيلات")
        st.success("**الجهد الطبيعي:** 24V أو 48V حسب نظام المنظومة")

    elif fault.startswith("E02"):
        st.error("**السبب المحتمل:** عطل في منظم الشحن الداخلي أو زيادة عدد الألواح الشمسية عن الحد المسموح")
        st.info("**الإجراء المقترح:** 1. فصل الألواح الشمسية فوراً 2. فحص منظم الشحن 3. التواصل مع الدعم الفني")

    elif fault.startswith("E05"):
        st.warning("**السبب المحتمل:** انسداد فتحات التهوية الخاصة بالانفرتر أو ارتفاع درجة حرارة الجو المحيط")
        st.info("**الإجراء المقترح:** 1. تنظيف المراوح وإزالة الأتربة 2. توفير مسافة 30سم على الأقل حول الانفرتر 3. تحسين التهوية في المكان")
        st.success("**درجة الحرارة الطبيعية للتشغيل:** أقل من 50 درجة مئوية")

    elif fault.startswith("E09"):
        st.error("**السبب المحتمل:** تلف في إحدى بطاريات المنظومة")
        st.info("**الإجراء المقترح:** 1. قياس جهد كل بطارية على حدة 2. استبدال البطارية التي جهدها أقل من 11V 3. التأكد من تاريخ تصنيع البطاريات")
        
    elif fault.startswith("E12"):
        st.error("**السبب المحتمل:** وجود دائرة قصر في أسلاك 220V أو عطل في أحد الأجهزة المتصلة")
        st.info("**الإجراء المقترح:** 1. فصل جميع الأجهزة 2. إعادة التشغيل جهازاً تلو الآخر لتحديد الجهاز المتسبب")

    elif fault.startswith("E15"):
        st.warning("**السبب المحتمل:** تجاوز إجمالي الأحمال للقدرة القصوى للانفرتر")
        st.info("**الإجراء المقترح:** 1. فصل جهاز ذو استهلاك عالي مثل المكيف أو السخان 2. توزيع الأحمال على فترات زمنية مختلفة")

    elif fault.startswith("E21"):
        st.warning("**السبب المحتمل:** قطع في كابل الألواح أو ارتخاء في موصلات MC4 أو تلف في الفيوز")
        st.info("**الإجراء المقترح:** 1. مراجعة توصيلات الألواح على التوالي 2. قياس جهد الألواح ويجب أن يكون أكبر من 200V")

    else: # E30
        st.error("**السبب المحتمل:** ضعف أو انقطاع التيار الكهربائي من الشبكة العامة")
        st.info("**الإجراء المقترح:** 1. الانتظار حتى استقرار الشبكة 2. فحص القاطع الرئيسي للمنزل")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ازرار
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 إعادة", use_container_width=True): st.rerun()
with col2:
    report = f"تقرير عطل SSE\nالكود: {fault}\nالوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    st.download_button("📄 تحميل التقرير", data=report, file_name="report.txt", use_container_width=True)
with col3:
    st.link_button("📞 اتصال 0110560222", "tel:0110560222", use_container_width=True)

st.markdown("---")

# فورم طلب مهندس
with st.expander("👷‍♂️ طلب مهندس موقع - تركيب أو صيانة"):
    with st.form("engineer_request"):
        st.markdown('<div class="contact-box">للتواصل المباشر: 0110560222</div>', unsafe_allow_html=True)
        name = st.text_input("الاسم *")
        phone = st.text_input("رقم الهاتف *")
        address = st.text_area("العنوان *")
        service_type = st.radio("نوع الخدمة المطلوبة", ["تركيب منظومة جديدة", "صيانة أعطال", "صيانة دورية"])
        details = st.text_area("وصف المشكلة أو تفاصيل التركيب")
        if st.form_submit_button("إرسال الطلب"):
            if name and phone and address:
                st.success(f"✅ تم استلام الطلب بنجاح! \nسيتم التواصل خلال ساعتين على الرقم {phone}")
            else:
                st.error("الرجاء ملء الحقول المطلوبة *")

st.markdown("---")
st.caption("في حال استمرار المشكلة، يرجى التواصل مع الدعم الفني: 0110560222 | المهندسة شهد")
