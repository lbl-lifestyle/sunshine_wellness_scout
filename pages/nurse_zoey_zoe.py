import streamlit as st
import requests
from openai import OpenAI

XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def show():
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
        .stTextArea > div > div > textarea {
            background-color: white !important;
            color: #1e3a2f !important;
            border: 2px solid #a0c4d8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
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

    st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)

    if st.button("← Back to Team", key="zoey_back_button"):
        st.session_state.current_page = "home"
        st.rerun()

    st.image("https://i.postimg.cc/BnFgfCTD/pexels-kampus-7551620.jpg", caption="LIVE BETTER LONGER")

    st.markdown("### 🩺 Hello! I'm Nurse Zoey Zoe – your friendly health educator")
    st.success("**This tool is completely free – no cost, no obligation!**")
    st.write("I provide general wellness education and help you understand symptoms, labs, and preventive habits.")
    st.warning("**Important**: I am not a doctor. This is general education only. Always consult a licensed healthcare professional.")

    user_name = st.text_input("Your first name (optional)", value=st.session_state.get("user_name", ""), key="zoey_name_input")
    if user_name:
        st.session_state.user_name = user_name.strip()
    else:
        st.session_state.user_name = "there"

    with st.expander("💡 Quick Start Ideas"):
        st.markdown("""
        - Explain my bloodwork in simple terms
        - What lifestyle changes help lower blood pressure?
        - Review my symptoms and when to see a doctor
        - Suggest preventive screenings for my age
        """)

    st.markdown("### Tell Zoey about your health questions or data")
    uploaded_file = st.file_uploader("Upload labs/health data (PDF, text, image)", type=["pdf", "txt", "jpg", "png"], key="zoey_upload")
    health_data = st.text_area("Or enter data manually", height=200, key="zoey_data")
    question = st.text_input("Your main question or concern (optional)", key="zoey_question")

    insight_sections = st.multiselect("Add optional sections:", [
        "Sleep Optimization Tips", "Stress Management Strategies", "Nutrition for Longevity",
        "Exercise Recommendations", "Preventive Screening Guidelines", "Supplement Education (general)",
        "When to See a Doctor"
    ], default=["Sleep Optimization Tips", "Stress Management Strategies", "Nutrition for Longevity"], key="zoey_sections")

    if st.button("Get Insights", type="primary", key="zoey_generate"):
        if not uploaded_file and not health_data and not question:
            st.warning("Please provide data or a question!")
        else:
            with st.spinner("Nurse Zoey Zoe is reviewing..."):
                file_content = ""
                if uploaded_file:
                    try:
                        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
                    except:
                        file_content = "[File uploaded]"
                combined = file_content or health_data

                core_prompt = """
### Key Insights
Bullet points summarizing general observations.
### General Recommendations
Evidence-based lifestyle suggestions.
### Next Steps
When to consult a professional.
"""
                optional_prompt = ""
                if "Sleep Optimization Tips" in insight_sections: optional_prompt += "### Sleep Optimization Tips\nPractical habits.\n\n"
                if "Stress Management Strategies" in insight_sections: optional_prompt += "### Stress Management Strategies\nTechniques.\n\n"
                if "Nutrition for Longevity" in insight_sections: optional_prompt += "### Nutrition for Longevity\nFood choices.\n\n"
                if "Exercise Recommendations" in insight_sections: optional_prompt += "### Exercise Recommendations\nMovement ideas.\n\n"
                if "Preventive Screening Guidelines" in insight_sections: optional_prompt += "### Preventive Screening Guidelines\nAge-appropriate tests.\n\n"
                if "Supplement Education (general)" in insight_sections: optional_prompt += "### Supplement Education (general)\nOverview — consult doctor.\n\n"
                if "When to See a Doctor" in insight_sections: optional_prompt += "### When to See a Doctor\nRed flags.\n\n"

                full_insights_prompt = core_prompt + optional_prompt + """
### Sleep Optimization Tips
### Stress Management Strategies
### Nutrition for Longevity
### Exercise Recommendations
### Preventive Screening Guidelines
### Supplement Education (general)
### When to See a Doctor
"""

                base_prompt = f"""
User name: {st.session_state.user_name}
Data/Question: {combined}
Specific question: {question or 'General insights'}
Provide general education only. Never diagnose.
"""

                try:
                    display_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Nurse Zoey Zoe, compassionate health educator."}, {"role": "user", "content": base_prompt + core_prompt + optional_prompt}],
                        max_tokens=2000,
                        temperature=0.6
                    )
                    display_insights = display_response.choices[0].message.content

                    full_response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "system", "content": "You are Nurse Zoey Zoe, compassionate health educator."}, {"role": "user", "content": base_prompt + full_insights_prompt}],
                        max_tokens=3000,
                        temperature=0.6
                    )
                    full_insights = full_response.choices[0].message.content

                    st.success("Nurse Zoey Zoe's insights:")
                    st.markdown(display_insights)
                    st.session_state.full_insights_for_email = full_insights
                    st.info("📧 Want the complete version? Fill in email below!")
                except Exception as e:
                    st.error("Connection issue.")

    if "full_insights_for_email" in st.session_state:
        st.markdown("### Get Your Full Insights Emailed")
        with st.form("lead_form_zoey", clear_on_submit=True):
            name = st.text_input("Your Name", key="zoey_email_name")
            email = st.text_input("Email (required)", key="zoey_email")
            phone = st.text_input("Phone (optional)", key="zoey_phone")
            submitted = st.form_submit_button("📧 Send My Full Insights")
            if submitted:
                if not email:
                    st.error("Email required!")
                else:
                    insights_to_send = st.session_state.full_insights_for_email
                    email_body = f"""Hi {st.session_state.user_name},
Here's your COMPLETE wellness insights from Nurse Zoey Zoe:
{insights_to_send}
Remember: General education only.
Warm regards,
Nurse Zoey Zoe & the LBL Team"""
                    data = {"from": "reports@lbllifestyle.com", "to": [email], "cc": [YOUR_EMAIL], "subject": "Your LBL Wellness Insights", "text": email_body}
                    headers = {"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
                    try:
                        response = requests.post("https://api.resend.com/emails", json=data, headers=headers)
                        if response.status_code == 200:
                            st.success(f"Sent to {email}!")
                            st.balloons()
                            del st.session_state.full_insights_for_email
                    except Exception as e:
                        st.error("Send error.")

    st.markdown("### Have a follow-up question? Chat with Nurse Zoey Zoe! 🩺")
    for msg in st.session_state.chat_history.get("zoey", []):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask Nurse Zoey Zoe...", key="zoey_chat_input"):
        st.session_state.chat_history.setdefault("zoey", []).append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": "You are Nurse Zoey Zoe. General education only."}] + st.session_state.chat_history["zoey"],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["zoey"].append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.write(reply)
            except Exception as e:
                st.error("Connection issue.")

    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Powered by Grok (xAI)</small>", unsafe_allow_html=True)

show()
