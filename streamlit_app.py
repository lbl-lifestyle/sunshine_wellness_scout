import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None  # Start with no agent selected

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Florida-themed CSS - clean, motivating, consistent alignment
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #ffecd2, #fcb69f);
        color: #0c4a6e;
    }
    .main-header { 
        font-size: 3.5rem; 
        color: #ea580c; 
        text-align: center; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2); 
        font-weight: bold;
    }
    .tagline { 
        font-size: 2rem; 
        color: #166534; 
        text-align: center; 
        font-style: italic; 
        margin-bottom: 2rem; 
    }
    .motivation-header {
        font-size: 2rem;
        color: #ea580c;
        text-align: center;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
    }
    .motivation-text {
        text-align: center;
        font-size: 1.4rem;
        line-height: 1.9;
        margin: 2rem 0 3rem 0;
        color: #0c4a6e;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .agent-name { 
        font-weight: bold; 
        font-size: 1.8rem; 
        color: #ea580c; 
        margin-bottom: 1rem; 
    }
    .agent-desc {
        min-height: 110px;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #ea580c;
        color: white;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.2rem;
        height: 4em;
        width: 100%;
    }
    /* Remove unwanted Streamlit backgrounds */
    .stMarkdown { background: transparent !important; }
    div[data-testid="stVerticalBlock"] > div { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL LIFESTYLE SOLUTIONS</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>LIVE BETTER LONGER</p>", unsafe_allow_html=True)

# Hero image
st.image("https://i.postimg.cc/tgsgw1dW/image.jpg", use_column_width=True, caption="Your Longevity Blueprint")

# === NEW: Motivating Summary Section ===
st.markdown("<h2 class='motivation-header'>Unlock Your Vibrant Longevity Lifestyle Today!</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='motivation-text'>
Get ready to <strong>live better longer</strong> than ever before with LBL Lifestyle Solutions—your ultimate holistic longevity blueprint designed for Florida's unbeatable sunshine and active vibe!<br><br>
Our powerhouse team is here to fuel your transformation: Fred the Wellness Home Scout finds your dream active-living paradise, Greg the fired-up Personal Trainer builds custom routines to make you stronger and unstoppable, and Nurse Zoey Zoe the caring Health Assessor delivers proactive insights to keep you thriving.<br><br>
Imagine waking up energized, hitting scenic trails, crushing workouts, and feeling incredible every single day—physically, mentally, and emotionally on fire!<br><br>
Jump in now and unlock the vibrant, joyful life you deserve—your best years are just getting started!
</div>
""", unsafe_allow_html=True)

# === MEET THE LIFESTYLE TEAM ===
st.markdown("### MEET THE LIFESTYLE TEAM")

cols = st.columns(3)

with cols[0]:
    st.markdown("<div class='agent-name'>FRED</div>", unsafe_allow_html=True)
    st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR WELLNESS HOME SCOUT* <br>A goal-focused realtor. Lets start by generating a detailed report of home options that match you lifestyle needs.</div>", unsafe_allow_html=True)
    if st.button("CLICK HERE TO GET STARTED", key="fred", use_container_width=True):
        st.session_state.selected_agent = "fred"

with cols[1]:
    st.markdown("<div class='agent-name'>GREG</div>", unsafe_allow_html=True)
    st.image("https://i.postimg.cc/yxf3Szvc/pexels-andres-ayrton-6551079.jpg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR PERSONAL TRAINER* <br>A motivated lifestyle coach. Let start with a workout routine tailored to you fitness goals and health needs</div>", unsafe_allow_html=True)
    if st.button("CLICK HERE TO GET STARTED", key="greg", use_container_width=True):
        st.session_state.selected_agent = "greg"

with cols[2]:
    st.markdown("<div class='agent-name'>NURSE ZOEY ZOE</div>", unsafe_allow_html=True)
    st.image("https://images.pexels.com/photos/5215021/pexels-photo-5215021.jpeg", width=200)
    st.markdown("<div class='agent-desc'>*YOUR HEALTH ASSESSOR* <br>A compassionate wellness guide. Ask Zoey any health question. She can help you develop a proactive health lifestyle</div>", unsafe_allow_html=True)
    if st.button("CLICK HERE TO GET STARTED", key="zoey", use_container_width=True):
        st.session_state.selected_agent = "zoey"

st.markdown("---")

# Model name - current reasoning model (Dec 2025)
MODEL_NAME = "grok-4-1-fast-reasoning"

# === Agent Content ===
if st.session_state.selected_agent == "fred":
    st.markdown("### 🏡 FRED – Your Wellness Home Scout")
    st.success("**The report generated by this tool is completely free – no cost, no obligation! You will receive five total tailored recommendations. The first two recommendations immediately. You will then receive the full report via email.**")
    st.write("The perfect home that supports your lifestyle awaits.")
    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg-J1J8SDEAY-unsplash.jpg", use_column_width=True, caption="Your Keys Await – Welcome to your longevity lifestyle")
    client_needs = st.text_area("DESCRIBE YOUR DREAM WELLNESS NEEDS IN DETAIL. LET FRED DO THE REST!!!", height=220, placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
    with col2:
        location = st.text_input("Preferred area in Florida", value="Tampa Bay, St. Petersburg, Clearwater, Brandon")
    if st.button("🔍 GENERATE MY REPORT", type="primary"):
        if not client_needs.strip():
            st.warning("Please describe your lifestyle needs above!")
        else:
            with st.spinner("Fred is finding your perfect matches..."):
                full_prompt = f"""
                Client description:
                {client_needs}
                Budget: ${budget:,}
                Preferred location(s) in Florida: {location}
                You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties.
                Follow this EXACT structure with no deviations. Use the precise bracket format.
                ### Introduction
                5-6 sentences introducing how well their needs match the area and budget.
                ### Top 5 Neighborhoods/Suburbs and Why They Fit
                1. [Neighborhood Name Here] - [Detailed explanation: include specific trails/parks by name if possible, wellness amenities (gyms, yoga studios, community centers), community vibe, typical home styles available in this budget range, proximity to water/nature, and exactly how it supports their active lifestyle and home workout needs. 5-8 full sentences.]
                2. [Neighborhood Name Here] - [Same level of depth and detail. 5-8 sentences.]
                3. [Neighborhood Name Here] - [Same level of depth and detail. 5-8 sentences.]
                4. [Neighborhood Name Here] - [Same level of depth and detail. 5-8 sentences.]
                5. [Neighborhood Name Here] - [Same level of depth and detail. 5-8 sentences.]
                ### Top 5 Must-Have Home Features
                1. [Feature Name Here] - [In-depth reason why essential: explain daily benefits, health impact, real-life examples of use, and how it aligns with their wellness goals. 5-8 sentences.]
                2. [Feature Name Here] - [Same depth and detail. 5-8 sentences.]
                3. [Feature Name Here] - [Same depth and detail. 5-8 sentences.]
                4. [Feature Name Here] - [Same depth and detail. 5-8 sentences.]
                5. [Feature Name Here] - [Same depth and detail. 5-8 sentences.]
                ### Wellness/Outdoor Highlights
                6-10 sentences covering key trails, parks, waterfront access, fitness communities, farmers markets, outdoor events, year-round climate advantages, and wellness resources in the region.
                Use clear, professional language. Do not add extra commentary or deviate from this structure.
                """
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": "You are Fred, a professional goal-focused real estate advisor."},
                            {"role": "user", "content": full_prompt}
                        ],
                        max_tokens=2000,
                        temperature=0.7
                    )
                    full_report = response.choices[0].message.content
                except Exception as e:
                    st.error("Fred is reviewing listings... try again soon.")
                    st.caption(f"Note: {str(e)}")
                    st.stop()

                st.session_state.email_status = None
                st.session_state.email_message = ""

                teaser = "**Free Sample – Here's a preview of your matches**\n\n"
                intro_match = re.search(r'### Introduction\s*(.*?)(###|$)', full_report, re.DOTALL | re.IGNORECASE)
                if intro_match:
                    teaser += intro_match.group(1).strip() + "\n\n"
                teaser += "**Top 2 Recommended Neighborhoods (of 5)**\n\n"
                neighborhoods_section = re.search(r'### Top 5 Neighborhoods.*?###', full_report, re.DOTALL | re.IGNORECASE)
                if neighborhoods_section:
                    bracket_matches = re.findall(r'(\d+\.\s*\[([^\]]+)\]\s*-\s*\[([^\]]+)\])', neighborhoods_section.group(0))[:2]
                    if bracket_matches:
                        for num, name, desc in bracket_matches:
                            teaser += f"**{num.strip()} {name.strip()}**\n{desc.strip()}\n\n"
                    else:
                        plain_matches = re.findall(r'^\d+\.\s*(.+)', neighborhoods_section.group(0), re.MULTILINE)[:2]
                        for i, line in enumerate(plain_matches, 1):
                            teaser += f"**{i}. {line.strip()}**\n\n"
                teaser += "**Top 2 Must-Have Home Features (of 5)**\n\n"
                features_section = re.search(r'### Top 5 Must-Have Home Features.*?###', full_report, re.DOTALL | re.IGNORECASE)
                if features_section:
                    bracket_matches = re.findall(r'(\d+\.\s*\[([^\]]+)\]\s*-\s*\[([^\]]+)\])', features_section.group(0))[:2]
                    if bracket_matches:
                        for num, name, desc in bracket_matches:
                            teaser += f"**{num.strip()} {name.strip()}**\n{desc.strip()}\n\n"
                    else:
                        plain_matches = re.findall(r'^\d+\.\s*(.+)', features_section.group(0), re.MULTILINE)[:2]
                        for i, line in enumerate(plain_matches, 1):
                            teaser += f"**{i}. {line.strip()}**\n\n"
                teaser += "**Wellness Highlight**\nYear-round active living awaits...\n\n"
                teaser += "**Free tool!** Get the full report emailed."
                st.success("Fred found your matches!")
                st.markdown(teaser)

                st.markdown("### Get Your Full Free Report from Fred")
                with st.form("lead_form"):
                    name = st.text_input("Your Name")
                    email = st.text_input("Email (required)", placeholder="you@example.com")
                    phone = st.text_input("Phone (optional)")
                    submitted = st.form_submit_button("📧 Send Full Report")
                    if submitted:
                        if not email:
                            st.error("Email required!")
                        else:
                            data = {
                                "from": "onboarding@resend.dev",
                                "to": [email],
                                "cc": [YOUR_EMAIL],
                                "subject": f"{name}'s LBL Lifestyle Home Report",
                                "text": f"""
Hi {name},
Thank you for exploring LBL Lifestyle Solutions – Your Holistic Longevity Blueprint.
Here's your full personalized Florida wellness home report:
{full_report}
Reply anytime to discuss how we can build your complete longevity plan.
Best regards,
Fred & the LBL Team
                                """
                            }
                            headers = {
                                "Authorization": f"Bearer {RESEND_API_KEY}",
                                "Content-Type": "application/json"
                            }
                            try:
                                response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                                if response.status_code == 200:
                                    st.session_state.email_status = "success"
                                    st.session_state.email_message = f"Full report sent to {email}! Check your inbox."
                                else:
                                    st.session_state.email_status = "error"
                                    st.session_state.email_message = f"Send failed: {response.text}"
                            except Exception as e:
                                st.session_state.email_status = "error"
                                st.session_state.email_message = f"Send error: {str(e)}"
                if st.session_state.email_status == "success":
                    st.success(st.session_state.email_message)
                    st.balloons()
                elif st.session_state.email_status == "error":
                    st.error(st.session_state.email_message)

elif st.session_state.selected_agent == "greg":
    st.image("https://i.postimg.cc/mDy2FKQg/outdoor-fitness-scaled.webp", use_column_width=True, caption="Greatness Await – Welcome to your longevity lifestyle")
    st.markdown("### 💪 HI!!! IM GREG – Your Awesome Personal Trainer. GET SOME!!!!")
    st.write("Im a motivated gym rat helping you build strength, endurance, and longevity. Lets get started by building you a personalized workout routine. Please fill out the form below. I will write up a plan that is right for you. Congatulations on choosing a longevity lifestyle. Your tomorrow self will thank you")
    age = st.slider("Your age", 18, 80, 45)
    fitness_level = st.selectbox("CURRENT FITNESS LEVEL", ["Beginner", "Intermediate", "Advanced"])
    goals = st.multiselect("PRIMARY GOALS", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"])
    equipment = st.multiselect("AVAILABLE EQUIPMENT", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym", "Community gym free weights", "Community gym resistance machines"])
    injuries = st.text_area("ANY INJURIES OR LIMITATIONS? (optional)")
    days_per_week = st.slider("DAYS PER WEEK YOU CAN TRAIN", 1, 7, 4)
    session_length = st.selectbox("PREFERRED SESSION LENGTH", ["20-30 minutes", "30-45 minutes", "45-60 minutes"])
    if st.button("Generate My Custom Workout Plan", type="primary"):
        with st.spinner("Greg is building your plan..."):
            trainer_prompt = f"""
            You are Greg, a motivated gym rat and certified personal trainer focused on longevity.
            Client: Age {age}, {fitness_level} level, goals: {', '.join(goals)}
            Equipment: {', '.join(equipment) or 'Bodyweight'}
            Injuries: {injuries or 'None'}
            Training {days_per_week} days/week, {session_length} sessions
            Create a full weekly workout plan in markdown:
            - Warm-up
            - Main exercises (sets, reps, rest)
            - Cool-down
            - Progression tips
            Be encouraging and safe.
            """
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Greg, a motivated personal trainer."},
                        {"role": "user", "content": trainer_prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                plan = response.choices[0].message.content
                st.success("Greg's custom plan for you!")
                st.markdown(plan)
            except Exception as e:
                st.error("Greg is pumping iron... try again soon.")
                st.caption(f"Note: {str(e)}")

elif st.session_state.selected_agent == "zoey":
    st.image("https://i.postimg.cc/BnFgfCTD/pexels-kampus-7551620.jpg", use_column_width=True, caption="LIVE BETTER LONGER – Welcome to your longevity lifestyle")
    st.markdown("### 🩺 GREETINGS. IM NURSE ZOEY ZOE – your friendly nurse assistant, here to support you with compassionate and reliable guidance every step of the way. ")
    st.write("I can help you understand medical conditions, symptoms, treatments, and medications in simple, easy-to-follow terms; offer general advice on managing everyday health concerns like pain relief, wound care, or chronic issues such as diabetes or hypertension; provide tips for wellness, nutrition, exercise, and mental health support; explain procedures or post-care instructions; assist caregivers with practical strategies for supporting loved ones; and always listen with empathy to offer reassurance during stressful times—remember, though, I'm here for information and support, so please consult your healthcare provider for personalized advice or emergencies..")
    st.warning("**Important**: This is for educational purposes only. I do not provide medical diagnoses or treatment. Always consult a licensed healthcare professional.")
    st.write("Upload labs or enter data for general insights, or ask wellness questions.")
    uploaded_file = st.file_uploader("Upload labs/health data (PDF, text)", type=["pdf", "txt"])
    health_data = st.text_area("Or enter data manually", height=150)
    question = st.text_input("General question (optional)")
    if st.button("Get Insights", type="primary"):
        if not uploaded_file and not health_data and not question:
            st.warning("Please provide data or a question!")
        else:
            with st.spinner("Dr. Zoey Zoe is reviewing..."):
                zoey_prompt = f"""
                You are Dr. Zoey Zoe, a compassionate nurse providing general wellness education.
                Data: {health_data or 'From file'}
                Question: {question or 'General review'}
                Give educational insights only. Use phrases like "Based on standard guidelines..." Do not diagnose.
                Structure:
                ### Key Insights
                - Bullet
