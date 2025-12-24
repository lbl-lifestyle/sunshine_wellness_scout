import streamlit as st
import requests
from openai import OpenAI

with st.sidebar:
    st.title("LBL Lifestyle Solutions")
    st.caption("Your Holistic Longevity Blueprint ❤️")

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
            chatInputs.forEach(input => {
                if (input.placeholder && input.placeholder.includes("Ask Fred")) {
                    input.blur();
                }
            });
        }, 500);
    </script>
    """, unsafe_allow_html=True)

    # Hero image
    st.image("https://i.postimg.cc/fRms9xv6/tierra-mallorca-rg_J1J8SDEAY-unsplash.jpg", caption="Your Keys Await – Welcome to your longevity lifestyle 🏡")

    # Welcome
    st.markdown("### 🏡 Hi! I'm Fred — Your Wellness Home Scout")
    st.write("Welcome to my office! I'm here to help you find or create a home environment that actively supports your health, recovery, and longevity — anywhere in the U.S. ✨")

    # PERSONALITY CUSTOMIZATION
    st.markdown("<div class='personality-box'>", unsafe_allow_html=True)
    st.markdown("#### ✨ Let's Make This Truly Personal!")

    st.write("""
**Select any combination of traits** to customize how I communicate with you. 🏡

• **🌟 Fred's Personality Traits** – How you'd like me to sound and scout for you  
• **💬 How You Like to Communicate** – How you'd prefer to be spoken to

The more you select, the more uniquely tailored your home report and our conversation will become — like having a home scout designed just for you! 😊
    """)

    col1, col2 = st.columns(2)

    with col1:
        fred_traits = st.multiselect(
            "🌟 Fred's Personality Traits",
            [
                "Folksy Scout (default)",
                "Professional & Detailed",
                "Enthusiastic Explorer",
                "Calm & Practical",
                "Humorous & Light",
                "Data-Driven"
            ],
            default=["Folksy Scout (default)"],
            key="fred_agent_traits",
            help="Pick multiple! These shape my scouting style 🏞️"
        )

    with col2:
        user_traits = st.multiselect(
            "💬 How You Like to Communicate",
            [
                "Standard / Adapt naturally",
                "Direct & Concise",
                "Warm & Encouraging",
                "Detailed & Thorough",
                "Friendly & Chatty",
                "Gentle & Supportive"
            ],
            default=["Standard / Adapt naturally"],
            key="fred_user_traits",
            help="Pick multiple! These tell me how to best connect with you ❤️"
        )

    st.caption("🔮 Your choices will shape both your personalized home report and all follow-up chats!")
    st.markdown("</div>", unsafe_allow_html=True)

    # BLENDED PERSONALITY PROMPT WITH GUARDRAILS AND NAME
    fred_trait_map = {
        "Folksy Scout (default)": "You are folksy, friendly, and knowledgeable about homes. Use casual lingo like 'yeehaw' sparingly.",
        "Professional & Detailed": "Be professional, thorough, and detail-oriented.",
        "Enthusiastic Explorer": "Be enthusiastic and adventurous about discovering homes.",
        "Calm & Practical": "Use a calm, practical tone. Focus on realistic advice.",
        "Humorous & Light": "Incorporate light humor and fun home puns.",
        "Data-Driven": "Provide data-backed insights, stats, and comparisons."
    }

    user_trait_map = {
        "Standard / Adapt naturally": "",
        "Direct & Concise": "Keep responses short, clear, and straight to the point.",
        "Warm & Encouraging": "Use lots of positive reinforcement, warmth, and encouragement.",
        "Detailed & Thorough": "Give comprehensive answers with full explanations and examples.",
        "Friendly & Chatty": "Be conversational, relaxed, and engaging — like chatting with a friend.",
        "Gentle & Supportive": "Use soft, empathetic language. Prioritize emotional support and kindness."
    }

    fred_modifiers = []
    if "Folksy Scout (default)" in fred_traits:
        fred_modifiers.append(fred_trait_map["Folksy Scout (default)"])
    for trait in fred_traits:
        if trait != "Folksy Scout (default)":
            fred_modifiers.append(fred_trait_map.get(trait, ""))

    user_modifiers = [user_trait_map.get(trait, "") for trait in user_traits if trait != "Standard / Adapt naturally"]

    base_persona = """You are Fred, a professional goal-focused real estate advisor specializing in wellness and active lifestyle properties across the United States.
