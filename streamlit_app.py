import streamlit as st
import requests
from openai import OpenAI
import re

# === API KEYS FROM SECRETS ONLY ===
# These will be loaded securely from Streamlit Secrets (no hardcoding)
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
            Provide robust, detailed recommendations in this EXACT structure (use these headings and numbering, with detailed explanations for each neighborhood and feature):

            ### Introduction
            [2-3 sentence intro about the fit]

            ### Top 5 Neighborhoods/Suburbs and Why They Fit
            1. [Neighborhood 1] - [Robust, detailed reason why it fits, 2-3 sentences]
            2. [Neighborhood 2] - [Robust, detailed reason why it fits, 2-3 sentences]
            3. [Neighborhood 3] - [Robust, detailed reason why it fits, 2-3 sentences]
            4. [Neighborhood 4] - [Robust, detailed reason why it fits, 2-3 sentences]
            5. [Neighborhood 5] - [Robust, detailed reason why it fits, 2-3 sentences]

            ### Top 5 Must-Have Home Features
            1. [Feature 1] - [Robust, detailed reason why important, 2-3 sentences]
            2. [Feature 2] - [Robust, detailed reason why important, 2-3 sentences]
            3. [Feature 3] - [Robust, detailed reason why important, 2-3 sentences]
            4. [Feature 4] - [Robust, detailed reason why important, 2-3 sentences]
            5. [Feature 5] - [Robust, detailed reason why important, 2-3 sentences]

            ### Wellness/Outdoor Highlights
            [3-5 sentences on key highlights like trails, communities, etc.]

            Use friendly, structured markdown with bold headings.
            """

            response = client.chat.completions.create(
                model="grok-4",
                messages=[
                    {"role": "system", "content": "You are an expert Florida real estate advisor specializing in wellness and active lifestyle properties."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            full_report = response.choices[0].message.content

            # === TEASER: 2 + 2 WITH HEADINGS & BULLETS ===
            teaser = "**Free Teaser – Here's a preview of your personalized matches**\n\n"

            # Introduction
            intro_match = re.search(r'### Introduction(.*?)### Top 5 Neighborhoods', full_report, re.DOTALL)
            if intro_match:
                teaser += intro_match.group(1).strip() + "\n\n"

            # Top 2 Neighborhoods
            teaser += "**Top 2 Recommended Neighborhoods (of 5)**\n\n"
            neighborhood_lines = re.findall(r'^\d+\.\s*(.+)', full_report.split('### Top 5 Neighborhoods/Suburbs')[1].split('### Top 5 Must-Have')[0], re.MULTILINE)[:2]
            teaser += "\n".join([f"• {line}" for line in neighborhood_lines]) + "\n\n"

            # Top 2 Must-Have Features
            teaser += "**Top 2 Must-Have Home Features (of 5)**\n\n"
            feature_lines = re.findall(r'^\d+\.\s*(.+)', full_report.split('### Top 5 Must-Have Home Features')[1].split('### Wellness')[0], re.MULTILINE)[:2]
            teaser += "\n".join([f"• {line}" for line in feature_lines]) + "\n\n"

            # Wellness Highlight
            teaser += "**Wellness Teaser Highlight**\n"
            teaser += "Great trail access, wellness communities, and homes designed for active living in the Sunshine State...\n\n"

            teaser += "**This tool is completely free!** Like what you see? Get the **full report** with all 5 neighborhoods, complete features, wellness details, and more – instantly emailed to you."

            st.success("Here's your free teaser!")
            st.markdown(teaser)

            # === LEAD CAPTURE ===
            st.markdown("### Get Your Full Free Report")
            st.info("Enter your info – I'll email the complete report instantly (no spam, just helpful info).")

            with st.form("lead_form"):
                name = st.text_input("Your Name")
                email = st.text_input("Email (required)", placeholder="you@example.com")
                phone = st.text_input("Phone (optional)")
                submitted = st.form_submit_button("📧 Send Me the Full Free Report")

                if submitted:
                    if not email:
                        st.error("Email is required for the report!")
                    else:
                        # Send email via Resend
                        data = {
                            "from": "onboarding@resend.dev",
                            "to": [email],
                            "cc": [YOUR_EMAIL],
                            "subject": f"{name}'s Sunshine State Wellness Report (Free)",
                            "text": f"""
Hi {name},

Thanks for using the Sunshine State Wellness Home Scout – it's completely free!

Here's your full personalized report:

{full_report}

I'll follow up soon if you'd like to discuss your matches.

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
                                st.success(f"Full free report sent to {email}! Check your inbox.")
                                st.balloons()
                            else:
                                st.error(f"Send failed (code {response.status_code}): {response.text}")
                        except Exception as e:
                            st.error(f"Send failed: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by Grok (xAI) • Sunshine State Wellness Lifestyle Scout | Completely Free Tool")