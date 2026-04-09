import sys
sys.path.insert(0, "app")
from scorer import score_resume, rank_candidates

def test_perfect_match():
    resume = "skilled in python, sql, and docker"
    job    = "requires python, sql, docker"
    result = score_resume(resume, job)
    assert result["match_score"] == 100.0
    assert result["missing_skills"] == []

def test_partial_match():
    resume = "knows python and flask"
    job    = "needs python, sql, docker, flask"
    result = score_resume(resume, job)
    assert result["match_score"] == 50.0
    assert "sql" in result["missing_skills"]
    assert "docker" in result["missing_skills"]

def test_no_match():
    resume = "marketing and sales background"
    job    = "python, machine learning, docker"
    result = score_resume(resume, job)
    assert result["match_score"] == 0.0

def test_ranking_order():
    candidates = [
        {"name": "Alice", "match_score": 75},
        {"name": "Bob",   "match_score": 92},
        {"name": "Carol", "match_score": 60}
    ]
    ranked = rank_candidates(candidates)
    assert ranked[0]["name"] == "Bob"
    assert ranked[1]["name"] == "Alice"
    assert ranked[2]["name"] == "Carol"
    assert ranked[0]["rank"] == 1