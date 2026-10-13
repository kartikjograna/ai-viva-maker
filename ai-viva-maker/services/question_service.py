from services.ai_service import AIService
from database.db import add_question, get_questions_for_session

class QuestionService:
    def __init__(self):
        self.ai = AIService()

    def generate_and_save_questions(self, session_id, doc_id, text, subject, topic, difficulty, num_questions, q_type):
        """Coordinates AI generation and database storage of questions."""
        raw_json = self.ai.generate_questions(text, subject, topic, difficulty, num_questions, q_type)

        if not raw_json:
            return None

        import json
        try:
            questions_data = json.loads(raw_json)
        except json.JSONDecodeError:
            return None

        saved_ids = []
        for q in questions_data:
            q_id = add_question(
                session_id,
                doc_id,
                q['question'],
                q['expected_answer'],
                q['difficulty'],
                q['topic'],
                q['explanation']
            )
            saved_ids.append(q_id)

        return saved_ids
