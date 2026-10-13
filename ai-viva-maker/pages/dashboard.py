import streamlit as st
from database.db import get_sessions, get_all_documents
import pandas as pd

def show():
    st.title("🚀 Home Dashboard")
    st.markdown("Welcome to **AI Viva Maker**, your intelligent partner for viva preparation. Upload your materials and let AI challenge you!")

    # Fetch data for metrics
    docs = get_all_documents()
    sessions = get_sessions()

    # Calculate metrics
    total_docs = len(docs)
    total_sessions = len(sessions)
    avg_score = 0
    if sessions:
        avg_score = sum(s['average_score'] or 0 for s in sessions) / total_sessions

    # Metric Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Documents Uploaded", total_docs)
    col2.metric("Viva Sessions", total_sessions)
    col3.metric("Overall Avg Score", f"{avg_score:.2f}/10")

    st.markdown("---")

    # Recent Activity
    st.subheader("📅 Recent Sessions")
    if not sessions:
        st.info("No sessions recorded yet. Start by uploading material!")
    else:
        df = pd.DataFrame([
            {
                "Subject": s['subject'],
                "Topic": s['topic'],
                "Date": s['start_time'],
                "Score": s['average_score']
            } for s in sessions
        ])
        st.table(df.head(5))

    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    c1, c2 = st.columns(2)
    if c1.button("➕ Upload New Material"):
        # Streamlit cannot easily 'redirect' via button,
        # but the user can change the radio button in the sidebar.
        st.info("Please select 'Upload Material' from the sidebar.")
    if c2.button("✍️ Start New Viva"):
        st.info("Please select 'Generate Questions' from the sidebar.")
