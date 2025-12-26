import streamlit as st
import requests
from openai import OpenAI
from geopy.geocoders import Nominatim
import re

with st.sidebar:
    st.title("LBL Lifestyle Solutions")
    st.caption("Your Holistic Longevity Blueprint ❤️")

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
WALKSCORE_API_KEY = st.secrets.get("WALKSCORE_API_KEY", "")
AIRNOW_API_KEY = st.secrets.get("AIRNOW_API_KEY", "")
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"
geolocator = Nominatim(user_agent="lbl_fred_scout")

# WALK SCORE & AIRNOW ENRICHMENT (no lat/lon shown to user)
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
        }
        #backToTopBtn:hover {
            background-color: #40916c;
            transform: scale(1.1);
        }
    </style>
    """, unsafe_allow_html=True)

    # Back to Top Button
    st.markdown("""
    <button id="backToTopBtn">↑ Back to Top</button>
    <script>
        const btn = document.getElementById('backToTopBtn');
        const checkScroll = () => {
            const scrolled = window.pageYOffset > 300;
            btn.style.display = scrolled ? 'block' : 'none';
        };
        window.onscroll = checkScroll;
        btn.onclick = () => window.scrollTo({top: 0, behavior: 'smooth'});
        setTimeout(() => {
            const chatInput = document.querySelector('.stChatInput input');
            if (chatInput) chatInput.blur();
        }, 100);
    </script>
    """, unsafe_allow_html=True)

    # HERO & WELCOME
    st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", use_column_width=True)
    st.markdown("<h1>Meet Fred – Your Patient Wellness Home Scout 🏡</h1>", unsafe_allow_html=True)
    st.markdown("**Take your time.** I’m here to help you find (or create) a home that truly supports a longer, healthier, more joyful life — whether buying, renting, or just exploring ideas.")
    st.caption("No rush. The more you share, the better I can help ❤️")

    # PERSONALITY (Greg-style wording)
    st.markdown("<div class='personality-box'>", unsafe_allow_html=True)
    st.markdown("<h3>✨ Let's Make This Truly Personal!</h3>", unsafe_allow_html=True)
    st.caption("Select any combination of traits to customize how I communicate with you. 😊")
    st.markdown("• **Fred's Personality Traits** – How you'd like me to scout for you")
    st.markdown("• **How You Like to Communicate** – How you'd prefer to be spoken to")
    st.caption("The more you select, the more uniquely tailored our conversation will become — like having a wellness home scout designed just for you! 🏡")

    agent_traits = st.multiselect(
        "Fred's Personality Traits",
        ["Friendly & Encouraging", "Professional & Efficient", "Analytical & Data-Driven", "Creative & Visionary", "Humorous & Light-Hearted"],
        default=["Friendly & Encouraging"]
    )

    user_prefs = st.multiselect(
        "How You Like to Communicate",
        ["Detailed & Thorough", "Direct & Concise", "Empathetic & Supportive", "Inspirational & Motivating", "Casual & Conversational"],
        default=["Detailed & Thorough"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # DISCLAIMERS
    st.success("Fred is a free educational tool, not professional real estate or medical advice. Always consult licensed experts. 🏡❤️")
    st.warning("Reports are AI-generated based on public data – verify with local sources.")

    # USER NAME
    st.session_state.user_name = st.text_input("Your Name (so I can make this personal)", value=st.session_state.get("user_name", ""), help="I'll use your name in the report and chat ❤️")

    # QUICK STARTS
    with st.expander("Need Inspiration? Try a Quick Start"):
        st.caption("These are gentle examples — click any to see what a report looks like")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Peaceful neighborhoods near trails"):
                st.session_state.quick_start = "Peaceful neighborhoods near trails in Florida with good air quality"
        with col2:
            if st.button("Wellness-friendly rentals"):
                st.session_state.quick_start = "Wellness-friendly rentals in Sarasota or Naples"
        with col3:
            if st.button("Modify my current home"):
                st.session_state.quick_start = "How to modify my current home for aging in place and longevity"

    # FORM
    st.markdown("### Take Your Time — Share Your Vision")
    st.caption("The more you tell me, the better I can help. There's no wrong way to fill this in ❤️")

    buy_or_rent = st.radio("Are you thinking of buying, renting, or open to both?", ("Buy a home", "Rent a home", "Open to either"), horizontal=True)

    st.caption("Your budget helps me find options that feel comfortable and realistic")
    if "Rent" in buy_or_rent:
        min_rent = st.text_input("Minimum Monthly Rent", value="1500")
        max_rent = st.text_input("Maximum Monthly Rent", value="3500")
        budget = f"${min_rent}–${max_rent}/month"
    else:
        min_buy = st.text_input("Minimum Purchase Budget", value="300000")
        max_buy = st.text_input("Maximum Purchase Budget", value="750000")
        budget = f"${min_buy}–${max_buy}"

    locations = st.text_input("Preferred Locations", placeholder="e.g., Naples FL, Sarasota, Asheville NC", help="Type any cities, neighborhoods, or states you're curious about — or leave blank for my best suggestions")

    must_haves = st.multiselect(
        "Must-Have Wellness Features",
        ["Near trails/parks", "Quiet/low noise", "Good air quality", "Walkable to shops", "Home gym space", "Natural light", "Low EMF potential", "Community amenities", "Near healthy grocery", "Garden/yard space"],
        help="What would make a home feel perfect for your health and happiness?"
    )

    deal_breakers = st.multiselect(
        "Deal-Breakers",
        ["Busy roads/high traffic", "High crime area", "Poor air quality", "No nature access", "Strict HOA", "Flood zone", "Far from medical facilities", "Industrial area"],
        help="And what would you rather avoid?"
    )

    home_type_options = ["Single family home", "Condo/Townhouse", "55+ community", "Villa/Patio home", "No preference"]
    if "Rent" in buy_or_rent:
        home_type_options.insert(0, "Apartment")
    home_type = st.selectbox("Home Type Preference", home_type_options, help="I'll focus on what fits your life best")

    timeline = st.select_slider("When are you thinking of making a move?", options=["Exploring now", "3–6 months", "6–12 months", "1+ years"], value="Exploring now")

    household = st.multiselect("Who is this home for? (select all that apply)", ["Solo", "Couple", "Family with kids", "Multi-generational", "Pets"])

    st.caption("These three sections are always included — choose more if you'd like")
    additional_sections = st.multiselect(
        "Extra Topics for Your Report",
        ["Cost of Living & Financial Breakdown", "Climate & Seasonal Wellness Tips", "Transportation & Daily Convenience", "Future-Proofing for Aging in Place", "Sample Daily Wellness Routine in This Area", "Top Property Recommendations"]
    )

    client_needs = st.text_area(
        "Tell me anything else about your vision",
        value=st.session_state.get("quick_start", ""),
        placeholder="Just talk to me like you would a friend. The more you share, the better I can help ❤️",
        height=150
    )
    if "quick_start" in st.session_state:
        del st.session_state.quick_start

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
User is {buy_or_rent.lower()}. Budget: {budget}.
Preferred locations: {locations or 'Open to suggestions'}.
Must-haves: {', '.join(must_haves) or 'None'}.
Deal-breakers: {', '.join(deal_breakers) or 'None'}.
Home type: {home_type}.
Timeline: {timeline}.
Household: {', '.join(household) or 'None'}.
Extra sections: {', '.join(additional_sections) or 'None'}.
"""

                    user_prompt = f"{structured_inputs}\nUser's thoughts: {client_needs}\n"
                    if specific_input:
                        user_prompt += f"Specific to analyze: {specific_input}\n"

                    # Report prompt — warm, professional, always includes 3 minimum + selected
                    report_prompt = """
You are Fred, the Wellness Home Scout. Write the main report in a warm, professional, detailed, and inspirational tone — like a trusted longevity advisor sharing a beautiful blueprint.
Use flowing paragraphs and clear headings.
Always include these three sections:
- Wellness/Outdoor Highlights
- Healthcare Access & Longevity Metrics
- Community & Social Wellness
Include any extra sections the user selected.
Always include Top 5 Neighborhoods/Suburbs with brief longevity reasoning and Top 5 Must-Have Features for each.
Do not include latitude/longitude coordinates.
Do not use bullets or asterisks for main content — use flowing paragraphs.
"""

                    messages = [
                        {"role": "system", "content": report_prompt},
                        {"role": "user", "content": user_prompt}
                    ]

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        max_tokens=2500,
                        temperature=0.7
                    )
                    report_text = response.choices[0].message.content

                    enriched_report = enrich_report(report_text, locations or "Florida")
                    full_report = enriched_report  # Pexels paused

                    st.session_state.full_report_for_email = full_report
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}. Please try again.")

    # PERSISTENT FULL REPORT DISPLAY (always visible if generated)
    if "full_report_for_email" in st.session_state:
        st.markdown("<div id='report-anchor'></div>", unsafe_allow_html=True)
        st.markdown("### Your Personalized Wellness Home Report 🏡")
        st.caption("Made just for you — feel free to scroll and reference while we chat")
        st.markdown(st.session_state.full_report_for_email)

        # EMAIL FORM
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

    # CHAT SECTION (chat can reference report)
    st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Ready to talk about your report?")
    st.caption("Ask me anything — I'm here to help refine or explain")

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
                # Chat uses selected personality and can reference report
                chat_prompt = f"""
You are Fred. Be {' and '.join(agent_traits).lower()}.
Respond in a {' and '.join(user_prefs).lower()} style.
Use the user's name if provided.
Reference the report if relevant.
Stay warm and caring.
Report content: {st.session_state.full_report_for_email if "full_report_for_email" in st.session_state else 'No report generated yet'}
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
