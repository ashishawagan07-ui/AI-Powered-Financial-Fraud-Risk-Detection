import streamlit as st
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import initialize_database, get_user_predictions

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

initialize_database()

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.page_link("pages/login.py", label="Go to Login")
    st.stop()

st.title("📜 Prediction History")
st.caption("View your previous fraud detection predictions.")

st.divider()

records = get_user_predictions(
    st.session_state["user"]["id"]
)

if records:
    columns = [
        "ID",
        "Model",
        "Transaction Type",
        "Amount",
        "Prediction",
        "Fraud Probability",
        "Date & Time"
    ]

    df = pd.DataFrame(records, columns=columns)

    df["Fraud Probability"] = (
        df["Fraud Probability"] * 100
    ).round(2).astype(str) + "%"

    df["Amount"] = df["Amount"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Predictions", len(df))
    c2.metric(
        "Fraud Detected",
        int((df["Prediction"] == "Fraud").sum())
    )
    c3.metric(
        "Genuine Transactions",
        int((df["Prediction"] == "Genuine").sum())
    )

    st.divider()

    st.subheader("Your Prediction Records")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Prediction History",
        data=csv,
        file_name="prediction_history.csv",
        mime="text/csv"
    )

else:
    st.info("No prediction history available yet.")

st.divider()

if st.button("⬅ Back to Dashboard"):
    st.switch_page("app.py")