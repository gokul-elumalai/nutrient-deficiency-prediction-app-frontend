import time

import streamlit as st
import requests

from utils.constants import BACKEND_URL

DELETE_URL = f"{BACKEND_URL}/user/delete"

st.set_page_config(page_title="Delete Account | NutriApp")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to be logged in to delete your account.")
    st.stop()

st.title("⚠️ Delete Your Account")

st.error("This action is irreversible. All your data will be permanently deleted.")


# Optional: Ask for password again for security
password = st.text_input("Re-enter your password to confirm", type="password")

# Confirmation checkbox
confirm = st.checkbox("I understand the consequences and want to delete my account")

if st.button("🗑️ Delete My Account", type="primary", disabled=not confirm or not password, help="Delete Account"):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    with st.spinner("Deleting your account..."):
        params = {'confirmation_pwd': password}
        response = requests.delete(DELETE_URL, headers=headers, params=params)

    if response.status_code == 200:
        st.success("Your account has been deleted successfully.")

        # Clear session state
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        st.session_state.user_id = None

        st.success("You will be redirected shortly...")
        time.sleep(2)  # Wait for 2 seconds
        st.switch_page("Home.py")

    else:
        st.error(response.json().get("detail", "Failed to delete your account."))
