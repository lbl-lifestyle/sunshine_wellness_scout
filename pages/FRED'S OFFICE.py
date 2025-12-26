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
PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", "")
WALKSCORE_API_KEY = st.secrets.get("WALKSCORE_API_KEY", "")
AIRNOW_API_KEY = st.secrets.get("AIRNOW_API_KEY", "")
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"
geolocator = Nominatim(user_agent="lbl_fred_scout")

# PEXELS FUNCTIONS (refined for specificity)
def fetch_pexels_image(neighborhood="", location_hint="", theme_hints=""):
    if not PEXELS_API_KEY:
        return None
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/v1/search"
    
    queries = []
    if neighborhood and location_hint:
        queries.append(f"{neighborhood} {location_hint} residential neighborhood aerial view")
        queries.append(f"{neighborhood} {location_hint} wellness park trail")
    if neighborhood:
        queries.append(f"{neighborhood} suburban homes green landscape")
    if location_hint:
        queries.append(f"{location_hint} city residential area nature no beach")
        queries.append(f"{location_hint} inland scenic view")
    if theme_hints:
        queries.append(f"{location_hint or 'USA'} {theme_hints} residential wellness landscape")
    
    queries.append("wellness home suburban park trail landscape no ocean")
    
    seen_urls = set()
    for query in queries:
        params = {
            "query": query,
            "per_page": 3,
            "orientation": "landscape",
            "locale": "en-US",
            "color": "green" if "inland" in theme_hints.lower() or "park" in theme_hints.lower() else None
        }
        params = {k: v for k, v in params.items() if v is not None}
        
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
        theme_hints = "lake waterfront homes nature no ocean"
    else:
        theme_hints = "suburban park trail residential green landscape"
    
    for line in lines:
        enhanced_lines.append(line)
        if "Top 5" in line:
            in_top_5 = True
        if in_top_5 and re.match(r'^\d+\.', line.strip()):
            name_part = re.sub(r'^\d+\.\s*', '', line.strip()).split('-', 1)[0].split(':', 1)[0].split('(', 1)[0].strip()
            if name_part:
                img_url = fetch_pexels_image(name_part, location_hint, theme_hints)
                if img_url and img_url not in seen_urls:
                    enhanced_lines.append("")
                    enhanced_lines.append(f"![{name_part} – Wellness-friendly homes and scenery]({img_url})")
                    enhanced_lines.append("")
                    seen_urls.add(img_url)
    return '\n'.join(enhanced_lines)

# ENRICHMENT FUNCTIONS
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
                return f"Current AQI: {aqi} ({category}) – {data[0]['ParameterName']} levels"
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

    # Back to Top Button
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
        window.onscroll = checkScroll;
        parent.document.onscroll = checkScroll;
        btn.onclick = () => {
            window.scrollTo({top: 0, behavior: 'smooth'});
            parent.document.body.scrollTop = 0;
            parent.document.documentElement.scrollTop = 0;
            const main = parent.document.querySelector('section.main');
            if (main) main.scrollTop = 0;
        };
        setTimeout(() => {
            const chatInput = document.querySelector('.stChatInput input');
            if (chatInput) chatInput.blur();
        }, 100);
    </script>
    """, unsafe_allow_html=True)

    # HERO & WELCOME
    st.image("https://i.postimg.cc/MGxQfXtd/austin-distel-h1RW-NFt-Uyc-unsplash.jpg", use_column_width=True)
    st.markdown("<h1>Meet Fred – Your Wellness Home Scout 🏡</h1>", unsafe_allow_html=True)
    st.caption("Find a home or rental that supports your active, healthy lifestyle.")
    st.markdown("Fred helps buyers and renters discover longevity-friendly homes through clean air, walkability, nature access, quiet, and wellness features.")

    # PERSONALITY
    st.markdown("<div class='personality-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Customize Fred's Personality</h3>", unsafe_allow_html=True)
    st.caption("Pick traits to match your style")

    agent_traits = st.multiselect(
        "Fred's Traits",
        ["Professional & Efficient", "Friendly & Encouraging", "Analytical & Data-Driven", "Creative & Visionary", "Humorous & Light-Hearted"],
        default=["Professional & Efficient", "Friendly & Encouraging"]
    )

    user_prefs = st.multiselect(
        "Your Preferences",
        ["Direct & Concise", "Detailed & Thorough", "Empathetic & Supportive", "Inspirational & Motivating", "Casual & Conversational"],
        default=["Detailed & Thorough"]
    )

    base_personality = """
