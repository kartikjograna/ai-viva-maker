import streamlit as st
from database.db import get_all_documents, create_session
from services.question_service import QuestionService

def show():
    st.title("⚙️ Generate Viva Questions")
    st.markdown("Configure your viva session and let AI create the questions.")

    docs = get_all_documents()
    if not docs:
        st.warning("No documents found. Please upload material first.")
        return

    # Document selection
    doc_options = {f"{d['subject']} - {d['topic']} (ID: {d['id']})": d['id'] for d in docs}
    selected_doc_label = st.selectbox("Select Study Material", options=list(doc_options.keys()))
    doc_id = doc_options[selected_doc_label]

    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        num_q = st.selectbox("Number of Questions", [5, 10, 15])
    with col2:
        q_type = st.selectbox("Question Type", ["Conceptual", "Definition-based", "Application-based", "Scenario-based", "Mixed"])

    if st.button("🚀 Generate Questions"):
        with st.spinner("AI is analyzing the document and crafting questions..."):
            from database.db import get_document
            doc = get_document(doc_id)

            # Create a new session
            session_id = create_session(doc_id)

            qs = QuestionService().generate_and_save_questions(
                session_id,
                doc_id,
                doc['content'],
                doc['subject'],
                doc['topic'],
                difficulty,
                num_q,
                q_type
            )

            if qs:
                st.success(f"Generated {len(qs)} questions successfully!")
                st.session_state['current_session_id'] = session_id
                st.info("You can now head to 'Practice Viva' to start your session.")
            else:
                st.error("AI could not generate questions. The material might be too short or irrelevant.")
