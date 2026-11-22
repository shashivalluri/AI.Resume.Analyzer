import re
from typing import Iterable

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "we", "with",
}


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\s+#.-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    text = clean_text(text).lower()
    tokens = re.findall(r"[a-z0-9+#.]+", text)
    lemmas = [simple_lemma(token) for token in tokens if token not in STOP_WORDS]
    return " ".join(lemmas)


def simple_lemma(token: str) -> str:
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 4 and token.endswith("ing"):
        token = token[:-3]
    elif len(token) > 4 and token.endswith("ed"):
        token = token[:-2]
    elif len(token) > 3 and token.endswith("s"):
        token = token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9+#.]+", normalize_text(text))


def keyword_candidates(text: str, limit: int = 30) -> list[str]:
    counts: dict[str, int] = {}
    for token in tokenize(text):
        if len(token) >= 3:
            counts[token] = counts.get(token, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]


def unique(items: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        value = item.strip()
        key = value.lower()
        if value and key not in seen:
            seen.add(key)
            result.append(value)
    return result
