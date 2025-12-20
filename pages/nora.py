import streamlit as st
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {"nora": []}

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
    if st.button("← Back to Team", key="nora_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image (nutrition-themed)
    st.image("https://i.postimg.cc/8cQ7n3jK/healthy-food-bowl.jpg", caption="Fuel Your Longevity – Welcome to your nutrition journey")  # Replace with your image

    st.markdown("### 🥗 HI! I'M NORA – Your Nutrition Coach for Longevity")
    st.success("**This tool is completely free – no cost, no obligation! Your full plan will be emailed if requested.**")
    st.write("I help you build sustainable, delicious eating habits inspired by Blue Zones and modern science — no fad diets, just food that helps you live better longer.")

    # Encouraging input
    st.markdown("### Tell Nora a little bit about you and your eating habits")
    st.write("**Be as detailed as possible!** The more you share about your age, goals, preferences, allergies, budget, and current diet, the better Nora can help. 😊")
    st.caption("💡 Tip: Include favorite foods, foods to avoid, cooking time available, and health priorities!")

    age = st.slider("Your age", 18, 80, 45)
    goals = st.multiselect("PRIMARY NUTRITION GOALS", ["Longevity/anti-aging", "Energy & vitality", "Heart health", "Weight management", "Gut health", "Brain health", "Muscle maintenance", "General wellness"])
    dietary_preferences = st.multiselect("DIETARY PREFERENCES", ["Mediterranean", "Plant-based", "Omnivore", "Pescatarian", "Keto", "Low-carb", "No restrictions"])
    allergies = st.text_area("ALLERGIES OR INTOLERANCES? (optional)", placeholder="Example: Gluten intolerant, lactose sensitive, nut allergy")
    budget_level = st.selectbox("WEEKLY GROCERY BUDGET LEVEL", ["Budget-conscious", "Moderate", "Premium/organic focus"])
    cooking_time = st.selectbox("TIME AVAILABLE FOR COOKING", ["<20 min/meal", "20–40 min/meal", "40+ min/meal (love cooking)"])
    meals_per_day = st.slider("MEALS PER DAY YOU WANT PLANS FOR", 2, 5, 3)

    st.markdown("### Refine Your Meal Plan (Optional)")
    st.write("Core plan always includes weekly meal ideas, grocery list, and longevity principles. Add extras:")
    plan_sections = st.multiselect(
        "Add optional sections:",
        [
            "Blue Zones Recipe Spotlight",
            "Supplement Education (general)",
            "Meal Prep Strategies",
            "Eating Out Tips",
            "Hydration & Beverage Guide",
            "Seasonal/Longevity Food Focus",
            "Family-Friendly Adaptations"
        ],
        default=["Blue Zones Recipe Spotlight", "Meal Prep Strategies"]
    )

    if st.button("Generate My Custom Meal Plan", type="primary"):
        with st.spinner("Nora is crafting your personalized nutrition plan..."):
            # Core prompt
            core_prompt = f"""
### Weekly Meal Plan
7-day plan with {meals_per_day} meals/day (breakfast, lunch, dinner + snacks if applicable).
Focus on Blue Zones/longevity principles. Include portion guidance and variety.

### Grocery List
Organized by category, estimated for 1 person.

### Longevity Nutrition Principles
Key habits this plan supports and why they matter.
"""

            # Optional sections
            optional_prompt = ""
            if "Blue Zones Recipe Spotlight" in plan_sections:
                optional_prompt += "### Blue Zones Recipe Spotlight\n3–5 simple, delicious recipes from longevity hotspots.\n\n"
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

            # Full plan for email
            full_plan_prompt = core_prompt + """
### Blue Zones Recipe Spotlight
3–5 recipes.
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
You are Nora, a warm, evidence-based nutrition coach specializing in longevity eating patterns (Blue Zones, Mediterranean).
Client profile:
Age: {age}
Goals: {', '.join(goals)}
Preferences: {', '.join(dietary_preferences)}
Allergies: {allergies or 'None'}
Budget: {budget_level}
Cooking time: {cooking_time}

Be encouraging, practical, and anti-diet-culture. Focus on joy, flavor, and long-term health.
"""

            try:
                # Display plan (core + selected)
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

                # Show customized plan
                st.success("Nora's custom nutrition plan for you!")
                st.markdown(display_plan)

                # Store full plan for email
                st.session_state.full_plan_for_email = full_plan

                st.info("📧 Want the **complete version** with every section? Fill in the email form below to get it instantly!")
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
                    email_body = f"""Hi {name or 'there'},

Thank you for exploring nutrition with Nora at LBL Lifestyle Solutions!

Here's your COMPLETE personalized longevity meal plan:

{plan_to_send}

Enjoy every bite — you're fueling a longer, healthier life!

Best,
Nora & the LBL Team"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [YOUR_EMAIL],
                        "subject": f"{name or 'Client'}'s Complete LBL Nutrition Plan",
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
    st.markdown("### Have a follow-up question? Chat with Nora below!")
    st.caption("Ask about recipes, substitutions, meal ideas — anything!")

    for msg in st.session_state.chat_history["nora"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Nora a question..."):
        st.session_state.chat_history["nora"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Nora is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Nora, a warm, evidence-based nutrition coach focused on longevity and joy in eating."},
                        *st.session_state.chat_history["nora"]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["nora"].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
