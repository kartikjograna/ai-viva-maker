# AI Viva Maker

AI-powered study application that generates viva questions from study materials and evaluates student answers.

## Features
- 📄 Upload PDF, DOCX, TXT files.
- 🤖 AI-powered question generation based on provided text.
- ✍️ Interactive Viva practice mode.
- 📊 Detailed performance reports with AI feedback.
- 📜 Session history persistence using SQLite.
- 🛠️ Demo mode for immediate testing without API keys.

## Technology Stack
- **Language:** Python 3.9+
- **Frontend:** Streamlit
- **AI Engine:** Google Gemini Pro
- **Database:** SQLite
- **Document Processing:** PyMuPDF, python-docx

## Installation (Windows)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-viva-maker
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key:**
   - Create a `.env` file in the root directory.
   - Add your Gemini API key:
     `GEMINI_API_KEY=your_api_key_here`

## How to Run
```bash
streamlit run app.py
```

## Demo Mode
If no `GEMINI_API_KEY` is provided in the `.env` file, the application automatically enters **Demo Mode**. In this mode:
- AI responses are simulated using hardcoded samples.
- You can still upload documents and generate questions, but the feedback will be generic.

## Project Structure
- `app.py`: Main entry point.
- `pages/`: Contains the individual screens.
- `services/`: Backend logic for AI, Documents, and Evaluation.
- `database/`: SQL schema and DB helper functions.
- `sample_data/`: Sample text for demonstration.

## Testing
To run basic tests:
```bash
python -m pytest tests/
```
