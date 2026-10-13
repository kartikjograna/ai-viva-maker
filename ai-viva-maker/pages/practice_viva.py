import streamlit as st
from database.db import get_questions_for_session, update_session_summary
from services.evaluation_service import EvaluationService
import pandas as pd

def show():
    st.title("✍️ Interactive Viva Practice")

    if 'current_session_id' not in st.session_state:
        st.warning("No active session found. Please generate questions first.")
        return

    session_id = st.session_state['current_session_id']

    # Initialize session progress
    if 'q_idx' not in st.session_state:
        st.session_state['q_idx'] = 0
        st.session_state['scores'] = []

    questions = get_questions_for_session(session_id)
    if not questions:
        st.error("No questions found for this session.")
        return

    # Check if session is already complete
    if st.session_state['q_idx'] >= len(questions):
        # Finalize session
        avg_score = sum(st.session_state['scores']) / len(questions) if questions else 0
        update_session_summary(session_id, sum(st.session_state['scores']), avg_score)

        st.success("🎉 Viva Session Completed!")
        st.balloons()
        st.markdown(f"**Your Final Average Score: {avg_score:.2f}/10**")
        if st.button("Restart Session"):
            st.session_state['q_idx'] = 0
            st.session_state['scores'] = []
            st.rerun()
        return

    # Display current question
    q = questions[st.session_state['q_idx']]
    st.markdown(f"### Question {st.session_state['q_idx'] + 1} of {len(questions)}")
    st.info(q['question_text'])
    st.caption(f"Difficulty: {q['difficulty']} | Topic: {q['topic']}")

    # User answer
    user_ans = st.text_area("Your Answer:", key=f"ans_{st.session_state['q_idx']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer"):
            if not user_ans:
                st.warning("Please enter an answer before submitting.")
            else:
                with st.spinner("AI is evaluating your answer..."):
                    eval_result = EvaluationService().evaluate_and_save_answer(
                        session_id,
                        q['id'],
                        q['question_text'],
                        q['expected_answer'],
                        user_ans
                    )

                    if eval_result:
                        score = eval_result.get('score', 0)
                        st.session_state['scores'].append(score)

                        # Show detailed feedback
                        st.markdown("---")
                        st.subheader(f"Evaluation Result: {score}/10")
                        st.write(f"**Accuracy:** {eval_result.get('accuracy')}")
                        st.write(f"**Feedback:** {eval_result.get('feedback')}")

                        st.markdown("**✅ Strong Points:**")
                        st.write(eval_result.get('strong_points'))

                        st.markdown("**❌ Missing Points:**")
                        st.write(eval_result.get('missing_points'))

                        st.markdown("**💡 Example Answer:**")
                        st.write(eval_result.get('example_answer'))

                        st.session_state['submitted'] = True
                    else:
                        st.error("AI evaluation failed. Please try again.")

    with col2:
        if st.session_state.get('submitted'):
            if st.button("Next Question ➡️"):
                st.session_state['q_idx'] += 1
                st.session_state['submitted'] = False
                st.rerun()

    # Handle state reset on button click
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False
