from io import BytesIO
from pypdf import PdfReader
from docx import Document
from .preprocessing_service import clean_text

def extract_text(stream, file_type):
    try:
        if file_type == 'txt':
            raw = stream.read(); text = raw.decode('utf-8', errors='replace')
        elif file_type == 'pdf':
            reader = PdfReader(BytesIO(stream.read()))
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        elif file_type == 'docx':
            document = Document(BytesIO(stream.read()))
            text = '\n'.join(p.text for p in document.paragraphs)
        else: raise ValueError('Unsupported file type.')
    except ValueError: raise
    except Exception as exc: raise ValueError(f'Unable to read this {file_type.upper()} file. It may be corrupted.') from exc
    text = clean_text(text)
    if not text: raise ValueError('No readable text was found in this document.')
    return text
