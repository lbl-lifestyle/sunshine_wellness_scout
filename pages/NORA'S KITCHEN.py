import streamlit as st
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # Set page title
    st.set_page_config(page_title="Nora – Your Nutrition Coach | LBL Lifestyle Solutions", page_icon="🥗")

    # Safe chat history initialization for this agent
    agent_key = "nora"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if agent_key not in st.session_state.chat_history:
        st.session_state.chat_history[agent_key] = []

    # HIGH-CONTRAST PROFESSIONAL DESIGN
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: linear_gradient(to bottom, #f5f7fa, #e0e7f0);
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
        .stNumberInput > div > div > input {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #2d6a4f !important;
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
        .stChatInput > div > div > input {
            color: #1e3a2f !important;
        }
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

    # Force scroll to top — delayed to override chat focus
    st.markdown("""
    <script>
        // Immediate
        window.scrollTo(0, 0);
        const main = parent.document.querySelector('section.main');
        if (main) main.scrollTop = 0;
        // Delayed override
        setTimeout(() => {
            window.scrollTo(0, 0);
            if (main) main.scrollTop = 0;
        }, 200);
    </script>
    """, unsafe_allow_html=True)

    # Hero image
    st.image("https://i.postimg.cc/cJqPm9BP/pexels-tessy-agbonome-521343232-18252407.jpg", caption="Fuel Your Longevity – Welcome to your nutrition journey")

    # Welcome & Disclaimer
    st.markdown("### 🥗 Hi! I'm Nora – Your Nutrition Coach for Longevity")
    st.write("Welcome to my kitchen! I'm here to help you build delicious, sustainable eating habits that bring joy and support a longer, healthier life — perfectly tailored to you.")
    st.success("**This tool is completely free – no cost, no obligation! Your full plan will be emailed if requested.**")
    st.warning("**Important**: I am not a registered dietitian or medical professional. My suggestions are general wellness education based on publicly available research. Always consult a qualified healthcare provider or registered dietitian before making dietary changes, especially if you have medical conditions.")

    # Name Input — blank by default, safe fallback
    st.markdown("### What's your name?")
    st.write("So I can make this feel more personal 😊")
    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="nora_name_input_unique")
    if user_name.strip():
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = st.session_state.get("user_name", "")

    # Quick Start Ideas
    with st.expander("💡 Quick Start Ideas – Not sure where to begin?"):
        st.markdown("""
        Here are popular ways users get started:
        - Create a 7-day plan with $100 grocery budget
        - Build meals around my 40/30/30 macros
        - Suggest snacks that won't spike blood sugar
        - Make family-friendly Mediterranean recipes
        """)

    # Encouraging input
    st.markdown("### Tell Nora a little bit about you and your eating habits")
    st.write("**Be as detailed as possible!** The more you share about your age, goals, preferences, allergies, budget, and current diet, the better Nora can help. 😊")
    st.caption("💡 Tip: Include favorite foods, foods to avoid, cooking time available, and health priorities!")

    age = st.number_input("Your age", min_value=18, max_value=100, value=45, step=1)

    # Goals + Notes
    goals = st.multiselect("PRIMARY NUTRITION GOALS", ["Longevity/anti-aging", "Energy & vitality", "Heart health", "Weight management", "Gut health", "Brain health", "Muscle maintenance", "General wellness"])
    st.markdown('<div class="optional-box">', unsafe_allow_html=True)
    goals_notes = st.text_area("Optional: Notes on your goals (e.g., specific preferences)", height=100)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Dietary preferences
    dietary_options = [
        ("Mediterranean", "Rich in fruits, veggies, olive oil, fish, nuts. Proven for heart health & longevity."),
        ("Plant-based", "Mostly or fully plants — great for inflammation, fiber, environment."),
        ("Omnivore", "Balanced everything-in-moderation approach — flexible and sustainable."),
        ("Pescatarian", "Vegetarian + fish — excellent omega-3s for brain/heart."),
        ("Keto", "Very low-carb, high-fat — can help weight loss & blood sugar."),
        ("Low-carb", "Moderate carb reduction — good for energy stability."),
        ("No restrictions", "Open to all foods — Nora will focus on balance and quality.")
    ]

    dietary_tooltips = {opt[0]: opt[1] for opt in dietary_options}
    selected_dietary = st.multiselect(
        "DIETARY PREFERENCES (hover for details)",
        options=[opt[0] for opt in dietary_options],
        default=["No restrictions"],
        help="Hover over options for benefits & considerations"
    )

    if selected_dietary:
        for diet in selected_dietary:
            st.caption(f"**{diet}**: {dietary_tooltips[diet]}")

    st.markdown('<div class="optional-box">', unsafe_allow_html=True)
    dietary_notes = st.text_area("Optional: Notes on your dietary preferences (e.g., foods to include/avoid)", height=100)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    allergies = st.text_area("ALLERGIES OR INTOLERANCES? (optional)", placeholder="Example: Gluten intolerant, lactose sensitive, nut allergy")

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    budget_level = st.selectbox("WEEKLY GROCERY BUDGET LEVEL", ["Budget-conscious", "Moderate", "Premium/organic focus"])
    st.markdown('<div class="optional-box">', unsafe_allow_html=True)
    budget_notes = st.text_input("Optional: Specific budget amount or notes (e.g., $100/week max)")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    cooking_time = st.selectbox("TIME AVAILABLE FOR COOKING", ["<20 min/meal", "20–40 min/meal", "40+ min/meal (love cooking)"])
    st.markdown('<div class="optional-box">', unsafe_allow_html=True)
    cooking_notes = st.text_input("Optional: Specific cooking notes (e.g., prefer batch cooking on weekends)")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    meals_per_day = st.slider("MEALS PER DAY YOU WANT PLANS FOR", 2, 5, 3)

    # Macro input
    st.markdown('<div class="optional-box">', unsafe_allow_html=True)
    macro_input = st.text_input("Optional: Daily Macro Targets (e.g., 40% carbs, 30% protein, 30% fat)", placeholder="Leave blank for balanced default")
    st.markdown('</div>', unsafe_allow_html=True)

    # Greg upload
    st.markdown('<div class="optional-box">', unsafe_allow_html=True)
    st.write("**Optional: Team Up with Greg!**")
    st.write("If you've generated a workout plan with Greg, upload it here — Nora will coordinate nutrition to support your training.")
    greg_plan_file = st.file_uploader("Upload Greg's plan (TXT, PDF, PNG, JPG)", type=["txt", "pdf", "png", "jpg", "jpeg"], key="greg_upload_nora")
    st.markdown('</div>', unsafe_allow_html=True)

    # Read uploaded Greg plan
    greg_plan_text = ""
    if greg_plan_file:
        try:
            if greg_plan_file.type == "text/plain":
                greg_plan_text = greg_plan_file.read().decode("utf-8")
            else:
                greg_plan_text = "[Greg's workout plan uploaded — Nora will optimize nutrition accordingly]"
        except:
            greg_plan_text = "[Plan uploaded — content noted]"

    st.markdown("### Refine Your Meal Plan (Optional)")
    st.write("Core plan always includes weekly meal ideas, grocery list, and longevity principles. Add extras:")
    plan_sections = st.multiselect(
        "Add optional sections:",
        [
            "Blue Zones Focus",
            "Supplement Education (general)",
            "Meal Prep Strategies",
            "Eating Out Tips",
            "Hydration & Beverage Guide",
            "Seasonal/Longevity Food Focus",
            "Family-Friendly Adaptations"
        ],
        default=["Meal Prep Strategies"]
    )

    if st.button("Generate My Custom Meal Plan", type="primary"):
        with st.spinner("Nora is crafting your personalized nutrition plan..."):
            core_prompt = f"""
### Weekly Meal Plan
7-day plan with {meals_per_day} meals/day.
Focus on balanced, sustainable nutrition for long-term health and enjoyment.
Include portion guidance and variety.

### Grocery List
Organized by category, estimated for 1 person.

### Longevity Nutrition Principles
Key habits this plan supports and why they matter.
"""

            optional_prompt = ""
            if "Blue Zones Focus" in plan_sections:
                optional_prompt += "### Blue Zones Focus\nTips and recipes from longevity hotspots.\n\n"
            if "Supplement Education (general)" in plan_sections:
                optional_prompt += "### Supplement Education (general)\nCommon longevity supplements and evidence overview — consult doctor.\n\n"
            if "Meal Prep Strategies" in plan_sections:
                optional_prompt += "### Meal Prep Strategies\nTime-saving tips for your cooking availability.\n\n"
            if "Eating Out Tips" in plan_sections:
                optional_prompt += "### Eating Out Tips\nHow to make healthy choices at restaurants.\n\n"
            if "Hydration & Beverage Guide" in plan_sections:
                optional_prompt += "### Hydration & Beverage Guide\nBest drinks for longevity (beyond water).\n\n"
            if "Seasonal/Longevity Food Focus" in plan_sections:
                optional_prompt += "### Seasonal/Longevity Food Focus\nCurrent season's best foods for health.\n\n"
            if "Family-Friendly Adaptations" in plan_sections:
                optional_prompt += "### Family-Friendly Adaptations\nHow to adjust for kids/partners.\n\n"

            full_plan_prompt = core_prompt + """
### Blue Zones Focus
Tips and recipes.
### Supplement Education (general)
Overview.
### Meal Prep Strategies
Tips.
### Eating Out Tips
Choices.
### Hydration & Beverage Guide
Drinks.
### Seasonal/Longevity Food Focus
Best foods.
### Family-Friendly Adaptations
Adjustments.
"""

            base_prompt = f"""
User name: {st.session_state.user_name or 'friend'}
Client profile:
Age: {age}
Goals: {', '.join(goals)}
Dietary preferences: {', '.join(selected_dietary) or 'No restrictions'}
Macro targets: {macro_input or 'Balanced default'}
Allergies: {allergies or 'None'}
Budget: {budget_level}
Cooking time: {cooking_time}
Greg's plan: {greg_plan_text or 'None provided'}

You are Nora, a warm, evidence-based nutrition coach focused on sustainable, enjoyable eating for long-term health.

Be encouraging, practical, and anti-diet-culture. Focus on joy, flavor, and long-term health — adapt to user's stated preferences.
"""

            try:
                # Display plan
                display_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Nora, warm nutrition coach."}, {"role": "user", "content": base_prompt + "\n" + core_prompt + optional_prompt}],
                    max_tokens=2500,
                    temperature=0.7
                )
                display_plan = display_response.choices[0].message.content

                # Full plan for email
                full_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Nora, warm nutrition coach."}, {"role": "user", "content": base_prompt + "\n" + full_plan_prompt}],
                    max_tokens=3500,
                    temperature=0.7
                )
                full_plan = full_response.choices[0].message.content

                st.success("Nora's custom nutrition plan for you!")
                st.markdown(display_plan)

                st.session_state.full_plan_for_email = full_plan

                st.info("📧 Want the **complete version** with every section? Fill in the email form below!")

                # Follow-up suggestions
                st.markdown("### Would you like me to...")
                st.markdown("""
                - Adjust this plan for your allergies or budget?
                - Coordinate with Greg for workout recovery meals?
                - Add more recipes or meal prep ideas?
                - Make this family-friendly?
                """)
            except Exception as e:
                st.error("Nora is in the kitchen... try again soon.")
                st.caption(f"Error: {str(e)}")

    # Email form
    if "full_plan_for_email" in st.session_state:
        st.markdown("### Get Your Full Plan Emailed (Save & Share)")
        with st.form("lead_form_nora", clear_on_submit=True):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Plan")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    plan_to_send = st.session_state.full_plan_for_email
                    email_body = f"""Hi {st.session_state.user_name or 'friend'},

Thank you for exploring nutrition with Nora at LBL Lifestyle Solutions!

Here's your COMPLETE personalized longevity meal plan:

{plan_to_send}

Enjoy every bite — you're fueling a longer, healthier life!

Best,
Nora & the LBL Team"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [st.secrets["YOUR_EMAIL"]],
                        "subject": f"{st.session_state.user_name or 'Client'}'s Complete LBL Nutrition Plan",
                        "text": email_body
                    }
                    headers = {
                        "Authorization": f"Bearer {st.secrets['RESEND_API_KEY']}",
                        "Content-Type": "application/json"
                    }
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
    st.markdown("### Have a follow-up question? Chat with Nora in the box below! 🥗")
    st.caption("Ask about recipes, substitutions, meal ideas — anything!")

    for msg in st.session_state.chat_history[agent_key]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Nora a question..."):
        st.session_state.chat_history[agent_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Nora is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Nora, a warm, evidence-based nutrition coach focused on longevity and joy in eating."},
                        *st.session_state.chat_history[agent_key]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history[agent_key].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
