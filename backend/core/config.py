import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    _ENV_PATH = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(_ENV_PATH)
except ImportError:
    pass
APP_TITLE = "ATS RESUME ANALYSER API"
APP_VERSION="1.0.0"
APP_DESCRIPTION="Analyse the resume again the job description with NLP and ML."
ALLOWED_ORIGINS=[
    'https://atsscorerapp-bn6rwhcjax6iwts4vax8ss.streamlit.app',
]
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
SUPPORTED_FILE_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}
SPACY_MODEL_PRIMARY="en_core_web_md"
SPACY_MODEL_SECONDARY="en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL="sentence-transformers/all-MiniLM-L6-v2"
# Fine-tuned resume <-> job description model (jupyter_notebooks/03_BERT_FINE_TUNING.ipynb),
# hosted on the Hugging Face Hub. Used only for the resume vs JD similarity score, the task
# it was trained on. Leave empty to use SENTENCE_TRANSFORMER_MODEL for that score too.
# If the Hub repo is private, also set HF_TOKEN (read access) in the environment.
JD_MATCH_MODEL = os.getenv("JD_MATCH_MODEL", "").strip()
SCORE_WEIGHTS = {
    "formatting": 20,
    "content": 25,
    "keywords": 25,
    "skill_validation": 15,
    "ats_compatibility": 15}
JD_KEYWORDS_WEIGHT = 0.6
JD_SEMANTIC_WEIGHT = 0.4
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")