<div align="center">

<img src="assets/hero-banner.png" alt="ResumeAnalyzer AI — Intelligent resume insights" width="100%">

# ResumeAnalyzer AI

### Turn your resume into a clearer, more job-ready story.

An AI-assisted resume analysis platform that helps candidates understand resume quality, compare their experience with a target job, uncover skill gaps, and get practical improvement recommendations.

<p>
  <a href="https://atsscorerapp-bn6rwhcjax6iwts4vax8ss.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_TRY_THE_LIVE_APP-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Try the live Streamlit app">
  </a>
  <a href="https://github.com/dileepkumar2626/ATS_Scorer_App">
    <img src="https://img.shields.io/badge/💻_VIEW_SOURCE-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="View source on GitHub">
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/AI-Groq-F55036?style=flat-square">
  <img src="https://img.shields.io/badge/Auth-Supabase-3FCF8E?style=flat-square&logo=supabase&logoColor=white">
  <img src="https://img.shields.io/badge/NLP-spaCy-09A3D5?style=flat-square">
  <img src="https://img.shields.io/badge/Embeddings-Sentence_Transformers-7C3AED?style=flat-square">
</p>

<p><b>Built by <a href="https://github.com/dileepkumar2626">Dileep Kumar</a></b></p>

</div>

---

## ✨ Explore the application

**Want to try it instead of just reading about it?**

<div align="center">

<a href="https://atsscorerapp-bn6rwhcjax6iwts4vax8ss.streamlit.app/">
  <img src="https://img.shields.io/badge/OPEN_RESUMEANALYZER_AI-Click_to_launch_the_Streamlit_app-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open ResumeAnalyzer AI">
</a>

<br>

<sub>The live interface is hosted on Streamlit. The FastAPI service runs separately on Railway.</sub>

</div>

## 🖼️ Product preview

The visual below is an **illustrative dashboard concept**, not a captured screenshot of the deployed interface. Open the live app above to explore the actual product.

<div align="center">
  <img src="assets/dashboard-preview.png" alt="Illustrative ResumeAnalyzer AI dashboard preview" width="100%">
</div>

---

## 🚀 What can it do?

<table>
<tr>
<td width="50%" valign="top">

### 📄 Resume analysis
- Upload PDF, DOC, or DOCX resumes.
- Extract structured resume information.
- Review an overall ATS-oriented score.
- Understand strengths and improvement areas.
- Get detailed feedback and recommendations.

</td>
<td width="50%" valign="top">

### 🎯 Job description matching
- Add a target job description.
- Compare resume keywords with job requirements.
- Measure semantic similarity.
- Find matched and missing keywords.
- Identify potential skill gaps.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧠 Skill evidence validation
- Extract skills, projects, and experience.
- Check whether listed skills are supported by resume evidence.
- Separate validated and unvalidated skills.
- Identify where stronger examples may be needed.

</td>
<td width="50%" valign="top">

### 🔐 Accounts and reports
- Supabase email/password authentication.
- Google OAuth sign-in (when configured).
- Password-reset flow.
- User-specific analysis history.
- Delete saved analyses.
- Generate downloadable PDF reports.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧰 Career workspace
- Resume scorer.
- Job matching.
- Skill-gap analysis.
- Resume builder view.
- Analysis history.
- Saved reports and learning resources.

</td>
<td width="50%" valign="top">

### ⚙️ Full-stack architecture
- Streamlit interactive frontend.
- FastAPI backend.
- NLP and embedding-based analysis.
- Groq-powered structured extraction.
- Supabase authentication and persistence.

</td>
</tr>
</table>

## 🧩 How the analysis works

```mermaid
flowchart TD
    A["👤 User"] --> B["🖥️ Streamlit Frontend"]
    B --> C["🔐 Supabase Authentication"]
    B --> D["⚡ FastAPI Backend"]
    D --> E["📄 Resume Validation & Text Extraction"]
    E --> F["🤖 Groq Structured Parser"]
    F --> G["🧠 Structured Resume Data"]
    G --> H["spaCy NLP"]
    G --> I["Sentence Transformer Embeddings"]
    H --> J["📊 ATS Scoring Engine"]
    I --> K["🎯 Skill Validation & Job Matching"]
    G --> L["💡 Feedback & Recommendations"]
    J --> M["📈 Analysis Results"]
    K --> M
    L --> M
    M --> N["🗄️ Supabase Analysis History"]
    M --> B
    B --> O["📑 PDF Report"]
```

### 🔍 Step-by-step workflow

1. **Sign in** — authenticate through Supabase in the Streamlit app.
2. **Upload** — select a supported resume file and optionally provide a job description.
3. **Extract** — FastAPI validates the file and extracts its text.
4. **Parse** — Groq-powered parsing converts the resume into structured information.
5. **Process** — spaCy and Sentence Transformers support NLP and semantic analysis.
6. **Validate** — the pipeline checks whether listed skills have evidence in projects or experience.
7. **Score** — the scoring engine calculates the component scores and overall result.
8. **Compare** — when a job description is supplied, keyword matching and semantic similarity identify overlaps and gaps.
9. **Recommend** — feedback services produce strengths, issues, and practical suggestions.
10. **Save and export** — the backend attempts to save analysis history in Supabase, and the frontend can generate a PDF report.

