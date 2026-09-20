import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'development-only-change-me')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_BYTES', 10 * 1024 * 1024))
    DATABASE = os.getenv('DATABASE_PATH', str(BASE_DIR / 'database' / 'app.db'))
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
    # T5-small is ~60M parameters: realistic for a typical CPU-only student laptop.
    MODEL_NAME = os.getenv('SUMMARIZATION_MODEL', 'google-t5/t5-small')
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    MAX_TEXT_CHARS = int(os.getenv('MAX_TEXT_CHARS', 500000))
