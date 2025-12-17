import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "fred"

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
    .agent-card { text-align: center; padding: 1.5rem; border-radius: 15px; background: rgba(255,255,255,0.9); box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 10px; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 3em; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL Wellness Solutions</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Your Holistic Longevity Blueprint</p>", unsafe_allow_html=True)

# Hero image — the original tropical sunset beach with pier and palms that worked before
st.image("https://thumbs.dreamstime.com/b/tropical-sunset-beach-scene-pier-palm-trees-vibrant-colors-serene-water-rocky-shore-ai-generated-356600072.jpg", use_column_width=True, caption="Your Florida Longevity Lifestyle – Active Trails at Sunset")

# === Meet Your LBL Wellness Team ===
st.markdown("### Meet Your LBL Wellness Team")

cols = st.columns(2)

with cols[0]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://thumbs.dreamstime.com/b/cartoon-realtor-presenting-colorful-house-model-style-stands-facing-forward-white-background-wearing-dark-blue-suit-393019561.jpg", width=150)
    st.markdown("**Fred**")
    st.markdown("*Wellness Home Scout*  \nProfessional goal-focused realtor")
    if st.button("Talk to Fred", key="fred", use_container_width=True):
        st.session_state.selected_agent = "fred"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[1]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://www.shutterstock.com/image-vector/man-struggling-lift-heavy-barbell-260nw-2699957111.jpg", width=150)
    st.markdown("**Greg**")
    st.markdown("*Personal Trainer*  \nMotivated gym rat")
    if st.button("Talk to Greg", key="greg", use_container_width=True):
        st.session_state.selected_agent = "greg"
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# === Agent Content ===
if st.session_state.selected_agent == "fred":
    st.markdown("### 🏡 Fred – Your Wellness Home Scout")
    st.success("**This tool is completely free – no cost, no obligation!**")
    st.write("Find the perfect Florida home that supports trails, natural light, home gym space, and active living.")

    st.image("https://thebiostation.com/wp-content/uploads/2023/06/outdoor-group-exercise-class-scaled.jpg", use_column_width=True, caption="Community wellness – part of your Florida longevity lifestyle")

    client_needs = st.text_area("Describe your dream wellness/active home in Florida", height=220, placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
    with col2:
        location = st.text_input("Preferred area in Florida", value="Tampa Bay, St. Petersburg, Clearwater, Brandon")

    if st.button("🔍 Show Me Free Teaser Matches", type="primary"):
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
                3-5 sentences introducing how well their needs match the area and budget.

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
                        model="grok-4-1-fast-reasoning",
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

                teaser = "**Free Teaser – Here's a preview of your matches**\n\n"
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
                                "subject": f"{name}'s LBL Wellness Home Report",
                                "text": f"""
Hi {name},

Thank you for exploring LBL Wellness Solutions – Your Holistic Longevity Blueprint.

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
    st.markdown("### 💪 Greg – Your Personal Trainer")
    st.write("Motivated gym rat helping you build strength, endurance, and longevity.")

    age = st.slider("Your age", 18, 80, 45)
    fitness_level = st.selectbox("Current fitness level", ["Beginner", "Intermediate", "Advanced"])
    goals = st.multiselect("Primary goals", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"])
    equipment = st.multiselect("Available equipment", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym"])
    injuries = st.text_area("Any injuries or limitations? (optional)")
    days_per_week = st.slider("Days per week you can train", 1, 7, 4)
    session_length = st.selectbox("Preferred session length", ["20-30 minutes", "30-45 minutes", "45-60 minutes"])

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
                    model="grok-4-1-fast-reasoning",
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

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
