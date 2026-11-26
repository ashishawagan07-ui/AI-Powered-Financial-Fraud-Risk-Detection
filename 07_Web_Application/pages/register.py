import streamlit as st
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import initialize_database
from utils.auth import register_user

initialize_database()

st.set_page_config(
    page_title="Create Account | Fraud Detection",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #EAF3FF, #FFFFFF);
}
.register-box {
    background: white;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #DCE8F7;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;color:#174A82;'>Create Account</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#66809F;'>"
    "Join AI-Powered Financial Fraud Detection Platform"
    "</p>",
    unsafe_allow_html=True
)

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input(
        "Confirm Password", type="password"
    )

    submitted = st.form_submit_button(
        "Create Account", use_container_width=True
    )

    if submitted:
        if not all([
            full_name.strip(),
            email.strip(),
            password,
            confirm_password
        ]):
            st.error("Please fill in all fields.")

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()
        ):
            st.error("Enter a valid email address.")

        elif len(password) < 10:
            st.error("Password must be at least 10 characters.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            success = register_user(
                full_name, email, password
            )

            if success:
                st.success("Account created successfully! Please login.")
            else:
                st.error("This email is already registered.")