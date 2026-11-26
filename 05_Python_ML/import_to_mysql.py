
from pathlib import Path
import csv
import mysql.connector
from getpass import getpass

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "01_Raw_Data" / "AI_Powered_Financial_Fraud_Risk_Detection.csv"

print("Connecting to MySQL...")

conn = mysql.connector.connect(
    host="localhost",
    user=input("MySQL username (usually root): "),
    password=getpass("MySQL password: "),
    database="financial_fraud_detection",
    port=3306
)

cursor = conn.cursor()

# Prevent accidental duplicate import
cursor.execute("SELECT COUNT(*) FROM transactions")
existing = cursor.fetchone()[0]

if existing > 0:
    print(f"Table already contains {existing} records.")
    print("Import cancelled to prevent duplicates.")
    cursor.close()
    conn.close()
    raise SystemExit

insert_sql = """
INSERT INTO transactions (
    step, type, amount, nameOrig, oldbalanceOrg,
    newbalanceOrig, nameDest, oldbalanceDest,
    newbalanceDest, isFraud, isFlaggedFraud
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

batch = []
batch_size = 5000
total = 0

with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    for row in reader:
        values = (
            int(row[0]),
            row[1],
            float(row[2]),
            row[3],
            float(row[4]),
            float(row[5]),
            row[6],
            float(row[7]),
            float(row[8]),
            int(row[9]),
            int(row[10])
        )

        batch.append(values)

        if len(batch) >= batch_size:
            cursor.executemany(insert_sql, batch)
            conn.commit()
            total += len(batch)
            batch.clear()
            print(f"Imported: {total:,} records")

    if batch:
        cursor.executemany(insert_sql, batch)
        conn.commit()
        total += len(batch)

print(f"\nIMPORT COMPLETED! Total records: {total:,}")

cursor.close()
conn.close()
