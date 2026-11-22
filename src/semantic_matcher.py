from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .preprocessing import normalize_text


@lru_cache(maxsize=1)
def _load_sentence_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2"), "sentence-transformers"
    except Exception:
        return None, "tfidf-fallback"


def calculate_semantic_similarity(resume_text: str, job_text: str) -> dict:
    if not resume_text or not job_text:
        return {"score": 0.0, "method": "none", "explanation": "Insufficient text for semantic matching."}

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)
    matrix = vectorizer.fit_transform([normalize_text(resume_text), normalize_text(job_text)])
    tfidf_score = float(cosine_similarity(matrix[0], matrix[1])[0][0] * 100)

    model, method = _load_sentence_model()
    if model is None:
        return {
            "score": round(tfidf_score, 2),
            "method": method,
            "explanation": "Sentence Transformers is unavailable; TF-IDF cosine similarity is used instead.",
        }

    embeddings = model.encode([resume_text[:8000], job_text[:8000]], show_progress_bar=False)
    semantic_score = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0] * 100)
    combined = 0.55 * semantic_score + 0.45 * tfidf_score
    return {
        "score": round(max(0.0, min(combined, 100.0)), 2),
        "semantic_score": round(max(0.0, semantic_score), 2),
        "tfidf_score": round(tfidf_score, 2),
        "method": method,
        "explanation": "Combined score: 55% Sentence Transformers similarity + 45% TF-IDF cosine similarity.",
    }
