import io
import os
import sys
import tempfile
from docx import Document
from pypdf import PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from utils.text_chunker import chunk_text

class FakeSummarizer:
    def summarize(self,text,length): return 'A concise test summary of the supplied document.'

def app():
    fd,path=tempfile.mkstemp(); os.close(fd)
    application=create_app({'TESTING':True,'DATABASE':path})
    application.extensions['summarizer']=FakeSummarizer()
    yield application
    os.unlink(path)

def test_health():
    application=next(app()); client=application.test_client()
    assert client.get('/api/health').status_code==200

def test_text_history_and_delete():
    application=next(app()); client=application.test_client()
    result=client.post('/api/summarize-text',json={'text':'This is enough text to test the complete summarization endpoint and database storage behavior. It contains several words for validation.','summary_length':'medium'})
    assert result.status_code==200; item_id=result.json['id']
    assert len(client.get('/api/history').json['items'])==1
    assert client.get(f'/api/history/{item_id}').status_code==200
    assert client.delete(f'/api/history/{item_id}').status_code==200

def test_txt_and_validation():
    application=next(app()); client=application.test_client()
    ok=client.post('/api/summarize',data={'file':(io.BytesIO(b'A valid text document contains enough text for a concise test summary.'),'note.txt'),'summary_length':'short'})
    assert ok.status_code==200
    assert client.post('/api/summarize-text',json={'text':''}).status_code==400
    assert client.post('/api/summarize',data={'file':(io.BytesIO(b'x'),'bad.exe')}).status_code==400

def test_docx_and_chunking():
    application=next(app()); client=application.test_client(); buffer=io.BytesIO(); document=Document(); document.add_paragraph('A DOCX document has readable text that can be summarized during this test.'); document.save(buffer); buffer.seek(0)
    assert client.post('/api/summarize',data={'file':(buffer,'test.docx')}).status_code==200
    assert len(chunk_text(' '.join(['Sentence one.']*1000),20))>1

def test_pdf_upload():
    application=next(app()); client=application.test_client(); writer=PdfWriter(); page=writer.add_blank_page(width=612,height=792)
    font=DictionaryObject({NameObject('/F1'):DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})})
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):font}); stream=DecodedStreamObject(); stream.set_data(b'BT /F1 12 Tf 72 720 Td (A valid PDF document includes text for this endpoint test.) Tj ET'); page[NameObject('/Contents')]=stream
    buffer=io.BytesIO(); writer.write(buffer); buffer.seek(0)
    assert client.post('/api/summarize',data={'file':(buffer,'test.pdf')}).status_code==200
