import streamlit as st
import requests
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", "")

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def fetch_pexels_image(neighborhood="", location_hint="", theme_hints=""):
    """Smart fallback: neighborhood → city/state → theme"""
    if not PEXELS_API_KEY:
        return None
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/v1/search"
    queries = []
    if neighborhood and location_hint:
        queries.append(f"{neighborhood} {location_hint} neighborhood homes landscape nature aerial view")
    if neighborhood:
        queries.append(f"{neighborhood} residential homes nature")
    if location_hint:
        queries.append(f"{location_hint} city skyline landscape homes nature")
        queries.append(f"{location_hint} scenic view aerial")
    if theme_hints:
        queries.append(f"{location_hint or 'USA'} {theme_hints} landscape nature")
    queries.append("wellness home nature landscape sunset")
    seen_urls = set()
    for query in queries:
        params = {"query": query, "per_page": 3, "orientation": "landscape"}
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for photo in data.get("photos", []):
                    img_url = photo["src"]["large2x"]
                    if img_url not in seen_urls:
                        seen_urls.add(img_url)
                        return img_url
        except:
            continue
    return None

def add_images_to_report(report_text, location_hint="", client_needs=""):
    """Add one relevant photo under each Top 5 neighborhood"""
    lines = report_text.split('\n')
    enhanced_lines = []
    in_top_5 = False
    seen_urls = set()
    lower_needs = client_needs.lower()
    theme_hints = ""
    if any(word in lower_needs for word in ["beach", "ocean", "tampa", "florida", "coast"]):
        theme_hints = "beach ocean sunset palm trees waterfront"
    elif any(word in lower_needs for word in ["mountain", "asheville", "colorado", "hike", "trail", "cabins"]):
        theme_hints = "mountains cabins forest autumn nature scenic"
    elif any(word in lower_needs for word in ["lake", "waterfront"]):
        theme_hints = "lake waterfront homes nature"
    for line in lines:
        enhanced_lines.append(line)
        if "Top 5 Neighborhoods" in line or "Top 5 Suburbs" in line:
            in_top_5 = True
        if in_top_5 and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            parts = line.split('-', 1)
            if len(parts) > 1:
                name_part = parts[0].strip()[2:].strip()
                img_url = fetch_pexels_image(name_part, location_hint, theme_hints)
                if img_url and img_url not in seen_urls:
                    enhanced_lines.append("")
                    enhanced_lines.append(f"![{name_part} – Beautiful homes and scenery]({img_url})")
                    enhanced_lines.append("")
                    seen_urls.add(img_url)
    return '\n'.join(enhanced_lines)

