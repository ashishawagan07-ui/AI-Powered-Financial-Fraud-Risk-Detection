
import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "fraud_detection.db"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            model_name TEXT,
            transaction_type TEXT,
            amount REAL,
            prediction TEXT,
            fraud_probability REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def create_user(full_name, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (
                full_name, email, password_hash, role
            )
            VALUES (?, ?, ?, 'user')
        """, (
            full_name,
            email,
            password_hash
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def save_prediction(
    user_id,
    model_name,
    transaction_type,
    amount,
    prediction,
    probability
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            user_id,
            model_name,
            transaction_type,
            amount,
            prediction,
            fraud_probability
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        model_name,
        transaction_type,
        amount,
        prediction,
        probability
    ))

    conn.commit()
    conn.close()


def get_user_predictions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            model_name,
            transaction_type,
            amount,
            prediction,
            fraud_probability,
            created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()

    return records
