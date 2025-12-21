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
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: linear-gradient(to bottom, #f5f7fa, #e0e7f0);
            color: #1e3a2f;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3, .main-header {
            font-family: 'Playfair Display', serif;
            color: #2d6a4f;
            font-weight: 600;
        }
        .main-header {
            font-size: 4.2rem;
            text-align: center;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
            margin-bottom: 0.5rem;
        }
        .tagline {
            font-size: 2.8rem;
            color: #40916c;
            text-align: center;
            font-style: italic;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 3rem;
            font-weight: 600;
        }
        .opening-statement {
            font-size: 1.35rem;
            line-height: 1.8;
            text-align: center;
            max-width: 900px;
            margin: 40px auto;
            padding: 30px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.05);
            color: #1e3a2f;
        }
        .opening-statement strong {
            color: #2d6a4f;
            font-weight: 600;
        }
        .agent-name {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            color: #2d6a4f;
            text-align: center;
            margin-bottom: 1rem;
        }
        .agent-subtitle {
            font-weight: bold;
            font-size: 1.4rem;
            color: #2d6a4f;
            text-align: center;
            margin: 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .agent-examples {
            font-size: 1.05rem;
            color: #1e3a2f;
            text-align: center;
            margin: 1rem 0;
            font-style: italic;
        }
        .stButton>button {
            background-color: #2d6a4f;
            color: white;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            height: 3.5em;
            width: 100%;
            border: none;
            box-shadow: 0 4px 8px rgba(45, 106, 79, 0.2);
        }
        .stButton>button:hover {
            background-color: #40916c;
        }
        img {
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)
    
    # NEW VIDEO EMBED — clean, looping, no distractions
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 40px 0; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.1);">
        <iframe width="800" height="450" 
                src="https://www.youtube.com/embed/IhiRZbkENGo?autoplay=1&mute=0&loop=1&playlist=IhiRZbkENGo&controls=1&rel=0&modestbranding=1&playsinline=1&end=28" 
                title="LBL Lifestyle Solutions – Live Better Longer" 
                frameborder="0" 
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
    </iframe>
    </div>
    """, unsafe_allow_html=True)
       
    
    # VERSION 1 OPENING STATEMENT
    st.markdown("""
    <div class='opening-statement'>
    The future is now — and it's personal.<br><br>
    Imagine having your own team of world-class longevity experts working for you 24/7: a wellness-focused home advisor, personal trainer, nutrition coach, and health educator — all coordinating to build the exact lifestyle that helps you thrive for decades.<br><br>
    No generic plans. No conflicting advice. Just clear, joyful steps tailored to <strong>your</strong> goals, <strong>your</strong> body, <strong>your</strong> life.<br><br>
    And the crazy part? This level of guidance would cost <strong>$10,000–$20,000+ a year</strong> if you hired each specialist individually. Here, you get the full team — instantly, privately, and always evolving as the AI gets smarter every day.<br><br>
    You're not just keeping up. You're using tomorrow's tools today to get ahead — while others are still searching for answers.<br><br>
    Ready to meet your team and start living better longer?
    </div>
    """, unsafe_allow_html=True)

    st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", caption="Your Longevity Blueprint")

    st.markdown("<h2>How It Works – 3 Simple Steps</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; font-size: 1.4rem; line-height: 1.9; max-width: 900px; margin: auto;'>
    1. **Choose Your Agent** – Click one of the team members below to get started.<br><br>
    2. **Get Personalized Guidance** – Fill out the form or chat — your agent will create a custom report or plan just for you.<br><br>
    3. **Build Your Longevity Lifestyle** – Save your reports, come back anytime, and unlock more agents as you go!<br><br>
    Ready to live better longer? 👇 Pick an agent below!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### MEET THE LIFESTYLE TEAM")
    st.markdown("<p style='text-align:center; color:#1e3a2f; font-size:1.2rem;'>Click an agent to begin your longevity journey</p>", unsafe_allow_html=True)

    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR WELLNESS HOME SCOUT</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>A goal-focused advisor helping you find or create a home that supports your health and longevity.</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-examples'>Examples:<br>• Find quiet neighborhoods with trails near Tampa<br>• Suggest homes with gym space under $600k<br>• Compare walkability in Asheville vs Sarasota<br>• Modify my current home for aging in place</div>", unsafe_allow_html=True)
        if st.button("Talk to Fred →", key="fred_home"):
            navigate_to("fred")

    with cols[1]:
        st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR PERSONAL TRAINER</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>A motivated coach building sustainable strength, mobility, and endurance routines tailored to your goals.</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-examples'>Examples:<br>• Build a 3-day home workout for busy parents<br>• Create a plan for beginners with bad knees<br>• Add mobility work to my current routine<br>• Design a program for better sleep and energy</div>", unsafe_allow_html=True)
        if st.button("Talk to Greg →", key="greg_home"):
            navigate_to("greg")

    with cols[2]:
        st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
        st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR HEALTH ASSESSOR</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>A compassionate guide helping you understand labs, symptoms, and preventive wellness habits.</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-examples'>Examples:<br>• Explain my bloodwork in simple terms<br>• What lifestyle changes help lower blood pressure?<br>• Review my symptoms and when to see a doctor<br>• Suggest preventive screenings for my age</div>", unsafe_allow_html=True)
        if st.button("Talk to Nurse Zoey Zoe →", key="zoey_home"):
            navigate_to("zoey")

    with cols[3]:
        st.markdown("<div class='agent-name'>NORA</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/cJqPm9BP/pexels-tessy-agbonome-521343232-18252407.jpg", width=200)
        st.markdown("<div class='agent-subtitle'>YOUR NUTRITION COACH</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-desc'>Personalized longevity meal plans, grocery lists — delicious food for a longer life.</div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-examples'>Examples:<br>• Create a 7-day plan with $100 grocery budget<br>• Build meals around my 40/30/30 macros<br>• Suggest snacks that won't spike blood sugar<br>• Make family-friendly Mediterranean recipes</div>", unsafe_allow_html=True)
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




