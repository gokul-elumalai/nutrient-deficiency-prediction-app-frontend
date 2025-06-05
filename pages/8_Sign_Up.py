import time

import streamlit as st
import requests
from pydantic import EmailStr, BaseModel, Field, ValidationError
from streamlit import switch_page

from utils.constants import LOGIN_URL, LOGGED_IN, USERNAME, USER_ID, AUTH_TOKEN, REGISTER_URL, DASHBOARD_PAGE, \
    CustomError, CustomSuccess, TOKEN


# Pydantic model for local validation
class SignUpForm(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# ------------------------
# Session State Initialization
# ------------------------
def init_session_state():
    defaults = {
        LOGGED_IN: False,
        USERNAME: "",
        USER_ID: None,
        TOKEN: None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ------------------------
# Sign Up Logic
# ------------------------
def signup_form():
    st.title("📝 Create Your NutriApp Account")

    # Sign Up Form
    with st.form("signup_form", clear_on_submit=False):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Create Account", help="Create Account")

    if submit_btn:
        try:
            form = SignUpForm(email=email, password=password, full_name=full_name)

            with st.spinner("Creating your account..."):
                reg_response = requests.post(REGISTER_URL, json=form.model_dump())

            if reg_response.status_code == 200:
                st.success(CustomSuccess.S0002)

                # Automatically log in the user
                login_response = requests.post(LOGIN_URL, data={"username": email, "password": password})

                if login_response.status_code == 200:
                    data = login_response.json()
                    st.session_state.logged_in = True
                    st.session_state.username = data.get(USERNAME)
                    st.session_state.user_id = data.get(USER_ID)
                    st.session_state.token = data.get(TOKEN)
                    st.success(f"Welcome {st.session_state.username.capitalize()}!")
                    st.success(f"Your Email ID is your username")
                    st.success("Redirecting to Dashboard...")

                    time.sleep(6)

                    # Redirect to dashboard
                    switch_page(DASHBOARD_PAGE)
                else:
                    st.error(CustomError.EOOO4)

            else:
                st.error(reg_response.json().get("detail", CustomError.E0005))

        except ValidationError as ve:
            for error in ve.errors():
                st.warning(f"{error['loc'][0].capitalize()}: {error['msg']}")

def run():
    st.set_page_config(page_title="Sign Up | NutriApp")

    try:

        init_session_state()

        signup_form()

    except requests.exceptions.ConnectionError:
        st.error(CustomError.E0025)
    except Exception as e:
        st.error(CustomError.E0011)


if __name__ == "__main__":
    run()