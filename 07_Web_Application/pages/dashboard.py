import streamlit as st

st.set_page_config(
    page_title="Fraud Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Fraud Analytics")
st.info("Main analytics dashboard is available on the Home page.")

st.markdown("""
### Dashboard Modules

- Total Transaction Analytics
- Fraud vs Genuine Analysis
- Fraud Amount Analysis
- Transaction Type Analysis
- Machine Learning Model Performance
- Risk Monitoring
""")

if st.button("Back to Home Dashboard"):
    st.switch_page("app.py")