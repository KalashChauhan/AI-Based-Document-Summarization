import sqlite3
from flask import current_app, g # type: ignore

SCHEMA = '''
CREATE TABLE IF NOT EXISTS documents (
 id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, file_type TEXT NOT NULL,
 original_text_length INTEGER NOT NULL, uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS summaries (
 id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER NOT NULL, summary TEXT NOT NULL,
 summary_length TEXT NOT NULL, original_word_count INTEGER NOT NULL, summary_word_count INTEGER NOT NULL,
 processing_time REAL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
);'''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def close_db(_=None):
    db = g.pop('db', None)
    if db: db.close()

def init_db(app):
    from pathlib import Path
    Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        get_db().executescript(SCHEMA); get_db().commit()

def create_record(filename, file_type, text_length, summary, length, words, summary_words, processing_time):
    db = get_db()
    cursor = db.execute('INSERT INTO documents(filename,file_type,original_text_length) VALUES(?,?,?)', (filename, file_type, text_length))
    document_id = cursor.lastrowid
    summary_id = db.execute('''INSERT INTO summaries(document_id,summary,summary_length,original_word_count,summary_word_count,processing_time)
        VALUES(?,?,?,?,?,?)''', (document_id, summary, length, words, summary_words, processing_time)).lastrowid
    db.commit(); return summary_id, document_id

def list_records():
    return get_db().execute('''SELECT s.*,d.filename,d.file_type,d.uploaded_at FROM summaries s JOIN documents d ON d.id=s.document_id ORDER BY s.created_at DESC''').fetchall()

def get_record(summary_id):
    return get_db().execute('''SELECT s.*,d.filename,d.file_type,d.original_text_length,d.uploaded_at FROM summaries s JOIN documents d ON d.id=s.document_id WHERE s.id=?''', (summary_id,)).fetchone()

def delete_record(summary_id):
    db=get_db(); row=get_record(summary_id)
    if not row: return False
    db.execute('DELETE FROM summaries WHERE id=?',(summary_id,)); 
    db.execute('DELETE FROM documents WHERE id=?',(row['document_id'],)); db.commit(); return True
