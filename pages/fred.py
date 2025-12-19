import streamlit as st
import requests
from openai import OpenAI
import re

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

MODEL_NAME = "grok-4-1-fast-reasoning"

# CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
    .chat-container { margin-top: 3rem; padding: 1.5rem; background: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .user-message { background: #ea580c; color: white; padding: 12px; border-radius: 15px; margin: 8px 0; text-align: right; max-width: 80%; margin-left: auto; }
    .assistant-message { background: #f0f0f0; color: #0c4a6e; padding: 12px; border-radius: 15px; margin: 8px 0; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to Team"):
    st.session_state.selected_agent = None
    st.session_state.chat_history = {}
    st.rerun()

# Auto-scroll anchor
st.markdown("<div id='agent-interaction'></div>", unsafe_allow_html=True)
st.markdown("""
<script>
    const element = document.getElementById('agent-interaction');
    if (element) element.scrollIntoView({ behavior: 'smooth', block: 'start' });
</script>
""", unsafe_allow_html=True)

# Hero image
st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg-J1J8SDEAY-unsplash.jpg", use_column_width=True, caption="Your Keys Await – Welcome to your longevity lifestyle")

st.markdown("### 🏡 FRED – Your Wellness Home Scout")
st.success("**This tool is completely free – no cost, no obligation! You will receive the full personalized report below and via email.**")
st.write("The perfect home that supports your lifestyle awaits — anywhere in the U.S.!")

# (full Fred report generation code — same as before)

# Chat box (same as before)

st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
