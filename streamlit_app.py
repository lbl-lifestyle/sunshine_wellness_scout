import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""

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
    .stButton>button { background-color: #ea580c; color: white; border-radius: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Hero image: Biker on sunset waterfront path with palms (Option #1 vibe)
st.image("https://image.shutterstock.com/image-photo/male-riding-backpack-rucksack-alone-600w-2481911065.jpg", use_column_width=True, caption="Your Florida Longevity Lifestyle – Active Trails at Sunset")

st.markdown("<h1 class='main-header'>LBL Wellness Solutions</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Your Holistic Longevity Blueprint</p>", unsafe_allow_html=True)

st.success("**This tool is completely free – no cost, no obligation!**")
st.write("Discover Florida homes that support your active, wellness-focused lifestyle – trails, natural light, home gym space, waterfront access, and more.")

# Second image: Group of 6 people in outdoor seated fitness class (original working style)
st.image("https://image.shutterstock.com/image-photo/group-people-doing-yoga-exercises-600w-2267904077.jpg", use_column_width=True, caption="Community wellness and group fitness – part of your longevity blueprint")

# Inputs
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
        with st.spinner("Grok is crafting your personalized Florida longevity matches..."):
            full_prompt = f"""
            Client description:
            {client_needs}
            Budget: ${budget:,}
            Preferred location(s) in Florida: {location}

            You are an expert Florida real estate advisor specializing in wellness and active lifestyle properties.

            Follow this EXACT structure with no deviations. Use the precise bracket format for every neighborhood and feature.

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
                        {"role": "system", "content": "You are an expert Florida real estate advisor specializing in wellness and active lifestyle properties."},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                full_report = response.choices[0].message.content
            except Exception as e:
                st.error("Sorry! Grok is taking a quick sunshine break. Please try again in a moment.")
                st.caption(f"Technical note: {str(e)}")
                st.stop()

            st.session_state.email_status = None
            st.session_state.email_message = ""

            teaser = "**Free Teaser – Here's a preview of your personalized Florida matches**\n\n"

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

            teaser += "**Wellness Teaser Highlight**\nYear-round sunshine, trails, and waterfront living await...\n\n"
            teaser += "**This tool is completely free!** Get the **full in-depth report** emailed instantly."

            st.success("Here's your free teaser!")
            st.markdown(teaser)

            # Optional third image (modern home)
            st.image("https://photos.prod.cirrussystem.net/1345/87b5b2578644499ae245ac9c09fe3c1c/2565310842.jpeg", caption="Modern Florida homes designed for wellness and longevity", use_column_width=True)

            # Lead capture
            st.markdown("### Get Your Full Free Report")
            st.info("Enter your info – the complete report will be emailed instantly (no spam).")

            with st.form("lead_form"):
                name = st.text_input("Your Name")
                email = st.text_input("Email (required)", placeholder="you@example.com")
                phone = st.text_input("Phone (optional)")
                submitted = st.form_submit_button("📧 Send Me the Full Free Report")

                if submitted:
                    if not email:
                        st.error("Email is required!")
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
LBL Wellness Solutions Team
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

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Real estate recommendations powered by AI • Not affiliated with any brokerage</small>", unsafe_allow_html=True)
