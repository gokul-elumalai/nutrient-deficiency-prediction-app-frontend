import pandas as pd
import requests
import streamlit as st
from streamlit import switch_page
import plotly.express as px

from utils.constants import USER_DETAILS_URL, CustomError, LOGGED_IN, LOGOUT, APP_MAIN_PAGE, BMI_Category, \
    LATEST_FOOD_LOG_URL, Button, LOG_FOOD_PAGE, DIET_PREDICT_URL, LOG_DATE, BMI, SIGN_IN_PAGE, NUTRIENT_ANALYSIS_PAGE
from utils.helper import get_bmi_color

def authenticate():
    if not st.session_state.get(LOGGED_IN, False):
        st.warning(CustomError.E0001)

        if st.button("🔐 Go to Login Page"):
            switch_page(SIGN_IN_PAGE)

        st.stop()

def logout_button():
    if st.button(f"⟳ {LOGOUT}", key=Button.LOGOUT_BUTTON, help="Click to logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        switch_page(APP_MAIN_PAGE)

def fetch_user_details(headers):
    try:
        res = requests.get(USER_DETAILS_URL, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            st.info("📌 To unlock full features like BMI analysis and diet recommendations, please update your profile.")
            st.markdown("👉 Go to **User Profile** from the sidebar to update your profile.")
            st.stop()
    except Exception as e:
        st.error("Error fetching user details.")
        st.exception(e)
        st.stop()

def classify_bmi(bmi):
    if bmi < 18.5:
        return BMI_Category.UNDERWEIGHT
    elif 18.5 <= bmi < 25:
        return BMI_Category.NORMAL
    elif 25 <= bmi < 30:
        return BMI_Category.OVERWEIGHT
    else:
        return BMI_Category.OBESE

def fetch_food_logs(headers):
    try:
        res = requests.get(LATEST_FOOD_LOG_URL, headers=headers)
        if res.status_code != 200:
            st.warning(CustomError.E0012)
            st.markdown("👉 Go to **Log Food** from the sidebar.")
            st.button("Log Food Now", on_click=lambda: switch_page(LOG_FOOD_PAGE))
            return pd.DataFrame()

        logs = res.json()
        if not logs:
            st.info(CustomError.E0013)
            st.markdown("👉 Go to **Log Food** from the sidebar to get started.")
            st.stop()

        df = pd.DataFrame(logs)
        if df.empty:
            st.info(CustomError.E0013)
            st.markdown("👉 Go to **Log Food** from the sidebar to get started.")
            st.stop()

        return df
    except Exception as e:
        st.error(CustomError.E0015)
        st.exception(e)
        return pd.DataFrame()

def display_metrics(bmi, bmi_class, df):
    col1, col2 = st.columns(2)
    bmi_color = get_bmi_color(bmi_class)

    col1.markdown(f"""
    <div style='font-size:24px; font-weight:600;'>BMI</div>
    <div style='font-size:36px; color:{bmi_color};'>{bmi} ({bmi_class})</div>
    """, unsafe_allow_html=True)

    avg_cal = round(df['calories'].mean(), 1)
    col2.markdown(f"""
    <div style='font-size:24px; font-weight:600;'>Avg Weekly Calories</div>
    <div style='font-size:36px; color:#2196F3;'>{avg_cal} kcal</div>
    """, unsafe_allow_html=True)

def show_charts(df):
    df[LOG_DATE] = pd.to_datetime(df[LOG_DATE])#.dt.date
    daily_cal = df.groupby(LOG_DATE)['calories'].sum().reset_index()

    st.subheader("Your Weekly Nutrition Overview")

    st.markdown("#### Calories from Last 7 days")
    # daily_cal[LOG_DATE] = pd.to_datetime(daily_cal[LOG_DATE]).dt.date
    line_fig = px.line(daily_cal, x=LOG_DATE, y='calories', markers=True)
    line_fig.update_layout(
        xaxis_tickformat="%b %d %H:%M",  # Example: Jun 03 14:15
        xaxis_title="Date",
        yaxis_title="Calories (kcal)",
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        font=dict(size=16)
    )
    st.plotly_chart(line_fig, use_container_width=True)

    st.markdown("#### Macronutrient Breakdown")
    macros = df[['protein', 'fat', 'carbs']].sum().to_dict()
    macro_df = pd.DataFrame.from_dict({k.capitalize(): v for k, v in macros.items()}, orient='index', columns=['g']).reset_index()
    macro_df.columns = ['Macronutrient', 'g']
    bar_fig = px.bar(macro_df, x='Macronutrient', y='g', text='g', color='Macronutrient')
    bar_fig.update_layout(
        xaxis_title="Macronutrient",
        yaxis_title="Grams (g)",
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        legend_title_font=dict(size=16),
        legend=dict(font=dict(size=16)),
        font=dict(size=14)
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown("#### Meal Type Distribution")
    meal_dist = df['meal_type'].value_counts()
    pie_fig = px.pie(names=[m.capitalize() for m in meal_dist.index], values=meal_dist.values)
    pie_fig.update_layout(
        legend=dict(font=dict(size=16)),
        font=dict(size=14)
    )
    st.plotly_chart(pie_fig, use_container_width=True)

def show_diet_recommendation(user_data, headers):
    st.subheader("🍽️ Personalized Diet Recommendation")
    try:
        res = requests.post(DIET_PREDICT_URL, json=user_data, headers=headers)
        if res.status_code == 200:
            recommendation = res.json().get("recommendation", "no recommendation available.").capitalize()
            st.markdown(f"<div style='font-size:18px; color: green; font-weight: 600;'>✅ {recommendation}</div>", unsafe_allow_html=True)
        else:
            st.warning(CustomError.E0014)

        st.divider()
        if st.button("📊 Check out Nutrient Analysis Page", help="Click to go Nutrient Analysis Page"):
            switch_page(NUTRIENT_ANALYSIS_PAGE)

    except Exception as e:
        st.error(CustomError.E0016)
        st.exception(e)

def run():
    try:
        st.set_page_config(page_title="Nutri Dashboard")

        authenticate()

        st.title(f"👋 Welcome, {st.session_state.username.capitalize()}!")
        st.sidebar.success(f"Welcome {st.session_state.username.capitalize()} 👋")
        logout_button()

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        user_data = fetch_user_details(headers)
        bmi = user_data.get(BMI)
        bmi_class = classify_bmi(bmi)

        df = fetch_food_logs(headers)

        display_metrics(bmi, bmi_class, df)
        st.divider()
        show_charts(df)
        st.divider()
        show_diet_recommendation(user_data, headers)

    except requests.exceptions.ConnectionError:
        st.error(CustomError.E0025)
    except Exception as e:
        st.error(CustomError.E0011)


if __name__ == "__main__":
    run()
