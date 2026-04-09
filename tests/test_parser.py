import sys
sys.path.insert(0, "app")
from parser import extract_skills_from_text

def test_finds_basic_skills():
    text = "experienced with python and machine learning"
    result = extract_skills_from_text(text, ["python", "java", "machine learning"])
    assert "python" in result
    assert "machine learning" in result
    assert "java" not in result

def test_case_insensitive():
    text = "PYTHON developer with SQL experience"
    result = extract_skills_from_text(text, ["python", "sql"])
    assert "python" in result
    assert "sql" in result

def test_empty_text():
    assert extract_skills_from_text("", ["python"]) == []

def test_no_false_positives():
    text = "i enjoy java coffee and python snakes"
    result = extract_skills_from_text(text, ["java", "python"])
    assert "java" in result
    assert "python" in result