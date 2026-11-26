import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import initialize_database, get_connection

st.set_page_config(
    page_title="Admin Panel | Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

initialize_database()

st.markdown("""
<style>
.stApp { background: #F4F8FF; }
.admin-title { color: #174A82; font-size: 32px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)


def is_admin():
    try:
        return (
            "admin" in st.secrets
            and st.secrets["admin"]["email"]
            and st.secrets["admin"]["password"]
        )
    except Exception:
        return False


if not st.session_state.get("is_admin", False):

    st.markdown(
        "<h1 style='text-align:center;color:#174A82;'>"
        "ADMIN LOGIN"
        "</h1>",
        unsafe_allow_html=True
    )

    with st.form("admin_login"):
        email = st.text_input("Admin Email")
        password = st.text_input("Admin Password", type="password")
        submit = st.form_submit_button("Secure Admin Login")

        if submit:
            if not is_admin():
                st.error("Admin configuration is missing.")
            elif (
                email.strip().lower()
                == st.secrets["admin"]["email"].strip().lower()
                and password
                == st.secrets["admin"]["password"]
            ):
                st.session_state["is_admin"] = True
                st.success("Admin login successful!")
                st.rerun()
            else:
                st.error("Invalid admin credentials.")

else:

    st.markdown(
        "<div class='admin-title'>ADMIN CONTROL CENTER</div>",
        unsafe_allow_html=True
    )

    if st.button("Admin Logout"):
        st.session_state["is_admin"] = False
        st.rerun()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric("Registered Users", total_users)
    col2.metric("Total Predictions", total_predictions)

    st.subheader("Registered Users")

    cursor.execute("""
        SELECT id, full_name, email, role, created_at
        FROM users ORDER BY id DESC
    """)

    users = cursor.fetchall()

    st.dataframe(
        users,
        use_container_width=True,
        column_config={
            "0": "ID",
            "1": "Full Name",
            "2": "Email",
            "3": "Role",
            "4": "Created At"
        }
    )

    st.subheader("Recent Predictions")

    cursor.execute("""
        SELECT id, user_id, model_name, transaction_type,
               amount, prediction, fraud_probability, created_at
        FROM predictions
        ORDER BY id DESC LIMIT 100
    """)

    predictions = cursor.fetchall()

    st.dataframe(predictions, use_container_width=True)

    conn.close()