import streamlit as st
import requests
from streamlit import switch_page

from utils.constants import CustomError, LOGGED_IN, USER_DETAILS_URL, USER_ID, CustomSuccess, GENDERS, CHRONIC_DISEASES, \
    OPTIONS, DIETARY_HABITS, CUISINES, ALLERGIES, FOOD_AVERSIONS, SIGN_IN_PAGE


# --- Authentication Check ---
def authenticate():
    if not st.session_state.get(LOGGED_IN, False):
        st.warning(CustomError.E0001)

        if st.button("🔐 Go to Login Page",help="Go to Login Page"):
            switch_page(SIGN_IN_PAGE)

        st.stop()



# --- Fetch existing user details ---
def fetch_user_details(headers: dict):
    try:
        response = requests.get(USER_DETAILS_URL, headers=headers)

        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 404:
            st.info(CustomError.E0006)
            return False, {}
        else:
            st.error(CustomError.E0007)
            return False, {}
    except requests.exceptions.Timeout:
        st.error(CustomError.E0008)
        st.stop()
    except requests.exceptions.ConnectionError:
        st.error(CustomError.E0009)
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.stop()

# --- Form ---
def user_details_form(form_defaults: dict, is_update: bool, headers: dict, user_id: str):
    with st.form("user_details_form"):
        st.subheader("Personal Info")
        age = st.number_input("Age", min_value=1, max_value=120, value=form_defaults.get("age", 25))
        gender = st.selectbox("Gender", GENDERS, index=GENDERS.index(form_defaults.get("gender", "Male")))
        height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=form_defaults.get("height_cm", 170.0))
        weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=500.0, value=form_defaults.get("weight_kg", 70.0))

        st.subheader("Health Info")
        chronic_disease = st.selectbox("Chronic Disease", CHRONIC_DISEASES,
                                       index=CHRONIC_DISEASES.index(form_defaults.get("chronic_disease", "NA")))
        cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0, value=form_defaults.get("cholesterol_level", 180.0))
        blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=0.0, value=form_defaults.get("blood_sugar_level", 90.0))
        systolic = st.number_input("Blood Pressure - Systolic (mmHg)", min_value=0, value=form_defaults.get("blood_pressure_systolic", 120))
        diastolic = st.number_input("Blood Pressure - Diastolic (mmHg)", min_value=0, value=form_defaults.get("blood_pressure_diastolic", 80))

        st.subheader("Lifestyle")
        daily_steps = st.number_input("Daily Steps", min_value=0, value=form_defaults.get("daily_steps", 5000))
        exercise = st.number_input("Exercise Frequency (times/week)", min_value=0, max_value=7, value=form_defaults.get("exercise_frequency", 3))
        sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=form_defaults.get("sleep_hours", 7.0))
        alcohol = st.selectbox("Alcohol Consumption", OPTIONS, index=OPTIONS.index(form_defaults.get("alcohol_consumption", "No")))
        smoking = st.selectbox("Smoking Habit", OPTIONS, index=OPTIONS.index(form_defaults.get("smoking_habit", "No")))

        st.subheader("Dietary")
        diet = st.selectbox("Dietary Habit", DIETARY_HABITS, index=DIETARY_HABITS.index(form_defaults.get("dietary_habits", "Regular")))
        cuisine = st.selectbox("Preferred Cuisine", CUISINES, index=CUISINES.index(form_defaults.get("preferred_cuisine", "Indian")))
        aversion = st.selectbox("Food Aversion", FOOD_AVERSIONS, index=FOOD_AVERSIONS.index(form_defaults.get("food_aversions", "NA")))
        allergy = st.selectbox("Allergies", ALLERGIES, index=ALLERGIES.index(form_defaults.get("allergies", "NA")))
        genetic = st.selectbox("Genetic Risk Factor", OPTIONS, index=OPTIONS.index(form_defaults.get("genetic_risk_factor", "No")))

        st.subheader("Macronutrient Intake")
        calorie = st.number_input("Calorie Intake (kcal/day)", min_value=0.0, value=form_defaults.get("calorie_intake", 2000.0))
        protein = st.number_input("Protein (g)", min_value=0.0, value=form_defaults.get("protein_intake", 50.0))
        fat = st.number_input("Fat (g)", min_value=0.0, value=form_defaults.get("fat_intake", 70.0))
        carb = st.number_input("Carbohydrates (g)", min_value=0.0, value=form_defaults.get("carbohydrate_intake", 250.0))

        submitted = st.form_submit_button("Update" if is_update else "Save")

    if submitted:
        payload = {
            "age": age,
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "chronic_disease": chronic_disease,
            "cholesterol_level": cholesterol,
            "blood_sugar_level": blood_sugar,
            "blood_pressure_systolic": systolic,
            "blood_pressure_diastolic": diastolic,
            "daily_steps": daily_steps,
            "exercise_frequency": exercise,
            "sleep_hours": sleep,
            "alcohol_consumption": alcohol,
            "smoking_habit": smoking,
            "dietary_habits": diet,
            "preferred_cuisine": cuisine,
            "food_aversions": aversion,
            "allergies": allergy,
            "genetic_risk_factor": genetic,
            "calorie_intake": calorie,
            "protein_intake": protein,
            "fat_intake": fat,
            "carbohydrate_intake": carb,
        }

        try:
            if is_update:
                res = requests.patch(USER_DETAILS_URL, json=payload, headers=headers)
            else:
                payload[USER_ID] = user_id
                res = requests.post(USER_DETAILS_URL, json=payload, headers=headers)

            if res.status_code in (200, 201):
                st.success(CustomSuccess.S0003)
            else:
                st.error(f"Failed to save profile: {res.text}")

        except requests.exceptions.Timeout:
            st.error(CustomError.E0010)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")


def run():
    st.set_page_config(page_title="Update Profile")
    st.title("Update Your Profile")

    try:

        authenticate()

        token = st.session_state.token
        user_id = st.session_state.user_id
        headers = {"Authorization": f"Bearer {token}"}

        is_update, form_defaults = fetch_user_details(headers)
        user_details_form(form_defaults, is_update, headers, user_id)

    except Exception as e:
        st.error(CustomError.E0011)
        st.exception(e)


# Call run() if this script is directly executed
if __name__ == "__main__":
    run()
