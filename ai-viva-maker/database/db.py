import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("database", "viva_maker.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    # Ensure the database directory exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database using the schema.sql file."""
    # Resolve schema path relative to this file's location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(current_dir, "schema.sql")

    with open(schema_path, 'r') as f:
        schema = f.read()


    conn = get_connection()
    try:
        conn.executescript(schema)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()

# Document Operations
def add_document(subject, topic, content, file_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (subject, topic, content, file_name) VALUES (?, ?, ?, ?)",
        (subject, topic, content, file_name)
    )
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def get_all_documents():
    conn = get_connection()
    docs = conn.execute("SELECT * FROM documents").fetchall()
    conn.close()
    return docs

def get_document(doc_id):
    conn = get_connection()
    doc = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    conn.close()
    return doc

# Session Operations
def create_session(document_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (document_id) VALUES (?)", (document_id,))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def update_session_summary(session_id, total_score, avg_score):
    conn = get_connection()
    conn.execute(
        "UPDATE sessions SET end_time = ?, total_score = ?, average_score = ? WHERE id = ?",
        (datetime.now(), total_score, avg_score, session_id)
    )
    conn.commit()
    conn.close()

def get_sessions():
    conn = get_connection()
    sessions = conn.execute("""
        SELECT s.*, d.subject, d.topic
        FROM sessions s
        JOIN documents d ON s.document_id = d.id
        ORDER BY s.start_time DESC
    """).fetchall()
    conn.close()
    return sessions

# Question Operations
def add_question(session_id, document_id, text, expected, diff, topic, expl):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO questions (session_id, document_id, question_text, expected_answer, difficulty, topic, explanation) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (session_id, document_id, text, expected, diff, topic, expl)
    )
    q_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return q_id

def get_questions_for_session(session_id):
    conn = get_connection()
    qs = conn.execute("SELECT * FROM questions WHERE session_id = ?", (session_id,)).fetchall()
    conn.close()
    return qs

# Answer Operations
def add_answer(question_id, session_id, student_answer, score, accuracy, feedback, strong, missing, example):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO answers (question_id, session_id, student_answer, ai_score, accuracy, feedback, strong_points, missing_points, example_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (question_id, session_id, student_answer, score, accuracy, feedback, strong, missing, example)
    )
    ans_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ans_id

def get_answers_for_session(session_id):
    conn = get_connection()
    ans = conn.execute("SELECT * FROM answers WHERE session_id = ?", (session_id,)).fetchall()
    conn.close()
    return ans

def delete_history():
    conn = get_connection()
    conn.execute("DELETE FROM answers")
    conn.execute("DELETE FROM questions")
    conn.execute("DELETE FROM sessions")
    conn.execute("DELETE FROM documents")
    conn.commit()
    conn.close()
