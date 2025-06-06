from enum import Enum, unique

# === Backend Base URL ===
# BACKEND_URL = "http://localhost:8000/api/v1"
BACKEND_URL = "https://a97a-2401-4900-93ed-1784-fdcb-86b3-e5d0-a27.ngrok-free.app/api/v1"

# === Authentication ===
LOGIN_URL = f"{BACKEND_URL}/auth/login/access-token"
AUTH_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJleHAiOjE3NDU2NzgyNjQsInN1YiI6IjEzNTA3MjUxLTkxZmEtNDI1MS05NDY5LWZmYjk5MWU3N2VjMiJ9."
    "X4fEOk_CopHgJSDIe5yVPNds5KZQRBfxhy3vHYUO0D0"
)

# === Food Log ===
FOOD_LOG_URL = f"{BACKEND_URL}/food-log"
LATEST_FOOD_LOG_URL = f"{FOOD_LOG_URL}/latest/?days=7"
DELETE_FOOD_LOG_URL_TEMPLATE = f"{FOOD_LOG_URL}/{{}}"  # format with log ID
DIET_PREDICT_URL = f"{BACKEND_URL}/predict/diet"
NUTRIENT_ANALYSIS_URL = f"{FOOD_LOG_URL}/nutrition-summary/"

# === User Details ===
USER_DETAILS_URL = f"{BACKEND_URL}/user-details"
REGISTER_URL = f"{BACKEND_URL}/user/register"
DELETE_USER_URL = f"{BACKEND_URL}/user/delete"

# === Streamlit Pages ===
APP_MAIN_PAGE = "Home.py"
SIGN_UP_PAGE = "pages/8_Sign_Up.py"
SIGN_IN_PAGE = "pages/7_Sign_In.py"
DASHBOARD_PAGE = "pages/2_User_Dashboard.py"
LOG_FOOD_PAGE = "pages/4_Log_Food"
NUTRIENT_ANALYSIS_PAGE = "pages/5_Nutrient_Analysis.py"
VIEW_FOOD_LOG_PAGE = "pages/6_View_Food_Logs.py"


# Streamlit Constants

LOGGED_IN = "logged_in"
LOGIN = "Login"
LOGOUT = "Logout"
USERNAME = "username"
USER_ID = "user_id"
TOKEN = "token"


@unique
class Button(str, Enum):
    SIGN_UP_BUTTON = "📝 Sign Up"
    SIGN_IN_BUTTON = "🔐 Sign In"
    LOGOUT_BUTTON = "logout_button"

    def __str__(self):
        return self.value



# Field names
BMI = "bmi"
GENDERS = ["Male", "Female", "Other"]
CHRONIC_DISEASES = ["NA", "Diabetes", "Heart Disease", "Hypertension", "Obesity"]
OPTIONS = ["No", "Yes"]
DIETARY_HABITS = ["Regular", "Keto", "Vegetarian", "Vegan"]
CUISINES = ["Indian", "Asian", "Western", "Mediterranean"]
FOOD_AVERSIONS = ["NA", "Spicy", "Sweet", "Salty"]
ALLERGIES = ["NA", "Lactose Intolerance", "Nut Allergy", "Gluten Intolerance"]
LOG_DATE = 'log_date'
NUMERIC_NUTRIENTS = ['calories', 'protein', 'carbs', 'fat']

DISPLAY_NAME_MAP = {
    'calories': 'Calories (kcal)',
    'protein': 'Protein (g)',
    'fat': 'Fat (g)',
    'carbs': 'Carbohydrate (g)',
    'fiber': "Fiber (g)",
    'sugar': "Sugar (g)",
    'sodium': "Sodium (g)",
    'potassium': "Potassium (g)",
    'iron': "Iron (g)",
    'calcium': "Calcium (g)",
    'vitamin_a': "Vitamin A (IU)",
    'vitamin_c': "Vitamin C (IU)",
    'saturated_fat':'Saturated Fat',
    'trans_fat': "Trans Fat",
    'polyunsaturated_fat': "Polyunsaturated Fat",
    "monounsaturated_fat": "Monounsaturated Fat"
}


@unique
class CustomError(str, Enum):
    E0001 = "You must be logged in to view this page."
    E0002 = "Invalid credentials. Please try again."
    E0003 = "Please enter both username and password."
    EOOO4 = "Account created but automatic login failed. Please sign in manually."
    E0005 = "Registration failed."
    E0006 = "You haven't filled in your profile details yet."
    E0007 = "Failed to fetch user details."
    E0008 = "The request timed out. Please check your connection."
    E0009 = "Failed to connect to the backend. Try again later."
    E0010 = "Request timed out while saving your profile."
    E0011 = "⚠️ An unexpected error occurred. Please try again."
    E0012 = "No food logs available yet. Start by logging your first meal!"
    E0013 = "You're all set! But it looks like you haven't logged any food yet."
    E0014 = "Could not fetch diet recommendation at the moment."
    E0015 = "Failed to fetch food logs"
    E0016 = "Failed to fetch diet recommendation."
    E0017 = "Error saving food log."
    E0018 = "⚠️ Network error. Please check your internet connection."
    EOO19 = "No food logs found."
    E0020 = "❌ Failed to delete."
    E0021 = "Failed to fetch nutrient data."
    E0022 = "⚠️ Please enter a valid food name."
    E0023 = "❌ Please enter a non-zero calorie value."
    E0024 = "❌ Failed to delete your account."
    E0025 = "⚠️ Cannot connect to the server. Please check your internet connection or try again later."

    def __str__(self):
        return self.value


@unique
class CustomSuccess(str, Enum):
    S0001 = "Login successful!"
    S0002 = "Account created successfully! Logging you in..."
    S0003 = "User profile saved successfully!"
    S0004 = "Food log created successfully."
    S0005 = "✅ Deleted successfully. Please refresh the page."
    S0006 = "✅ Your account has been deleted successfully."

    def __str__(self):
        return self.value


@unique
class BMI_Category(str, Enum):
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal"
    OVERWEIGHT = "Overweight"
    OBESE = "Obese"

    def __str__(self):
        return self.value

