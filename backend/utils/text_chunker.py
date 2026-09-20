import re

def chunk_text(text, max_words=650):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks=[]; current=[]; size=0
    for sentence in sentences:
        words=sentence.split()
        if not words: continue
        if len(words)>max_words:
            if current: chunks.append(' '.join(current)); current=[]; size=0
            chunks.extend(' '.join(words[i:i+max_words]) for i in range(0,len(words),max_words)); continue
        if current and size+len(words)>max_words:
            chunks.append(' '.join(current)); current=[]; size=0
        current.append(sentence); size+=len(words)
    if current: chunks.append(' '.join(current))
    return chunks
