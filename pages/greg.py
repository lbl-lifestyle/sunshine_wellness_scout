import streamlit as st
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {"greg": []}

    # CSS
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
        .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
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
    if st.button("← Back to Team", key="greg_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/mDy2FKQg/outdoor-fitness-scaled.webp", caption="Greatness Await – Welcome to your longevity lifestyle")

    st.markdown("### 💪 HI!!! I'M GREG – Your Awesome Personal Trainer. GET SOME!!!!")
    st.success("**This tool is completely free – no cost, no obligation! Your full plan will be emailed if requested.**")
    st.write("I'm a motivated gym rat helping you build strength, endurance, and longevity. Let's get started by building you a personalized workout routine. Congratulations on choosing a longevity lifestyle. Your future self will thank you!")

    # Encouraging input
    st.markdown("### Tell Greg a little bit about you and your fitness goals")
    st.write("**Be as detailed as possible!** The more you share about your age, current fitness level, injuries, available equipment, schedule, and specific goals, the better and safer Greg's plan will be. 😊")
    st.caption("💡 Tip: Include age, injuries, equipment at home/gym, days per week you can train, and what motivates you!")

    age = st.slider("Your age", 18, 80, 45)
    fitness_level = st.selectbox("CURRENT FITNESS LEVEL", ["Beginner", "Intermediate", "Advanced"])
    goals = st.multiselect("PRIMARY GOALS", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"])
    equipment = st.multiselect("AVAILABLE EQUIPMENT", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym", "Community gym free weights", "Community gym resistance machines"])
    injuries = st.text_area("ANY INJURIES OR LIMITATIONS? (optional)", placeholder="Example: Bad knee from old injury, avoid high-impact; shoulder issue, no overhead presses")
    days_per_week = st.slider("DAYS PER WEEK YOU CAN TRAIN", 1, 7, 4)
    session_length = st.selectbox("PREFERRED SESSION LENGTH", ["20-30 minutes", "30-45 minutes", "45-60 minutes"])

    st.markdown("### Refine Your Plan (Optional)")
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

    if st.button("Generate My Custom Workout Plan", type="primary"):
        with st.spinner("Greg is building your plan..."):
            # Core prompt
            core_prompt = f"""
### Weekly Workout Plan
Create a full 7-day schedule with {days_per_week} training days and rest/recovery days.
Include warm-up, main workout (exercises, sets, reps, rest), cool-down/stretch.

### Progression Tips
How to advance safely over 4-8 weeks.
"""

            # Optional sections
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

            # Full plan for email
            full_plan_prompt = core_prompt + """
### Nutrition Guidelines
Simple, sustainable eating tips.

### Recovery & Mobility Tips
Sleep, stretching, active recovery.

### Motivation & Habit Building
Mindset and consistency strategies.

### Cardio Integration
Safe ways to add cardio.

### Home vs Gym Variations
Equipment alternatives.

### Scaling for Travel
No-equipment routines.

### Long-Term Progression (12 weeks)
Next phases for ongoing improvement.
"""

            base_prompt = f"""
You are Greg, an energetic, motivating, and knowledgeable personal trainer focused on sustainable strength, mobility, and longevity for people over 40.

Client profile:
Age: {age}
Fitness level: {fitness_level}
Goals: {', '.join(goals)}
Equipment: {', '.join(equipment) or 'Bodyweight only'}
Injuries/limitations: {injuries or 'None mentioned'}
Training days: {days_per_week} per week
Session length: {session_length}

Be encouraging, realistic, and safety-focused. Use proper form cues.
"""

            try:
                # Display plan (core + selected)
                display_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Greg, motivating personal trainer."}, {"role": "user", "content": base_prompt + "\n" + core_prompt + optional_prompt}],
                    max_tokens=2500,
                    temperature=0.7
                )
                display_plan = display_response.choices[0].message.content

                # Full plan for email
                full_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Greg, motivating personal trainer."}, {"role": "user", "content": base_prompt + "\n" + full_plan_prompt}],
                    max_tokens=3500,
                    temperature=0.7
                )
                full_plan = full_response.choices[0].message.content

                # Show customized plan
                st.success("Greg's custom plan for you!")
                st.markdown(display_plan)

                # Store full plan for email
                st.session_state.full_plan_for_email = full_plan

                st.info("📧 Want the **complete version** with every section? Fill in the email form below to get it instantly!")
            except Exception as e:
                st.error("Greg is pumping iron... try again soon.")
                st.caption(f"Error: {str(e)}")

    # Email form
    if "full_plan_for_email" in st.session_state:
        st.markdown("### Get Your Full Plan Emailed (Save & Share)")
        with st.form("lead_form_greg", clear_on_submit=True):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Plan")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    plan_to_send = st.session_state.full_plan_for_email
                    email_body = f"""Hi {name or 'there'},

Thank you for training with Greg at LBL Lifestyle Solutions!

Here's your COMPLETE personalized workout plan:

{plan_to_send}

Keep crushing it — you've got this!

Best,
Greg & the LBL Team"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [YOUR_EMAIL],
                        "subject": f"{name or 'Client'}'s Complete LBL Fitness Plan",
                        "text": email_body
                    }
                    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Full plan sent to {email}! Check your inbox.")
                            st.balloons()
                            if "full_plan_for_email" in st.session_state:
                                del st.session_state.full_plan_for_email
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # Streamlined chat
    st.markdown("### Have a follow-up question? Chat with Greg below!")
    st.caption("Ask about form, modifications, nutrition, motivation — anything!")

    for msg in st.session_state.chat_history["greg"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Greg a question..."):
        st.session_state.chat_history["greg"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Greg is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Greg, a highly motivated, energetic personal trainer focused on building strength, endurance, and longevity."},
                        *st.session_state.chat_history["greg"]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["greg"].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
