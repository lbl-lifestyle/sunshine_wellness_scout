import streamlit as st
import requests
from openai import OpenAI
import re

# Initialize session state
if "email_status" not in st.session_state:
    st.session_state.email_status = None
    st.session_state.email_message = ""
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "fred"

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

# Florida-themed CSS
st.markdown("""
<style>
    .stApp {
        background: linear_gradient(to bottom, #ffecd2, #fcb69f);
        color: #0c4a6e;
    }
    .main-header { font-size: 3rem; color: #ea580c; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .tagline { font-size: 1.8rem; color: #166534; text-align: center; font-style: italic; margin-bottom: 2rem; }
    .agent-card { text-align: center; padding: 1.5rem; border-radius: 15px; background: rgba(255,255,255,0.9); box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 10px; }
    .stButton>button { background-color: #ea580c; color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 3em; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>LBL Wellness Solutions</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Your Holistic Longevity Blueprint</p>", unsafe_allow_html=True)

# Hero image - original that worked
st.image("https://thumbs.dreamstime.com/b/tropical-sunset-beach-scene-pier-palm-trees-vibrant-colors-serene-water-rocky-shore-ai-generated-356600072.jpg", use_column_width=True, caption="Your Florida Longevity Lifestyle – Active Trails at Sunset")

# === Meet Your LBL Wellness Team ===
st.markdown("### Meet Your LBL Wellness Team")

cols = st.columns(3)

with cols[0]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://thumbs.dreamstime.com/b/cartoon-realtor-presenting-colorful-house-model-style-stands-facing-forward-white-background-wearing-dark-blue-suit-393019561.jpg", width=150)
    st.markdown("**Fred**")
    st.markdown("*Wellness Home Scout*  \nProfessional goal-focused realtor")
    if st.button("Talk to Fred", key="fred", use_container_width=True):
        st.session_state.selected_agent = "fred"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[1]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://www.shutterstock.com/image-vector/man-struggling-lift-heavy-barbell-260nw-2699957111.jpg", width=150)
    st.markdown("**Greg**")
    st.markdown("*Personal Trainer*  \nMotivated gym rat")
    if st.button("Talk to Greg", key="greg", use_container_width=True):
        st.session_state.selected_agent = "greg"
    st.markdown("</div>", unsafe_allow_html=True)

with cols[2]:
    st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
    st.image("https://image.shutterstock.com/image-vector/cute-asian-female-doctor-cartoon-600w-2267904077.jpg", width=150)  # Dr. Zoey Zoe - caring animated Asian nurse
    st.markdown("**Dr. Zoey Zoe**")
    st.markdown("*Health Assessor*  \nCaring, compassionate wellness guide")
    if st.button("Talk to Dr. Zoey Zoe", key="zoey", use_container_width=True):
        st.session_state.selected_agent = "zoey"
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# === Agent Content ===
if st.session_state.selected_agent == "fred":
    st.markdown("### 🏡 Fred – Your Wellness Home Scout")
    st.success("**This tool is completely free – no cost, no obligation!**")
    st.write("Find the perfect Florida home that supports trails, natural light, home gym space, and active living.")

    st.image("https://thebiostation.com/wp-content/uploads/2023/06/outdoor-group-exercise-class-scaled.jpg", use_column_width=True, caption="Community wellness – part of your Florida longevity lifestyle")

    # (Fred's full code - inputs, Grok call, teaser, form - same as before)

elif st.session_state.selected_agent == "greg":
    st.markdown("### 💪 Greg – Your Personal Trainer")
    # (Greg's full code - same as before)

elif st.session_state.selected_agent == "zoey":
    st.markdown("### 🩺 Dr. Zoey Zoe – Your Health Assessor")
    st.warning("**Important**: This is for educational purposes only. I do not provide medical diagnoses or treatment. Always consult a licensed healthcare professional.")
    st.write("Upload labs or enter data for general insights, or ask wellness questions.")

    uploaded_file = st.file_uploader("Upload labs/health data (PDF, text)", type=["pdf", "txt"])
    health_data = st.text_area("Or enter data manually", height=150)
    question = st.text_input("General question (optional)")

    if st.button("Get Insights", type="primary"):
        if not uploaded_file and not health_data and not question:
            st.warning("Please provide data or a question!")
        else:
            with st.spinner("Dr. Zoey Zoe is reviewing..."):
                zoey_prompt = f"""
                You are Dr. Zoey Zoe, a caring and compassionate nurse providing general wellness education.

                Data: {health_data or 'From file'}
                Question: {question or 'General review'}

                Give educational insights only. Use phrases like "Based on standard guidelines..." Do not diagnose.
                """

                try:
                    response = client.chat.completions.create(
                        model="grok-4-1-fast-reasoning",
                        messages=[
                            {"role": "system", "content": "You are Dr. Zoey Zoe, a compassionate nurse."},
                            {"role": "user", "content": zoey_prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.6
                    )
                    insights = response.choices[0].message.content
                    st.success("Dr. Zoey Zoe's insights:")
                    st.markdown(insights)
                except Exception as e:
                    st.error("Dr. Zoey Zoe is consulting... try again.")
                    st.caption(f"Note: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<small>LBL Wellness Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)
