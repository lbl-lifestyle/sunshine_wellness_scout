import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #ffecd2, #fcb69f);
        color: #0c4a6e;
    }
    .main-header { font-size: 3.5rem; color: #ea580c; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); font-weight: bold; }
    .tagline { font-size: 2rem; color: #166534; text-align: center; font-style: italic; margin-bottom: 2rem; }
    .motivation-header { font-size: 2rem; color: #ea580c; text-align: center; font-weight: bold; margin: 2rem 0 1rem 0; }
    .motivation-text { text-align: center; font-size: 1.4rem; line-height: 1.9; margin: 2rem 0 3rem 0; color: #0c4a6e; max-width: 900px; margin-left: auto; margin-right: auto; }
    .agent-name { font-weight: bold; font-size: 1.8rem; color: #ea580c; margin-bottom: 1rem; }
    .agent-desc { min-height: 110px; font-size: 1.1rem; line-height: 1.6; margin: 1rem 0; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
    .chat-container { margin-top: 3rem; padding: 1.5rem; background: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .user-message { background: #ea580c; color: white; padding: 12px; border-radius: 15px; margin: 8px 0; text-align: right; max-width: 80%; margin-left: auto; }
    .assistant-message { background: #f0f0f0; color: #0c4a6e; padding: 12px; border-radius: 15px; margin: 8px 0; max-width: 80%; }
    .back-button { margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)

# Hero image
st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", use_column_width=True, caption="Your Longevity Blueprint")

# Onboarding
st.markdown("<h2 class='motivation-header'>How It Works – 3 Simple Steps</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='motivation-text'>
1. **Choose Your Agent** – Click one of the team members below to get started.<br><br>
2. **Get Personalized Guidance** – Fill out the form or chat — your agent will create a custom report or plan just for you.<br><br>
3. **Build Your Longevity Lifestyle** – Save your reports, come back anytime, and unlock more agents as you go!<br><br>
Ready to live better longer? 👇 Pick an agent below!
</div>
""", unsafe_allow_html=True)

# Back button when agent selected
if st.session_state.selected_agent:
    if st.button("← Back to Team", key="back_to_team"):
        st.session_state.selected_agent = None
        st.session_state.chat_history = {}
        st.rerun()

# Team selection (only if no agent selected)
if not st.session_state.selected_agent:
    st.markdown("### MEET THE LIFESTYLE TEAM")
    st.markdown("<p style='text-align:center; color:#0c4a6e; font-size:1.2rem;'>Click an agent to begin your longevity journey</p>", unsafe_allow_html=True)

    cols = st.columns(3)

    with cols[0]:
        st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
        st.markdown("<div class='agent-desc'>*YOUR WELLNESS HOME SCOUT* <br>A goal-focused realtor. Lets start by generating a detailed report of home options that match your lifestyle needs — anywhere in the U.S.!</div>", unsafe_allow_html=True)
        if st.button("Talk to Fred →", key="fred"):
            st.session_state.selected_agent = "fred"
            st.rerun()

    with cols[1]:
        st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
        st.markdown("<div class='agent-desc'>*YOUR PERSONAL TRAINER* <br>A motivated lifestyle coach. Let start with a workout routine tailored to your fitness goals and health needs to Live Better Longer.</div>", unsafe_allow_html=True)
        if st.button("Talk to Greg →", key="greg"):
            st.session_state.selected_agent = "greg"
            st.rerun()

    with cols[2]:
        st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
        st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
        st.markdown("<div class='agent-desc'>*YOUR HEALTH ASSESSOR* <br>A compassionate wellness guide. Ask Zoey any health question. She can help you develop a proactive health lifestyle</div>", unsafe_allow_html=True)
        if st.button("Talk to Nurse Zoey Zoe →", key="zoey"):
            st.session_state.selected_agent = "zoey"
            st.rerun()

else:
    # Dedicated agent view with auto-scroll to main content
    agent = st.session_state.selected_agent
    agent_name = "Fred" if agent == "fred" else "Greg" if agent == "greg" else "Nurse Zoey Zoe"

    # Anchor for auto-scroll
    st.markdown("<div id='agent-start'></div>", unsafe_allow_html=True)

    # Auto-scroll script (runs once when agent selected)
    st.markdown("""
    <script>
        window.location.hash = 'agent-start';
    </script>
    """, unsafe_allow_html=True)

    # Agent content
    if agent == "fred":
        st.markdown("### 🏡 FRED – Your Wellness Home Scout")
        # ... (rest of Fred's code unchanged)

    elif agent == "greg":
        st.markdown("### 💪 HI!!! IM GREG – Your Awesome Personal Trainer. GET SOME!!!!")
        # ... (rest of Greg's code unchanged)

    elif agent == "zoey":
        st.markdown("### 🩺 GREETINGS. IM NURSE ZOEY ZOE – your friendly nurse assistant, here to support you with compassionate and reliable guidance every step of the way. ")
        # ... (rest of Zoey's code unchanged)

    # Chat box (unchanged)
    # ... (chat code as before)

# Footer
st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
