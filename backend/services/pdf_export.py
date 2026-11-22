import io
import logging
from xhtml2pdf import pisa

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    combined_html = "".join(html_docs.values())
    buffer = io.BytesIO()
    result = pisa.CreatePDF(src=combined_html, dest=buffer)
    if result.err:
        raise RuntimeError(f"PDF generation failed with {result.err} error(s)")
    return buffer.getvalue()
