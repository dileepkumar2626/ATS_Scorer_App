
import logging
import httpx
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
logger=logging.getLogger("ATS_Resume_Scorer")
from backend.core.config import (
    SUPABASE_URL,
    SUPABASE_KEY,)
def _get_header():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
async def save_analysis(user_id: str, filename:str,analysis_result:Dict) -> Optional[str]:
    headers = _get_header()
    if not headers:
        logger.error("Supabase headers are not set. Please check your configuration.")
        return None
    def _json_default(o):
        if hasattr(o, 'model_dump'):
            return o.model_dump()
        return str(o)
    serializable_result=json.loads(json.dumps(analysis_result,default=_json_default))
    doc={
        "user_id":user_id,
        "filename":filename,
        "ats_score":serializable_result.get("ats_score",0),
        "keyword_match":serializable_result.get("keyword_match",0),
        "missing_keywords":serializable_result.get("missing_keywords",[]),
        "analysis_result":serializable_result
    }
    url=f"{SUPABASE_URL.rstrip("/")}/rest/v1/analysis"
    try:
        async with httpx.AsyncClient() as client:
            response=await client.post(url,headers=headers,json=doc)
            response.raise_for_status()
            data=response.json()
            if data and len(data)>0:
                inserted_id=str(data[0].get("id"))
                logger.info(f"Saved analysis for user {user_id}: {inserted_id}")
                return inserted_id
            return None
    except Exception as exc:
        logger.error(f"Failed to save analysis to supabase: {exc}")
        return None