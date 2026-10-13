import streamlit as st
from database.db import get_sessions, get_answers_for_session
import plotly.express as px
import pandas as pd

def show():
    st.title("📊 Performance Reports")
    st.markdown("Analyze your viva performance and identify areas for improvement.")

    sessions = get_sessions()
    if not sessions:
        st.info("No completed sessions found.")
        return

    # Session selection
    session_options = {f"Session {s['id']} - {s['subject']} ({s['start_time']})": s['id'] for s in sessions}
    selected_session_label = st.selectbox("Select a Session", options=list(session_options.keys()))
    session_id = session_options[selected_session_label]

    # Fetch answers for this session
    answers = get_answers_for_session(session_id)
    if not answers:
        st.warning("No answers recorded for this session.")
        return

    # Metrics
    avg_score = sum(a['ai_score'] for a in answers) / len(answers)

    col1, col2 = st.columns(2)
    col1.metric("Average Score", f"{avg_score:.2f}/10")
    col2.metric("Questions Attempted", len(answers))

    # Score Chart
    df = pd.DataFrame([{"Question": i+1, "Score": a['ai_score']} for i, a in enumerate(answers)])
    fig = px.line(df, x="Question", y="Score", title="Score Trend", markers=True)
    st.plotly_chart(fig)

    # Detailed Feedback
    st.subheader("Detailed Analysis")
    for a in answers:
        with st.expander(f"Question {a['id']} - Score: {a['ai_score']}/10"):
            st.write(f"**Your Answer:** {a['student_answer']}")
            st.write(f"**Feedback:** {a['feedback']}")
            st.write(f"**Missing Concepts:** {a['missing_points']}")

    # Overall suggestions
    st.markdown("---")
    st.subheader("💡 Personalized Study Suggestions")
    if avg_score < 5:
        st.error("Focus on the foundational definitions and conceptual clarity of the topic.")
    elif avg_score < 8:
        st.warning("You have a good grasp, but need to incorporate more technical details and examples in your answers.")
    else:
        st.success("Excellent performance! Try harder questions or move to the next topic.")
