import streamlit as st
from streamlit import switch_page

from utils.constants import Button, SIGN_IN_PAGE, SIGN_UP_PAGE

st.set_page_config(
    page_title="NutriApp",
    page_icon="🍏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styles
st.markdown("""
    <style>
    body, .main {
        background-color: #eff1f0;
    }
    .banner {
        text-align: center;
        padding: 3rem 1rem 2rem;
        animation: fadeIn 1.5s ease-in-out;
    }
    .banner h1 {
        font-size: 3rem;
        color: #eff1f0;  /* Dark Grey */
        margin-bottom: 0.5rem;
    }
    .banner p {
        font-size: 1.25rem;
        color: #94a0a0;  /* Grey */
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
    }
    .stButton button {
        border-radius: 30px !important;
        padding: 0.6rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        background-color: #4CAF50;
        color: #151616;
        border: none;
    }
    .stButton button:hover {
        background-color: #388E3C;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
""", unsafe_allow_html=True)

# Banner
st.markdown("""
    <div class="banner">
        <h1>Stay Healthy, Stay Empowered.</h1>
        <p>Join NutriApp to track your meals, analyze your nutrition, and stay on top of your health goals.</p>
    </div>
""", unsafe_allow_html=True)


# Centered Sign In and Sign Up buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    colA, colB = st.columns(2)
    with colA:
        if st.button(Button.SIGN_IN_BUTTON, help="Click to Sign In"):
            switch_page(SIGN_IN_PAGE)

    with colB:
        if st.button(Button.SIGN_UP_BUTTON, help="Click to Sign Up"):
            switch_page(SIGN_UP_PAGE)
