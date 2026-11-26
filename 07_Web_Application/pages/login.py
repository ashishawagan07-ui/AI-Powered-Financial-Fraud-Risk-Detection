import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import initialize_database
from utils.auth import authenticate_user

initialize_database()

st.set_page_config(
    page_title="Login | AI Fraud Detection",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #EAF3FF, #FFFFFF);
}
[data-testid="stForm"] {
    background: white;
    padding: 25px;
    border: 1px solid #DCE8F7;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;color:#174A82;'>"
    "AI FRAUD DETECTION"
    "</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#66809F;'>"
    "Secure Login Portal | Version 2026"
    "</p>",
    unsafe_allow_html=True
)

with st.form("login_form"):
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button(
        "Login", use_container_width=True
    )

    if submitted:
        if not email or not password:
            st.error("Enter email and password.")

        else:
            user = authenticate_user(email, password)

            if user:
                st.session_state["user"] = user
                st.success(f"Welcome, {user['full_name']}!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

st.markdown("---")
st.write("New user? Open the Register page from the sidebar.")