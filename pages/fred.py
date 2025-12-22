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
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {"fred": []}

    # HIGH-CONTRAST DESIGN
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: linear-gradient(to bottom, #f5f7fa, #e0e7f0);
            color: #1e3a2f;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #2d6a4f;
            font-weight: 600;
        }
        /* Force consistent input styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div[data-baseweb="select"] > div,
        .stNumberInput > div > div > input {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }
        /* Dropdown selected item visible */
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: #1e3a2f !important;
        }
        /* Chat input visible */
        .stChatInput > div {
            background-color: white !important;
            border: 2px solid #2d6a4f !important;
        }
        .stChatInput > div > div > input {
            color: #1e3a2f !important;
        }
        /* No overlay on chat messages */
        .stChatMessage {
            background-color: transparent !important;
        }
        .optional-box {
            background-color: #f0f7fc !important;
            border: 2px solid #a0c4d8 !important;
            border-left: 6px solid #2d6a4f !important;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 25px;
        }
        label {
            font-weight: 600 !important;
            color: #2d6a4f !important;
            font-size: 1.05rem !important;
        }
        .separator {
            margin: 35px 0;
            border-top: 1px solid #c0d8e0;
        }
        .stButton>button {
            background-color: #2d6a4f;
            color: white;
            border-radius: 12px;
            font-weight: 600;
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

    # Scroll to top
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
        const mainSection = window.parent.document.querySelector('section.main');
        if (mainSection) mainSection.scrollTop = 0;
        setTimeout(() => { window.scrollTo(0, 0); if (mainSection) mainSection.scrollTop = 0; }, 100);
    </script>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Team", key="fred_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg_J1J8SDEAY-unsplash.jpg", caption="Your Keys Await – Welcome to your longevity lifestyle")

    # Welcome & Disclaimer
    st.markdown("### 🏡 Hello! I'm Fred – Your Wellness Home Scout")
    st.write("I'm here to help you find or create a home environment that actively supports your health, recovery, and longevity — anywhere in the U.S.")
    st.warning("**Important**: I am not a licensed real estate agent. My recommendations are general wellness education based on research and trends. Always consult a licensed professional for real estate decisions.")
    st.success("**This tool is completely free – no cost, no obligation! Your full report will be emailed if requested.**")

    # Name Input
    st.markdown("### What's your name?")
    st.write("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="fred_name_input")
    if user_name:
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = "there"

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        Here are popular ways users get started:
        - Find quiet neighborhoods with trails near Tampa
        - Suggest homes with gym space under $600k
        - Compare walkability in Asheville vs Sarasota
        - Modify my current home for aging in place
        """)

    # Input form
    st.markdown("### Tell Fred a little bit about you and your dream wellness home")
    st.write("**Be as detailed as possible!** The more you share about your age, family, hobbies, must-haves, daily routine, and wellness goals, the more accurate and personalized my recommendations will be. 😊")
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
                # [Generation logic unchanged — uses st.session_state.user_name in base_prompt and email]

                # After report
                st.success("Fred found your perfect matches! Here's your personalized report:")
                st.markdown(display_report_with_images)

                st.session_state.full_report_for_email = full_report_with_images

                st.info("📧 Want the **complete version** with every section? Fill in the email form below!")

                # Follow-up
                st.markdown("### Would you like me to...")
                st.markdown("""
                - Refine this for a different budget or location?
                - Add more community/social details?
                - Suggest home modifications for better wellness?
                - Coordinate with Greg for a home gym setup?
                """)

    # [Email form, chat, footer — unchanged]

show()