## 📊 Scoring methodology

The overall resume score uses five weighted dimensions configured in `backend/core/config.py`.

| Dimension | Weight |
|---|---:|
| 📝 Formatting | 20% |
| 📄 Content | 25% |
| 🔑 Keywords | 25% |
| ✅ Skill validation | 15% |
| 🤖 ATS compatibility | 15% |
| **Total** | **100%** |

Job-description matching combines:

| Matching signal | Weight |
|---|---:|
| 🔎 Keyword matching | 60% |
| 🧠 Semantic similarity | 40% |

> **A note on scores:** These are the application's own configured heuristics, not an official score from an employer's ATS. Results are estimates intended to guide improvements; they cannot guarantee that a resume will pass an employer's screening process or lead to an interview.

## 🛠️ Technology stack

<div align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,git,github,vscode&theme=dark" alt="Technology icons: Python, FastAPI, Git, GitHub and VS Code">
</div>

| Layer | Technologies |
|---|---|
| 🖥️ Frontend | Python, Streamlit, custom CSS |
| ⚡ Backend | FastAPI, Uvicorn, Pydantic |
| 🧠 NLP | spaCy |
| 🔎 Semantic embeddings | Sentence Transformers, `all-MiniLM-L6-v2` |
| ✨ LLM-assisted parsing | Groq API |
| 📑 Document parsing | pdfplumber, PyPDF2, python-docx |
| 🔐 Authentication | Supabase Auth, Google OAuth, JWT verification |
| 🗄️ Persistence | Supabase REST API |
| 📄 PDF reports | Jinja2, xhtml2pdf |
| 🔬 Experiments | Jupyter Notebook, pandas, NumPy, BERT embeddings |

## 🏗️ Project structure

```text
ATS_Scorer_App/
│
├── assets/                         # README banner and visual previews
│
├── backend/
│   ├── api/
│   │   ├── auth.py                 # Supabase JWT verification
│   │   └── routes.py               # Analysis, health, history and PDF routes
│   ├── core/
│   │   └── config.py               # Models, score weights, limits and CORS
│   ├── database/
│   │   └── supabase_db.py          # Supabase history operations
│   ├── models/
│   │   └── schemas.py              # Pydantic response schemas
│   ├── services/
│   │   ├── ats_scorer.py           # Weighted scoring and skill validation
│   │   ├── feedback_engine.py      # Resume feedback
│   │   ├── groq_parser.py          # Groq-powered structured extraction
│   │   ├── jd_matcher.py           # Job-description matching
│   │   ├── pdf_export.py           # PDF export
│   │   ├── recommendation_engine.py
│   │   ├── report_generator.py
│   │   ├── resume_analyser.py      # Analysis orchestration
│   │   └── resume_parser.py        # File validation and text extraction
│   ├── templates/                  # HTML report templates
│   └── main.py                     # FastAPI application
│
├── frontend/
│   ├── assets/                     # Frontend styles
│   ├── components/                 # Reusable UI components
│   ├── services/
│   │   ├── api_client.py           # Calls the FastAPI backend
│   │   └── supabase_client.py      # Supabase authentication
│   ├── views/                      # Streamlit pages and views
│   └── streamlit_app.py            # Streamlit entry point
│
├── jupyter_notebooks/              # EDA and embedding experiments
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── railway.toml                    # Railway backend start configuration
├── requirements.txt
├── runtime.txt
└── README.md
```

## ⚡ Run locally

### 1. Clone the repository

```bash
git clone https://github.com/dileepkumar2626/ATS_Scorer_App.git
cd ATS_Scorer_App
```

### 2. Create a virtual environment

