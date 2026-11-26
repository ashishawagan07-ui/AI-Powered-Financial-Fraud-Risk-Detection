import joblib
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODEL_FILES = {
    "Logistic Regression": "Logistic_Regression.pkl",
    "Decision Tree": "Decision_Tree.pkl",
    "Random Forest": "Random_Forest.pkl"
}

def load_model(model_name):
    if model_name not in MODEL_FILES:
        raise ValueError("Invalid model selected.")

    model_path = ROOT / MODEL_FILES[model_name]

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    return joblib.load(model_path)


def predict_fraud(
    model_name,
    step,
    transaction_type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest
):
    model = load_model(model_name)

    input_data = pd.DataFrame([{
        "step": step,
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    prediction = int(model.predict(input_data)[0])

    probability = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        classes = list(model.classes_)
        probability = float(probabilities[classes.index(1)])

    result = "Fraud" if prediction == 1 else "Genuine"

    if probability is not None:
        risk_level = (
            "High" if probability >= 0.70
            else "Medium" if probability >= 0.30
            else "Low"
        )
    else:
        risk_level = "Not Available"

    return {
        "prediction": result,
        "fraud_probability": probability,
        "risk_level": risk_level,
        "model": model_name
    }