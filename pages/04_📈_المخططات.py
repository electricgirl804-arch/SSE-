import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 المخططات والرسوم البيانية")

if 'num_panels' in st.session_state:
    st.success("عرض البيانات بيانياً")
    
    data = {
        "المكون": ["ألواح", "بطاريات", "انفرتر", "كيبل وحمايات", "تركيب"],
        "التكلفة": [
            st.session_state.num_panels * 85,
            st.session_state.num_batteries * 280,
            st.session_state.inverter_kw * 450,
            st.session_state.num_panels * 12,
            st.session_state.num_panels * 15
        ]
    }
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["المكون"], df["التكلفة"], color="#FF4B4B")
    ax.set_ylabel("التكلفة بالدولار")
    ax.set_title("توزيع تكلفة النظام")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.dataframe(df, use_container_width=True)
else:
    st.warning("ارجع للصفحة الرئيسية لإدخال البيانات أولاً")
