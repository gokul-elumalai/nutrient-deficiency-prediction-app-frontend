import time
import streamlit as st
import requests
from streamlit import switch_page

from utils.constants import DELETE_USER_URL, LOGGED_IN, CustomError, SIGN_IN_PAGE, CustomSuccess, APP_MAIN_PAGE


def authenticate_user():
    """Ensure the user is logged in; otherwise, redirect to login page."""
    if not st.session_state.get(LOGGED_IN, False):
        st.warning(CustomError.E0001)
        if st.button("🔐 Go to Login Page", help="Go to Login Page"):
            switch_page(SIGN_IN_PAGE)
        st.stop()


def delete_user_account(password: str):
    """Send DELETE request to delete the user account."""
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    params = {"confirmation_pwd": password}
    return requests.delete(DELETE_USER_URL, headers=headers, params=params)


def clear_session_and_redirect():
    """Clear session state and redirect to home."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.token = ""
    st.session_state.user_id = None

    st.success(CustomSuccess.S0006)
    st.info("You will be redirected shortly...")
    time.sleep(2)
    switch_page(APP_MAIN_PAGE)


def render_delete_form():
    """Render the delete account form UI."""
    st.title("⚠️ Delete Your Account")
    st.error("This action is irreversible. All your data will be permanently deleted.")

    password = st.text_input("Re-enter your password to confirm", type="password")
    confirm = st.checkbox("I understand the consequences and want to delete my account")

    if st.button("🗑️ Delete My Account", type="primary", disabled=not (password and confirm), help="Delete Account"):
        with st.spinner("Deleting your account..."):
            response = delete_user_account(password)

        if response.status_code == 200:
            clear_session_and_redirect()
        else:
            st.error(response.json().get("detail", CustomError.E0024))


def run():
    st.set_page_config(page_title="Delete Account | NutriApp")

    try:
        authenticate_user()
        render_delete_form()

    except requests.exceptions.ConnectionError:
        st.error(CustomError.E0025)
    except Exception as e:
        st.error(CustomError.E0011)
        # st.exception(e)


if __name__ == "__main__":
    run()
