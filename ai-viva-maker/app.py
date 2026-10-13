import streamlit as st
from database.db import init_db

# Initialize database on start
init_db()

st.set_page_config(
    page_title="AI Viva Maker",
    page_icon="🎓",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("🎓 AI Viva Maker")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate to:",
    [
        "Dashboard",
        "Upload Material",
        "Generate Questions",
        "Practice Viva",
        "Performance Reports",
        "Session History",
        "Settings"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Project: BTech IT College Project\nVersion: 1.0")

# Page Routing
if page == "Dashboard":
    import pages.dashboard as dashboard
    dashboard.show()
elif page == "Upload Material":
    import pages.upload_material as upload
    upload.show()
elif page == "Generate Questions":
    import pages.generate_questions as gen
    gen.show()
elif page == "Practice Viva":
    import pages.practice_viva as practice
    practice.show()
elif page == "Performance Reports":
    import pages.reports as reports
    reports.show()
elif page == "Session History":
    import pages.history as history
    history.show()
elif page == "Settings":
    import pages.settings as settings
    settings.show()
