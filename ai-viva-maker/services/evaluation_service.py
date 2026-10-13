from services.ai_service import AIService
from database.db import add_answer

class EvaluationService:
    def __init__(self):
        self.ai = AIService()

    def evaluate_and_save_answer(self, session_id, question_id, question_text, expected_answer, student_answer):
        """Coordinates AI evaluation and database storage of the answer."""
        raw_json = self.ai.evaluate_answer(question_text, expected_answer, student_answer)

        if not raw_json:
            return None

        import json
        try:
            eval_data = json.loads(raw_json)
        except json.JSONDecodeError:
            return None

        ans_id = add_answer(
            question_id,
            session_id,
            student_answer,
            eval_data.get('score', 0),
            eval_data.get('accuracy', 'N/A'),
            eval_data.get('feedback', ''),
            eval_data.get('strong_points', ''),
            eval_data.get('missing_points', ''),
            eval_data.get('example_answer', '')
        )

        return eval_data
