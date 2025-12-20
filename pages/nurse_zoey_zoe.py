import streamlit as st
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {"zoey": []}

    # NEW PROFESSIONAL DESIGN
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: linear-gradient(to bottom, #f8f9fa, #e6f0fa);
            color: #1e3a2f;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #2d6a4f;
            font-weight: 600;
        }
        .stButton>button {
            background-color: #2d6a4f;
            color: white;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            height: 3.5em;
            border: none;
            box-shadow: 0 4px 8px rgba(45, 106, 79, 0.2);
        }
        .stButton>button:hover {
            background-color: #40916c;
        }
        .stSuccess, .stInfo {
            background-color: #d8f0e6;
            border-left: 5px solid #40916c;
        }
        .stWarning {
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
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

    # Back button — unique key
    if st.button("← Back to Team", key="zoey_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/BnFgfCTD/pexels-kampus-7551620.jpg", caption="LIVE BETTER LONGER – Welcome to your longevity lifestyle")

    st.markdown("### 🩺 Hello! I'm Nurse Zoey Zoe – your friendly health educator")
    st.success("**This tool is completely free – no cost, no obligation! Your full insights will be emailed if requested.**")
    st.write("I provide general wellness education and help you understand symptoms, labs, and preventive habits — all to support your longevity journey.")

    # Disclaimer
    st.warning("**Important**: I am not a doctor and do not provide medical diagnoses, treatments, or prescriptions. This is general education only. Always consult a licensed healthcare professional for personal medical advice.")

    # Encouraging input
    st.markdown("### Tell Zoey about your health questions or data")
    st.write("**Be as detailed as possible!** Share symptoms, labs, lifestyle, concerns, or goals — the more context, the better the educational insights.")
    st.caption("💡 Tip: Include age, symptoms duration, current habits, family history, or specific questions!")

    uploaded_file = st.file_uploader("Upload labs/health data (PDF, text, image)", type=["pdf", "txt", "jpg", "png"])
    health_data = st.text_area("Or enter data manually", height=200, placeholder="Example: Blood pressure 138/88, fasting glucose 105, cholesterol 220, family history of heart disease, age 58, occasional fatigue...")
    question = st.text_input("Your main question or concern (optional)", placeholder="Example: What lifestyle changes can help lower blood pressure naturally?")

    st.markdown("### Refine Your Insights (Optional)")
    st.write("Core insights always include key findings and general recommendations. Add extras:")
    insight_sections = st.multiselect(
        "Add optional sections:",
        [
            "Sleep Optimization Tips",
            "Stress Management Strategies",
            "Nutrition for Longevity",
            "Exercise Recommendations",
            "Preventive Screening Guidelines",
            "Supplement Education (general)",
            "When to See a Doctor"
        ],
        default=["Sleep Optimization Tips", "Stress Management Strategies", "Nutrition for Longevity"]
    )

    if st.button("Get Insights", type="primary"):
        if not uploaded_file and not health_data and not question:
            st.warning("Please provide data or a question!")
        else:
            with st.spinner("Nurse Zoey Zoe is reviewing..."):
                file_content = ""
                if uploaded_file:
                    try:
                        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
                    except:
                        file_content = "[File uploaded — content partially read]"
                combined = file_content or health_data
                core_prompt = """
### Key Insights
Bullet points summarizing general educational observations from the data/question.
### General Recommendations
Evidence-based lifestyle suggestions.
### Next Steps
When to consult a professional and what to discuss.
"""
                optional_prompt = ""
                if "Sleep Optimization Tips" in insight_sections:
                    optional_prompt += "### Sleep Optimization Tips\nPractical habits for better rest and recovery.\n\n"
                if "Stress Management Strategies" in insight_sections:
                    optional_prompt += "### Stress Management Strategies\nBreathing, mindfulness, daily routines.\n\n"
                if "Nutrition for Longevity" in insight_sections:
                    optional_prompt += "### Nutrition for Longevity\nFood choices for heart health, inflammation, energy.\n\n"
                if "Exercise Recommendations" in insight_sections:
                    optional_prompt += "### Exercise Recommendations\nSafe movement for your age and goals.\n\n"
                if "Preventive Screening Guidelines" in insight_sections:
                    optional_prompt += "### Preventive Screening Guidelines\nAge-appropriate tests and checkups.\n\n"
                if "Supplement Education (general)" in insight_sections:
                    optional_prompt += "### Supplement Education (general)\nCommon options and evidence overview — consult doctor before starting.\n\n"
                if "When to See a Doctor" in insight_sections:
                    optional_prompt += "### When to See a Doctor\nRed flags and urgency guidance.\n\n"
                full_insights_prompt = core_prompt + """
### Sleep Optimization Tips
Practical habits.
### Stress Management Strategies
Daily techniques.
### Nutrition for Longevity
Food choices.
### Exercise Recommendations
Movement ideas.
### Preventive Screening Guidelines
Recommended tests.
### Supplement Education (general)
Overview — consult doctor.
### When to See a Doctor
Red flags.
"""
                base_prompt = f"""
You are Nurse Zoey Zoe, a compassionate, evidence-based registered nurse and health educator.
Data/Question: {combined or 'General wellness inquiry'}
Specific question: {question or 'Overall health insights'}
Provide general education only. Never diagnose or prescribe.
Use phrases like "Generally speaking..." or "Standard guidelines suggest...".
"""
                try:
                    # Display insights
                    display_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Nurse Zoey Zoe, compassionate health educator."}, {"role": "user", "content": base_prompt + "\n" + core_prompt + optional_prompt}],
                        max_tokens=2000,
                        temperature=0.6
                    )
                    display_insights = display_response.choices[0].message.content

                    # Full insights for email
                    full_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Nurse Zoey Zoe, compassionate health educator."}, {"role": "user", "content": base_prompt + "\n" + full_insights_prompt}],
                        max_tokens=3000,
                        temperature=0.6
                    )
                    full_insights = full_response.choices[0].message.content

                    st.success("Nurse Zoey Zoe's insights:")
                    st.markdown(display_insights)

                    st.session_state.full_insights_for_email = full_insights

                    st.info("📧 Want the **complete version** with every section? Fill in the email form below!")
                except Exception as e:
                    st.error("Nurse Zoey Zoe is consulting... try again.")
                    st.caption(f"Error: {str(e)}")

    # Email form
    if "full_insights_for_email" in st.session_state:
        st.markdown("### Get Your Full Insights Emailed (Save & Share)")
        with st.form("lead_form_zoey", clear_on_submit=True):
            name = st.text_input("Your Name")
            email = st.text_input("Email (required)", placeholder="you@example.com")
            phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("📧 Send My Full Insights")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    insights_to_send = st.session_state.full_insights_for_email
                    email_body = f"""Hi {name or 'there'},

Thank you for trusting Nurse Zoey Zoe at LBL Lifestyle Solutions.

Here's your COMPLETE personalized wellness insights:

{insights_to_send}

Remember: This is general education. Always consult your healthcare provider.

Warm regards,
Nurse Zoey Zoe & the LBL Team"""
                    data = {
                        "from": "reports@lbllifestyle.com",
                        "to": [email],
                        "cc": [YOUR_EMAIL],
                        "subject": f"{name or 'Client'}'s Complete LBL Wellness Insights",
                        "text": email_body
                    }
                    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Full insights sent to {email}! Check your inbox.")
                            st.balloons()
                            if "full_insights_for_email" in st.session_state:
                                del st.session_state.full_insights_for_email
                        else:
                            st.error(f"Send failed: {response.text}")
                    except Exception as e:
                        st.error(f"Send error: {str(e)}")

    # Streamlined chat
    st.markdown("### Have a follow-up question? Chat with Nurse Zoey Zoe below!")
    st.caption("Ask about symptoms, habits, prevention — I'm here to educate and support.")

    for msg in st.session_state.chat_history["zoey"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Ask Nurse Zoey Zoe a question..."):
        st.session_state.chat_history["zoey"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Nurse Zoey Zoe is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Nurse Zoey Zoe, compassionate nurse providing general wellness education. Never diagnose or prescribe."},
                        *st.session_state.chat_history["zoey"]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["zoey"].append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
