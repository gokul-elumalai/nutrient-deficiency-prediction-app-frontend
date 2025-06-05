import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from streamlit import switch_page

from utils.constants import CustomError, SIGN_IN_PAGE, LOGGED_IN, NUTRIENT_ANALYSIS_URL, DISPLAY_NAME_MAP


# ---------------- Auth Check ----------------
def authenticate():
    if not st.session_state.get(LOGGED_IN, False):
        st.warning(CustomError.E0001)
        if st.button("🔐 Go to Login Page"):
            switch_page(SIGN_IN_PAGE)
        st.stop()


# ---------------- Data Fetching ----------------
def fetch_nutrient_data():

    token = st.session_state.get("token")

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(NUTRIENT_ANALYSIS_URL, headers=headers)
        if response.status_code != 200:
            st.error(CustomError.E0022)
            st.stop()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()


# ---------------- Data Preparation ----------------
def prepare_nutrient_dataframe(data):
    avg = data["average"]
    rec = data["recommended"]
    nutrients = [DISPLAY_NAME_MAP.get(nutrient, "") for nutrient in avg.keys()]

    df = pd.DataFrame({
        "Nutrient": nutrients,
        "Average": avg.values(),
        "Recommended": rec.values()
    })
    df["% Met"] = (df["Average"] / df["Recommended"] * 100).round(2)
    return df


# ---------------- Styling ----------------
def highlight(val):
    if val < 70:
        return 'background-color: #f08080'  # red
    elif val < 100:
        return 'background-color: #fffacd'  # yellow
    return 'background-color: #90ee90'      # green


def render_styled_table(df):
    st.subheader("📋 Nutrient Intake Table")
    styled_df = (
        df.style
        .applymap(highlight, subset=["% Met"])
        .format(precision=2)
        .set_table_styles([
            {'selector': 'td', 'props': [('font-size', '16px')]},
            {'selector': 'th', 'props': [('font-size', '18px')]}
        ])
    )
    st.markdown(styled_df.to_html(), unsafe_allow_html=True)


# ---------------- Plot ----------------
def render_bar_chart(df):
    st.subheader("📉 Actual vs Recommended Nutrient Intake")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["Nutrient"], y=df["Average"], name="Average Intake"))
    fig.add_trace(go.Bar(x=df["Nutrient"], y=df["Recommended"], name="Recommended Intake"))

    fig.update_layout(
        barmode="group",
        xaxis_tickangle=-45,
        font=dict(size=18),
        xaxis=dict(
            title="Nutrient",
            title_font=dict(size=20),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title="Intake Value (mg)",
            title_font=dict(size=20),
            tickfont=dict(size=16)
        ),
        legend=dict(
            font=dict(size=18)
        )
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------- Main ----------------
def run():

    st.set_page_config(page_title="Nutrient Analysis", layout="wide")
    st.title("📊 Macro & Micro Nutrient Analysis")

    try:
        authenticate()
        data = fetch_nutrient_data()
        df = prepare_nutrient_dataframe(data)
        render_styled_table(df)
        render_bar_chart(df)

    except requests.exceptions.ConnectionError:
        st.error(CustomError.E0025)
    except Exception as e:
        st.error(CustomError.E0011)


if __name__ == "__main__":
    run()
