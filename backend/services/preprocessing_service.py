import re
from collections import Counter

def clean_text(text):
    text = text.replace('\x00', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def word_count(text): return len(re.findall(r'\b\w+\b', text))

def has_meaningful_content(text):
    """Reject repeated-character noise and text made mostly of one repeated token."""
    alphanumeric = re.findall(r"[\w]+", text.casefold(), flags=re.UNICODE)
    if not alphanumeric:
        return False

    compact = re.sub(r"\s+", "", text)
    if len(compact) >= 8 and len(set(compact.casefold())) <= 2:
        return False

    counts = Counter(alphanumeric)
    token_count = len(alphanumeric)
    if token_count >= 5 and counts.most_common(1)[0][1] / token_count >= 0.8:
        return False

    return any(len(token) > 1 for token in alphanumeric)

def clean_summary(text):
    """Tidy common spacing and casing artifacts from extracted/model text."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,;:])(?=\S)", r"\1 ", text)
    text = re.sub(r"([.!?])(?=[A-Za-z])", r"\1 ", text)
    text = re.sub(r"([.!?])\s+([a-z])", lambda m: m.group(1) + " " + m.group(2).upper(), text)
    return text
