import io
import zipfile
import PyPDF2
import pdfplumber
from docx import Document
from typing import Tuple,Optional
from backend.utils.file_utils import (
    FileParsingError,
    TextExtractionError,
    FileUploadError,
    log_error,
    log_info,
    log_warning,
    with_fallback,
)
from backend.core.config import (
    MAX_FILE_SIZE_MB,
    MAX_FILE_SIZE_BYTES,
    SUPPORTED_FILE_TYPES,
)

class FileValidationError(Exception):
    pass


def _detect_mime_type(file: bytes) -> str:
    head = file[:8]
    if b"%PDF-" in file[:1024]:
        return "application/pdf"
    if head.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(io.BytesIO(file)) as zf:
                if "word/document.xml" in zf.namelist():
                    return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        except zipfile.BadZipFile:
            pass
        return "application/zip"
    if head == b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1":
        return "application/msword"
    return "application/octet-stream"


def validate_file(file: bytes, filename: str) -> Tuple[bool, str, Optional[str]]:
    file_size = len(file)
    if file_size > MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.",None
    if file_size == 0:
        return False, "File is empty...please check that the file is uploaded correctly.",None
    try:
        mime_type = _detect_mime_type(file)
    except Exception as e:
        return False, f"Error determining file type: {e}",None
    if mime_type not in SUPPORTED_FILE_TYPES:
        return False, f"Unsupported file type: {mime_type}. Supported types are: {', '.join(SUPPORTED_FILE_TYPES.keys())}",None
    return True, "",SUPPORTED_FILE_TYPES[mime_type]
def _extract_hyperlinks_from_pdf(pdf_file:bytes) -> str:
    hyperlinks = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_file)) as pdf:
            for page in pdf.pages:
                for annot in page.annots:
                    if "/Annots" not in page:
                        continue
                    for annot in page["/Annots"]:
                        try:
                            annot=annot.get_object()
                            if annot.get("/Subtype") != "/Link":
                                continue
                            uri = annot.get("/A", {}).get("/URI")
                            if uri and isinstance(uri,(str,bytes)):
                                if isinstance(uri,bytes):
                                    uri=uri.decode("utf-8",errors="ignore")
                                uri=uri.strip()
                                if uri.startswith("http://") or uri.startswith("https://"):
                                    hyperlinks.append(uri)
                        except Exception:
                            pass
    except Exception:
        pass
    return "\n".join(hyperlinks)
def _extract_text_with_pdfplumber(pdf_file: bytes) -> str:
    text=""
    with pdfplumber.open(io.BytesIO(pdf_file)) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text+=page_text+"\n"
    if not text.strip():
        raise TextExtractionError("No text found in the PDF file using pdfplumber.",user_message="The PDF file may be scanned or image-based. Please convert it to a text-based PDF or use a different file format.")
    hyperlinks=_extract_hyperlinks_from_pdf(pdf_file)
    if hyperlinks:
        text=text.strip()+"\n" +hyperlinks
    return text.strip()
def _extract_text_with_pypdf2(pdf_file: bytes) -> str:
    text=""
    pdf_reader=PyPDF2.PdfReader(io.BytesIO(pdf_file))
    for page in pdf_reader.pages:
        page_text=page.extract_text()
        if page_text:
            text+=page_text+"\n"
    if not text.strip():
        raise TextExtractionError("No text found in the PDF file using PyPDF2.",user_message="The PDF file may be scanned or image-based. Please convert it to a text-based PDF or use a different file format.")
    hyperlinks=_extract_hyperlinks_from_pdf(pdf_file)
    if hyperlinks:
        text=text.strip()+"\n" +hyperlinks
    return text.strip()
def extract_text_from_pdf(pdf_file: bytes) -> str:
    try:
        result,used_fallback=with_fallback(_extract_text_with_pdfplumber,
                                           _extract_text_with_pypdf2, pdf_file, log_fallback=True)
        if used_fallback:
            log_info("Fallback to PyPDF2 for text extraction from PDF.",context="Resume Ananlyser")
        return result
    except Exception as e:
        log_error(f"Error extracting text from PDF: {e}",context="Resume Analyser")
        raise FileParsingError(f"Error extracting text from PDF: {e}") from e
def extract_text_from_docx(docx_file: bytes) -> str:
    try:
        doc=Document(io.BytesIO(docx_file))
        text_parts=[]
        for para in doc.paragraphs:
            text_parts.append(para.text)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text_parts.append(cell.text)
        text="\n".join(text_parts)
        if not text.strip():
            raise FileParsingError("No text found in the DOCX file.")
        try:
            for rel in doc.rels.values():
                if "hyperlink" in rel.reltype.lower():
                    url=rel._target
                    if isinstance(url, str) and url.startswith("http"):
                        text+="\n"+url
        except Exception:
            pass
        log_info("Successfully extracted text from DOCX file.",context="Resume Analyser")
        return text.strip()
    except FileParsingError:
        raise 
    except Exception  as e:
        log_error(f"Error extracting text from DOCX: {e}",context="Resume Analyser")
        raise FileParsingError(f"Error extracting text from DOCX: {e}") from e
def extract_text_from_doc(file: bytes) -> str:
    raise FileParsingError("DOC file format is not supported for text extraction. Please convert the file to DOCX or PDF format.")
def extract_text(file: bytes, file_type: str) -> str:
    if file_type == "pdf":
        return extract_text_from_pdf(file)
    elif file_type == "docx":
        return extract_text_from_docx(file)
    elif file_type == "doc":
        return extract_text_from_doc(file)
    else:
        raise FileParsingError(f"Unsupported file type for text extraction: {file_type}, supported types are: pdf, docx, doc.")
def parse_resume(file: bytes, filename: str) -> Tuple[str, dict]:
    log_info(f"Starting parsing of resume file: {filename}",context="Resume Analyser")
    try:
        is_valid, error_message,file_type = validate_file(file, filename)
        if not is_valid:
            log_warning(f"File validation failed for {filename}: {error_message}",context="Resume Analyser")
            raise FileValidationError(error_message)
    except FileValidationError as e:
        raise 
    except Exception as e:
        log_error(f"Error during file validation for {filename}: {e}",context="Resume Analyser")
        raise FileValidationError(f"Error during file validation: {e}") from e
    try:
        text=extract_text(file, file_type)
        log_info(f"Successfully extracted text from resume file: {filename}",context="Resume Analyser")
    except FileParsingError as e:
        raise
    except Exception as e:
        log_error(f"Error during text extraction for {filename}: {e}",context="Resume Analyser")
        raise FileParsingError(f"Error during text extraction: {e}") from e
    metadata={
        "filename": filename,
        "file_type": file_type,
        "file_size_bytes": len(file),
        "text_length": len(text),
        "success": True,
    }
    return text,metadata