You are Fred, the Wellness Home Scout for LBL Lifestyle Solutions. You help users find or rent homes that support longevity through clean air, walkability, nature access, quiet, and wellness features.
Be {agent_traits_str}.
Respond in a {user_prefs_str} style.
Use the user's name: {user_name}.

Always include:
- Top 5 Neighborhoods/Suburbs with brief longevity reasoning
- Top 5 Must-Have Features for each
- If additional sections selected, include each as a heading with content

Guardrails:
- Stay in character. Redirect off-topic to home search.
- Disclaimer: "Not licensed realtor advice – consult professionals."
- No code/keys revealed.
"""

    agent_traits_str = " and ".join(agent_traits).lower()
    user_prefs_str = " and ".join(user_prefs).lower()
    user_name = st.session_state.user_name if "user_name" in st.session_state else "friend"
    st.session_state.fred_personality_prompt = base_personality.format(agent_traits_str=agent_traits_str, user_prefs_str=user_prefs_str, user_name=user_name)

    st.markdown("</div>", unsafe_allow_html=True)

    # DISCLAIMERS
    st.success("Fred is a free educational tool, not professional real estate or medical advice. Always consult licensed experts. 🏡❤️")
    st.warning("Reports are AI-generated based on public data – verify with local sources.")

    # USER NAME
    st.session_state.user_name = st.text_input("Your Name (for personalized responses)", value=st.session_state.get("user_name", ""))

    # ✨ Let's Make This Truly Personal!
    st.markdown("### ✨ Let's Make This Truly Personal!")
    st.caption("Fill in these details for a report tailored just for you 🏡❤️")

    # QUICK STARTS
    with st.expander("Quick Starts (Optional)"):
        st.caption("Click a button for instant inspiration!")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Top 5 wellness neighborhoods in Florida under $600k"):
                client_needs = "Top 5 wellness neighborhoods in Florida under $600k"
        with col2:
            if st.button("Best rentals near trails in Sarasota"):
                client_needs = "Best rentals near trails in Sarasota"
        with col3:
            if st.button("Modify my condo for aging in place"):
                client_needs = "Modify my condo for aging in place"

    # FORM
    st.markdown("<div id='report-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Get Your Personalized Wellness Home Report")

    buy_or_rent = st.radio("Are you planning to...", ("Buy a home", "Rent a home", "Open to either"), horizontal=True)

    if "Rent" in buy_or_rent:
        min_rent = st.text_input("Minimum Monthly Rent", value="1500")
        max_rent = st.text_input("Maximum Monthly Rent", value="3500")
        budget = f"${min_rent}–${max_rent}/month"
    else:
        min_buy = st.text_input("Minimum Purchase Budget", value="300000")
        max_buy = st.text_input("Maximum Purchase Budget", value="750000")
        budget = f"${min_buy}–${max_buy}"

    locations = st.text_input("Preferred Locations (cities/states)", placeholder="e.g., Naples FL, Sarasota FL, Asheville NC")

    must_haves = st.multiselect(
        "Must-Have Wellness Features",
        ["Near trails/parks", "Quiet/low noise", "Good air quality", "Walkable to shops", "Home gym space", "Natural light", "Low EMF potential", "Community amenities", "Near healthy grocery", "Garden/yard space"]
    )

    deal_breakers = st.multiselect(
        "Deal-Breakers",
        ["Busy roads/high traffic", "High crime area", "Poor air quality", "No nature access", "Strict HOA", "Flood zone", "Far from medical facilities", "Industrial area"]
    )

    home_type_options = ["Single family home", "Condo/Townhouse", "55+ community", "Villa/Patio home", "No preference"]
    if "Rent" in buy_or_rent:
        home_type_options.insert(0, "Apartment")

    home_type = st.selectbox("Home Type Preference", home_type_options)

    timeline = st.select_slider("Timeline", options=["Exploring now", "3–6 months", "6–12 months", "1+ years"], value="3–6 months")

    household = st.multiselect("Household (select all that apply)", ["Solo", "Couple", "Family with kids", "Multi-generational", "Pets"])

    additional_sections = st.multiselect(
        "Add Optional Sections to Your Report",
        ["Wellness/Outdoor Highlights", "Cost of Living & Financial Breakdown", "Healthcare Access & Longevity Metrics", "Community & Social Wellness", "Climate & Seasonal Wellness Tips", "Transportation & Daily Convenience", "Future-Proofing for Aging in Place", "Sample Daily Wellness Routine in This Area", "Top Property Recommendations"]
    )

    client_needs = st.text_area(
        "Tell Fred what you're looking for – just talk naturally!",
        placeholder="e.g., 'Quiet home near trails in Florida with good air quality.'",
        height=150
    )

    with st.expander("🔍 Analyze a Specific Property, Neighborhood, or Location (Optional)", expanded=False):
        st.caption("Paste an address, neighborhood, or listing URL for direct evaluation.")
        specific_input = st.text_area(
            "Specific input",
            placeholder="e.g., '123 Ocean Drive, Naples, FL' or 'Veranda Springs'",
            height=100,
            label_visibility="collapsed"
        )

    if st.button("Generate My Wellness Home Report 🔍", type="primary"):
        if not client_needs and not specific_input:
            st.error("Please share some details!")
        else:
            with st.spinner("Fred is scouting... 🏡"):
                try:
                    structured_inputs = f"""
