import threading
from transformers import pipeline
from .preprocessing_service import word_count
from utils.text_chunker import chunk_text

LENGTHS = {'short': (25, 75), 'medium': (60, 150), 'detailed': (120, 260)}

class SummarizationService:
    def __init__(self, model_name): self.model_name=model_name; self._pipeline=None; self._lock=threading.Lock()
    def load(self):
        if self._pipeline is None:
            with self._lock:
                if self._pipeline is None:
                    # Force PyTorch so Transformers does not attempt to initialize TensorFlow too.
                    self._pipeline=pipeline('summarization', model=self.model_name, device=-1, framework='pt')
    def _summarize_piece(self, text, length):
        words=word_count(text)
        if words < 18: return text
        min_len,max_len=LENGTHS[length]
        max_len=min(max_len, max(20, int(words * .8)))
        min_len=min(min_len, max_len-5)
        model_input = f'summarize: {text}' if 't5' in self.model_name.lower() else text
        result=self._pipeline(model_input, min_length=max(5,min_len), max_length=max_len, do_sample=False, truncation=True)
        return result[0]['summary_text'].strip()
    def summarize(self, text, length='medium'):
        if length not in LENGTHS: raise ValueError('summary_length must be short, medium, or detailed.')
        self.load(); chunks=chunk_text(text)
        summaries=[self._summarize_piece(chunk,length) for chunk in chunks]
        combined=' '.join(summaries)
        if len(summaries)>1 and word_count(combined)>350:
            combined=self._summarize_piece(combined, length)
        return combined
