import streamlit as st
import requests
from openai import OpenAI
import re
from geopy.geocoders import Nominatim

with st.sidebar:
    st.title("LBL Lifestyle Solutions")
    st.caption("Your Holistic Longevity Blueprint ❤️")

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", "")
WALKSCORE_API_KEY = st.secrets.get("WALKSCORE_API_KEY", "")
AIRNOW_API_KEY = st.secrets.get("AIRNOW_API_KEY", "")
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

# Initialize geolocator
geolocator = Nominatim(user_agent="lbl_wellness_scout")

# THEMED WELLNESS IMAGES (safe, beautiful, no duplicates)
WELLNESS_THEMES = [
    "sunset nature trail wellness walk landscape USA",
    "peaceful home garden natural light sunset wellness",
    "yoga outdoors nature park trail sunset USA",
    "serene suburban home green landscape wellness",
    "family walking trail nature wellness sunset",
    "outdoor meditation garden wellness home sunset",
    "tranquil backyard nature wellness sunset Florida"
]

seen_image_urls = set()  # Global to prevent duplicates across report

def fetch_thematic_image():
    global seen_image_urls
    if not PEXELS_API_KEY:
        return None
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/v1/search"
    
    for query in WELLNESS_THEMES:
        params = {
            "query": query,
            "per_page": 5,
            "orientation": "landscape",
            "locale": "en-US"
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for photo in data.get("photos", []):
                    img_url = photo["src"]["large2x"]
                    if img_url not in seen_image_urls:
                        seen_image_urls.add(img_url)
                        return img_url
        except:
            continue
    return None

def add_thematic_images(report_text):
    lines = report_text.split('\n')
    enhanced_lines = []
    image_count = 0
    max_images = 4
    
    for line in lines:
        enhanced_lines.append(line)
        if image_count < max_images and (line.strip() == "" or "Highlights" in line or "Metrics" in line or "Wellness" in line or "Score" in line or line.strip().endswith(".")):
            img_url = fetch_thematic_image()
            if img_url:
                enhanced_lines.append("")
                enhanced_lines.append(f"![Inspiring wellness lifestyle]({img_url})")
                enhanced_lines.append("")
                image_count += 1
    return '\n'.join(enhanced_lines)

# ENRICHMENT (Walk Score + AirNow)
def get_walk_scores(lat, lon):
    if not WALKSCORE_API_KEY:
        return "Walk Score data unavailable"
    url = "https://walk-score.p.rapidapi.com/score"
    querystring = {"lat": str(lat), "lon": str(lon), "format": "json"}
    headers = {
        "X-RapidAPI-Key": WALKSCORE_API_KEY,
        "X-RapidAPI-Host": "walk-score.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            walk = data.get("walkscore", "N/A")
            transit = data.get("transit", {}).get("score", "N/A")
            bike = data.get("bike", {}).get("score", "N/A")
            return f"Walk Score: {walk}/100 | Transit: {transit}/100 | Bike: {bike}/100"
    except:
        pass
    return "Scores temporarily unavailable"

def get_air_quality(lat, lon):
    if not AIRNOW_API_KEY:
        return "Air quality data unavailable"
    url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=25&API_KEY={AIRNOW_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                aqi = data[0]["AQI"]
                category = data[0]["Category"]["Name"]
                return f"Current AQI: {aqi} ({category})"
    except:
        pass
    return "Air quality data temporarily unavailable"

def geocode_location(location_name, state):
    try:
        location = geolocator.geocode(f"{location_name}, {state}, USA", timeout=10)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None, None

def enrich_report(report_text, state):
    lines = report_text.split('\n')
    enhanced_lines = []
    in_top_5 = False
    
    for line in lines:
        enhanced_lines.append(line)
        if "Top 5" in line:
            in_top_5 = True
        if in_top_5 and re.match(r'^\d+\.', line.strip()):
            name_part = re.sub(r'^\d+\.\s*', '', line.strip()).split('-', 1)[0].split(':', 1)[0].split('(', 1)[0].strip()
            if name_part:
                lat, lon = geocode_location(name_part, state)
                if lat and lon:
                    enhanced_lines.append(f"\n**Wellness Enrichment for {name_part}:**")
                    enhanced_lines.append(get_walk_scores(lat, lon))
                    enhanced_lines.append(get_air_quality(lat, lon))
                    enhanced_lines.append("")
    return '\n'.join(enhanced_lines)

def show():
    st.set_page_config(page_title="Fred – Your Wellness Home Scout | LBL Lifestyle Solutions", page_icon="🏡")

    agent_key = "fred"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if agent_key not in st.session_state.chat_history:
        st.session_state.chat_history[agent_key] = []

    # DESIGN & STYLING
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
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div[data-baseweb="select"] > div,
        .stMultiSelect > div > div > div,
        .stNumberInput > div > div > input {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }
        .stMultiSelect > div {
            background-color: white !important;
        }
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: #1e3a2f !important;
        }
        .stChatInput > div {
            background-color: white !important;
            border: 2px solid #2d6a4f !important;
            border-radius: 20px !important;
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
        .personality-box {
            background-color: #f0f7fc;
            border: 2px solid #a0c4d8;
            border-radius: 16px;
            padding: 24px;
            margin: 30px 0;
            text-align: center;
        }
        .separator {
            margin: 35px 0;
            border-top: 1px solid #c0d8e0;
        }
        /* Back to Top Button — Bottom-Left */
        #backToTopBtn {
            position: fixed;
            bottom: 120px;
            left: 20px;
            z-index: 999;
            display: none;
            background-color: #2d6a4f;
            color: white;
            padding: 14px 18px;
            border-radius: 50px;
            border: none;
            font-size: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        #backToTopBtn:hover {
            background-color: #40916c;
            transform: scale(1.1);
        }
        #report-anchor, #chat-anchor {
            margin-top: 100px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Back to Top Button + Disable Chat Auto-Focus
    st.markdown("""
    <button id="backToTopBtn">↑ Back to Top</button>
    <script>
        const btn = document.getElementById('backToTopBtn');
        const checkScroll = () => {
            const scrolled = window.pageYOffset > 300 ||
                             (parent.document.body.scrollTop > 300) ||
                             (parent.document.documentElement.scrollTop > 300) ||
                             (parent.document.querySelector('section.main') && parent.document.querySelector('section.main').scrollTop > 300);
            btn.style.display = scrolled ? 'block' : 'none';
        };
        window.addEventListener('load', checkScroll);
        window.addEventListener('scroll', checkScroll);
        const mainSection = parent.document.querySelector('section.main');
        if (mainSection) mainSection.addEventListener('scroll', checkScroll);
        btn.addEventListener('click', () => {
            window.scrollTo({top: 0, behavior: 'smooth'});
            if (mainSection) mainSection.scrollTo({top: 0, behavior: 'smooth'});
        });
        checkScroll();

        setTimeout(() => {
            const chatInputs = document.querySelectorAll('input[type="text"]');
            chatInputs.forEach(input => input.blur());
        }, 100);
    </script>
    """, unsafe_allow_html=True)

    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg_J1J8SDEAY-unsplash.jpg", use_column_width=True)

    st.markdown("<h1>Welcome to my office — I’m Fred, your Wellness Home Scout 🏡</h1>", unsafe_allow_html=True)
    st.markdown("**Take your time.** I’m here to help you find (or create) a home that truly supports a longer, healthier, more joyful life — whether buying, renting, or just exploring ideas.")
    st.caption("No rush. The more you share, the better I can help ❤️")

    # NAME BLOCK
    st.markdown("### What's your name? ✏️")
    st.caption("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", placeholder="e.g., Alex, Sarah", label_visibility="collapsed")
    if user_name:
        st.session_state.user_name = user_name.strip()
        st.success(f"Nice to meet you, {st.session_state.user_name}! ✨")
    else:
        if "user_name" in st.session_state:
            del st.session_state.user_name

    # PERSONALITY
    st.markdown("<div class='personality-box'>", unsafe_allow_html=True)
    st.markdown("<h3>✨ Let's Make This Truly Personal!</h3>", unsafe_allow_html=True)
    st.caption("Select any combination of traits to customize how I communicate with you. 😊")
    st.markdown("• **Fred's Personality Traits** – How you'd like me to scout for you")
    st.markdown("• **How You Like to Communicate** – How you'd prefer to be spoken to")
    st.caption("The more you select, the more uniquely tailored our conversation will become — like having a wellness home scout designed just for you! 🏡")

    col1, col2 = st.columns(2)
    with col1:
        agent_traits = st.multiselect(
            "Fred's Personality Traits",
            ["Friendly & Encouraging", "Professional & Efficient", "Analytical & Data-Driven", "Creative & Visionary", "Humorous & Light-Hearted"],
            default=["Friendly & Encouraging"]
        )
    with col2:
        user_prefs = st.multiselect(
            "How You Like to Communicate",
            ["Detailed & Thorough", "Direct & Concise", "Empathetic & Supportive", "Inspirational & Motivating", "Casual & Conversational"],
            default=["Detailed & Thorough"]
        )

    # INPUT FORM
    st.markdown("### Tell me about your wellness home vision 🏡")
    st.caption("Share as much or as little as you'd like — I'll craft a personalized report just for you ❤️")

    with st.expander("Quick Start Ideas 💡"):
        st.markdown("""
        - "Quiet Florida suburbs with parks, budget $500k"
        - "Nature-filled rentals in Colorado for active 60s couple"
        - "Wellness mods for my current home in NC"
        """)

    buy_or_rent = st.selectbox("Buy, rent, or modify current home?", ["Buy", "Rent", "Modify Existing"])
    locations = st.text_input("Preferred locations? (e.g., states, cities)", placeholder="Florida, North Carolina, open to suggestions")
    budget = st.text_input("Budget? (optional)", placeholder="e.g., Up to $750k or $2,500/month rent")
    home_type = st.selectbox("Home type?", ["House", "Condo/Apartment", "Townhome", "Any"])
    home_type_notes = st.text_area("More on home type? (optional)", placeholder="e.g., Single-level for accessibility", height=100)
    timeline = st.selectbox("Timeline?", ["Immediate", "3-6 months", "6-12 months", "Just exploring"])
    household = st.multiselect("Household? (select all that apply)", ["Solo", "Couple", "Kids", "Pets", "Elderly family", "Multi-generational"])
    household_notes = st.text_area("More on household? (optional)", placeholder="e.g., 'We have two large dogs' or 'Multi-generational with elderly parents'", height=100)

    priorities = st.multiselect(
        "Wellness Priorities (select all that apply)",
        ["Walkability & Trails", "Blue Zones Inspired", "Proximity to Nature", "Clean Air Quality", "Community Events", "Farmers Markets", "Yoga/Wellness Spaces", "Low Stress Environment"],
        default=["Walkability & Trails", "Proximity to Nature"]
    )

    must_haves = st.multiselect("Must-Haves", ["Backyard/Garden", "Natural Light", "Quiet Area", "Nearby Parks/Trails", "Home Gym Space", "Meditation Room"])
    must_haves_notes = st.text_area("More on must-haves? (optional)", placeholder="e.g., 'Space for vegetable garden'", height=100)
    deal_breakers = st.multiselect("Deal-Breakers", ["Busy Highways", "High Pollution", "No Green Space", "Poor Walkability", "High Crime"])
    deal_breakers_notes = st.text_area("More on deal-breakers? (optional)", placeholder="e.g., 'No homes near industrial areas'", height=100)

    st.caption("These three are always included — choose more if you'd like deeper insights:")
    additional_sections = st.multiselect(
        "Extra Topics for Your Report",
        ["Cost of Living & Financial Breakdown", "Climate & Seasonal Wellness Tips", "Transportation & Daily Convenience", "Future-Proofing for Aging in Place", "Sample Daily Wellness Routine in This Area", "Top Property Recommendations"],
        default=[],
        help="Wellness/Outdoor Highlights, Healthcare Access & Longevity Metrics, and Community & Social Wellness are always in your report"
    )

    client_needs = st.text_area(
        "Tell me anything else about your vision",
        placeholder="We're a couple in our early 50s with two dogs, love morning walks, yoga, and cooking healthy meals. Looking for a quiet, nature-filled neighborhood with trails and parks nearby, a home with space for a yoga/meditation room, natural light, and a garden. Prefer single-level or main-floor master for aging in place. Budget up to $750k. Interested in Florida, North Carolina, or Colorado. We value community events, farmers markets, and low stress — no busy highways please!",
        height=150
    )

    with st.expander("🔍 Have a specific property, neighborhood, or listing in mind?"):
        st.caption("Paste it here and I'll evaluate it directly for wellness fit")
        specific_input = st.text_area(
            "Specific address, neighborhood, or listing URL",
            placeholder="e.g., '123 Ocean Drive, Naples, FL' or 'Veranda Springs'",
            height=100,
            label_visibility="collapsed"
        )

    st.markdown("### Ready When You Are")
    st.caption("When you're happy with what you've shared, click below — I'll create your report with care")

    if st.button("Create My Wellness Home Report 🏡", type="primary"):
        if not client_needs and not specific_input and not locations:
            st.info("No worries — share just a little and I'll get started. Or try one of the Quick Starts above ❤️")
        else:
            with st.spinner("Taking my time to craft your perfect report..."):
                try:
                    structured_inputs = f"""
User name: {st.session_state.user_name or 'there'}
User is {buy_or_rent.lower()}. Budget: {budget}.
Preferred locations: {locations or 'Open to suggestions'}.
Priorities: {', '.join(priorities) or 'Wellness-focused defaults'}.
Must-haves: {', '.join(must_haves) or 'None'}.
Deal-breakers: {', '.join(deal_breakers) or 'None'}.
Home type: {home_type}.
Timeline: {timeline}.
Household: {', '.join(household) or 'None'}.
Extra sections: {', '.join(additional_sections) or 'None'}.
Additional notes: Must-haves: {must_haves_notes} Deal-breakers: {deal_breakers_notes} Home type: {home_type_notes} Household: {household_notes}
"""

                    user_prompt = f"{structured_inputs}\nUser's thoughts: {client_needs}\n"
                    if specific_input:
                        user_prompt += f"Specific to analyze: {specific_input}\n"

                    report_prompt = """
You are Fred, the Wellness Home Scout. Write the main report in a warm, professional, detailed, and deeply aspirational tone — like a trusted longevity advisor sharing a beautiful blueprint.
Use flowing paragraphs of 5–7 sentences. Paint vivid pictures of the lifestyle.
Always include:
- Introduction (5-6 sentences)
- Longevity Score (1–10) with brief explanation
- Top 5 Neighborhoods/Suburbs with longevity reasoning (5-8 sentences each)
- Top 5 Must-Have Features (5-6 sentences each)
- Wellness/Outdoor Highlights (6-10 sentences)
- Healthcare Access & Longevity Metrics (4-6 sentences)
- Community & Social Wellness (4-6 sentences)
- If extra sections selected, include them
- One Thing to Watch (gentle note)
- Next Steps with the LBL Team teaser
Use clear, professional language. No bullets except for light reference.
"""

                    messages = [
                        {"role": "system", "content": report_prompt},
                        {"role": "user", "content": user_prompt}
                    ]

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        max_tokens=3000,
                        temperature=0.7
                    )
                    report_text = response.choices[0].message.content

                    enriched_report = enrich_report(report_text, locations or "Florida")
                    full_report = add_thematic_images(enriched_report)

                    st.session_state.full_report_for_email = full_report

                    # Report summary for chat (hidden)
                    report_summary = f"""
User's name: {st.session_state.user_name or 'friend'}
Seeking: {buy_or_rent.lower()}
Budget: {budget}
Preferred locations: {locations or 'open'}
Must-haves: {', '.join(must_haves) or 'none'}
Top neighborhoods: (from report)
Key themes: wellness, nature access, quiet, clean air
Longevity Score and main points from report
"""
                    st.session_state.report_summary = report_summary
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}. Please try again.")

    # PERSISTENT FULL REPORT DISPLAY — Collapsible sections
    if "full_report_for_email" in st.session_state:
        st.markdown("<div id='report-anchor'></div>", unsafe_allow_html=True)
        st.markdown("### Your Personalized Wellness Home Report 🏡")
        st.caption("Made just for you — with care")
        sections = st.session_state.full_report_for_email.split('## ')  # Assuming ## for headings; adjust if needed
        for section in sections[1:]:  # Skip intro if no heading
            with st.expander(section.split('\n')[0]):
                st.markdown('\n'.join(section.split('\n')[1:]))

        # EMAIL DELIVERY
        with st.form("email_form"):
            st.markdown("### Want a Copy of the Full Report Emailed?")
            st.caption("Perfect for saving or sharing with family ❤️")

            default_name = st.session_state.user_name if "user_name" in st.session_state else ""
            name_for_email = st.text_input("Your Name (optional)", value=default_name)

            email = st.text_input("Your Email", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Report")
            if submitted:
                if not email:
                    st.error("Email needed to send your report")
                else:
                    report_to_send = st.session_state.full_report_for_email
                    email_body = f"""Hi {name_for_email or st.session_state.user_name or 'there'},

Thank you for trusting me with your wellness home search at LBL Lifestyle Solutions.

Here is your complete, personalized Wellness Home Report — crafted with care to help you find a home that truly supports a longer, healthier, and more joyful life.

{report_to_send}

I'm always here if you'd like to discuss any part of this, refine your vision, or meet the rest of the team (Greg for fitness, Zoey for health, Nora for nutrition).

To your health and home,

Fred & the LBL Team 🏡❤️
"""
                    data = {
                        "from": "fred@lbllifestyle.com",
                        "to": [email],
                        "cc": [YOUR_EMAIL],
                        "subject": f"{name_for_email or st.session_state.user_name or 'Your'} Personalized Wellness Home Report",
                        "text": email_body
                    }
                    headers = {
                        "Authorization": f"Bearer {RESEND_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Report sent to {email}! Check your inbox 🎉")
                            st.balloons()
                        else:
                            st.error("Send failed — please try again")
                    except:
                        st.error("Connection issue — please try again")

    # CHAT SECTION
    st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Ready to talk about your report?")
    st.caption("Ask me anything — I'm here to help refine or explain")

    # Inject report summary once (hidden)
    if "report_summary" in st.session_state:
        if not any(m["role"] == "system" and "report summary" in m["content"].lower() for m in st.session_state.chat_history[agent_key]):
            st.session_state.chat_history[agent_key].insert(0, {"role": "system", "content": st.session_state.report_summary})

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Chat with Fred..."):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Thinking..."):
            try:
                chat_prompt = f"""
You are Fred. Be {' and '.join(agent_traits).lower() if agent_traits else 'friendly and encouraging'}.
Respond in a {' and '.join(user_prefs).lower() if user_prefs else 'detailed and thorough'} style.
Use the user's name: {st.session_state.user_name or 'there'}.
Reference the report summary when relevant.
Stay warm and caring.
"""

                messages = [
                    {"role": "system", "content": chat_prompt},
                    *st.session_state.chat_history[agent_key]
                ]

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content

                st.session_state.chat_history[agent_key].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Trouble connecting — try again")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI ❤️</small>", unsafe_allow_html=True)

show()
