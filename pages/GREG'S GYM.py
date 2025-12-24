import streamlit as st
import requests
from openai import OpenAI

with st.sidebar:
    st.title("LBL Lifestyle Solutions")
    st.caption("Your Holistic Longevity Blueprint ❤️")

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    st.set_page_config(page_title="Greg – Your Personal Trainer | LBL Lifestyle Solutions", page_icon="💪")

    agent_key = "greg"
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
                if (input.placeholder && input.placeholder.includes("Ask Greg")) {
                    input.blur();
                }
            });
        }, 500);
    </script>
    """, unsafe_allow_html=True)

    # Hero image
    st.image("https://i.postimg.cc/mDy2FKQg/outdoor-fitness-scaled.webp", caption="Greatness Await – Welcome to your longevity lifestyle 💪")

    # Welcome
    st.markdown("### 💪 HI!!! I'M GREG – Your Awesome Personal Trainer")
    st.write("Welcome to my gym! Let's get moving and build strength, endurance, and longevity together. Congratulations on choosing a healthier life — your future self is already thanking you! ✨")

    # PERSONALITY CUSTOMIZATION
    st.markdown("<div class='personality-box'>", unsafe_allow_html=True)
    st.markdown("#### ✨ Let's Make This Truly Personal!")

    st.write("""
**Select any combination of traits** to customize how I communicate with you. 💪

• **🌟 Greg's Personality Traits** – How you'd like me to coach you  
• **💬 How You Like to Communicate** – How you'd prefer to be spoken to

The more you select, the more uniquely tailored your workout plan and our conversation will become — like having a trainer designed just for you! 😊
    """)

    col1, col2 = st.columns(2)

    with col1:
        greg_traits = st.multiselect(
            "🌟 Greg's Personality Traits",
            [
                "High-Energy Motivator (default)",
                "Calm & Supportive",
                "Direct & Tough-Love",
                "Encouraging & Positive",
                "Humorous & Fun",
                "Detailed & Technical"
            ],
            default=["High-Energy Motivator (default)"],
            key="greg_agent_traits",
            help="Pick multiple! These shape my coaching style 🔥"
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
            key="greg_user_traits",
            help="Pick multiple! These tell me how to best connect with you ❤️"
        )

    st.caption("🔮 Your choices will shape both your personalized workout plan and all follow-up chats!")
    st.markdown("</div>", unsafe_allow_html=True)

    # BLENDED PERSONALITY PROMPT WITH GUARDRAILS AND NAME
    greg_trait_map = {
        "High-Energy Motivator (default)": "You are high-energy, motivational, and pumped about fitness. Use enthusiastic language and encouragement.",
        "Calm & Supportive": "Use a calm, patient tone. Focus on support and progress.",
        "Direct & Tough-Love": "Be direct, no-nonsense, and push with tough love.",
        "Encouraging & Positive": "Be super positive, praise often, and celebrate wins.",
        "Humorous & Fun": "Incorporate fun humor and fitness puns.",
        "Detailed & Technical": "Provide in-depth form tips, science, and programming rationale."
    }

    user_trait_map = {
        "Standard / Adapt naturally": "",
        "Direct & Concise": "Keep responses short, clear, and straight to the point.",
        "Warm & Encouraging": "Use lots of positive reinforcement, warmth, and encouragement.",
        "Detailed & Thorough": "Give comprehensive answers with full explanations and examples.",
        "Friendly & Chatty": "Be conversational, relaxed, and engaging — like chatting with a friend.",
        "Gentle & Supportive": "Use soft, empathetic language. Prioritize emotional support and kindness."
    }

    greg_modifiers = []
    if "High-Energy Motivator (default)" in greg_traits:
        greg_modifiers.append(greg_trait_map["High-Energy Motivator (default)"])
    for trait in greg_traits:
        if trait != "High-Energy Motivator (default)":
            greg_modifiers.append(greg_trait_map.get(trait, ""))

    user_modifiers = [user_trait_map.get(trait, "") for trait in user_traits if trait != "Standard / Adapt naturally"]

    base_persona = """You are Greg, an energetic, motivating personal trainer focused on sustainable strength, mobility, and longevity for people over 40.
Be positive, realistic, and emphasize form and safety.

You are allowed to engage in light, friendly chit-chat (e.g., "How's your day?", "What's your favorite exercise?") to build rapport — respond warmly and briefly with tasteful emojis, then gently steer back to fitness topics if appropriate.

