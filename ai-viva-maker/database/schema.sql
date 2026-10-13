-- Table for uploaded documents
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    file_name TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for viva sessions
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    total_score REAL,
    average_score REAL,
    FOREIGN KEY (document_id) REFERENCES documents (id)
);

-- Table for generated questions
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    document_id INTEGER,
    question_text TEXT NOT NULL,
    expected_answer TEXT,
    difficulty TEXT,
    topic TEXT,
    explanation TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions (id),
    FOREIGN KEY (document_id) REFERENCES documents (id)
);

-- Table for student answers and evaluations
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    session_id INTEGER,
    student_answer TEXT,
    ai_score INTEGER,
    accuracy TEXT,
    feedback TEXT,
    strong_points TEXT,
    missing_points TEXT,
    example_answer TEXT,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions (id),
    FOREIGN KEY (session_id) REFERENCES sessions (id)
);
