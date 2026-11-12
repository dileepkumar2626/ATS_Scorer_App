import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    _ENV_PATH = Path(__file__).parent.parent / ".env"
    load_dotenv(_ENV_PATH)
except ImportError:
    pass
APP_TITLE = "ATS RESUME ANALYSER API"
APP_VERSION="1.0.0"
APP_DESCRIPTION="Analyse the resume again the job description with NLP and ML."
ALLOWED_ORIGINS=[
    "www.google.com",
]
MAX_FILE_SIZE = 5
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
SUPPORTED_FILE_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}
SPACY_MODEL_PRIMARY="en_core_web_sm"
SPACY_MODEL_SECONDARY="en_core_web_md"
SENTENCE_TRANSFORMER_MODEL="sentence-transformers/all-MiniLM-L6-v2"
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