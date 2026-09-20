# Test report

Run on 2026-09-14 with Python 3.13 and `python -m pytest -q`.

| Area | Result | Coverage |
|---|---:|---|
| Health API | Pass | `/api/health` contract |
| Raw text | Pass | Summary creation, validation and SQLite persistence |
| TXT upload | Pass | Extraction and endpoint response |
| DOCX upload | Pass | Paragraph extraction and endpoint response |
| PDF upload | Pass | Text-bearing PDF extraction and endpoint response |
| Validation | Pass | Empty text and unsupported extension |
| History | Pass | List, detail and delete endpoints |
| Chunking | Pass | Long input yields multiple chunks |

**Result:** 5 passed in 24.59 seconds. A pre-existing Python environment warning reports an incompatible `requests`/`urllib3` combination; it did not affect execution. The production React build completed successfully with Vite.
