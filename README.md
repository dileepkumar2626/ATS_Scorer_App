# ResumeAnalyzer AI — Intelligent ATS Resume Analyzer

**Analyze your resume, understand how it aligns with a job description, and get actionable recommendations to improve it.**

ResumeAnalyzer AI is a full-stack resume analysis application built with **Streamlit, FastAPI, NLP, sentence embeddings, Groq, and Supabase**. It evaluates key resume quality dimensions, extracts structured information from uploaded resumes, validates listed skills against project and experience evidence, and optionally compares a resume with a target job description.

> **Important:** This tool provides an estimate and improvement guidance. It does not reproduce the proprietary scoring logic of every Applicant Tracking System (ATS), guarantee that a resume will pass an ATS, or guarantee an interview.

---

## Table of contents

- [Highlights](#highlights)
- [How it works](#how-it-works)
- [Scoring methodology](#scoring-methodology)
- [Technology stack](#technology-stack)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Running the application](#running-the-application)
- [API reference](#api-reference)
- [Machine learning notebooks](#machine-learning-notebooks)
- [Deployment notes](#deployment-notes)
- [Security and privacy](#security-and-privacy)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Highlights

### Resume analysis

- Upload resumes in **PDF, DOC, or DOCX** format.
- Extract resume text and structured information.
- Analyze resume quality across multiple weighted dimensions.
- Identify strengths, issues, and areas that need attention.
- Receive detailed feedback and improvement recommendations.

### Job description matching

- Optionally provide a target job description.
- Extract relevant keywords and required/preferred skills.
- Compare resume keywords with job requirements.
- Calculate semantic similarity using sentence embeddings.
- Identify matched keywords, missing keywords, and skill gaps.

### Skill validation

- Extract skills, projects, and experience from the resume.
- Check whether listed skills are supported by evidence in projects or experience.
- Separate validated and unvalidated skills.
- Highlight skills that may need stronger evidence in the resume.

### Account and report features

- Email/password authentication through Supabase.
- Google sign-in through Supabase OAuth.
- Password-reset flow.
- User-specific analysis history.
- Delete saved analysis records.
- Generate downloadable PDF analysis reports, including reports from saved history.

### Additional workspace views

The Streamlit interface includes dedicated views for resume scoring, job matching, skill-gap analysis, resume building, analysis history, saved reports, and learning resources.

## How it works

The application follows a frontend–backend architecture.

1. **Sign in:** The user authenticates through Supabase in the Streamlit interface.
2. **Upload:** The user uploads a supported resume file and can optionally enter a job description.
3. **Text extraction:** The FastAPI backend validates the file and extracts its text.
4. **Resume parsing:** The Groq-powered parser converts resume text into structured information such as skills, projects, experience, keywords, and action verbs.
5. **NLP processing:** spaCy processes text, while a Sentence Transformers model generates embeddings for semantic comparisons.
6. **Skill validation:** The analysis pipeline checks whether extracted skills are demonstrated in the candidate's projects and experience.
7. **Scoring:** The scoring engine calculates component scores and an overall ATS-oriented score.
8. **Job matching (optional):** When a job description is supplied, the system extracts job requirements and calculates keyword and semantic matches.
9. **Feedback:** The feedback and recommendation engines produce issues, strengths, and suggested improvements.
10. **Persistence:** The backend attempts to save the analysis to Supabase so the authenticated user can access their history. A history-save failure is logged and does not block the analysis response.
11. **Report generation:** The user can generate a PDF report from the current analysis or a saved analysis.

## Scoring methodology

The overall score is composed of five weighted dimensions:

| Dimension | Weight |
|---|---:|
| Formatting | 20% |
| Content | 25% |
| Keywords | 25% |
| Skill validation | 15% |
| ATS compatibility | 15% |
| **Total** | **100%** |

For job-description matching, the configured combination is:

- Keyword matching: **60%**
- Semantic similarity: **40%**

These are the weights configured in the current codebase. The result should be treated as an application-specific estimate, not an official ATS score.

## Technology stack

| Area | Technologies |
|---|---|
| Frontend | Python, Streamlit, custom CSS |
| Backend API | FastAPI, Uvicorn, Pydantic |
| NLP | spaCy |
| Semantic embeddings | Sentence Transformers, `all-MiniLM-L6-v2` |
| LLM-assisted parsing | Groq API |
| Resume parsing | pdfplumber, PyPDF2, python-docx |
| Authentication | Supabase Auth, Google OAuth, JWT verification |
| Database / persistence | Supabase REST API |
| PDF reports | Jinja2, xhtml2pdf |
| HTTP clients | Requests, HTTPX |
| Research and experimentation | Jupyter Notebook, pandas, NumPy, BERT embeddings |

## Architecture

```mermaid
flowchart TD
    U[User] --> UI[Streamlit Frontend]
    UI --> AUTH[Supabase Authentication]
    UI --> API[FastAPI Backend]
    API --> FILE[Resume File Parser]
    FILE --> TEXT[Extracted Resume Text]
    TEXT --> LLM[Groq Resume Parser]
    LLM --> STRUCT[Structured Resume Data]
    STRUCT --> NLP[spaCy NLP]
    STRUCT --> EMB[Sentence Transformer Embeddings]
    NLP --> SCORE[ATS Scoring Engine]
    EMB --> VALIDATE[Skill Validation and JD Matching]
    STRUCT --> FEEDBACK[Feedback and Recommendation Engines]
    SCORE --> RESULT[Analysis Response]
    VALIDATE --> RESULT
    FEEDBACK --> RESULT
    RESULT --> DB[Supabase Analysis History]
    RESULT --> UI
    UI --> PDF[PDF Report Generation]
```

### Main backend services

| Module | Responsibility |
|---|---|
| `resume_parser.py` | File validation and text extraction from supported resume formats |
| `groq_parser.py` | LLM-assisted extraction of structured resume and job-description data |
| `resume_analyser.py` | Orchestrates the full resume-analysis pipeline |
| `ats_scorer.py` | Calculates weighted scores and generates score-based insights |
| `jd_matcher.py` | Keyword matching, semantic similarity, and skill-gap comparison |
| `feedback_engine.py` | Detects resume issues and summarizes feedback |
| `recommendation_engine.py` | Produces prioritized improvement recommendations |
| `report_generator.py` / `pdf_export.py` | Prepares report content and PDF output |
| `supabase_db.py` | Saves, retrieves, and deletes user analysis history |

## Project structure

```text
ATS_Scorer_App-main/
├── backend/
│   ├── api/
│   │   ├── auth.py                 # Supabase JWT authentication
│   │   └── routes.py               # Analysis, history, and PDF endpoints
│   ├── core/
│   │   └── config.py               # Application configuration
│   ├── database/
│   │   └── supabase_db.py          # Supabase persistence operations
│   ├── models/
│   │   └── schemas.py              # Pydantic response schemas
│   ├── services/
│   │   ├── ats_scorer.py
│   │   ├── feedback_engine.py
│   │   ├── groq_parser.py
│   │   ├── jd_matcher.py
│   │   ├── recommendation_engine.py
│   │   ├── report_generator.py
│   │   ├── resume_analyser.py
│   │   └── resume_parser.py
│   ├── templates/                  # HTML report templates
│   ├── utils/                      # File and text utilities
│   └── main.py                     # FastAPI application entry point
├── frontend/
│   ├── assets/                     # Application styles
│   ├── components/                 # Reusable Streamlit UI components
│   ├── services/                   # API and Supabase clients
│   ├── views/                      # Application pages
│   └── streamlit_app.py            # Streamlit entry point
├── jupyter_notebooks/
│   ├── data/                       # Research and experimentation data
│   ├── 01_EDA_and_DATA_prep.ipynb
│   ├── 02_BERT_Embeddings..ipynb
│   ├── 03_BERT_FINE_TUNING.ipynb
│   └── resume_embeddings.pkl
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── requirements.txt
└── README.md
```

## Getting started

### 1. Prerequisites

- Python **3.10 or newer** (Python 3.11 is a good choice for a compatible environment).
- A Groq API key.
- A Supabase project for authentication and analysis history.
- Git (optional, for cloning the repository).

The backend loads the spaCy and Sentence Transformers models during application startup. The first startup may take longer because model files may need to be downloaded.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ATS_Scorer_App.git
cd ATS_Scorer_App
```

Replace the repository URL with your own GitHub URL.

### 3. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The requirements file includes the spaCy English model packages. If your environment does not have the models installed after dependency installation, run:

```bash
python -m spacy download en_core_web_md
```

The backend first attempts to load `en_core_web_md` and falls back to `en_core_web_sm` if the primary model is unavailable.

## Configuration

Do not commit API keys, service-role keys, JWT secrets, or other credentials to GitHub.

### Backend environment variables

Create a `.env` file in the repository root:

```env
# Required for LLM-assisted parsing
GROQ_API_KEY=your_groq_api_key

# Supabase project configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_server_key

# Used when verifying HS256 Supabase JWTs.
# For asymmetric signing keys, the backend can retrieve the project's JWKS using SUPABASE_URL.
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
```

`SUPABASE_KEY` is used by the backend to access the Supabase REST API for analysis persistence. Use a server-side key with the permissions required by your database policies, and keep it exclusively on the backend. Never put a service-role key in Streamlit frontend secrets or expose it in browser code.

### Frontend Streamlit secrets

Create `.streamlit/secrets.toml` using the example file as a starting point:

```toml
[backend]
url = "http://localhost:8000"

[supabase]
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_key"

[google_oauth]
redirect_uri = "http://localhost:8501"
```

For deployment, replace the backend URL with your deployed FastAPI URL and set the OAuth redirect URI to your deployed Streamlit app URL. Add the same values through the hosting provider's secret-management interface rather than committing the secrets file.

### Supabase setup

1. Create a project in Supabase.
2. Copy the project URL and the appropriate API keys into the backend and frontend configuration described above.
3. Enable the authentication providers you intend to use (email/password and Google OAuth, if using Google sign-in).
4. Configure the OAuth redirect URLs in Supabase to include your local and deployed Streamlit URLs.
5. Create an `analysis` table compatible with the fields used by the backend persistence layer:

| Column | Purpose |
|---|---|
| `id` | Unique analysis identifier (UUID recommended) |
| `user_id` | Supabase user ID |
| `filename` | Uploaded resume filename |
| `ats_score` | Overall score |
| `keyword_match` | Job-description keyword match percentage |
| `missing_keywords` | Array/JSONB of missing keywords |
| `analysis_result` | JSONB containing the analysis response |
| `created_at` | Creation timestamp |

Use appropriate database permissions and row-level security policies for your deployment. The exact SQL schema and policies are not included in this repository, so configure them to match your Supabase project and security requirements.

## Running the application

Run the backend and frontend in **separate terminals**. Start the backend first so that the frontend can reach its API.

### Terminal 1 — FastAPI backend

From the repository root:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend URLs:

- API base: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- Health endpoint: `http://localhost:8000/health`

### Terminal 2 — Streamlit frontend

From the repository root:

```bash
streamlit run frontend/streamlit_app.py
```

Open the local URL printed by Streamlit, normally:

```text
http://localhost:8501
```

Make sure `.streamlit/secrets.toml` points to `http://localhost:8000` while running locally.

## API reference

All application routes are under `/api/v1`. The analysis and history routes require a valid Supabase access token in the `Authorization` header.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/analyze-resume` | Analyze a PDF, DOC, or DOCX resume; optionally include a job description |
| `GET` | `/api/v1/health` | Check whether the NLP and embedding models are loaded |
| `GET` | `/api/v1/history` | Retrieve the authenticated user's analysis history |
| `DELETE` | `/api/v1/history/{analysis_id}` | Delete an analysis belonging to the authenticated user |
| `POST` | `/api/v1/generate-pdf` | Generate a PDF from submitted analysis data |
| `GET` | `/api/v1/history/{analysis_id}/pdf` | Generate a PDF for a saved analysis |
| `GET` | `/health` | Basic API information and endpoint overview |

### Example: analyze a resume

The analysis endpoint accepts multipart form data:

- `resume`: the uploaded resume file (maximum configured size: 5 MB)
- `job_description`: optional job-description text
- Header: `Authorization: Bearer YOUR_SUPABASE_ACCESS_TOKEN`

Example using cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze-resume" \
  -H "Authorization: Bearer YOUR_SUPABASE_ACCESS_TOKEN" \
  -F "resume=@./resume.pdf" \
  -F "job_description=Python developer with experience in FastAPI, SQL, and machine learning"
```

## Machine learning notebooks

The `jupyter_notebooks/` directory contains experimentation materials related to the project:

- `01_EDA_and_DATA_prep.ipynb` — exploratory data analysis and data preparation.
- `02_BERT_Embeddings..ipynb` — BERT embedding experiments.
- `03_BERT_FINE_TUNING.ipynb` — BERT fine-tuning experiments.
- `data/` — datasets used in the notebooks.
- `resume_embeddings.pkl` — stored resume embeddings artifact.

These notebooks are research and experimentation assets; the production API currently loads the configured spaCy model and `sentence-transformers/all-MiniLM-L6-v2` model at startup. The notebook artifacts should not be assumed to be part of the live inference path unless explicitly integrated into the backend.

## Deployment notes

The application is designed to run as two separately configured services:

1. **FastAPI backend:** deploy the API and configure its environment variables (`GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, and, when needed, `SUPABASE_JWT_SECRET`). Ensure the host has enough memory and startup time for the NLP and embedding models.
2. **Streamlit frontend:** deploy the Streamlit app and configure `.streamlit/secrets.toml` values through the hosting platform's secret settings. Set `[backend].url` to the public backend URL.

Before deploying, also:

- Update the backend CORS allowlist in `backend/core/config.py` to include the exact deployed frontend origin.
- Configure Supabase authentication redirect URLs for the deployed frontend.
- Verify the `analysis` table and its access policies.
- Keep backend-only secrets out of frontend configuration.
- Test resume upload, authentication, history retrieval, deletion, and PDF generation on the deployed services.

## Security and privacy

- Never commit `.env` or `.streamlit/secrets.toml` files.
- Rotate any credential that has accidentally been committed or shared publicly.
- Keep privileged Supabase keys and JWT secrets on the backend only.
- Apply least-privilege database permissions and appropriate row-level security policies.
- Treat uploaded resumes and extracted personal information as sensitive data. Use only resumes you are authorized to process, and review your hosting, logging, retention, and privacy requirements before deploying this application for real users.

## Limitations

- The score is a heuristic estimate based on this project's scoring logic, not a score returned by a commercial ATS platform.
- Results depend on the quality and formatting of the uploaded document and the quality of the supplied job description.
- LLM-assisted extraction can make mistakes; review extracted skills, experience, and recommendations.
- Semantic similarity indicates textual relatedness, not proof that a candidate satisfies a job requirement.
- Model downloads and inference can require substantial memory and startup time, especially on smaller hosting instances.
- PDF export may require additional system libraries on Linux, depending on the deployment environment.

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and test them locally.
4. Commit your changes: `git commit -m "Add your feature"`.
5. Push the branch and open a pull request.

For significant changes, please describe the motivation, implementation, and testing performed.

## License

No license file is currently included in this repository. Add a `LICENSE` file before presenting the project as open source, and specify the terms under which others may use, modify, and distribute it.

---

**Built with Python, NLP, machine learning, and a focus on making resume improvement more practical and explainable.**
