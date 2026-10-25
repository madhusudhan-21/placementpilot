# PlacementPilot

PlacementPilot is a Flask web application that helps job seekers compare their resume with a target career role. It uses a generative AI model to identify relevant and missing skills, suggest a learning roadmap, and prepare role-specific interview questions.

## Use of the project

Use PlacementPilot as a career-preparation aid: provide resume text and a target role to get a structured assessment of your current skills and areas to develop. Its results are AI-generated suggestions, not a guarantee of employment or a substitute for professional career advice.

## Key features

- Create an account and sign in to access the dashboard.
- Paste resume text or upload a PDF or DOCX resume.
- Compare a resume with a target career role.
- Review detected skills, skill gaps, a recommended learning roadmap, and interview questions.
- Save successful analyses and review them later in evaluation history.

## Tech stack

- **Language:** Python
- **Web application:** Flask, Jinja templates
- **Database and ORM:** SQLAlchemy; SQLite by default, with MySQL support through PyMySQL
- **AI analysis:** Google Gemini API
- **Resume parsing:** PyPDF2 for PDF and python-docx for DOCX
- **Configuration:** python-dotenv
- **Frontend:** HTML and CSS

## Architecture overview

The Flask application in `app.py` serves the signup, login, dashboard, history, and logout routes and renders templates from `templates/`. The dashboard accepts pasted or uploaded resume content, extracts text from supported files, and passes it with the target role to `ai.py`. That module sends the prompt to the Gemini API and returns structured analysis. `db.py` configures SQLAlchemy using `DATABASE_URL` or a local SQLite database, while `models.py` defines user and report records. Successful analysis reports are stored for the signed-in user and displayed on the history page.

## Project structure

```text
PlacementPilot/
├── ai.py                 # Gemini resume analysis
├── app.py                # Flask routes and application entry point
├── db.py                 # Database engine and SQLAlchemy sessions
├── models.py             # User and report models
├── requirements.txt      # Python dependencies
├── run.bat               # Windows virtualenv launcher
├── .env.example          # Example environment configuration
└── templates/
    ├── base.html         # Shared page layout
    ├── dashboard.html    # Resume input and analysis results
    ├── history.html      # Saved report history
    ├── login.html        # Login page
    ├── signup.html       # Signup page
    └── style.css         # Application styles
```

## Installation and setup

### Prerequisites

- Python 3.10 or newer
- A Google Gemini API key for resume analysis
- (Optional) A MySQL database if you do not want to use the default SQLite database

### Windows

```powershell
git clone https://github.com/madhusudhan-21/placementpilot.git
cd placementpilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell prevents virtual environment activation, run the application with `.venv\Scripts\python.exe app.py` instead. You can also use the included `run.bat` after creating and installing into `.venv`.

### macOS and Linux

```bash
git clone https://github.com/madhusudhan-21/placementpilot.git
cd placementpilot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY` to your key. Start the development server:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The database tables are created automatically on startup. Without `DATABASE_URL`, the app uses `placement_pilot.db` in the project directory.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes, for AI analysis | API key from [Google AI Studio](https://aistudio.google.com/app/apikey). |
| `GEMINI_MODEL` | No | Gemini model name to use. If unset, the application tries its built-in model list. |
| `DATABASE_URL` | No | SQLAlchemy database URL. Defaults to `sqlite:///./placement_pilot.db`. |
| `OPENAI_API_KEY` | No | Present in the example configuration, but OpenAI is not currently integrated as an AI provider. Set `GEMINI_API_KEY` for analysis. |

For MySQL, provide a SQLAlchemy URL using the PyMySQL driver, for example:

```dotenv
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/placementpilot
```

Keep `.env` private and never commit real API keys or database credentials. Before deploying beyond local development, replace the application's development secret key with a securely configured secret and disable Flask debug mode.

## Usage

1. Open the application and create an account, then sign in.
2. On the dashboard, paste your resume text or upload a `.pdf` or `.docx` file.
3. Enter the target career role and submit the form.
4. Review the detected skills, missing skills, roadmap, and interview questions.
5. Visit **History** to revisit successfully saved analyses, or use **Logout** to end your session.

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository and create a focused branch.
2. Install the dependencies and test your changes locally.
3. Keep changes scoped to the intended improvement and avoid including secrets or personal resume data.
4. Open a pull request with a clear summary and testing notes.

## License

No license file or license terms are currently included in this repository. All rights are otherwise reserved by the copyright holder; obtain permission before redistributing or reusing the project. Add a `LICENSE` file to specify reuse terms.

## Author

**Madhusudhan** — [GitHub](https://github.com/madhusudhan-21)