import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state for persistent email status
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""

# === API KEYS FROM SECRETS ONLY ===
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)

# Page setup
st.set_page_config(page_title="Sunshine State Wellness Home Scout", page_icon="☀️", layout="centered")
st.title("☀️ Sunshine State Wellness & Active Lifestyle Home Scout")
st.markdown("*Find Florida homes that fit how you want to live – trails, gym space, natural light, and more*")
st.success("**This tool is completely free – no cost, no obligation!**")

st.write("""
Describe your ideal lifestyle, budget, and preferred area.
Get an instant free teaser – enter your info for the full personalized report emailed to you.
""")

# Input fields
client_needs = st.text_area(
    "Describe your dream wellness/active home",
    height=220,
    placeholder="Example: Couple in 30s, love morning yoga & weight training, need home gym space, near trails, budget $450k..."
)

col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
with col2:
    location = st.text_input("Preferred area in Florida", value="Tampa Bay, St. Petersburg, Clearwater, Brandon")

if st.button("🔍 Show Me Free Teaser Matches", type="primary"):
    if not client_needs.strip():
        st.warning("Please describe your lifestyle needs above!")
    else:
        with st.spinner("Grok is crafting your free teaser..."):
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
                    max_tokens=2000,  # Increased slightly for longer responses
                    temperature=0.7
                )
                full_report = response.choices[0].message.content
            except Exception as e:
                st.error("Sorry! Grok is taking a quick sunshine break. Please try again in a moment.")
                st.caption(f"Technical note: {str(e)}")
                st.stop()

            # Reset email status when generating a new report
            st.session_state.email_status = None
            st.session_state.email_message = ""

            # === BUILD TEASER ===
            teaser = "**Free Teaser – Here's a preview of your personalized matches**\n\n"

            # Introduction
            intro_match = re.search(r'### Introduction\s*(.*?)(###|$)', full_report, re.DOTALL | re.IGNORECASE)
            if intro_match:
                teaser += intro_match.group(1).strip() + "\n\n"

            # Top 2 Neighborhoods
            teaser += "**Top 2 Recommended Neighborhoods (of 5)**\n\n"
            neighborhoods_section = re.search(r'### Top 5 Neighborhoods.*?###', full_report, re.DOTALL | re.IGNORECASE)
            if neighborhoods_section:
                # Primary: bracket format
                bracket_matches = re.findall(r'(\d+\.\s*\[([^\]]+)\]\s*-\s*\[([^\]]+)\])', neighborhoods_section.group(0))[:2]
                if bracket_matches:
                    for num, name, desc in bracket_matches:
                        teaser += f"**{num.strip()} {name.strip()}**\n{desc.strip()}\n\n"
                else:
                    # Fallback: any numbered line
                    plain_matches = re.findall(r'^\d+\.\s*(.+)', neighborhoods_section.group(0), re.MULTILINE)[:2]
                    for i, line in enumerate(plain_matches, 1):
                        teaser += f"**{i}. {line.strip()}**\n\n"

            # Top 2 Must-Have Features
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

            # Wellness highlight
            teaser += "**Wellness Teaser Highlight**\n"
            teaser += "Year-round sunshine, extensive trail systems, waterfront access, and thriving fitness communities make this area ideal for your active lifestyle.\n\n"
            teaser += "**This tool is completely free!** Get the **full in-depth report** with all 5 neighborhoods, features, and highlights – instantly emailed to you."

            st.success("Here's your free teaser!")
            st.markdown(teaser)

            # === LEAD CAPTURE ===
            st.markdown("### Get Your Full Free Report")
            st.info("Enter your info below – the complete detailed report will be emailed instantly (no spam).")

            with st.form("lead_form"):
                name = st.text_input("Your Name")
                email = st.text_input("Email (required)", placeholder="you@example.com")
                phone = st.text_input("Phone (optional)")
                submitted = st.form_submit_button("📧 Send Me the Full Free Report")

                if submitted:
                    if not email:
                        st.error("Email is required for the report!")
                    else:
                        data = {
                            "from": "onboarding@resend.dev",
                            "to": [email],
                            "cc": [YOUR_EMAIL],
                            "subject": f"{name}'s Personalized Sunshine State Wellness Home Report",
                            "text": f"""
Hi {name},

Thank you for using the Sunshine State Wellness Home Scout – it's 100% free!

Here's your full personalized report based on your description:

{full_report}

Feel free to reply if you'd like to discuss these recommendations further.

Best regards,
Sunshine State Wellness Scout Team
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
                                st.session_state.email_message = f"Full report successfully sent to {email}! Check your inbox (and spam folder)."
                            else:
                                st.session_state.email_status = "error"
                                st.session_state.email_message = f"Email send failed (code {response.status_code}). Try again or contact support."
                        except Exception as e:
                            st.session_state.email_status = "error"
                            st.session_state.email_message = f"Send error: {str(e)}"

            # Persistent email status message
            if st.session_state.email_status == "success":
                st.success(st.session_state.email_message)
                st.balloons()
            elif st.session_state.email_status == "error":
                st.error(st.session_state.email_message)

# Footer
st.markdown("---")
st.markdown("<small>Powered by Grok (xAI) • Sunshine State Wellness Lifestyle Scout | Completely Free Tool<br>Real estate recommendations powered by Grok • Not affiliated with any brokerage</small>", unsafe_allow_html=True)
