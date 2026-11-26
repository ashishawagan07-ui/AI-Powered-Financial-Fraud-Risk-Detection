
from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "01_Raw_Data" / "AI_Powered_Financial_Fraud_Risk_Detection.csv"
OUTPUT_DIR = BASE_DIR / "06_Final_Report"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")
print("Shape:", df.shape)

# 1. Transaction Type Analysis
type_analysis = df.groupby("type").agg(
    Total_Transactions=("isFraud", "count"),
    Fraud_Transactions=("isFraud", "sum"),
    Total_Amount=("amount", "sum")
).reset_index()

type_analysis["Fraud_Percentage"] = (
    type_analysis["Fraud_Transactions"] /
    type_analysis["Total_Transactions"] * 100
)

type_analysis.to_csv(
    OUTPUT_DIR / "transaction_type_analysis.csv", index=False
)

# 2. Fraud vs Non-Fraud
fraud_analysis = df["isFraud"].value_counts().reset_index()
fraud_analysis.columns = ["Transaction_Status", "Count"]
fraud_analysis["Transaction_Status"] = fraud_analysis[
    "Transaction_Status"
].map({0: "Non-Fraud", 1: "Fraud"})

fraud_analysis.to_csv(
    OUTPUT_DIR / "fraud_vs_nonfraud_analysis.csv", index=False
)

# 3. Fraud Amount Analysis
fraud_amount = df[df["isFraud"] == 1].groupby("type").agg(
    Fraud_Count=("isFraud", "count"),
    Total_Fraud_Amount=("amount", "sum"),
    Average_Fraud_Amount=("amount", "mean"),
    Maximum_Fraud_Amount=("amount", "max")
).reset_index()

fraud_amount.to_csv(
    OUTPUT_DIR / "fraud_amount_analysis.csv", index=False
)

# 4. Transaction Type Amount Analysis
amount_analysis = df.groupby("type").agg(
    Total_Transactions=("amount", "count"),
    Total_Amount=("amount", "sum"),
    Average_Amount=("amount", "mean"),
    Maximum_Amount=("amount", "max")
).reset_index()

amount_analysis.to_csv(
    OUTPUT_DIR / "transaction_amount_analysis.csv", index=False
)

# 5. Fraud by Step
fraud_by_step = df[df["isFraud"] == 1].groupby("step").agg(
    Fraud_Transactions=("isFraud", "count"),
    Fraud_Amount=("amount", "sum")
).reset_index()

fraud_by_step.to_csv(
    OUTPUT_DIR / "fraud_by_step_analysis.csv", index=False
)

print("\n===== EDA SUMMARY =====")
print("\nTransaction Type Analysis:")
print(type_analysis)

print("\nFraud Amount Analysis:")
print(fraud_amount)

print("\nEDA COMPLETED SUCCESSFULLY!")
print("Reports saved in:", OUTPUT_DIR)
