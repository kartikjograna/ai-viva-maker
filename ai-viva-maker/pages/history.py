import streamlit as st
from database.db import get_sessions, delete_history

def show():
    st.title("📜 Session History")
    st.markdown("Review your previous viva sessions and outcomes.")

    sessions = get_sessions()
    if not sessions:
        st.info("No history available.")
        return

    # Display as a table
    import pandas as pd
    df = pd.DataFrame([
        {
            "ID": s['id'],
            "Subject": s['subject'],
            "Topic": s['topic'],
            "Start Time": s['start_time'],
            "Avg Score": s['average_score']
        } for s in sessions
    ])
    st.table(df)

    # Delete history
    st.markdown("---")
    if st.button("🗑️ Clear All History"):
        delete_history()
        st.success("All history deleted successfully.")
        st.rerun()
