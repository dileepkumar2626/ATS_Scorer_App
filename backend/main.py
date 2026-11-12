import logging
from contextlib import asynccontextmanager, contextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import (
    ALLOWED_ORIGINS,
    APP_TITLE,
    APP_VERSION,
    APP_DESCRIPTION,
    SPACY_MODEL_PRIMARY,
    SPACY_MODEL_SECONDARY,
    SENTENCE_TRANSFORMER_MODEL,)
from backend.api.routes import router
logger = logging.getLogger("ATS_Resume_Scorer")
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ATS Resume Analyser..")
    logger.info(f"Loading spaCy NLP Model:{SPACY_MODEL_PRIMARY}")
    import spacy
    try:
        app.state.nlp=spacy.load(SPACY_MODEL_PRIMARY)
        logger.info(f"spaCy NLP Model:{SPACY_MODEL_PRIMARY} loaded successfully")
    except OSError:
        logger.warning(f"spaCy NLP Model:{SPACY_MODEL_PRIMARY} not found, falling back to:{SPACY_MODEL_SECONDARY}")
        app.state.nlp=spacy.load(SPACY_MODEL_SECONDARY)
        logger.info(f"spaCy NLP Model:{SPACY_MODEL_SECONDARY} (fallback) loaded successfully")
    logger.info(f"Loading Sentence Transformer Model:{SENTENCE_TRANSFORMER_MODEL}")
    from sentence_transformers import SentenceTransformer
    try:
        app.state.embedder=SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
        logger.info(f"Sentence Transformer Model:{SENTENCE_TRANSFORMER_MODEL} loaded successfully")
    except Exception as e:
        logger.error(f"Error loading Sentence Transformer Model:{SENTENCE_TRANSFORMER_MODEL}: {e}")
        raise e
    logger.info("All models loaded successfully, ATS Resume Analyser is ready to serve requests.")
    yield
    logger.info("Shutting down the api ...")
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
@app.get("/health")
async def health_check():
    return {
        "name": "ATS Resume Analyser API",
        "version": '1.0.0',
        "endpoints": {
            "POST/api/v1/analyse-resume": "Analyse the resume against the job description and return a score and feedback.",
            "GET/api/v1/history": "Get User's analysis history.",
            "DELETE/api/v1/history/:id": "Delete a specific analysis history by ID.",
            "GET/api/v1/health": "Check the health of the API.",
            "POST/api/v1/Generate-pdf": "Generate a PDF report of the analysis results.",
        }

    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)