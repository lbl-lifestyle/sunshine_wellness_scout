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

# Hero image: Your #1 favorite – biker on sunset waterfront path
st.image("https://www.floridarambler.com/wp-content/uploads/2023/04/shark-valley-biker-everglades.jpg", use_column_width=True, caption="Active Florida Living – Trails, Sunsets, and Longevity")

# === Meet The Team ===
st.markdown("### Meet Your LBL Wellness Team")

cols = st.columns(2)

with cols[0]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://image.shutterstock.com/image-photo/portrait-confident-mature-businessman-office-600w-2267904077.jpg", width=150)  # Professional realtor avatar
    st.markdown("**Fred**")
    st.markdown("*Wellness Home Scout*  \nProfessional goal-focused realtor")
    if st.button("Talk to Fred", key="fred", use_container_width=True):
        st.session_state.selected_agent = "fred"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[1]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://image.shutterstock.com/image-photo/muscular-man-doing-pushups-gym-600w-2267904077.jpg", width=150)  # Motivated gym rat avatar
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

    # Group fitness image (your second favorite)
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
                1. [Neighborhood Name Here] - [Detailed explanation: specific trails/parks, wellness amenities, vibe, home styles in budget, proximity to nature/water, how it supports active lifestyle. 5-8 sentences.]
                2. [Neighborhood Name Here] - [Same depth. 5-8 sentences.]
                3. [Neighborhood Name Here] - [Same depth. 5-8 sentences.]
                4. [Neighborhood Name Here] - [Same depth. 5-8 sentences.]
                5. [Neighborhood Name Here] - [Same depth. 5-8 sentences.]

                ### Top 5 Must-Have Home Features
                1. [Feature Name Here] - [In-depth reason: daily benefits, health impact, examples, wellness alignment. 5-8 sentences.]
                2. [Feature Name Here] - [Same depth. 5-8 sentences.]
                3. [Feature Name Here] - [Same depth. 5-8 sentences.]
                4. [Feature Name Here] - [Same depth. 5-8 sentences.]
                5. [Feature Name Here] - [Same depth. 5-8 sentences.]

                ### Wellness/Outdoor Highlights
                6-10 sentences on trails, parks, waterfront, fitness communities, year-round advantages.

                Use clear, professional language.
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
                            # Email logic same as before

if st.session_state.selected_agent == "greg":
    st.markdown("### 💪 Greg – Your Personal Trainer")
    st.write("Motivated gym rat helping you build strength, endurance, and longevity.")

    # Personal Trainer inputs and Grok plan (same as previous version)

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI)</small>", unsafe_allow_html=True)
