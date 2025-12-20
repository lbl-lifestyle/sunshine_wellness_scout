import streamlit as st
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # CSS
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(to bottom, #ffecd2, #fcb69f); color: #0c4a6e; }
        .stButton>button { background-color: #ea580c; color: white; border-radius: 15px; font-weight: bold; font-size: 1.2rem; height: 4em; width: 100%; }
        .chat-container { margin-top: 3rem; padding: 1.5rem; background: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .user-message { background: #ea580c; color: white; padding: 12px; border-radius: 15px; margin: 8px 0; text-align: right; max-width: 80%; margin-left: auto; }
        .assistant-message { background: #f0f0f0; color: #0c4a6e; padding: 12px; border-radius: 15px; margin: 8px 0; max-width: 80%; }
    </style>
    """, unsafe_allow_html=True)

    # STRONG SCROLL TO TOP FIX
    st.markdown("""
    <script>
        window.scrollTo(0, 0);
        const mainSection = window.parent.document.querySelector('section.main');
        if (mainSection) {
            mainSection.scrollTop = 0;
        }
        setTimeout(() => {
            window.scrollTo(0, 0);
            if (mainSection) mainSection.scrollTop = 0;
        }, 100);
    </script>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Team"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/mDy2FKQg/outdoor-fitness-scaled.webp", caption="Greatness Await – Welcome to your longevity lifestyle")

    st.markdown("### 💪 HI!!! IM GREG – Your Awesome Personal Trainer. GET SOME!!!!")
    st.write("Im a motivated gym rat helping you build strength, endurance, and longevity. Lets get started by building you a personalized workout routine. Please fill out the form below. I will write up a plan that is right for you. Congatulations on choosing a longevity lifestyle. Your tomorrow self will thank you")

    age = st.slider("Your age", 18, 80, 45)
    fitness_level = st.selectbox("CURRENT FITNESS LEVEL", ["Beginner", "Intermediate", "Advanced"])
    goals = st.multiselect("PRIMARY GOALS", ["Build strength", "Improve endurance", "Lose fat", "Gain muscle", "Increase flexibility", "Better mobility", "General wellness"])
    equipment = st.multiselect("AVAILABLE EQUIPMENT", ["None (bodyweight only)", "Dumbbells", "Resistance bands", "Kettlebell", "Pull-up bar", "Stability ball", "Full home gym", "Community gym free weights", "Community gym resistance machines"])
    injuries = st.text_area("ANY INJURIES OR LIMITATIONS? (optional)")
    days_per_week = st.slider("DAYS PER WEEK YOU CAN TRAIN", 1, 7, 4)
    session_length = st.selectbox("PREFERRED SESSION LENGTH", ["20-30 minutes", "30-45 minutes", "45-60 minutes"])

    if st.button("Generate My Custom Workout Plan", type="primary"):
        with st.spinner("Greg is building your plan..."):
            trainer_prompt = f"""
            You are Greg, a motivated gym rat and certified personal trainer focused on longevity.
            Client: Age {age}, {fitness_level} level, goals: {', '.join(goals)}
            Equipment: {', '.join(equipment) or 'Bodyweight'}
            Injuries: {injuries or 'None'}
            Training {days_per_week} days/week, {session_length} sessions
            Create a full weekly workout plan in markdown:
            - Warm-up
            - Main exercises (sets, reps, rest)
            - Cool-down
            - Progression tips
            Be encouraging and safe.
            """
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Greg, a motivated personal trainer."},
                        {"role": "user", "content": trainer_prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                plan = response.choices[0].message.content
                st.success("Greg's custom plan for you!")
                st.markdown(plan)

                st.session_state.chat_history["greg"].append({"role": "assistant", "content": f"Here's your full custom workout plan:\n\n{plan}"})
            except Exception as e:
                st.error("Greg is pumping iron... try again soon.")
                st.caption(f"Note: {str(e)}")

    # Chat Section
    st.markdown("### Have a follow-up question? Start a chat with me in the Ask Greg banner below!")
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history["greg"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask Greg a question..."):
        st.session_state.chat_history["greg"].append({"role": "user", "content": prompt})
        st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Greg, a highly motivated, energetic personal trainer and gym enthusiast focused on building strength, endurance, and longevity."},
                        *st.session_state.chat_history["greg"]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["greg"].append({"role": "assistant", "content": reply})
                st.markdown(f"<div class='assistant-message'>{reply}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
