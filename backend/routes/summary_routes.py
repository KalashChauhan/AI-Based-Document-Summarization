import time
from flask import Blueprint, current_app, jsonify, request
from services.preprocessing_service import clean_text, word_count
from services.document_service import extract_text
from utils.file_validator import validate_file
from models.database import create_record

summary_bp=Blueprint('summary',__name__)

def response(text, filename, file_type, length):
    if len(text)>current_app.config['MAX_TEXT_CHARS']: raise ValueError('Text is too large. Please upload less than 500,000 characters.')
    start=time.perf_counter(); summary=current_app.extensions['summarizer'].summarize(text,length); elapsed=round(time.perf_counter()-start,2)
    words=word_count(text); summary_words=word_count(summary)
    summary_id,document_id=create_record(filename,file_type,len(text),summary,length,words,summary_words,elapsed)
    return jsonify(success=True,id=summary_id,document_id=document_id,filename=filename,summary=summary,word_count=words,summary_word_count=summary_words,processing_time=elapsed)

@summary_bp.post('/summarize')
def summarize_file():
    try:
        filename, extension=validate_file(request.files.get('file'),current_app.config['ALLOWED_EXTENSIONS'])
        text=extract_text(request.files['file'].stream,extension)
        return response(text,filename,extension,request.form.get('summary_length','medium').lower())
    except ValueError as exc: return jsonify(success=False,error=str(exc)),400
    except Exception:
        current_app.logger.exception('Summarization failed'); return jsonify(success=False,error='Could not generate a summary. Please try again.'),500

@summary_bp.post('/summarize-text')
def summarize_text():
    try:
        data=request.get_json(silent=True) or {}; text=clean_text(data.get('text',''))
        if not text: raise ValueError('Enter text to summarize.')
        return response(text,'Pasted text','text',str(data.get('summary_length','medium')).lower())
    except ValueError as exc: return jsonify(success=False,error=str(exc)),400
    except Exception:
        current_app.logger.exception('Summarization failed'); return jsonify(success=False,error='Could not generate a summary. Please try again.'),500
