import streamlit as st

# ===================================================
# SESSION STATE INITIALIZATION
# ===================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "fred": [],
        "greg": [],
        "zoey": [],
        "nora": []
    }

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if st.session_state.current_page not in ["home", "fred", "greg", "zoey", "nora"]:
    st.session_state.current_page = "home"

def navigate_to(page: str):
    st.session_state.current_page = page
    st.rerun()

# ===================================================
# HOME PAGE
# ===================================================

if st.session_state.current_page == "home":
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
        .main-header {
            font-size: 4.2rem;
            color: #ea580c;
            text-align: center;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .tagline {
            font-size: 2.8rem;
            color: #166534;
            text-align: center;
            font-style: italic;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 3rem;
            font-weight: 600;
        }
        .motivation-header { font-size: 2rem; color: #ea580c; text-align: center; font-weight: bold; margin: 2rem 0 1rem 0; }
        .motivation-text { text-align: center; font-size: 1.4rem; line-height: 1.9; margin: 2rem 0 3rem 0; color: #0c4a6e; max-width: 900px; margin-left: auto; margin-right: auto; }
        .agent-name { font-weight: bold; font-size: 1.8rem; color: #ea580c; margin-bottom: 1rem; }
        .agent-subtitle {
            font-weight: bold;
            font-size: 1.4rem;  /* Larger and bold */
            color: #ea580c;
            margin: 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
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

    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR WELLNESS HOME SCOUT</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>A goal-focused realtor. Let's start by generating a detailed report of home options that match your lifestyle needs — anywhere in the U.S.!</div>", unsafe_allow_html=True)
        if st.button("Talk to Fred →", key="fred_home"):
            navigate_to("fred")

    with cols[1]:
        st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR PERSONAL TRAINER</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>A motivated lifestyle coach. Let's start with a workout routine tailored to your fitness goals and health needs to Live Better Longer.</div>", unsafe_allow_html=True)
        if st.button("Talk to Greg →", key="greg_home"):
            navigate_to("greg")

    with cols[2]:
        st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
        st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR HEALTH ASSESSOR</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>A compassionate wellness guide. Ask Zoey any health question. She can help you develop a proactive health lifestyle.</div>", unsafe_allow_html=True)
        if st.button("Talk to Nurse Zoey Zoe →", key="zoey_home"):
            navigate_to("zoey")

    with cols[3]:
        st.markdown("<div class='agent-name'>NORA</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/cJqPm9BP/pexels-tessy-agbonome-521343232-18252407.jpg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR NUTRITION COACH</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>Personalized longevity meal plans, grocery lists — delicious food for a longer life.</div>", unsafe_allow_html=True)
        if st.button("Talk to Nora →", key="nora_home"):
            navigate_to("nora")

    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

# ===================================================
# AGENT PAGES
# ===================================================

elif st.session_state.current_page == "fred":
    import pages.fred as fred_page
    fred_page.show()

elif st.session_state.current_page == "greg":
    import pages.greg as greg_page
    greg_page.show()

elif st.session_state.current_page == "zoey":
    import pages.nurse_zoey_zoe as zoey_page
    zoey_page.show()

elif st.session_state.current_page == "nora":
    import pages.nora as nora_page
    nora_page.show()
