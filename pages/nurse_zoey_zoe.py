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

    # FORCE SCROLL TO TOP WHEN PAGE LOADS
    st.markdown("""
    <script>
        window.parent.document.querySelector('section.main').scrollTop = 0;
        window.scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Team"):
        st.session_state.current_page = "home"
        st.rerun()

    # Hero image
    st.image("https://i.postimg.cc/BnFgfCTD/pexels-kampus-7551620.jpg", caption="LIVE BETTER LONGER – Welcome to your longevity lifestyle")

    st.markdown("### 🩺 GREETINGS. IM NURSE ZOEY ZOE – your friendly nurse assistant, here to support you with compassionate and reliable guidance every step of the way. ")
    st.write("I can help you understand medical conditions, symptoms, treatments, and medications in simple, easy-to-follow terms; offer general advice on managing everyday health concerns like pain relief, wound care, or chronic issues such as diabetes or hypertension; provide tips for wellness, nutrition, exercise, and mental health support; explain procedures or post-care instructions; assist caregivers with practical strategies for supporting loved ones; and always listen with empathy to offer reassurance during stressful times—remember, though, I'm here for information and support, so please consult your healthcare provider for personalized advice or emergencies..")
    st.warning("**Important**: This is for educational purposes only. I do not provide medical diagnoses or treatment. Always consult a licensed healthcare professional.")
    st.write("Upload labs or enter data for general insights, or ask wellness questions.")

    uploaded_file = st.file_uploader("Upload labs/health data (PDF, text)", type=["pdf", "txt"])
    health_data = st.text_area("Or enter data manually", height=150)
    question = st.text_input("General question (optional)")

    if st.button("Get Insights", type="primary"):
        if not uploaded_file and not health_data and not question:
            st.warning("Please provide data or a question!")
        else:
            with st.spinner("Nurse Zoey Zoe is reviewing..."):
                file_content = ""
                if uploaded_file:
                    try:
                        file_content = uploaded_file.read().decode("utf-8")
                    except:
                        file_content = "[File uploaded but unreadable]"
                combined = file_content or health_data
                zoey_prompt = f"""
                You are Nurse Zoey Zoe, a compassionate nurse providing general wellness education.
                Data: {combined}
                Question: {question or 'General review'}
                Give educational insights only. Use phrases like "Based on standard guidelines..." Do not diagnose.
                Structure:
                ### Key Insights
                - Bullet points
                ### General Recommendations
                - Lifestyle tips
                ### Next Steps
                - Suggest consulting a professional
                """
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": "You are Nurse Zoey Zoe, a compassionate nurse."},
                            {"role": "user", "content": zoey_prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.6
                    )
                    insights = response.choices[0].message.content
                    st.success("Nurse Zoey Zoe's insights:")
                    st.markdown(insights)

                    st.session_state.chat_history["zoey"].append({"role": "assistant", "content": f"Here's your wellness insights:\n\n{insights}"})
                except Exception as e:
                    st.error("Nurse Zoey Zoe is consulting... try again.")
                    st.caption(f"Note: {str(e)}")

    # Chat Section
    st.markdown("### Have a follow-up question? Chat with me!")
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history["zoey"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask Nurse Zoey Zoe a question..."):
        st.session_state.chat_history["zoey"].append({"role": "user", "content": prompt})
        st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Nurse Zoey Zoe, a compassionate and knowledgeable nurse providing general wellness education and supportive guidance. You never diagnose conditions or prescribe treatments. Always remind users to consult licensed healthcare professionals."},
                        *st.session_state.chat_history["zoey"]
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history["zoey"].append({"role": "assistant", "content": reply})
                st.markdown(f"<div class='assistant-message'>{reply}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Sorry, I'm having trouble right now. Try again soon.")

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<small>LBL Lifestyle Solutions • Your Holistic Longevity Blueprint<br>Powered by Grok (xAI) • Personalized wellness powered by AI</small>", unsafe_allow_html=True)

show()
