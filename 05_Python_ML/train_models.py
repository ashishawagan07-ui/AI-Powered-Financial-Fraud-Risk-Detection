import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)
import joblib
import os

# Project paths
DATA_PATH = r"..\01_Raw_Data\AI_Powered_Financial_Fraud_Risk_Detection.csv"
OUTPUT_DIR = r"..\06_Final_Report"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)

# Remove ID columns
df = df.drop(columns=["nameOrig", "nameDest"], errors="ignore")

X = df.drop("isFraud", axis=1)
y = df["isFraud"]

# Categorical and numerical columns
categorical_cols = ["type"]
numerical_cols = [
    "step", "amount", "oldbalanceOrg",
    "newbalanceOrig", "oldbalanceDest", "newbalanceDest"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000, class_weight="balanced"
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=12, class_weight="balanced", random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, max_depth=15,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
}

results = []

for name, model in models.items():
    print(f"\nTraining {name}...")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1_Score": f1_score(y_test, y_pred, zero_division=0),
        "ROC_AUC": roc_auc_score(y_test, y_prob)
    }

    results.append(metrics)

    print(metrics)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(pipeline, os.path.join(
        OUTPUT_DIR, name.replace(" ", "_") + ".pkl"
    ))

# Save model comparison
results_df = pd.DataFrame(results)
results_df.to_csv(
    os.path.join(OUTPUT_DIR, "model_performance.csv"),
    index=False
)

print("\nMODEL COMPARISON")
print(results_df.to_string(index=False))
print("\nTraining completed successfully!")