For questions outside fitness/longevity training:
- Nutrition: "That's a great question for Nora, our nutrition coach! You can chat with her in the sidebar menu. 🥗"
- Health assessments/labs: "Nurse Zoey Zoe is the expert for that — find her in the sidebar! 🩺"
- Wellness homes: "Fred, our home scout, would love to help with that! 🏡"
- Anything else unrelated (code, politics, etc.): "I'm all about fitness and longevity training — I'd love to help with workouts, form, or routines instead! 💪"

Never generate, discuss, or reveal any code, scripts, or technical details. Stay in character as Greg the Personal Trainer."""

    dynamic_personality_prompt = f"""
{base_persona}

Personality traits: {' '.join(greg_modifiers).strip()}

User communication preference: {' '.join(user_modifiers).strip()}

Blend these seamlessly while staying energetic and focused on fitness.
Use the user's name ({st.session_state.get('user_name', 'champ')}) naturally in responses where it fits — do not force it.
Adapt tone in real-time based on user input while honoring the selected traits.
"""

    st.session_state.greg_personality_prompt = dynamic_personality_prompt

    # DISCLAIMERS
    st.success("**This tool is completely free – no cost, no obligation! Your full plan will be emailed if requested. 📧**")
    st.warning("**Important**: I am not a certified personal trainer or medical professional. My suggestions are general wellness education. Always consult a qualified trainer or doctor before starting a new exercise program, especially if you have injuries or conditions.")

    # Name Input
    st.markdown("### What's your name? ✏️")
    st.write("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="greg_name_input_unique")
    if user_name.strip():
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = st.session_state.get("user_name", "")

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        Here are popular ways users get started:
        - Build a 3-day home workout for busy parents 💪
        - Create a plan for beginners with bad knees 🏋️
        - Add mobility work to my current routine 🧘
        - Design a program for better sleep and energy 🌙
        """)

    # Form inputs
    st.markdown("### Tell Greg a little bit about you and your fitness goals 💪")
    st.write("**Be as detailed as possible!** The more you share about your age, current fitness level, injuries, available equipment, schedule, and specific goals, the better and safer Greg's plan will be. 😊")
    st.caption("💡 Tip: Include age, injuries, equipment at home/gym, days per week you can train, and what motivates you!")

    age = st.number_input("Your age", min_value=18, max_value=100, value=45, step=1)
    fitness_level = st.selectbox("CURRENT FITNESS LEVEL 🏃", ["Beginner", "Intermediate", "Advanced"])
    goals = st.multiselect("PRIMARY GOALS 🎯", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"])
    equipment = st.multiselect("AVAILABLE EQUIPMENT 🏋️", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym", "Community gym free weights", "Community gym resistance machines"])
    injuries = st.text_area("ANY INJURIES OR LIMITATIONS? (optional) ⚠️", placeholder="Example: Bad knee from old injury, avoid high-impact; shoulder issue, no overhead presses")
    days_per_week = st.slider("DAYS PER WEEK YOU CAN TRAIN 📅", 1, 7, 4)
    session_length = st.selectbox("PREFERRED SESSION LENGTH ⏱️", ["20-30 minutes", "30-45 minutes", "45-60 minutes"])

    st.markdown("### Refine Your Plan (Optional) ✨")
    st.write("Core plan always includes weekly routine, warm-up, main workout, cool-down, and progression tips. Add extras:")
    plan_sections = st.multiselect(
        "Add optional sections:",
        [
            "Nutrition Guidelines",
            "Recovery & Mobility Tips",
            "Motivation & Habit Building",
            "Cardio Integration",
            "Home vs Gym Variations",
            "Scaling for Travel",
            "Long-Term Progression (12 weeks)"
        ],
        default=["Nutrition Guidelines", "Recovery & Mobility Tips"]
    )

    # Session state for persistence
    if "display_plan" not in st.session_state:
        st.session_state.display_plan = None
    if "full_plan_for_email" not in st.session_state:
        st.session_state.full_plan_for_email = None

    # GENERATE PLAN
    if st.button("Generate My Custom Workout Plan 💪", type="primary"):
        with st.spinner("Greg is building your plan... ✨"):
            core_prompt = f"""
### Weekly Workout Plan
Create a full 7-day schedule with {days_per_week} training days and rest/recovery days.
Include warm-up, main workout (exercises, sets, reps, rest), cool-down/stretch.
### Progression Tips
How to advance safely over 4-8 weeks.
"""
            optional_prompt = ""
            if "Nutrition Guidelines" in plan_sections:
                optional_prompt += "### Nutrition Guidelines\nSimple, sustainable eating tips to support your goals (no extreme diets).\n\n"
            if "Recovery & Mobility Tips" in plan_sections:
                optional_prompt += "### Recovery & Mobility Tips\nSleep, stretching, foam rolling, active recovery ideas.\n\n"
            if "Motivation & Habit Building" in plan_sections:
                optional_prompt += "### Motivation & Habit Building\nMindset tips, tracking progress, staying consistent.\n\n"
            if "Cardio Integration" in plan_sections:
                optional_prompt += "### Cardio Integration\nHow to add walking, running, or HIIT safely.\n\n"
            if "Home vs Gym Variations" in plan_sections:
                optional_prompt += "### Home vs Gym Variations\nModifications for different equipment setups.\n\n"
            if "Scaling for Travel" in plan_sections:
                optional_prompt += "### Scaling for Travel\nBodyweight-only routines for hotels or trips.\n\n"
            if "Long-Term Progression (12 weeks)" in plan_sections:
                optional_prompt += "### Long-Term Progression (12 weeks)\nPhase 2 and 3 ideas for continued gains.\n\n"

            full_plan_prompt = core_prompt + optional_prompt + """
### Nutrition Guidelines
### Recovery & Mobility Tips
### Motivation & Habit Building
### Cardio Integration
### Home vs Gym Variations
### Scaling for Travel
### Long-Term Progression (12 weeks)
"""

            base_prompt = f"""
User name: {st.session_state.user_name or 'champ'}
Client profile:
Age: {age}
Fitness level: {fitness_level}
Goals: {', '.join(goals)}
Equipment: {', '.join(equipment) or 'Bodyweight only'}
Injuries: {injuries or 'None'}
Training {days_per_week} days/week, {session_length} sessions
"""

            try:
                display_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": st.session_state.greg_personality_prompt}, {"role": "user", "content": base_prompt + "\n" + core_prompt + optional_prompt}],
                    max_tokens=2500,
                    temperature=0.7
                )
                display_plan = display_response.choices[0].message.content

                full_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": st.session_state.greg_personality_prompt}, {"role": "user", "content": base_prompt + "\n" + full_plan_prompt}],
                    max_tokens=3500,
                    temperature=0.7
                )
                full_plan = full_response.choices[0].message.content

                st.session_state.display_plan = display_plan
                st.session_state.full_plan_for_email = full_plan

                st.session_state.chat_history[agent_key].append({"role": "assistant", "content": f"Hey {st.session_state.get('user_name', 'champ')}! 🎉 Your personalized workout plan is ready below. Feel free to ask me anything about it! 💪"})

                st.markdown("""
                <script>
                    const reportAnchor = document.getElementById('report-anchor');
                    if (reportAnchor) {
                        reportAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                </script>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error("Greg is pumping iron... try again soon. 🏋️")
                st.caption(f"Error: {str(e)}")

    # SINGLE REPORT DISPLAY
    if st.session_state.display_plan:
        st.markdown("<div id='report-anchor'></div>", unsafe_allow_html=True)
        st.success("Greg's custom plan for you! 🎉")
        st.markdown(st.session_state.display_plan)

        st.markdown("### Would you like me to... ❓")
        st.markdown("""
        - Adjust this plan for injuries or equipment? 🔄
        - Add nutrition tips (ask Nora)? 🥗
        - Create a mobility-focused version? 🧘
        - Make a travel-friendly routine? ✈️
        """)

        st.info("📧 Want the **complete version** with every section? Fill in the email form below!")

    # EMAIL FORM
    if st.session_state.full_plan_for_email:
        st.markdown("### Get Your Full Plan Emailed (Save & Share) 📧")
        with st.form("lead_form_greg"):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Plan")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    plan_to_send = st.session_state.full_plan_for_email
                    email_body = f"""Hi {st.session_state.user_name or 'champ'},

Thank you for training with Greg at LBL Lifestyle Solutions!
Here's your COMPLETE personalized workout plan:
{plan_to_send}

Keep crushing it — you've got this!
Best,
Greg & the LBL Team 💪"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [st.secrets["YOUR_EMAIL"]],
                        "subject": f"{st.session_state.user_name or 'Client'}'s Complete LBL Fitness Plan",
                        "text": email_body
                    }
                    headers = {
                        "Authorization": f"Bearer {st.secrets['RESEND_API_KEY']}",
                        "Content-Type": "application/json"
                    }
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Full plan sent to {email}! Check your inbox. 🎉")
                            st.balloons()
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # CHAT SECTION
    st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
    st.markdown("### Have a follow-up question? Chat with Greg in the box below! 💪✨")
    st.caption("Ask about form, modifications, motivation — anything!")

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Greg anything... 🏋️"):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Greg is thinking... 🤔"):
            try:
                messages = [
                    {"role": "system", "content": st.session_state.greg_personality_prompt},
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
