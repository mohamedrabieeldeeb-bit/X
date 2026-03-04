import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة تحكم اتصالات العملاء", layout="wide")

st.markdown("""
<style>
.main { text-align: right; }
</style>
""", unsafe_allow_html=True)

st.title("📊 لوحة تحكم تحليل استفسارات العملاء")
st.write("قم برفع ملف البيانات (CSV) لمشاهدة التحليل التفاعلي")

uploaded_file = st.file_uploader("اختر ملف CSV", type="csv")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # ---------------- KPIs ----------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("إجمالي الحالات", len(df))

    with col2:
        if 'Case Type' in df.columns:
            top_channel = df['Case Type'].mode()[0]
        else:
            top_channel = "N/A"
        st.metric("القناة الأكثر استخداماً", top_channel)

    with col3:
        if 'Governorate (Customer)' in df.columns:
            top_gov = df['Governorate (Customer)'].mode()[0]
        else:
            top_gov = "N/A"
        st.metric("المحافظة الأكثر نشاطاً", top_gov)

    with col4:
        if 'Main Classification' in df.columns:
            complaints_count = len(df[df['Main Classification'] == 'Complaints'])
        else:
            complaints_count = 0
        st.metric("عدد الشكاوى", complaints_count)

    st.divider()

    # ---------------- Charts Row 1 ----------------
    colA, colB = st.columns(2)

    with colA:
        if 'Main Classification' in df.columns:
            st.subheader("📈 توزيع تصنيف الحالات")
            fig_class = px.pie(df, names='Main Classification', hole=0.4)
            st.plotly_chart(fig_class, use_container_width=True)

    with colB:
        if 'Case Type' in df.columns:
            st.subheader("📞 توزيع قنوات الاتصال")
            case_counts = df['Case Type'].value_counts().reset_index()
            case_counts.columns = ['Case Type', 'count']
            fig_type = px.bar(case_counts, x='Case Type', y='count')
            st.plotly_chart(fig_type, use_container_width=True)

    # ---------------- Charts Row 2 ----------------
    colC, colD = st.columns(2)

    with colC:
        if 'Governorate (Customer)' in df.columns:
            st.subheader("🌍 النشاط حسب المحافظة (أعلى 10)")
            top_10 = df['Governorate (Customer)'].value_counts().nlargest(10).reset_index()
            top_10.columns = ['Governorate (Customer)', 'count']
            fig_gov = px.bar(top_10, x='count', y='Governorate (Customer)', orientation='h')
            st.plotly_chart(fig_gov, use_container_width=True)

    with colD:
        if 'Case Title' in df.columns:
            st.subheader("📋 أكثر المواضيع تكراراً (Top 10)")
            top_cases = df['Case Title'].value_counts().nlargest(10).reset_index()
            top_cases.columns = ['Case Title', 'count']
            fig_cases = px.bar(top_cases, x='Case Title', y='count')
            st.plotly_chart(fig_cases, use_container_width=True)

    # ---------------- Time Analysis ----------------
    if 'Date' in df.columns:
        st.subheader("📅 تحليل حجم الحالات عبر الزمن")
        df_time = df.groupby(df['Date'].dt.date).size().reset_index(name='count')
        fig_time = px.line(df_time, x='Date', y='count')
        st.plotly_chart(fig_time, use_container_width=True)

    if st.checkbox("عرض البيانات الخام"):
        st.dataframe(df)

else:
    st.info("💡 بانتظار رفع ملف البيانات لبدء التحليل.")

st.markdown("---")

st.caption("تم التطوير بواسطة محمد ربيع الديب 🚀")
