from src.preprocessing import clean_text, normalize_text, tokenize


def test_clean_text():
    assert clean_text("  Python   developer\nSQL  ") == "Python developer SQL"


def test_normalize_text():
    normalized = normalize_text("Developing Python applications")
    assert "develop" in normalized
    assert "python" in normalized


def test_tokenize_filters_stop_words():
    tokens = tokenize("Python and SQL for data analysis")
    assert "and" not in tokens
    assert "python" in tokens