Use **Python 3.11** (the repository's `runtime.txt` specifies Python 3.11.9).

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If spaCy cannot find its English model, install it with:

```bash
python -m spacy download en_core_web_md
```

The backend loads spaCy and the Sentence Transformers model during startup. The first run may take longer while model files are downloaded.

### 4. Configure secrets

Create a root `.env` file for backend settings:

```env
GROQ_API_KEY=your_groq_api_key

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_server_side_supabase_key
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_jwt_secret
```

Create `.streamlit/secrets.toml` for the frontend:

```toml
[backend]
url = "http://localhost:8000"

[supabase]
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_key"

[google_oauth]
redirect_uri = "http://localhost:8501"
```

Use `.streamlit/secrets.toml.example` as the template. Never commit real credentials.

### 5. Start the FastAPI backend

In Terminal 1, from the repository root:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend links:

- Health: `http://localhost:8000/health`
- API health: `http://localhost:8000/api/v1/health`
- Swagger documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 6. Start the Streamlit frontend

In Terminal 2, from the repository root:

```bash
streamlit run frontend/streamlit_app.py
```

Open `http://localhost:8501` in your browser. Ensure `[backend].url` in Streamlit secrets points to the FastAPI backend.

## 🔌 API reference

The API router is mounted under `/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/analyze-resume` | Analyze a PDF, DOC, or DOCX resume; optional job description |
| `GET` | `/api/v1/health` | Check API and model readiness |
| `GET` | `/api/v1/history` | Retrieve the authenticated user's analysis history |
| `DELETE` | `/api/v1/history/{analysis_id}` | Delete a history entry |
| `POST` | `/api/v1/generate-pdf` | Generate a PDF from analysis data |
| `GET` | `/api/v1/history/{analysis_id}/pdf` | Generate a PDF for a saved analysis |
| `GET` | `/health` | Basic application health information |

Protected endpoints require a Supabase access token:

```http
Authorization: Bearer YOUR_SUPABASE_ACCESS_TOKEN
```

### Example: analyze a resume

```bash
curl -X POST "http://localhost:8000/api/v1/analyze-resume" \
  -H "Authorization: Bearer YOUR_SUPABASE_ACCESS_TOKEN" \
  -F "resume=@./resume.pdf" \
  -F "job_description=Python developer with FastAPI, SQL, and machine learning experience"
```

You can also explore the interactive API schema at `http://localhost:8000/docs` after starting the backend.

## ☁️ Deployment

The project uses two separately deployed services:

| Service | Platform | Responsibility |
|---|---|---|
| 🌐 Frontend | Streamlit | User interface and authentication experience |
| ⚙️ Backend | Railway | FastAPI, NLP models, resume analysis and API endpoints |

### Railway — FastAPI backend

1. Create a Railway project and deploy the GitHub repository.
2. Keep the service root at the repository root.
3. Add backend environment variables in Railway's Variables panel.
4. The repository's `railway.toml` starts the FastAPI service using the Railway-provided `$PORT`.
5. Generate a public Railway domain.
6. Test `/health` and `/api/v1/health` on the deployed backend URL.

The frontend API client currently has a Railway backend URL as its fallback. The recommended setup is to explicitly set `[backend].url` in Streamlit secrets to the deployed backend URL.

### Streamlit — frontend

1. Deploy the repository to Streamlit Community Cloud.
2. Set the main file path to `frontend/streamlit_app.py`.
3. Add the frontend secrets in Streamlit's app settings.
4. Set `[backend].url` to the Railway FastAPI URL.
5. Set the Google OAuth redirect URI to the exact deployed Streamlit app URL.
6. Add the deployed frontend origin to the backend CORS allowlist in `backend/core/config.py`.
7. Test sign-in, resume upload, job-description matching, history and PDF export.

### Live deployment

- **Streamlit frontend:** [Open ResumeAnalyzer AI](https://atsscorerapp-bn6rwhcjax6iwts4vax8ss.streamlit.app/)
- **Railway backend:** `https://atsscorerapp-production.up.railway.app`
- **Backend health:** [Check API health](https://atsscorerapp-production.up.railway.app/api/v1/health)

## 🔐 Security and privacy

- Never commit `.env`, `.streamlit/secrets.toml`, API keys, JWT secrets, or privileged Supabase keys.
- Use the Supabase anon/publishable key in the frontend. Keep privileged server-side keys on the backend only.
- Rotate credentials immediately if they are exposed in a public repository, logs, screenshots, or chat.
- Configure Supabase Row Level Security and verify that users can access only their own analysis records.
- Resumes contain personal information. Review data retention, logging, and hosting policies before uploading real candidate documents.
- Automated skill validation is based on resume text and embeddings; it is not proof of a person's actual proficiency.

## ⚠️ Limitations and responsible use

- The score is a project-specific estimate, not an official score from a company's ATS.
- Groq extraction may omit or misinterpret information; review the extracted details and recommendations.
- Semantic similarity measures textual relatedness, not verified ability.
- Results depend on document extraction quality and the completeness of the supplied job description.
- NLP and embedding models load during backend startup, which can increase memory use and cold-start time.
- Persistent history depends on a correctly configured Supabase schema and access policies.
- The notebooks are experimentation assets; they are not automatically part of the production inference pipeline.

## 📜 License

No `LICENSE` file is included in this repository at the time this README was prepared. Until a license is added, do not assume the code is licensed for reuse, redistribution, or commercial use.

---

<div align="center">

### ⭐ If you find this project interesting, consider starring the repository!

**Explore the code · Try the live app · Share your feedback**

<a href="https://atsscorerapp-bn6rwhcjax6iwts4vax8ss.streamlit.app/">
  <img src="https://img.shields.io/badge/Launch_ResumeAnalyzer_AI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Launch ResumeAnalyzer AI">
</a>

<br><br>

<sub>Built with Python, NLP, machine learning, and a focus on practical resume feedback.</sub>

</div>
