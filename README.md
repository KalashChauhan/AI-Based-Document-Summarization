# AI-Based Document Summarizer

A AI-Based web application that summarizes PDF, DOCX, TXT, and pasted text with a locally run Hugging Face model. It does not use paid or hosted LLM APIs.

## Features

- Safe PDF, DOCX and TXT extraction with size/extension validation
- Text cleanup, sentence-aware long-document chunking, and hierarchical summarization
- Short, medium and detailed output settings
- Flask REST API, SQLite-backed summary history, copy/download actions, and responsive React UI
- Error responses for empty, invalid, damaged, oversized, and unsupported inputs

## Architecture and schema

See [architecture.md](documentation/architecture.md).

## Project layout

```
backend/       Flask API, NLP services, SQLite, tests, evaluation
frontend/      Vite React application
documentation/ architecture diagrams and workflow
```
