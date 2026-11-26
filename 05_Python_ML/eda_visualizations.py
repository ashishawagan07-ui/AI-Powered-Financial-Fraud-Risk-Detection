from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "01_Raw_Data" / "AI_Powered_Financial_Fraud_Risk_Detection.csv"
OUTPUT_DIR = BASE_DIR / "06_Final_Report" / "Graphs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_FILE)
print("Dataset loaded:", df.shape)

sns.set_theme(style="whitegrid")

# 1. Fraud vs Non-Fraud
fraud_counts = df["isFraud"].value_counts()
plt.figure(figsize=(8, 5))
sns.barplot(x=["Non-Fraud", "Fraud"], y=fraud_counts.values)
plt.title("Fraud vs Non-Fraud Transactions")
plt.ylabel("Number of Transactions")
plt.savefig(OUTPUT_DIR / "01_fraud_vs_nonfraud.png")
plt.close()

# 2. Fraud by Transaction Type
fraud_type = df[df["isFraud"] == 1]["type"].value_counts()
plt.figure(figsize=(8, 5))
sns.barplot(x=fraud_type.index, y=fraud_type.values)
plt.title("Fraud Transactions by Type")
plt.xlabel("Transaction Type")
plt.ylabel("Fraud Count")
plt.savefig(OUTPUT_DIR / "02_fraud_by_type.png")
plt.close()

# 3. Fraud Amount Analysis
fraud_amount = df[df["isFraud"] == 1].groupby("type")["amount"].sum()
plt.figure(figsize=(8, 5))
sns.barplot(x=fraud_amount.index, y=fraud_amount.values)
plt.title("Total Fraud Amount by Transaction Type")
plt.xlabel("Transaction Type")
plt.ylabel("Fraud Amount")
plt.savefig(OUTPUT_DIR / "03_fraud_amount.png")
plt.close()

# 4. Transaction Type Distribution
type_counts = df["type"].value_counts()
plt.figure(figsize=(8, 5))
plt.pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%")
plt.title("Transaction Type Distribution")
plt.savefig(OUTPUT_DIR / "04_transaction_distribution.png")
plt.close()

# 5. Fraud Percentage by Type
type_total = df.groupby("type")["isFraud"].agg(["sum", "count"])
type_total["Fraud_Percentage"] = type_total["sum"] / type_total["count"] * 100

plt.figure(figsize=(8, 5))
sns.barplot(
    x=type_total.index,
    y=type_total["Fraud_Percentage"]
)
plt.title("Fraud Percentage by Transaction Type")
plt.xlabel("Transaction Type")
plt.ylabel("Fraud Percentage (%)")
plt.savefig(OUTPUT_DIR / "05_fraud_percentage.png")
plt.close()

print("\nAll 5 Graphs Created Successfully!")
print("Saved in:", OUTPUT_DIR)