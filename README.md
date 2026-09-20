# AI-Based Document Summarizer

A B.Tech CSE academic web application that summarizes PDF, DOCX, TXT, and pasted text with a locally run Hugging Face model. It does not use paid or hosted LLM APIs.

## Features

- Safe PDF, DOCX and TXT extraction with size/extension validation
- Text cleanup, sentence-aware long-document chunking, and hierarchical summarization
- Short, medium and detailed output settings
- Flask REST API, SQLite-backed summary history, copy/download actions, and responsive React UI
- Error responses for empty, invalid, damaged, oversized, and unsupported inputs

## Model and methodology

The default `google-t5/t5-small` is a compact, open-source T5 transformer (about 60M parameters). It is a practical CPU-compatible choice for student laptops and supports local abstractive summarization without paid APIs. The model name is configurable with `SUMMARIZATION_MODEL`. The service is created once per Flask application and loads its pipeline once on first use, avoiding repeated model downloads/initialization. Long input is split at sentence boundaries, each chunk is summarized, then lengthy combined summaries are summarized again.

## Architecture and schema

See [architecture.md](documentation/architecture.md). SQLite stores `documents(id, filename, file_type, original_text_length, uploaded_at)` and `summaries(id, document_id, summary, summary_length, original_word_count, summary_word_count, processing_time, created_at)`.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend status |
| POST | `/api/summarize` | Multipart `file`, `summary_length` |
| POST | `/api/summarize-text` | JSON `text`, `summary_length` |
| GET | `/api/history` | All saved summaries |
| GET/DELETE | `/api/history/:id` | Read/delete one summary |

## Run locally

Backend (Python 3.10+):

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The first summarization downloads the open-source model once. Start the frontend in another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Optionally copy `backend/.env.example` to `backend/.env` and set environment variables in your shell. Vite defaults to `http://localhost:5173`; Flask is at `http://localhost:5000`.

## Tests and evaluation

```powershell
cd backend
pytest -q
python evaluate.py --source source.txt --summary generated.txt --reference reference.txt
```

Tests cover health, text/TXT/DOCX handling, invalid input, history/delete, and chunking. `evaluate.py` reports ROUGE-1, ROUGE-2, ROUGE-L F1 plus word counts and compression. Use a genuine human reference summary; no accuracy figure is claimed without measurement.

## Limitations and future scope

CPU inference may be slow on very long documents, scanned PDFs need OCR (not included), and abstractive models can occasionally omit or rephrase details. Future work: OCR, language detection/multilingual models, user accounts, background jobs, and human feedback evaluation.

## Team contribution mapping

1. AI/NLP + backend: summarization service and REST application.
2. Document processing & input: validators, extractors, preprocessing.
3. Frontend & UI/UX: React pages and responsive components.
4. Database & history: SQLite model and history endpoints.
5. Testing, evaluation & documentation: test suite, ROUGE script, diagrams and reports.

## Project layout

```
backend/       Flask API, NLP services, SQLite, tests, evaluation
frontend/      Vite React application
documentation/ architecture diagrams and workflow
```
