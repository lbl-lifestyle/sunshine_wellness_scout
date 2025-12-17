import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Florida-themed CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #ffecd2, #fcb69f);
        color: #0c4a6e;
    }
    .main-header { font-size: 3rem; color: #ea580c; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .tagline { font-size: 1.8rem; color: #166534; text-align: center; font-style: italic; margin-bottom: 2rem; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Hero image: Biker on sunset beach path with palms
st.image("https://www.shutterstock.com/image-photo/happiness-woman-traveler-her-bicycle-600nw-1396832807.jpg", use_column_width=True, caption="Your Florida Longevity Lifestyle – Active Trails at Sunset")

st.markdown("<h1 class='main-header'>LBL Wellness Solutions</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Your Holistic Longevity Blueprint</p>", unsafe_allow_html=True)

st.success("**This tool is completely free – no cost, no obligation!**")
st.write("Discover Florida homes that support your active, wellness-focused lifestyle – trails, natural light, home gym space, waterfront access, and more.")

# Wellness group image: Beach yoga/fitness class
st.image("https://www.annamaria.com/wp-content/uploads/2020/07/beachyoga-690x460.jpg", use_column_width=True, caption="Community wellness and group fitness – part of your longevity blueprint")

# Inputs
client_needs = st.text_area("Describe your dream wellness/active home in Florida", height=220, placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
with col2:
    location = st.text_input("Preferred area in Florida", value="Tampa Bay, St. Petersburg, Clearwater, Brandon")

if st.button("🔍 Show Me Free Teaser Matches", type="primary"):
    # (Full Grok prompt, response, teaser building, form, email sending – same as your last working version)
    # Paste the full block from your previous code here

    # Modern home image
    st.image("https://vankirkpools.com/wp-content/uploads/2025/03/florida-swimming-pool.jpg", use_column_width=True, caption="Modern Florida homes designed for wellness and natural light")

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Real estate recommendations powered by AI • Not affiliated with any brokerage</small>", unsafe_allow_html=True)
