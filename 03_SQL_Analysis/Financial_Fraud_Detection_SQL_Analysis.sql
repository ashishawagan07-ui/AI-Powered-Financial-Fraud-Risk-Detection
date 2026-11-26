USE financial_fraud_detection;

-- 1. Total Transactions and Fraud Count
SELECT
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    COUNT(*) - SUM(isFraud) AS genuine_transactions
FROM transactions;

-- 2. Fraud Percentage
SELECT
    ROUND(SUM(isFraud) * 100.0 / COUNT(*), 4) AS fraud_percentage
FROM transactions;

-- 3. Fraud by Transaction Type
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(SUM(isFraud) * 100.0 / COUNT(*), 4) AS fraud_percentage
FROM transactions
GROUP BY type
ORDER BY fraud_transactions DESC;

-- 4. Fraud Amount Analysis
SELECT
    type,
    COUNT(*) AS fraud_count,
    ROUND(SUM(amount), 2) AS total_fraud_amount,
    ROUND(AVG(amount), 2) AS average_fraud_amount
FROM transactions
WHERE isFraud = 1
GROUP BY type;

-- 5. Top 10 Fraud Transactions
SELECT
    step, type, amount, nameOrig, nameDest
FROM transactions
WHERE isFraud = 1
ORDER BY amount DESC
LIMIT 10;

-- 6. Final Fraud Summary
SELECT
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS total_fraud,
    COUNT(*) - SUM(isFraud) AS genuine_transactions,
    ROUND(SUM(amount), 2) AS total_transaction_amount,
    ROUND(SUM(CASE WHEN isFraud = 1 THEN amount ELSE 0 END), 2) AS total_fraud_amount,
    ROUND(AVG(CASE WHEN isFraud = 1 THEN amount END), 2) AS avg_fraud_amount
FROM transactions;


USE financial_fraud_detection;

SELECT
    isFraud,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY isFraud;

SELECT
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(
        SUM(isFraud) * 100.0 / COUNT(*), 4
    ) AS fraud_percentage
FROM transactions;

SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(
        SUM(isFraud) * 100.0 / COUNT(*), 4
    ) AS fraud_percentage
FROM transactions
GROUP BY type
ORDER BY fraud_transactions DESC;

SELECT
    type,
    COUNT(*) AS fraud_count,
    ROUND(SUM(amount), 2) AS total_fraud_amount,
    ROUND(AVG(amount), 2) AS average_fraud_amount,
    ROUND(MAX(amount), 2) AS maximum_fraud_amount
FROM transactions
WHERE isFraud = 1
GROUP BY type
ORDER BY total_fraud_amount DESC;


SELECT
    step,
    type,
    amount,
    nameOrig,
    nameDest
FROM transactions
WHERE isFraud = 1
ORDER BY amount DESC
LIMIT 10;


SELECT
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS total_fraud,
    COUNT(*) - SUM(isFraud) AS genuine_transactions,
    ROUND(SUM(amount), 2) AS total_transaction_amount,
    ROUND(
        SUM(CASE WHEN isFraud = 1 THEN amount ELSE 0 END), 2
    ) AS total_fraud_amount,
    ROUND(
        AVG(CASE WHEN isFraud = 1 THEN amount END), 2
    ) AS avg_fraud_amount
FROM transactions;