import re

def chunk_text(text, max_words=650, tokenizer=None, max_tokens=450):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks=[]; current=[]; size=0

    def token_size(value):
        if tokenizer is None:
            return len(value.split())
        return len(tokenizer.encode(value, add_special_tokens=True))

    for sentence in sentences:
        words=sentence.split()
        if not words: continue
        if tokenizer is not None and token_size(sentence) > max_tokens:
            if current: chunks.append(' '.join(current)); current=[]; size=0
            # A single unusually long sentence still needs splitting by model tokens.
            token_ids=tokenizer.encode(sentence, add_special_tokens=False)
            chunks.extend(tokenizer.decode(token_ids[i:i+max_tokens], skip_special_tokens=True)
                          for i in range(0,len(token_ids),max_tokens))
            continue
        sentence_size = token_size(sentence) if tokenizer is not None else len(words)
        over_limit = (size + sentence_size > max_tokens) if tokenizer is not None else (size + len(words) > max_words)
        if current and over_limit:
            chunks.append(' '.join(current)); current=[]; size=0
        current.append(sentence); size+=sentence_size
    if current: chunks.append(' '.join(current))
    return chunks
