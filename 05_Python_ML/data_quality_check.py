
from pathlib import Path
import pandas as pd
import numpy as np

# Project folders
project_folder = Path(__file__).resolve().parent.parent
raw_folder = project_folder / "01_Raw_Data"
report_folder = project_folder / "06_Final_Report"
report_folder.mkdir(exist_ok=True)

# Find CSV file
csv_files = list(raw_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("CSV file not found in 01_Raw_Data folder.")

file_path = csv_files[0]
print("Dataset:", file_path.name)

# Process dataset in chunks
chunk_size = 200_000
total_records = 0
missing_values = None
fraud_count = 0
non_fraud_count = 0

hash_file = report_folder / "row_hashes.bin"
if hash_file.exists():
    hash_file.unlink()

for chunk in pd.read_csv(file_path, chunksize=chunk_size):

    total_records += len(chunk)

    if missing_values is None:
        missing_values = chunk.isna().sum()
    else:
        missing_values += chunk.isna().sum()

    fraud_values = pd.to_numeric(
        chunk["isFraud"], errors="coerce"
    )

    fraud_count += (fraud_values == 1).sum()
    non_fraud_count += (fraud_values == 0).sum()

    # Store row hashes for duplicate checking
    row_hashes = pd.util.hash_pandas_object(
        chunk, index=False
    ).to_numpy(dtype=np.uint64)

    with open(hash_file, "ab") as f:
        row_hashes.tofile(f)

    print("Processed records:", total_records)

# Duplicate check using disk-backed hashes
hashes = np.memmap(
    hash_file, dtype=np.uint64, mode="r+"
)
hashes.sort()

duplicate_records = int(
    np.count_nonzero(hashes[1:] == hashes[:-1])
)

total_columns = len(missing_values)
total_missing = int(missing_values.sum())

fraud_percentage = (
    fraud_count / total_records * 100
    if total_records else 0
)

# Display results
print("\n===== DATA QUALITY REPORT =====")
print("Total Records:", total_records)
print("Total Columns:", total_columns)
print("Missing Values:", total_missing)
print("Duplicate Records:", duplicate_records)
print("Fraud Transactions:", fraud_count)
print("Non-Fraud Transactions:", non_fraud_count)
print("Fraud Percentage:", round(fraud_percentage, 4), "%")

print("\n===== MISSING VALUES BY COLUMN =====")
print(missing_values)

# Save reports
missing_values.to_csv(
    report_folder / "missing_values_report.csv",
    header=["Missing_Values"]
)

report = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total Columns",
        "Missing Values",
        "Duplicate Records",
        "Fraud Transactions",
        "Non-Fraud Transactions",
        "Fraud Percentage"
    ],
    "Result": [
        total_records,
        total_columns,
        total_missing,
        duplicate_records,
        fraud_count,
        non_fraud_count,
        round(fraud_percentage, 4)
    ]
})

report.to_csv(
    report_folder / "data_quality_report.csv",
    index=False
)

print("\nReports saved in 06_Final_Report folder.")
print("DATA QUALITY CHECK COMPLETED!")


