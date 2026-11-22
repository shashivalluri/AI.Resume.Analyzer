import re
from pathlib import Path

SKILL_CATALOG = {
    "Programming Languages": {
        "Python": ["python", "python programming", "python3"],
        "Java": ["java", "java programming"],
        "JavaScript": ["javascript", "js"],
        "TypeScript": ["typescript"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "c sharp"],
        "Go": [r"\bgo\b", "golang"],
        "SQL": ["sql"],
        "R": [r"\br\b"],
    },
    "Frameworks": {
        "Django": ["django"], "Flask": ["flask"], "FastAPI": ["fastapi"],
        "React": ["react", "reactjs", "react.js"], "Angular": ["angular"],
        "Vue.js": ["vue", "vue.js", "vuejs"], "Spring": ["spring", "spring boot"],
        "Streamlit": ["streamlit"], "TensorFlow": ["tensorflow", "tf"],
        "PyTorch": ["pytorch"], "Scikit-learn": ["scikit-learn", "sklearn"],
    },
    "Databases": {
        "MySQL": ["mysql"], "PostgreSQL": ["postgresql", "postgres"],
        "MongoDB": ["mongodb", "mongo db"], "SQLite": ["sqlite"],
        "Redis": ["redis"], "Oracle": ["oracle database", "oracle"],
    },
    "Data Science": {
        "Pandas": ["pandas"], "NumPy": ["numpy", "num py"],
        "Data Analysis": ["data analysis", "data analytics"],
        "Statistical Analysis": ["statistical analysis", "statistics"],
        "Data Visualization": ["data visualization", "tableau", "power bi"],
    },
    "Machine Learning": {
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning", "neural network", "neural networks"],
        "NLP": ["natural language processing", "nlp"],
        "Computer Vision": ["computer vision", "opencv"],
    },
    "Artificial Intelligence": {
        "Artificial Intelligence": ["artificial intelligence", "ai"],
        "Generative AI": ["generative ai", "genai", "llm", "large language models"],
        "Prompt Engineering": ["prompt engineering"],
    },
    "Cloud Technologies": {
        "AWS": ["aws", "amazon web services"], "Azure": ["azure", "microsoft azure"],
        "Google Cloud": ["google cloud", "gcp"], "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
    },
    "Developer Tools": {
        "Git": ["git", "github", "gitlab"], "Linux": ["linux", "unix"],
        "REST APIs": ["rest api", "restful api", "rest apis"],
        "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
        "Jupyter": ["jupyter", "jupyter notebook"],
    },
    "Soft Skills": {
        "Communication": ["communication", "communication skills"],
        "Teamwork": ["teamwork", "team collaboration", "collaboration"],
        "Leadership": ["leadership", "people management"],
        "Problem Solving": ["problem solving", "problem-solving"],
        "Time Management": ["time management"],
    },
}


def _has_phrase(text: str, phrase: str) -> bool:
    if phrase.startswith(r"\b"):
        return re.search(phrase, text, flags=re.IGNORECASE) is not None
    pattern = r"(?<![A-Za-z0-9+#])" + re.escape(phrase) + r"(?![A-Za-z0-9+#])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text: str) -> dict:
    if not text:
        return {"skills": [], "categories": {}, "evidence": {}}
    normalized = text.lower()
    found = []
    categories = {}
    evidence = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for category, catalog_skills in SKILL_CATALOG.items():
        category_skills = []
        for canonical, variants in catalog_skills.items():
            if any(_has_phrase(normalized, variant) for variant in variants):
                if canonical not in found:
                    found.append(canonical)
                category_skills.append(canonical)
                snippets = []
                for line in lines:
                    if any(_has_phrase(line.lower(), variant) for variant in variants):
                        snippets.append(line[:220])
                        if len(snippets) >= 3:
                            break
                evidence[canonical] = snippets
        if category_skills:
            categories[category] = category_skills
    return {"skills": found, "categories": categories, "evidence": evidence}
