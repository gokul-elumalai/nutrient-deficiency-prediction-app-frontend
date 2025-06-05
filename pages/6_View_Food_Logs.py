import streamlit as st
import requests
import pandas as pd
from streamlit import switch_page

from utils.constants import (
    FOOD_LOG_URL, NUMERIC_NUTRIENTS, CustomError,
    SIGN_IN_PAGE, DELETE_FOOD_LOG_URL_TEMPLATE, LOG_DATE, CustomSuccess, LOGGED_IN
)
from utils.helper import prepare_view


def authenticate():
    """Check if the user is logged in; if not, show login button and stop."""
    if not st.session_state.get(LOGGED_IN, False):
        st.warning(CustomError.E0001)
        if st.button("🔐 Go to Login Page", help="Go to Login Page"):
            switch_page(SIGN_IN_PAGE)
        st.stop()


def fetch_food_logs():
    """Fetch food logs from API."""
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    return requests.get(FOOD_LOG_URL, headers=headers)


def delete_log(log_id):
    """Delete a specific food log entry by ID."""
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    return requests.delete(DELETE_FOOD_LOG_URL_TEMPLATE.format(log_id), headers=headers)


def render_log_entry(row, log_id, index):
    """Render a single food log entry as an expandable panel."""
    row = row.to_dict()
    date = row.pop('Date').date()

    meal_type = row.pop('Meal Type').capitalize()
    food = row.pop('Food')
    row.pop('id', None)

    with st.expander(f"{date} - {meal_type} - {food}"):
        st.markdown(prepare_view(row), unsafe_allow_html=True)

        if st.button("🗑️ Delete", key=f"delete_{index}", help="Delete Food Log"):
            delete_resp = delete_log(log_id)
            if delete_resp.status_code == 200:
                st.success(CustomSuccess.S0005)
            else:
                st.error(CustomError.E0021)


def display_food_logs():
    """Fetch, process, and display user's food logs."""
    try:
        response = fetch_food_logs()

        if response.status_code != 200:
            detail = response.json().get('detail', 'Unknown error')
            st.error(f"{CustomError.E0020}: {detail}")
            return

        logs = response.json().get('data', [])
        st.subheader("📒 Your Latest Food Logs")

        if not logs:
            st.info(CustomError.EOO19)
            return

        df = pd.DataFrame(logs)

        # Data Cleaning
        for col in NUMERIC_NUTRIENTS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

        df[LOG_DATE] = pd.to_datetime(df[LOG_DATE])
        df = df.sort_values(by=LOG_DATE, ascending=False)

        # Rename for display
        df = df.rename(columns={
            "log_date": "Date",
            "meal_type": "Meal Type",
            "food": "Food"
        })

        for i, row in df.iterrows():
            row_id = logs[i].get("id")
            render_log_entry(row, row_id, i)

    except Exception as e:
        st.error(f"Error {e}")


def run():
    st.set_page_config(page_title="View Food Logs")

    try:

        authenticate()
        display_food_logs()

    except Exception as e:
        st.error(CustomError.E0011)
        st.exception(e)


if __name__ == "__main__":
    run()
