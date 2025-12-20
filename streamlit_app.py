import streamlit as st

# ============================
# SESSION STATE INITIALIZATION
# ============================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "fred": [],
        "greg": [],
        "zoey": []
    }

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Optional: Helpful for debugging or future expansions
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

# =====================
# PAGE NAVIGATION LOGIC
# =====================

# Function to switch pages safely
def navigate_to(page: str):
    st.session_state.current_page = page
    st.rerun()

# Determine which page to show
page = st.session_state.current_page

# =====================
# HOME PAGE (Main Welcome)
# =====================

if page == "home":
    st.title("🌟 Welcome to LBL Lifestyle Solutions")
    st.markdown("""
    Get personalized guidance from our expert team.  
    Click on an advisor below to start chatting!
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🛋️ Talk to Fred\nWellness Home Scout", use_container_width=True):
            navigate_to("fred")

    with col2:
        if st.button("💪 Talk to Greg\nFitness Coach", use_container_width=True):
            navigate_to("greg")

    with col3:
        if st.button("🩺 Talk to Nurse Zoey Zoe\nHealth Advisor", use_container_width=True):
            navigate_to("zoey")

# =====================
# AGENT PAGES (Imported)
# =====================

elif page == "fred":
    import pages.fred as fred_page
    fred_page.show()  # We'll define a show() function in each page

elif page == "greg":
    import pages.greg as greg_page
    greg_page.show()

elif page == "zoey":
    import pages.zoey as zoey_page
    zoey_page.show()

else:
    st.error("Page not found!")
