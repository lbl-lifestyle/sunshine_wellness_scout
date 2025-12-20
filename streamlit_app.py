import streamlit as st

# ===================================================
# CRITICAL: INITIALIZE SESSION STATE FIRST THING
# This MUST be at the very top — nothing above it except the import
# ===================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "fred": [],
        "greg": [],
        "zoey": []
    }

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# ===================================================
# NAVIGATION HELPER
# ===================================================

def navigate_to(page: str):
    st.session_state.current_page = page
    st.rerun()

# ===================================================
# PAGE ROUTING
# ===================================================

page = st.session_state.current_page

if page == "home":
    st.markdown("""
    <h1 style='text-align: center; color: #2E8B57;'>🌟 LBL Lifestyle Solutions</h1>
    <p style='text-align: center; font-size: 1.2rem;'>
        Your personalized path to longevity, wellness, and a thriving life in Florida.<br>
        Get expert guidance from our dedicated team — anytime.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f8f0; border-radius: 15px;'>
            <h3>🛋️ Fred</h3>
            <p><strong>Wellness Home Scout</strong><br>
            Helps you find or create calming, healthy, functional living spaces.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Talk to Fred", use_container_width=True, type="primary"):
            navigate_to("fred")

    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f8f0; border-radius: 15px;'>
            <h3>💪 Greg</h3>
            <p><strong>Fitness Coach</strong><br>
            Builds sustainable strength, mobility, and energy routines.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Talk to Greg", use_container_width=True, type="primary"):
            navigate_to("greg")

    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f8f0; border-radius: 15px;'>
            <h3>🩺 Nurse Zoey Zoe</h3>
            <p><strong>Health Advisor</strong><br>
            Evidence-based wellness, prevention, and longevity education.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Talk to Nurse Zoey Zoe", use_container_width=True, type="primary"):
            navigate_to("zoey")

    st.markdown("---")
    st.caption("Powered by Grok 4.1 Fast Reasoning • Built for lifelong wellness in the Sunshine State ☀️")

elif page == "fred":
    import pages.fred as fred_page
    fred_page.show()

elif page == "greg":
    import pages.greg as greg_page
    greg_page.show()

elif page == "zoey":
    import pages.zoey as zoey_page
    zoey_page.show()

else:
    st.error("Unknown page!")
