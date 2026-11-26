import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT.parent / "06_Final_Report"

st.set_page_config(
    page_title="AI Fraud Detection | 2026",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_path = ROOT / "assets" / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text()}</style>",
        unsafe_allow_html=True
    )

# Authentication check
if "user" not in st.session_state:
    st.markdown(
        "<h1 style='color:#174A82;'>🛡️ AI FRAUD DETECTION</h1>",
        unsafe_allow_html=True
    )
    st.info("Please login to access the dashboard.")

    st.page_link("pages/login.py", label="🔐 Login")
    st.page_link("pages/register.py", label="📝 Create Account")

    st.stop()

user = st.session_state["user"]

# Sidebar
with st.sidebar:
    st.title("🛡️ FRAUD AI")
    st.caption("Financial Intelligence Platform")
    st.divider()

    st.write(f"Welcome, **{user['full_name']}**")
    st.caption(user["email"])

    if st.button("Logout", use_container_width=True):
        st.session_state.pop("user", None)
        st.rerun()

    st.divider()
    st.caption("AI Fraud Detection Platform")
    st.caption("Version 2026")

# Load project reports
def load_csv(filename):
    path = REPORT / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

summary = load_csv("final_fraud_summary.csv")
type_data = load_csv("transaction_type_analysis.csv")
fraud_data = load_csv("fraud_vs_genuine.csv")

def get_value(data, column, default=0):
    if not data.empty and column in data.columns:
        return data[column].iloc[0]
    return default

total = get_value(summary, "total_transactions", 6362620)
fraud = get_value(summary, "total_fraud", 8213)
genuine = get_value(summary, "genuine_transactions", 6354407)
fraud_amount = get_value(
    summary, "total_fraud_amount", 12056415427.84
)
avg_fraud = get_value(
    summary, "average_fraud_amount", 1467967.30
)

fraud_percentage = (fraud / total * 100) if total else 0

# Header
st.markdown(
    "<div class='main-title'>FINANCIAL FRAUD INTELLIGENCE</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div class='sub-title'>"
    "AI-Powered Transaction Monitoring & Risk Analytics | 2026"
    "</div>",
    unsafe_allow_html=True
)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Transactions", f"{int(total):,}")
c2.metric("Genuine Transactions", f"{int(genuine):,}")
c3.metric("Fraud Transactions", f"{int(fraud):,}")
c4.metric("Fraud Percentage", f"{fraud_percentage:.4f}%")

st.divider()

# Fraud overview
left, right = st.columns(2)

with left:
    st.subheader("📊 Fraud vs Genuine")
    chart_data = pd.DataFrame({
        "Category": ["Genuine", "Fraud"],
        "Transactions": [genuine, fraud]
    }).set_index("Category")

    st.bar_chart(chart_data)

with right:
    st.subheader("💰 Fraud Amount Overview")
    st.metric(
        "Total Fraud Amount",
        f"₹{float(fraud_amount):,.2f}"
    )
    st.metric(
        "Average Fraud Amount",
        f"₹{float(avg_fraud):,.2f}"
    )
    st.metric(
        "Fraud Rate",
        f"{fraud_percentage:.4f}%"
    )

# Transaction analysis
st.divider()
st.subheader("Transaction Type Analysis")

if not type_data.empty:
    st.dataframe(type_data, use_container_width=True)

    if "type" in type_data.columns and "fraud_transactions" in type_data.columns:
        chart = type_data.set_index("type")[["fraud_transactions"]]
        st.bar_chart(chart)
else:
    st.warning("Transaction analysis CSV not found.")

st.caption(
    "Analytics are based on the project's analyzed PaySim dataset. "
    "Live predictions will be available in the Prediction module."
)