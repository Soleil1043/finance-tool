import streamlit as st
from finance_tool.models import init_db
from finance_tool.reports import ReportGen

engine = init_db()
report = ReportGen(engine())

st.set_page_config(page_title="个人财务", layout="wide")
st.title("💰 收支仪表板")

# ===== 侧边栏 =====
year = st.sidebar.selectbox("年度", [2023, 2024])
month = st.sidebar.slider("月份", 1, 12, 1)

# ===== 主区域 =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("月度收支")
    df_flow = report.monthly_flow(year)
    st.dataframe(df_flow, use_container_width=True)

with col2:
    st.subheader("支出分布")
    fig = report.expense_pie(year, month)
    if fig:
        st.pyplot(fig)
    else:
        st.info("该月无支出")
