import streamlit as st
import requests
from datetime import date
from streamlit import switch_page

from utils.constants import (
    FOOD_LOG_URL, CustomError, CustomSuccess,
    SIGN_IN_PAGE, LOGGED_IN, VIEW_FOOD_LOG_PAGE
)


def authenticate():
    if not st.session_state.get(LOGGED_IN, False):
        st.warning(CustomError.E0001)
        if st.button("🔐 Go to Login Page", help="Go to Login Page"):
            switch_page(SIGN_IN_PAGE)
        st.stop()


def render_food_log_form():
    with st.form("food_log_form"):
        log_date = st.date_input("Date", value=date.today())
        food = st.text_input("Food Item")
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])

        nutrients = {
            "calories": st.number_input("Calories", min_value=0.0),
            "carbs": st.number_input("Carbs (g)", min_value=0.0),
            "protein": st.number_input("Protein (g)", min_value=0.0),
            "fat": st.number_input("Fat (g)", min_value=0.0),
            "sugar": st.number_input("Sugar (g)", min_value=0.0, format="%.2f"),
            "sodium": st.number_input("Sodium (mg)", min_value=0.0, format="%.2f"),
            "potassium": st.number_input("Potassium (mg)", min_value=0.0, format="%.2f"),
            "fiber": st.number_input("Fiber (g)", min_value=0.0, format="%.2f"),
            "iron": st.number_input("Iron (mg)", min_value=0.0, format="%.2f"),
            "calcium": st.number_input("Calcium (mg)", min_value=0.0, format="%.2f"),
            "cholesterol": st.number_input("Cholesterol (mg)", min_value=0.0, format="%.2f"),
            "vitamin_a": st.number_input("Vitamin A (IU)", min_value=0.0, format="%.2f"),
            "vitamin_c": st.number_input("Vitamin C (mg)", min_value=0.0, format="%.2f"),
            "saturated_fat": st.number_input("Saturated Fat (g)", min_value=0.0, format="%.2f"),
            "trans_fat": st.number_input("Trans Fat (g)", min_value=0.0, format="%.2f"),
            "polyunsaturated_fat": st.number_input("Polyunsaturated Fat (g)", min_value=0.0, format="%.2f"),
            "monounsaturated_fat": st.number_input("Monounsaturated Fat (g)", min_value=0.0, format="%.2f"),
        }

        submitted = st.form_submit_button("Submit Food Log")
        if submitted:

            if submitted:
                errors = []
                if not food.strip():
                    errors.append(CustomError.E0022)
                if nutrients['calories'] <= 0:
                    errors.append(CustomError.E0023)

                if errors:
                    for e in errors:
                        st.warning(e)
                else:
                    payload = {
                        "log_date": str(log_date),
                        "food": food,
                        "meal_type": meal_type,
                        "user_id": st.session_state.user_id,
                        **nutrients
                    }
                    return payload
    return None


def submit_food_log(payload):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    try:
        response = requests.post(FOOD_LOG_URL, json=payload, headers=headers)
        if response.status_code == 201:
            st.success(CustomSuccess.S0004)

        else:
            st.error(CustomError.E0017)
    except requests.exceptions.RequestException:
        st.error(CustomError.E0018)
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")


def run():
    st.title("🍽️ Log Your Food Intake")

    try:
        authenticate()
        payload = render_food_log_form()
        if payload:
            submit_food_log(payload)

        st.divider()
        if st.button("View Food Logs", help="Click to go view food logs"):
            switch_page(VIEW_FOOD_LOG_PAGE)

    except Exception as e:
        st.error(CustomError.E0011)
        st.exception(e)


if __name__ == "__main__":
    run()
