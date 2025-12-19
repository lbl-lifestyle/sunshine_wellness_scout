import streamlit as st
import requests
from openai import OpenAI

# === CONFIGURATION ===
MODEL_NAME = "grok-4-1-fast-reasoning"  # Latest fast + reasoning model (Premium+ access)

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# Secrets (configure in Streamlit secrets)
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Helper function for chat system prompts
def get_chat_system_prompt(agent):
    if agent == "fred":
        return "You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties across the United States."
    elif agent == "greg":
        return "You are Greg, a highly motivated, energetic personal trainer and gym enthusiast focused on building strength, endurance, and longevity."
    elif agent == "zoey":
        return ("You are Nurse Zoey Zoe, a compassionate and knowledgeable nurse providing general wellness education and supportive guidance. "
                "You never diagnose conditions or prescribe treatments. Always remind users to consult licensed healthcare professionals.")
    return "You are a helpful longevity lifestyle assistant."

# === CUSTOM CSS ===
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
</style>
""", unsafe_allow_html=True)

# === HEADER ===
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

# Back button
if st.session_state.selected_agent:
    if st.button("← Back to Team", key="back_to_team"):
        st.session_state.selected_agent = None
        st.session_state.chat_history = {}
        st.rerun()

# === TEAM SELECTION ===
if not st.session_state.selected_agent:
    st.markdown("### MEET THE LIFESTYLE TEAM")
    st.markdown("<p style='text-align:center; color:#0c4a6e; font-size:1.2rem;'>Click an agent to begin your longevity journey</p>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
        st.markdown("<div class='agent-desc'>*YOUR WELLNESS HOME SCOUT* <br>A goal-focused realtor. Let's start by generating a detailed report of home options that match your lifestyle needs — anywhere in the U.S.!</div>", unsafe_allow_html=True)
        if st.button("Talk to Fred →", key="fred"):
            st.session_state.selected_agent = "fred"
            st.rerun()
    
    with cols[1]:
        st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
        st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
        st.markdown("<div class='agent-desc'>*YOUR PERSONAL TRAINER* <br>A motivated lifestyle coach. Let's start with a workout routine tailored to your fitness goals and health needs to Live Better Longer.</div>", unsafe_allow_html=True)
        if st.button("Talk to Greg →", key="greg"):
            st.session_state.selected_agent = "greg"
            st.rerun()
    
    with cols[2]:
        st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
        st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
        st.markdown("<div class='agent-desc'>*YOUR HEALTH ASSESSOR* <br>A compassionate wellness guide. Ask Zoey any health question. She can help you develop a proactive health lifestyle.</div>", unsafe_allow_html=True)
        if st.button("Talk to Nurse Zoey Zoe →", key="zoey"):
            st.session_state.selected_agent = "zoey"
            st.rerun()

# === AGENT VIEWS ===
else:
    agent = st.session_state.selected_agent
    agent_name = "Fred" if agent == "fred" else "Greg" if agent == "greg" else "Nurse Zoey Zoe"
    
    st.markdown("<div id='agent-interaction'></div>", unsafe_allow_html=True)
    st.markdown("""
    <script>
        const element = document.getElementById('agent-interaction');
        if (element) element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    </script>
    """, unsafe_allow_html=True)

    if agent == "fred":
        st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg-J1J8SDEAY-unsplash.jpg", use_column_width=True, caption="Your Keys Await – Welcome to your longevity lifestyle")
        st.markdown("### 🏡 FRED – Your Wellness Home Scout")
        st.success("**This tool is completely free – no cost, no obligation! You will receive the full personalized report below and via email.**")
        st.write("The perfect home that supports your lifestyle awaits — anywhere in the U.S.!")

        client_needs = st.text_area("DESCRIBE YOUR DREAM WELLNESS NEEDS IN DETAIL. LET FRED DO THE REST!!!", height=220,
                                    placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
        with col2:
            location = st.text_input("Preferred state or area (e.g., North Carolina, Asheville, Tampa FL)", value="")

        st.markdown("### Refine Your Report (Optional)")
        report_sections = st.multiselect(
            "Select sections to include:",
            ["Introduction summary", "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)",
             "Top 5 Must-Have Home Features", "Wellness/Outdoor Highlights"],
            default=["Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)", "Top 5 Must-Have Home Features", "Wellness/Outdoor Highlights"]
        )

        if st.button("🔍 GENERATE MY REPORT", type="primary"):
            if not client_needs.strip():
                st.warning("Please describe your lifestyle needs above!")
            else:
                with st.spinner("Fred is crafting your personalized report..."):
                    sections_prompt = ""
                    if "Introduction summary" in report_sections:
                        sections_prompt += "### Introduction\n5-6 sentences introducing how well their needs match the area and budget.\n\n"
                    if "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)" in report_sections:
                        sections_prompt += "### Top 5 Neighborhoods/Suburbs and Why They Fit\n1. [Neighborhood] - [5-8 sentences] [Fun facts: 3-5 sentences]\n(repeat 2-5)\n\n"
                    if "Top 5 Must-Have Home Features" in report_sections:
                        sections_prompt += "### Top 5 Must-Have Home Features\n1. [Feature] - [5-8 sentences]\n(repeat 2-5)\n\n"
                    if "Wellness/Outdoor Highlights" in report_sections:
                        sections_prompt += "### Wellness/Outdoor Highlights\n6-10 sentences on trails, parks, etc.\n\n"

                    full_prompt = f"""
                    Client description: {client_needs}
                    Budget: ${budget:,}
                    Location: {location or 'wellness-friendly U.S. areas'}
                    You are Fred, professional wellness real estate advisor.
                    Follow this exact structure only:
                    {sections_prompt}
                    Professional, clear tone. No extra commentary.
                    """

                    try:
                        response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=[
                                {"role": "system", "content": "You are Fred, a professional real estate advisor."},
                                {"role": "user", "content": full_prompt}
                            ],
                            max_tokens=2000,
                            temperature=0.7
                        )
                        full_report = response.choices[0].message.content
                        st.success("Fred found your perfect matches! Here's your personalized report:")
                        st.markdown(full_report)

                        # Email form
                        st.markdown("### Get Your Full Report Emailed")
                        with st.form("lead_form", clear_on_submit=True):
                            name = st.text_input("Your Name")
                            email = st.text_input("Email (required)", placeholder="you@example.com")
                            phone = st.text_input("Phone (optional)")
                            submitted = st.form_submit_button("📧 Send My Full Report")
                            if submitted:
                                if not email:
                                    st.error("Email is required!")
                                else:
                                    data = {
                                        "from": "reports@lbllifestyle.com",
                                        "to": [email],
                                        "cc": [YOUR_EMAIL],
                                        "subject": f"{name or 'Client'}'s LBL Wellness Home Report",
                                        "text": f"Hi {name or 'there'},\n\nThank you for using LBL Lifestyle Solutions.\n\nHere's your report:\n\n{full_report}\n\nBest,\nFred & LBL Team"
                                    }
                                    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                                    try:
                                        resp = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                                        if resp.status_code == 200:
                                            st.session_state.email_status = "success"
                                            st.session_state.email_message = f"Report sent to {email}!"
                                        else:
                                            st.session_state.email_status = "error"
                                            st.session_state.email_message = f"Failed: {resp.text}"
                                    except Exception as e:
                                        st.session_state.email_status = "error"
                                        st.session_state.email_message = str(e)

                        if st.session_state.email_status == "success":
                            st.success(st.session_state.email_message)
                            st.balloons()
                        elif st.session_state.email_status == "error":
                            st.error(st.session_state.email_message)

                    except Exception as e:
                        st.error("Fred is busy... try again soon.")
                        st.caption(f"Error: {e}")

    elif agent == "greg":
        st.image("https://i.postimg.cc/mDy2FKQg/outdoor-fitness-scaled.webp", use_column_width=True, caption="Greatness Awaits – Welcome to your longevity lifestyle")
        st.markdown("### 💪 HI!!! I'M GREG – Your Awesome Personal Trainer. LET'S GET SOME!!!!")
        st.write("I'm a motivated gym rat helping you build strength, endurance, and longevity. Congratulations on choosing a longevity lifestyle — your future self will thank you!")

        age = st.slider("Your age", 18, 80, 45)
        fitness_level = st.selectbox("CURRENT FITNESS LEVEL", ["Beginner", "Intermediate", "Advanced"])
        goals = st.multiselect("PRIMARY GOALS", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"])
        equipment = st.multiselect("AVAILABLE EQUIPMENT", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym", "Community gym free weights", "Community gym resistance machines"])
        injuries = st.text_area("ANY INJURIES OR LIMITATIONS? (optional)")
        days_per_week = st.slider("DAYS PER WEEK YOU CAN TRAIN", 1, 7, 4)
        session_length = st.selectbox("PREFERRED SESSION LENGTH", ["20-30 minutes", "30-45 minutes", "45-60 minutes"])

        if st.button("Generate My Custom Workout Plan", type="primary"):
            with st.spinner("Greg is building your plan..."):
                prompt = f"""
                You are Greg, motivated personal trainer focused on longevity.
                Client: Age {age}, {fitness_level}, goals: {', '.join(goals)}
                Equipment: {', '.join(equipment) or 'Bodyweight'}
                Injuries: {injuries or 'None'}
                {days_per_week} days/week, {session_length} sessions
                Create a full weekly markdown workout plan with warm-up, exercises (sets/reps/rest), cool-down, and progression tips.
                Be encouraging and safe.
                """
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": "You are Greg, a motivated personal trainer."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1500,
                        temperature=0.7
                    )
                    st.success("Greg's custom plan for you!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error("Greg is pumping iron... try again.")
                    st.caption(f"Error: {e}")

    elif agent == "zoey":
        st.image("https://i.postimg.cc/BnFgfCTD/pexels-kampus-7551620.jpg", use_column_width=True, caption="LIVE BETTER LONGER – Welcome to your longevity lifestyle")
        st.markdown("### 🩺 GREETINGS. I'M NURSE ZOEY ZOE – your friendly nurse assistant.")
        st.write("I provide general wellness education and supportive guidance in simple terms.")
        st.warning("**Important**: Educational purposes only. Not medical advice. Always consult a licensed healthcare professional.")

        uploaded_file = st.file_uploader("Upload labs/health data (PDF, text)", type=["pdf", "txt"])
        health_data = st.text_area("Or enter data manually", height=150)
        question = st.text_input("General question (optional)")

        if st.button("Get Insights", type="primary"):
            if not uploaded_file and not health_data.strip() and not question.strip():
                st.warning("Please provide data or a question!")
            else:
                file_content = ""
                if uploaded_file:
                    try:
                        file_content = uploaded_file.read().decode("utf-8")
                    except:
                        file_content = "[File uploaded but unreadable]"

                combined = file_content or health_data

                with st.spinner("Nurse Zoey Zoe is reviewing..."):
                    prompt = f"""
                    You are Nurse Zoey Zoe, compassionate nurse providing education only.
                    Data: {combined}
                    Question: {question or 'General wellness review'}
                    Respond in markdown:
                    ### Key Insights
                    - General observations
                    ### General Recommendations
                    - Lifestyle tips
                    ### Next Steps
                    - Recommend professional consultation
                    Never diagnose.
                    """
                    try:
                        response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=[
                                {"role": "system", "content": "You are Nurse Zoey Zoe, providing education only."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=1000,
                            temperature=0.6
                        )
                        st.success("Nurse Zoey Zoe's insights:")
                        st.markdown(response.choices[0].message.content)
                    except Exception as e:
                        st.error("Try again soon.")
                        st.caption(f"Error: {e}")

    # === CHAT ===
    st.markdown("### Have a follow-up question? Chat with me!")
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    if agent not in st.session_state.chat_history:
        st.session_state.chat_history[agent] = []

    for msg in st.session_state.chat_history[agent]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input(f"Ask {agent_name} a question..."):
        st.session_state.chat_history[agent].append({"role": "user", "content": prompt})
        st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": get_chat_system_prompt(agent)},
                        *st.session_state.chat_history[agent]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history[agent].append({"role": "assistant", "content": reply})
                st.markdown(f"<div class='assistant-message'>{reply}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Trouble connecting. Try again.")
                st.caption(f"Error: {e}")

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("---")
st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