def show():
    # Initialize session state for chat history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {"fred": []}

    # CSS
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
        .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
        img { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 20px 0; max-width: 100%; height: auto; }
    </style>
    """, unsafe_allow_html=True)

    # Scroll to top
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
        const mainSection = window.parent.document.querySelector('section.main');
        if (mainSection) mainSection.scrollTop = 0;
        setTimeout(() => { window.scrollTo(0, 0); if (mainSection) mainSection.scrollTop = 0; }, 100);
    </script>
    """, unsafe_allow_html=True)

    # Back button — unique key
    if st.button("← Back to Team", key="fred_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg-J1J8SDEAY-unsplash.jpg", caption="Your Keys Await – Welcome to your longevity lifestyle")

    st.markdown("### 🏡 FRED – Your Wellness Home Scout")
    st.success("**This tool is completely free – no cost, no obligation! You will receive your personalized report below and a complete version via email if you request it.**")
    st.write("The perfect home that supports your lifestyle awaits — anywhere in the U.S.!")

    # Encouraging input
    st.markdown("### Tell Fred a little bit about you and your dream wellness home")
    st.write("**Be as detailed as possible!** The more you share about your age, family, hobbies, must-haves, daily routine, and wellness goals, the more accurate and personalized Fred's recommendations will be. 😊")
    st.caption("💡 Tip: Include age, family size, favorite activities, deal-breakers, and why longevity matters to you!")

    client_needs = st.text_area(
        "Share your story – the more details, the better Fred can help!",
        height=280,
        placeholder="""Example: We're a couple in our early 50s with two dogs, love morning walks, yoga, and cooking healthy meals. Looking for a quiet, nature-filled neighborhood with trails and parks nearby, a home with space for a yoga/meditation room, natural light, and a garden. Prefer single-level or main-floor master for aging in place. Budget up to $750k. Interested in Florida, North Carolina, or Colorado. We value community events, farmers markets, and low stress — no busy highways please!"""
    )

    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Maximum budget ($)", min_value=100000, value=500000, step=10000)
    with col2:
        location = st.text_input("Preferred state or area (e.g., North Carolina, Asheville, Tampa FL)", value="")

    location_hint = location.strip() if location else "wellness community USA"

    st.markdown("### Refine Your Report (Optional)")
    st.write("The report always includes: Introduction, Top 5 Neighborhoods, and Must-Have Features. Choose additional sections to add.")
    report_sections = st.multiselect(
        "Add optional sections:",
        [
            "Wellness/Outdoor Highlights",
            "Cost of Living & Financial Breakdown",
            "Healthcare Access & Longevity Metrics",
            "Community & Social Wellness",
            "Climate & Seasonal Wellness Tips",
            "Transportation & Daily Convenience",
            "Future-Proofing for Aging in Place",
            "Sample Daily Wellness Routine in This Area",
            "Top Property Recommendations"
        ],
        default=[
            "Wellness/Outdoor Highlights",
            "Cost of Living & Financial Breakdown",
            "Healthcare Access & Longevity Metrics"
        ]
    )

    if st.button("🔍 GENERATE MY REPORT", type="primary"):
        if not client_needs.strip():
            st.warning("Please share your story above so Fred can create the best report for you!")
        else:
            with st.spinner("Fred is crafting your personalized report..."):
                # Core sections (always included)
                core_prompt = """
### Introduction
5-6 sentences introducing how well their needs match the area and budget.
### Top 5 Neighborhoods/Suburbs and Why They Fit
1. [Neighborhood Name Here] - [Detailed explanation... 5-8 sentences.] [Fun facts: weather trends, cost of living, safety, commute/transportation, healthcare, culture/lifestyle, and overall vibe. 3-5 sentences.]
# (repeat for 2-5)
### Top 5 Must-Have Home Features
1. [Feature Name Here] - [In-depth reason... 5-8 sentences.]
# (repeat for 2-5)
"""
                # Optional sections (only if selected)
                optional_prompt = ""
                if "Wellness/Outdoor Highlights" in report_sections:
                    optional_prompt += "### Wellness/Outdoor Highlights\n6-10 sentences covering key trails, parks, etc.\n\n"
                if "Cost of Living & Financial Breakdown" in report_sections:
                    optional_prompt += "### Cost of Living & Financial Breakdown\nDetailed comparison of monthly expenses, property taxes, and affordability for longevity planning (6-8 sentences).\n\n"
                if "Healthcare Access & Longevity Metrics" in report_sections:
                    optional_prompt += "### Healthcare Access & Longevity Metrics\nTop hospitals, specialists, life expectancy, air quality, and wellness infrastructure (5-7 sentences).\n\n"
                if "Community & Social Wellness" in report_sections:
                    optional_prompt += "### Community & Social Wellness\nLocal groups, events, and opportunities for connection and belonging (5-7 sentences).\n\n"
                if "Climate & Seasonal Wellness Tips" in report_sections:
                    optional_prompt += "### Climate & Seasonal Wellness Tips\nYear-round activity potential, weather patterns, and tips for thriving in all seasons (5-7 sentences).\n\n"
                if "Transportation & Daily Convenience" in report_sections:
                    optional_prompt += "### Transportation & Daily Convenience\nWalkability, transit, and ease of daily errands for an active lifestyle (4-6 sentences).\n\n"
                if "Future-Proofing for Aging in Place" in report_sections:
                    optional_prompt += "### Future-Proofing for Aging in Place\nAvailability of accessible homes and long-term livability features (4-6 sentences).\n\n"
                if "Sample Daily Wellness Routine in This Area" in report_sections:
                    optional_prompt += "### Sample Daily Wellness Routine in This Area\nAn inspiring example day tailored to the recommended locations (6-8 sentences).\n\n"
                if "Top Property Recommendations" in report_sections:
                    optional_prompt += "### Top Property Recommendations\n1-3 specific property ideas with estimated prices, key wellness features, and why they fit (4-6 sentences each).\n\n"

                # Full report prompt (all possible sections) — used only for email
                full_report_prompt = core_prompt + """
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
### Top Property Recommendations
1-3 specific property ideas with estimated prices, key wellness features, and why they fit (4-6 sentences each).
"""

                base_prompt = f"""
                Client description:
                {client_needs}
                Budget: ${budget:,}
                Preferred location(s): {location or 'wellness-friendly areas across the U.S.'}
                You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties across the United States.
                Use warm, encouraging, insightful language.
                """

                try:
                    # Generate display report (core + selected optional)
                    display_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": "You are Fred, a professional goal-focused real estate advisor."},
                            {"role": "user", "content": base_prompt + "\n" + (core_prompt + optional_prompt)}
                        ],
                        max_tokens=3000,
                        temperature=0.7
                    )
                    display_report = display_response.choices[0].message.content

                    # Generate full report (all sections) for email only
                    full_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": "You are Fred, a professional goal-focused real estate advisor."},
                            {"role": "user", "content": base_prompt + "\n" + full_report_prompt}
                        ],
                        max_tokens=4000,
                        temperature=0.7
                    )
                    full_report = full_response.choices[0].message.content

                    # Add photos to both reports
                    display_report_with_images = add_images_to_report(display_report, location_hint, client_needs)
                    full_report_with_images = add_images_to_report(full_report, location_hint, client_needs)

                    # Display only the customized report on screen
                    st.success("Fred found your perfect matches! Here's your personalized report:")
                    st.markdown(display_report_with_images)

                    # Store the full report for email (hidden from UI)
                    st.session_state.full_report_for_email = full_report_with_images

                    # OPTIONAL: Add a helpful note
                    st.info("📧 Want the **complete version** with every possible section? Fill in the email form below to have it sent instantly!")

                except Exception as e:
                    st.error("Fred is reviewing listings... try again soon.")
                    st.caption(f"Error: {str(e)}")

    # Email form — only shown after report generated
    if "full_report_for_email" in st.session_state:
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
                    report_to_send = st.session_state.full_report_for_email
                    email_body = f"""Hi {name or 'there'},

Thank you for exploring LBL Lifestyle Solutions – Your Holistic Longevity Blueprint.

Here's your COMPLETE personalized wellness home report:

{report_to_send}

Reply anytime to discuss how we can build your complete longevity plan.

Best regards,
Fred & the LBL Team"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [YOUR_EMAIL],
                        "subject": f"{name or 'Client'}'s Complete LBL Wellness Home Report",
                        "text": email_body
                    }
                    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Complete report sent to {email}! Check your inbox.")
                            st.balloons()
                            if "full_report_for_email" in st.session_state:
                                del st.session_state.full_report_for_email
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # Streamlined follow-up chat (only for actual questions)
    st.markdown("### Have a follow-up question? Chat with Fred below!")
    st.caption("Ask anything to refine your search, explore a neighborhood, or get more details.")

    # Display chat history (only real conversation, not the report)
    for msg in st.session_state.chat_history["fred"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask Fred a question..."):
        # Add user message
        st.session_state.chat_history["fred"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Fred is thinking..."):
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
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
