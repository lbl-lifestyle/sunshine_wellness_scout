import streamlit as st
import requests
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", "")  # Safe if missing

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def fetch_pexels_image(query):
    """Fetch one high-quality image from Pexels for a neighborhood"""
    if not PEXELS_API_KEY:
        return None
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/v1/search"
    params = {
        "query": f"{query} neighborhood homes landscape nature aerial",
        "per_page": 1,
        "orientation": "landscape"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("photos"):
                return data["photos"][0]["src"]["large2x"]  # Highest resolution
    except:
        pass
    return None

def add_images_to_report(report_text, location_hint=""):
    """Insert one beautiful photo under each Top 5 neighborhood"""
    lines = report_text.split('\n')
    enhanced_lines = []
    in_top_5 = False

    for line in lines:
        enhanced_lines.append(line)

        # Detect start of Top 5 section
        if "Top 5 Neighborhoods" in line or "Top 5 Suburbs" in line:
            in_top_5 = True

        # Detect neighborhood entries: "1. Neighborhood Name", "2. Another Place", etc.
        if in_top_5 and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            parts = line.split('-', 1)
            if len(parts) > 1:
                name_part = parts[0].strip()[2:].strip()  # Remove "1. " or "2. "
                query = f"{name_part} {location_hint}".strip()
                img_url = fetch_pexels_image(query)
                if img_url:
                    enhanced_lines.append("")
                    enhanced_lines.append(f"![{name_part} – Beautiful homes and scenery]({img_url})")
                    enhanced_lines.append("")  # Spacing

    return '\n'.join(enhanced_lines)

def show():
    # CSS
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
        .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
        img { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 20px 0; max-width: 100%; height: auto; }
    </style>
    """, unsafe_allow_html=True)

    # Scroll to top fix
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
        const mainSection = window.parent.document.querySelector('section.main');
        if (mainSection) mainSection.scrollTop = 0;
        setTimeout(() => { window.scrollTo(0, 0); if (mainSection) mainSection.scrollTop = 0; }, 100);
    </script>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Team"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg-J1J8SDEAY-unsplash.jpg", caption="Your Keys Await – Welcome to your longevity lifestyle")

    st.markdown("### 🏡 FRED – Your Wellness Home Scout")
    st.success("**This tool is completely free – no cost, no obligation! You will receive the full personalized report below and via email.**")
    st.write("The perfect home that supports your lifestyle awaits — anywhere in the U.S.!")

    client_needs = st.text_area("DESCRIBE YOUR DREAM WELLNESS NEEDS IN DETAIL. LET FRED DO THE REST!!!", height=220, placeholder="Example: Active couple in our 40s, love trails and home workouts, need gym space, near nature, budget $500k...")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
    with col2:
        location = st.text_input("Preferred state or area (e.g., North Carolina, Asheville, Tampa FL)", value="")

    st.markdown("### Refine Your Report (Optional)")
    st.write("Choose what you'd like to focus on — or get the full report!")
    report_sections = st.multiselect(
        "Select sections to include:",
        [
            "Introduction summary",
            "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)",
            "Top 5 Must-Have Home Features",
            "Wellness/Outdoor Highlights",
            "Cost of Living & Financial Breakdown",
            "Healthcare Access & Longevity Metrics",
            "Community & Social Wellness",
            "Climate & Seasonal Wellness Tips",
            "Transportation & Daily Convenience",
            "Future-Proofing for Aging in Place",
            "Sample Daily Wellness Routine in This Area"
        ],
        default=[
            "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)",
            "Top 5 Must-Have Home Features",
            "Wellness/Outdoor Highlights",
            "Cost of Living & Financial Breakdown",
            "Healthcare Access & Longevity Metrics"
        ]
    )

    if st.button("🔍 GENERATE MY REPORT", type="primary"):
        if not client_needs.strip():
            st.warning("Please describe your lifestyle needs above!")
        else:
            with st.spinner("Fred is crafting your personalized report and finding beautiful photos of each neighborhood..."):
                # Build selected and full prompts (same as before)
                selected_prompt = ""
                full_sections_prompt = """
### Introduction
5-6 sentences introducing how well their needs match the area and budget.

### Top 5 Neighborhoods/Suburbs and Why They Fit
1. [Neighborhood Name Here] - [Detailed explanation... 5-8 sentences.] [Fun facts: weather trends, cost of living, safety, commute/transportation, healthcare, culture/lifestyle, and overall vibe. 3-5 sentences.]
# (repeat for 2-5)

### Top 5 Must-Have Home Features
1. [Feature Name Here] - [In-depth reason... 5-8 sentences.]
# (repeat for 2-5)

### Wellness/Outdoor Highlights
6-10 sentences covering key trails, parks, etc.

### Cost of Living & Financial Breakdown
Detailed comparison of monthly expenses, property taxes, and affordability for longevity planning (6-8 sentences).

### Healthcare Access & Longevity Metrics
Top hospitals, specialists, life expectancy, air quality, and wellness infrastructure (5-7 sentences).

### Community & Social Wellness
Local groups, events, and opportunities for connection and belonging (5-7 sentences).

### Climate & Seasonal Wellness Tips
Year-round activity potential, weather patterns, and tips for thriving in all seasons (5-7 sentences).

### Transportation & Daily Convenience
Walkability, transit, and ease of daily errands for an active lifestyle (4-6 sentences).

### Future-Proofing for Aging in Place
Availability of accessible homes and long-term livability features (4-6 sentences).

### Sample Daily Wellness Routine in This Area
An inspiring example day tailored to the recommended locations (6-8 sentences).
"""

                base_prompt = f"""
                Client description:
                {client_needs}
                Budget: ${budget:,}
                Preferred location(s): {location or 'wellness-friendly areas across the U.S.'}

                You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties across the United States.

                Use warm, encouraging, insightful language.
                """

                # Build selected prompt
                if "Introduction summary" in report_sections:
                    selected_prompt += "### Introduction\n5-6 sentences introducing how well their needs match the area and budget.\n\n"
                if "Top 5 Neighborhoods/Suburbs and Why They Fit (with fun facts)" in report_sections:
                    selected_prompt += "### Top 5 Neighborhoods/Suburbs and Why They Fit\n1. [Neighborhood Name Here] - [Detailed explanation... 5-8 sentences.] [Fun facts: weather trends, cost of living, safety, commute/transportation, healthcare, culture/lifestyle, and overall vibe. 3-5 sentences.]\n# (repeat for 2-5)\n\n"
                if "Top 5 Must-Have Home Features" in report_sections:
                    selected_prompt += "### Top 5 Must-Have Home Features\n1. [Feature Name Here] - [In-depth reason... 5-8 sentences.]\n# (repeat for 2-5)\n\n"
                if "Wellness/Outdoor Highlights" in report_sections:
                    selected_prompt += "### Wellness/Outdoor Highlights\n6-10 sentences covering key trails, parks, etc.\n\n"
                if "Cost of Living & Financial Breakdown" in report_sections:
                    selected_prompt += "### Cost of Living & Financial Breakdown\nDetailed comparison of monthly expenses, property taxes, and affordability for longevity planning (6-8 sentences).\n\n"
                if "Healthcare Access & Longevity Metrics" in report_sections:
                    selected_prompt += "### Healthcare Access & Longevity Metrics\nTop hospitals, specialists, life expectancy, air quality, and wellness infrastructure (5-7 sentences).\n\n"
                if "Community & Social Wellness" in report_sections:
                    selected_prompt += "### Community & Social Wellness\nLocal groups, events, and opportunities for connection and belonging (5-7 sentences).\n\n"
                if "Climate & Seasonal Wellness Tips" in report_sections:
                    selected_prompt += "### Climate & Seasonal Wellness Tips\nYear-round activity potential, weather patterns, and tips for thriving in all seasons (5-7 sentences).\n\n"
                if "Transportation & Daily Convenience" in report_sections:
                    selected_prompt += "### Transportation & Daily Convenience\nWalkability, transit, and ease of daily errands for an active lifestyle (4-6 sentences).\n\n"
                if "Future-Proofing for Aging in Place" in report_sections:
                    selected_prompt += "### Future-Proofing for Aging in Place\nAvailability of accessible homes and long-term livability features (4-6 sentences).\n\n"
                if "Sample Daily Wellness Routine in This Area" in report_sections:
                    selected_prompt += "### Sample Daily Wellness Routine in This Area\nAn inspiring example day tailored to the recommended locations (6-8 sentences).\n\n"

                try:
                    # Generate selected report for display
                    selected_full_prompt = base_prompt + "\nOnly include the requested sections:\n\n" + selected_prompt
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Fred, a professional real estate advisor."}, {"role": "user", "content": selected_full_prompt}],
                        max_tokens=3000,
                        temperature=0.7
                    )
                    displayed_report = response.choices[0].message.content

                    # Generate full report for email
                    full_email_prompt = base_prompt + "\nInclude ALL sections for a complete report:\n\n" + full_sections_prompt
                    full_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Fred, a professional real estate advisor."}, {"role": "user", "content": full_email_prompt}],
                        max_tokens=4000,
                        temperature=0.7
                    )
                    full_report = full_response.choices[0].message.content

                    # Add images to both versions
                    location_hint = location or "USA"
                    displayed_report_with_images = add_images_to_report(displayed_report, location_hint)
                    full_report_with_images = add_images_to_report(full_report, location_hint)

                    # Show on screen
                    st.success("Fred found your perfect matches! Here's your personalized report with photos:")
                    st.markdown(displayed_report_with_images)

                    # Save full to history
                    st.session_state.chat_history["fred"].append({"role": "assistant", "content": f"Here's your COMPLETE wellness home report with photos:\n\n{full_report_with_images}"})

                    # Email form
                    st.markdown("### Get Your Full Report Emailed (Save & Share)")
                    with st.form("lead_form", clear_on_submit=True):
                        name = st.text_input("Your Name")
                        email = st.text_input("Email (required)", placeholder="you@example.com")
                        phone = st.text_input("Phone (optional)")
                        submitted = st.form_submit_button("📧 Send My Full Report")
                        if submitted:
                            if not email:
                                st.error("Email required!")
                            else:
                                email_body = f"Hi {name or 'there'},\n\nThank you for exploring LBL Lifestyle Solutions!\n\nYour complete personalized wellness home report — with beautiful photos of each recommended neighborhood — is below:\n\n{full_report_with_images}\n\nI'm here to help you find your perfect longevity home.\n\nBest regards,\nFred & the LBL Team"
                                data = {
                                    "from": "reports@lbllifestyle.com",
                                    "to": [email],
                                    "cc": [YOUR_EMAIL],
                                    "subject": f"{name or 'Client'}'s Complete LBL Wellness Home Report with Photos",
                                    "text": email_body
                                }
                                headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                                try:
                                    response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                                    if response.status_code == 200:
                                        st.success(f"Full report with photos sent to {email}!")
                                        st.balloons()
                                    else:
                                        st.error(f"Send failed: {response.text}")
                                except Exception as e:
                                    st.error(f"Send error: {str(e)}")
                except Exception as e:
                    st.error("Fred is reviewing listings... try again soon.")
                    st.caption(f"Error: {str(e)}")

    # Streamlined chat
    st.markdown("### Have a follow-up question? Start a chat with me in the Ask Fred banner below!")

    for msg in st.session_state.chat_history["fred"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask Fred a question..."):
        st.session_state.chat_history["fred"].append({"role": "user", "content": prompt})
        st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties across the United States."},
                        *st.session_state.chat_history["fred"]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["fred"].append({"role": "assistant", "content": reply})
                st.markdown(f"<div class='assistant-message'>{reply}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
