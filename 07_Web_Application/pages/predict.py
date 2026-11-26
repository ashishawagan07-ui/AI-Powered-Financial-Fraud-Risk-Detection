
import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.prediction import predict_fraud
from database.db import initialize_database, save_prediction

st.set_page_config(
    page_title="AI Fraud Prediction",
    page_icon="🔍",
    layout="wide"
)

initialize_database()

if "user" not in st.session_state:
    st.warning("Please login first to access Fraud Prediction.")
    st.page_link("pages/login.py", label="Go to Login")
    st.stop()

st.title("🔍 AI-Powered Fraud Prediction")
st.caption("Analyze financial transactions using Machine Learning models.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Details")

    model_name = st.selectbox(
        "Select ML Model",
        ["Random Forest", "Decision Tree", "Logistic Regression"]
    )

    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"]
    )

    step = st.number_input(
        "Transaction Step",
        min_value=1,
        max_value=744,
        value=100
    )

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=10000.0
    )

with col2:
    st.subheader("Account Balance Details")

    oldbalanceOrg = st.number_input(
        "Original Balance Before Transaction",
        min_value=0.0,
        value=20000.0
    )

    newbalanceOrig = st.number_input(
        "Original Balance After Transaction",
        min_value=0.0,
        value=10000.0
    )

    oldbalanceDest = st.number_input(
        "Destination Balance Before Transaction",
        min_value=0.0,
        value=5000.0
    )

    newbalanceDest = st.number_input(
        "Destination Balance After Transaction",
        min_value=0.0,
        value=15000.0
    )

st.divider()

if st.button("🚀 Predict Fraud", use_container_width=True):

    try:
        with st.spinner("Analyzing transaction with ML model..."):

            result = predict_fraud(
                model_name=model_name,
                step=step,
                transaction_type=transaction_type,
                amount=amount,
                oldbalanceOrg=oldbalanceOrg,
                newbalanceOrig=newbalanceOrig,
                oldbalanceDest=oldbalanceDest,
                newbalanceDest=newbalanceDest
            )

            save_prediction(
                user_id=st.session_state["user"]["id"],
                model_name=model_name,
                transaction_type=transaction_type,
                amount=amount,
                prediction=result["prediction"],
                probability=result["fraud_probability"]
                if result["fraud_probability"] is not None
                else 0.0
            )

        st.subheader("Prediction Result")

        if result["prediction"] == "Fraud":
            st.error("⚠️ Model Prediction: FRAUD")
        else:
            st.success("✅ Model Prediction: GENUINE")

        c1, c2, c3 = st.columns(3)

        c1.metric("Selected Model", result["model"])

        if result["fraud_probability"] is not None:
            c2.metric(
                "Estimated Fraud Probability",
                f"{result['fraud_probability'] * 100:.2f}%"
            )
        else:
            c2.metric("Fraud Probability", "Not Available")

        c3.metric("Model Score Band", result["risk_level"])

        st.caption(
            "This is a model-based prediction using a synthetic PaySim "
            "dataset. It is for educational and demonstration purposes, "
            "not a real banking fraud decision."
        )

    except Exception as e:
        st.error(f"Prediction Error: {e}")