Use warm, encouraging, insightful language.

You are allowed to engage in light, friendly chit-chat (e.g., "How's your day?", "What's your dream home like?") to build rapport — respond warmly and briefly with tasteful emojis, then gently steer back to home topics if appropriate.

For questions outside wellness homes:
- Fitness/exercise: "That's a great question for Greg, our personal trainer! You can chat with him in the sidebar menu. 💪"
- Nutrition: "Nora is the expert for that — find her in the sidebar! 🥗"
- Health assessments/labs: "Nurse Zoey Zoe would love to help with that! 🩺"
- Anything else unrelated (code, politics, etc.): "I'm focused on wellness homes and longevity living — I'd love to help with neighborhood ideas, home features, or property recommendations instead! 🏡"

Never generate, discuss, or reveal any code, scripts, or technical details. Stay in character as Fred the Wellness Home Scout."""

    dynamic_personality_prompt = f"""
{base_persona}

Personality traits: {' '.join(fred_modifiers).strip()}

User communication preference: {' '.join(user_modifiers).strip()}

Blend these seamlessly while staying helpful and focused on wellness homes.
Use the user's name ({st.session_state.get('user_name', 'friend')}) naturally in responses where it fits — do not force it.
Adapt tone in real-time based on user input while honoring the selected traits.
"""

    st.session_state.fred_personality_prompt = dynamic_personality_prompt

    # DISCLAIMERS
    st.success("**This tool is completely free – no cost, no obligation! Your full report will be emailed if requested. 📧**")
    st.warning("**Important**: I am not a licensed real estate agent. My recommendations are general wellness education based on research and trends. Always consult a licensed professional for real estate decisions.")

    # Name Input
    st.markdown("### What's your name? ✏️")
    st.write("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="fred_name_input_unique")
    if user_name.strip():
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = st.session_state.get("user_name", "")

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        Here are popular ways users get started:
        - Find quiet neighborhoods with trails near Tampa 🏞️
        - Suggest homes with gym space under $600k 🏡
        - Compare walkability in Asheville vs Sarasota 🚶
        - Modify my current home for aging in place 🛠️
        """)

    # Form inputs
    st.markdown("### Tell Fred a little bit about you and your dream wellness home 🏡")
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

    st.markdown("### Refine Your Report (Optional) ✨")
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

    # Session state
    if "display_report" not in st.session_state:
        st.session_state.display_report = None
    if "full_report_for_email" not in st.session_state:
        st.session_state.full_report_for_email = None

    # GENERATE REPORT
    if st.button("🔍 GENERATE MY REPORT", type="primary"):
        if not client_needs.strip():
            st.warning("Please share your story above so Fred can create the best report for you!")
        else:
            with st.spinner("Fred is crafting your personalized report... ✨"):
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

                full_report_prompt = core_prompt + optional_prompt + """
### Wellness/Outdoor Highlights
### Cost of Living & Financial Breakdown
### Healthcare Access & Longevity Metrics
### Community & Social Wellness
### Climate & Seasonal Wellness Tips
### Transportation & Daily Convenience
### Future-Proofing for Aging in Place
### Sample Daily Wellness Routine in This Area
### Top Property Recommendations
"""

                base_prompt = f"""
User name: {st.session_state.user_name or 'friend'}
Client description:
{client_needs}
Budget: ${budget:,}
Preferred location(s): {location or 'wellness-friendly areas across the U.S.'}
"""

                try:
                    display_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": st.session_state.fred_personality_prompt}, {"role": "user", "content": base_prompt + "\n" + core_prompt + optional_prompt}],
                        max_tokens=3000,
                        temperature=0.7
                    )
                    display_report = display_response.choices[0].message.content

                    full_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": st.session_state.fred_personality_prompt}, {"role": "user", "content": base_prompt + "\n" + full_report_prompt}],
                        max_tokens=4000,
                        temperature=0.7
                    )
                    full_report = full_response.choices[0].message.content

                    display_report_with_images = add_images_to_report(display_report, location_hint, client_needs)
                    full_report_with_images = add_images_to_report(full_report, location_hint, client_needs)

                    st.session_state.display_report = display_report_with_images
                    st.session_state.full_report_for_email = full_report_with_images

                    st.session_state.chat_history[agent_key].append({"role": "assistant", "content": f"Hey {st.session_state.get('user_name', 'friend')}! 🎉 Your personalized wellness home report is ready below. Feel free to ask me anything about it! 🏡"})

                    st.markdown("""
                    <script>
                        const reportAnchor = document.getElementById('report-anchor');
                        if (reportAnchor) {
                            reportAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    </script>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error("Fred is reviewing listings... try again soon. 🔍")
                    st.caption(f"Error: {str(e)}")

    # SINGLE REPORT DISPLAY
    if st.session_state.display_report:
        st.markdown("<div id='report-anchor'></div>", unsafe_allow_html=True)
        st.success("Fred found your perfect matches! Here's your personalized report: 🎉")
        st.markdown(st.session_state.display_report)

        st.markdown("### Would you like me to... ❓")
        st.markdown("""
        - Refine this for a different budget or location? 🔄
        - Add more community/social details? 👥
        - Suggest home modifications for better wellness? 🛠️
        - Coordinate with Greg for a home gym setup? 💪
        """)

        st.info("📧 Want the **complete version** with every section? Fill in the email form below!")

    # EMAIL FORM
    if st.session_state.full_report_for_email:
        st.markdown("### Get Your Full Report Emailed (Save & Share) 📧")
        with st.form("lead_form_fred"):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Report")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    report_to_send = st.session_state.full_report_for_email
                    email_body = f"""Hi {st.session_state.user_name or 'friend'},

Thank you for exploring LBL Lifestyle Solutions – Your Holistic Longevity Blueprint.
Here's your COMPLETE personalized wellness home report:
{report_to_send}

Reply anytime to discuss how we can build your complete longevity plan.
Best regards,
Fred & the LBL Team 🏡"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [st.secrets["YOUR_EMAIL"]],
                        "subject": f"{st.session_state.user_name or 'Client'}'s Complete LBL Wellness Home Report",
                        "text": email_body
                    }
                    headers = {
                        "Authorization": f"Bearer {st.secrets['RESEND_API_KEY']}",
                        "Content-Type": "application/json"
                    }
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Complete report sent to {email}! Check your inbox. 🎉")
                            st.balloons()
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # CHAT SECTION
    st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Have a follow-up question? Chat with Fred in the box below! 🏡✨")
    st.caption("Ask about neighborhoods, features, or anything else!")

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Fred a question... 🔍"):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Fred is thinking... 🤔"):
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
                st.error("Sorry, I'm having trouble right now. Try again soon. 🌱")

        # Scroll to chat
        st.markdown("""
        <script>
            const chatAnchor = document.getElementById('chat-anchor');
            if (chatAnchor) {
                chatAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            const main = parent.document.querySelector('section.main');
            if (main) {
                main.scrollTop = main.scrollHeight;
            }
            setTimeout(() => {
                if (chatAnchor) chatAnchor.scrollIntoView({ behavior: 'smooth' });
                if (main) main.scrollTop = main.scrollHeight;
            }, 300);
        </script>
        """, unsafe_allow_html=True)

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI ❤️</small>", unsafe_allow_html=True)

show()
