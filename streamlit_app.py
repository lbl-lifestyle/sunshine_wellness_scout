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
    st.session_state.chat_history = {}  # {agent: list of messages}

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
    .chat-container { margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.9); border-radius: 15px; }
    .user-message { background: #ea580c; color: white; padding: 10px; border-radius: 15px; margin: 5px 0; text-align: right; max-width: 80%; margin-left: auto; }
    .assistant-message { background: #f0f0f0; color: #0c4a6e; padding: 10px; border-radius: 15px; margin: 5px 0; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)

# Hero image
st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", use_column_width=True, caption="Your Longevity Blueprint")

# Motivating section
st.markdown("<h2 class='motivation-header'>Unlock Your Vibrant Longevity Lifestyle Today!</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='motivation-text'>
Get ready to <strong>live better longer</strong> than ever before with LBL Lifestyle Solutions—your ultimate holistic longevity blueprint for an active, healthy life anywhere in the U.S.!<br><br>
Our powerhouse team is here to fuel your transformation: Fred the Wellness Home Scout finds your dream active-living paradise, Greg the fired-up Personal Trainer builds custom routines to make you stronger and unstoppable, and Nurse Zoey Zoe the caring Health Assessor delivers proactive insights to keep you thriving.<br><br>
Imagine waking up energized, hitting scenic trails, crushing workouts, and feeling incredible every single day—physically, mentally, and emotionally on fire!<br><br>
Jump in now and unlock the vibrant, joyful life you deserve—your best years are just getting started!
</div>
""", unsafe_allow_html=True)

# Team selection
st.markdown("### MEET THE LIFESTYLE TEAM")
cols = st.columns(3)

with cols[0]:
    st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
    st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR WELLNESS HOME SCOUT* <br>A goal-focused realtor. Lets start by generating a detailed report of home options that match your lifestyle needs — anywhere in the U.S.!</div>", unsafe_allow_html=True)
    if st.button("CLICK HERE TO GET STARTED", key="fred", use_container_width=True):
        st.session_state.selected_agent = "fred"

with cols[1]:
    st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
    st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR PERSONAL TRAINER* <br>A motivated lifestyle coach. Let start with a workout routine tailored to your fitness goals and health needs to Live Better Longer.</div>", unsafe_allow_html=True)
    if st.button("CLICK HERE TO GET STARTED", key="greg", use_container_width=True):
        st.session_state.selected_agent = "greg"

with cols[2]:
    st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
    st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR HEALTH ASSESSOR* <br>A compassionate wellness guide. Ask Zoey any health question. She can help you develop a proactive health lifestyle</div>", unsafe_allow_html=True)
    if st.button("CLICK HERE TO GET STARTED", key="zoey", use_container_width=True):
        st.session_state.selected_agent = "zoey"

st.markdown("---")

# Model
MODEL_NAME = "grok-4-1-fast-reasoning"

# Agent system prompts (personality + boundaries)
def get_system_prompt(agent):
    if agent == "fred":
        return "You are Fred, a professional, goal-focused real estate advisor specializing in wellness and active lifestyle properties across the U.S. You are enthusiastic about helping people find homes that support longevity. Only answer questions about real estate, neighborhoods, locations, cost of living, safety, healthcare access, commute, culture, or lifestyle. If asked about workouts, nutrition, or medical conditions, politely refer to Greg (Fitness) or Nurse Zoey Zoe (Health)."
    elif agent == "greg":
        return "You are Greg, a motivated, energetic personal trainer (gym rat style). You love helping people get stronger and live longer. Only answer questions about workouts, fitness, exercise, strength, endurance. If asked about homes or health conditions, refer to Fred (Home Scout) or Nurse Zoey Zoe (Health)."
    elif agent == "zoey":
        return "You are Nurse Zoey Zoe, a compassionate, caring nurse providing general wellness education. You are warm and reassuring. Only answer general health questions. Never diagnose. If asked about workouts or homes, refer to Greg (Fitness) or Fred (Home Scout). Always end with a reminder to consult a doctor."

# Chat function
def chat_with_agent(agent, user_input):
    if agent not in st.session_state.chat_history:
        st.session_state.chat_history[agent] = []

    # Add user message
    st.session_state.chat_history[agent].append({"role": "user", "content": user_input})

    # Call Grok
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": get_system_prompt(agent)},
                *st.session_state.chat_history[agent]
            ],
            max_tokens=800,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history[agent].append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Sorry, I'm having trouble responding right now. Error: {str(e)}"

# Agent content with chat
if st.session_state.selected_agent:
    agent = st.session_state.selected_agent
    agent_name = "Fred" if agent == "fred" else "Greg" if agent == "greg" else "Nurse Zoey Zoe"

    st.markdown(f"### Chat with {agent_name}")

    # Existing agent content (Fred report, Greg plan, Zoey insights) — keep as is

    # Chat box
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    st.markdown("### Have a follow-up question? Ask me anything in my expertise!")

    # Display chat history
    if agent in st.session_state.chat_history:
        for msg in st.session_state.chat_history[agent]:
            if msg["role"] == "user":
                st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input(f"Ask {agent_name} a question..."):
        with st.spinner("Thinking..."):
            reply = chat_with_agent(agent, prompt)
            st.markdown(f"<div class='assistant-message'>{reply}</div>", unsafe_allow_html=True)
            st.rerun()  # Refresh to show new message

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
