import streamlit as st

# CSS (updated — removed deprecated use_column_width)
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
    .main-header { font-size: 3.5rem; color: #ea580c; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); font-weight: bold; }
    .tagline { font-size: 2rem; color: #166534; text-align: center; font-style: italic; margin-bottom: 2rem; }
    .motivation-header { font-size: 2rem; color: #ea580c; text-align: center; font-weight: bold; margin: 2rem 0 1rem 0; }
    .motivation-text { text-align: center; font-size: 1.4rem; line-height: 1.9; margin: 2rem 0 3rem 0; color: #0c4a6e; max-width: 900px; margin-left: auto; margin-right: auto; }
    .agent-name { font-weight: bold; font-size: 1.8rem; color: #ea580c; margin-bottom: 1rem; }
    .agent-desc { min-height: 110px; font-size: 1.1rem; line-height: 1.6; margin: 1rem 0; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)

st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", caption="Your Longevity Blueprint")

st.markdown("<h2 class='motivation-header'>How It Works – 3 Simple Steps</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='motivation-text'>
1. **Choose Your Agent** – Click one of the team members below to get started.<br><br>
2. **Get Personalized Guidance** – Fill out the form or chat — your agent will create a custom report or plan just for you.<br><br>
3. **Build Your Longevity Lifestyle** – Save your reports, come back anytime, and unlock more agents as you go!<br><br>
Ready to live better longer? 👇 Pick an agent below!
</div>
""", unsafe_allow_html=True)

st.markdown("### MEET THE LIFESTYLE TEAM")
st.markdown("<p style='text-align:center; color:#0c4a6e; font-size:1.2rem;'>Click an agent to begin your longevity journey</p>", unsafe_allow_html=True)

cols = st.columns(3)

with cols[0]:
    st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
    st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR WELLNESS HOME SCOUT* <br>A goal-focused realtor. Let's start by generating a detailed report of home options that match your lifestyle needs — anywhere in the U.S.!</div>", unsafe_allow_html=True)
    if st.button("Talk to Fred →", key="fred"):
        st.switch_page("pages/fred.py")

with cols[1]:
    st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
    st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR PERSONAL TRAINER* <br>A motivated lifestyle coach. Let's start with a workout routine tailored to your fitness goals and health needs to Live Better Longer.</div>", unsafe_allow_html=True)
    if st.button("Talk to Greg →", key="greg"):
        st.switch_page("pages/greg.py")

with cols[2]:
    st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
    st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR HEALTH ASSESSOR* <br>A compassionate wellness guide. Ask Zoey any health question. She can help you develop a proactive health lifestyle.</div>", unsafe_allow_html=True)
    if st.button("Talk to Nurse Zoey Zoe →", key="zoey"):
        st.switch_page("pages/nurse_zoey_zoe.py")

st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