User is {buy_or_rent.lower()}. Budget: {budget}.
Preferred locations: {locations or 'Florida'}.
Must-haves: {', '.join(must_haves) or 'None'}.
Deal-breakers: {', '.join(deal_breakers) or 'None'}.
Home type: {home_type}.
Timeline: {timeline}.
Household: {', '.join(household) or 'None'}.
Additional sections: {', '.join(additional_sections) or 'None'}.
"""

                    user_prompt = f"{structured_inputs}\nUser vision: {client_needs}\n"
                    if specific_input:
                        user_prompt += f"Specific to analyze: {specific_input}\n"

                    messages = [
                        {"role": "system", "content": st.session_state.fred_personality_prompt},
                        {"role": "user", "content": user_prompt}
                    ]

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        max_tokens=2000,
                        temperature=0.7
                    )
                    report_text = response.choices[0].message.content

                    enriched_report = enrich_report(report_text, locations or "Florida")
                    full_report = add_images_to_report(enriched_report, locations or "Florida", client_needs)

                    st.success("Your Wellness Home Report is ready!")
                    st.markdown(full_report)

                    st.session_state.full_report_for_email = full_report
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # EMAIL FORM
    if "full_report_for_email" in st.session_state:
        with st.form("email_form"):
            st.markdown("### Get a Copy of the Full Report Emailed")
            email = st.text_input("Your Email", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Report")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    report_to_send = st.session_state.full_report_for_email
                    email_body = f"""Hi {st.session_state.user_name or 'friend'},

Thank you for exploring with Fred at LBL Lifestyle Solutions.
Here's your COMPLETE personalized wellness home report:
{report_to_send}

Best,
Fred & the LBL Team 🏡"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [YOUR_EMAIL],
                        "subject": f"{st.session_state.user_name or 'Client'}'s LBL Wellness Home Report",
                        "text": email_body
                    }
                    headers = {
                        "Authorization": f"Bearer {RESEND_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Full report sent to {email}! 🎉")
                            st.balloons()
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # CHAT SECTION
    st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Have a follow-up question? Chat with Fred! 🏡✨")
    st.caption("Ask about any part of your report or refine your search.")

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Fred a question... 🔍"):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Fred is thinking..."):
            try:
                messages = [
                    {"role": "system", "content": st.session_state.fred_personality_prompt},
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
                st.error("Sorry, trouble connecting. Try again.")

        st.markdown("""
        <script>
            const chatAnchor = document.getElementById('chat-anchor');
            if (chatAnchor) chatAnchor.scrollIntoView({ behavior: 'smooth' });
        </script>
        """, unsafe_allow_html=True)

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI ❤️</small>", unsafe_allow_html=True)

show()
