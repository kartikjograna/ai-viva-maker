import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.demo_mode = False

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Gemini configuration error: {e}")
                self.demo_mode = True
        else:
            self.demo_mode = True

    def _generate_content(self, prompt):
        """Internal helper to call Gemini API or return demo response."""
        if self.demo_mode:
            return self._get_demo_response(prompt)

        try:
            response = self.model.generate_content(prompt)
            # Attempt to clean JSON markdown wrappers if present
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return text
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return None

    def _get_demo_response(self, prompt):
        """Provides hardcoded responses for demo mode."""
        if "generate questions" in prompt.lower():
            return json.dumps([
                {
                    "question": "What is a Process in Operating Systems?",
                    "expected_answer": "A process is a program in execution, containing the program code, current activity, and resources.",
                    "difficulty": "Easy",
                    "topic": "Process Management",
                    "explanation": "Processes are the basic unit of work in an OS."
                },
                {
                    "question": "Difference between a Process and a Thread?",
                    "expected_answer": "A process is an independent execution unit with its own memory space, while a thread is a lightweight unit within a process that shares memory with other threads of the same process.",
                    "difficulty": "Medium",
                    "topic": "Threads",
                    "explanation": "Threads allow for concurrency within a single application."
                },
                {
                    "question": "Explain CPU Scheduling and why it is needed.",
                    "expected_answer": "CPU scheduling is the process of determining which process in the ready queue is allocated the CPU. It is needed to maximize CPU utilization and ensure fairness.",
                    "difficulty": "Medium",
                    "topic": "CPU Scheduling",
                    "explanation": "Scheduling algorithms like Round Robin or FCFS manage CPU time."
                }
            ])
        elif "evaluate" in prompt.lower():
            return json.dumps({
                "score": 7,
                "accuracy": "Mostly Correct",
                "feedback": "You covered the main points but missed the detail about memory sharing.",
                "strong_points": "Correctly identified the definition of a thread.",
                "missing_points": "Did not explicitly mention that threads share the same heap memory.",
                "example_answer": "A thread is a lightweight process. Multiple threads within a process share the same address space and resources, allowing for faster communication."
            })
        return "{}"

    def generate_questions(self, text, subject, topic, difficulty, num_questions, q_type):
        """Generates a list of viva questions based on study material."""
        prompt = f"""
        You are an expert academic examiner. Based on the following study material, generate {num_questions} viva questions.

        Subject: {subject}
        Topic: {topic}
        Difficulty: {difficulty}
        Question Type: {q_type}

        Material:
        {text}

        Return the result as a JSON list of objects. Each object must have:
        - "question": The question text
        - "expected_answer": Key points that should be in the answer
        - "difficulty": {difficulty}
        - "topic": {topic}
        - "explanation": A brief explanation of the concept

        Ensure the questions are grounded ONLY in the provided material. If the material is insufficient, return an empty list.
        Strictly return ONLY valid JSON.
        """
        return self._generate_content(prompt)

    def evaluate_answer(self, question, expected_answer, student_answer):
        """Evaluates a student's answer against the expected answer."""
        prompt = f"""
        You are a fair and precise examiner. Evaluate the student's answer to the following viva question.

        Question: {question}
        Expected Key Points: {expected_answer}
        Student Answer: {student_answer}

        Evaluation Rubric:
        - Score: 0 to 10 (0 for blank/irrelevant, 10 for comprehensive/perfect)
        - Accuracy: Short label (e.g., Correct, Mostly Correct, Partially Correct, Incorrect)
        - Feedback: Constructive educational feedback
        - Strong Points: What the student got right
        - Missing Points: What the student missed or got wrong
        - Example Answer: A high-scoring version of the answer

        Return the result as a JSON object with these keys:
        "score", "accuracy", "feedback", "strong_points", "missing_points", "example_answer"

        Strictly return ONLY valid JSON.
        """
        return self._generate_content(prompt)
