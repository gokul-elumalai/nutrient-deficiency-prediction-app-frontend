import streamlit as st
import requests
from streamlit import switch_page
from utils.constants import AUTH_TOKEN, LOGIN_URL, LOGGED_IN, USERNAME, USER_ID, Button, LOGIN, CustomSuccess, \
    DASHBOARD_PAGE, CustomError, LOGOUT, APP_MAIN_PAGE, TOKEN


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
# API Call
# ------------------------
def authenticate_user(username, password):
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = requests.post(LOGIN_URL, data={"username": username, "password": password}, headers=headers)
    return response


# ------------------------
# Login Logic
# ------------------------
def login_form():
    st.title(Button.SIGN_IN_BUTTON.value)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(LOGIN, help="Click to Sign In"):
        if username and password:
            response = authenticate_user(username, password)

            if response.status_code == 200:
                data = response.json()
                st.session_state.logged_in = True
                st.session_state.username = data.get(USERNAME)
                st.session_state.user_id = data.get(USER_ID)
                st.session_state.token = data.get(TOKEN)

                st.success(CustomSuccess.S0001)
                switch_page(DASHBOARD_PAGE)
            elif response.status_code == 404:
                st.error(response.json()['detail'])
            elif response.status_code == 400:
                st.error(response.json()['detail'])
            else:
                st.error(CustomError.E0002)
        else:
            st.warning(CustomError.E0003)


# ------------------------
# Logout Logic
# ------------------------
def logout_section():
    st.success(f"You're logged in as **{st.session_state.username}**")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:

        if st.button("Go to Dashboard", help="Click to go Dashboard"):
            switch_page(DASHBOARD_PAGE)

    with col3:
        colA, colB = st.columns(2)
        with colB:
            if st.button(LOGOUT, key=Button.LOGOUT_BUTTON, help="Click to logout"):
                for key in [LOGGED_IN, USERNAME, USER_ID, TOKEN]:
                    st.session_state[key] = None if key != LOGGED_IN else False
                switch_page(APP_MAIN_PAGE)




def run():
    st.set_page_config(page_title="Sign In", page_icon="🔐")

    try:

        init_session_state()

        if st.session_state.logged_in:
            logout_section()
        else:
            login_form()

    except requests.exceptions.ConnectionError:
        st.error(CustomError.E0025)
    except Exception as e:
        st.error(CustomError.E0011)


if __name__ == "__main__":
    run()
