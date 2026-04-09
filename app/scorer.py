from parser import extract_skills_from_text

SKILL_LIBRARY = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "html", "css", "react", "vue", "angular", "nodejs",
    "flask", "django", "fastapi", "spring boot",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn", "opencv",
    "docker", "kubernetes", "jenkins", "github actions", "ci/cd",
    "aws", "azure", "gcp", "linux", "bash",
    "git", "rest api", "graphql", "microservices", "devops",
    "agile", "scrum", "jira"
]

def score_resume(resume_text: str, job_description: str) -> dict:
    job_skills    = extract_skills_from_text(job_description.lower(), SKILL_LIBRARY)
    resume_skills = extract_skills_from_text(resume_text, SKILL_LIBRARY)

    if not job_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "total_required": 0,
            "error": "No recognizable skills found in job description"
        }

    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    score   = round((len(matched) / len(job_skills)) * 100, 1)

    return {
        "match_score":    score,
        "matched_skills": matched,
        "missing_skills": missing,
        "total_required": len(job_skills)
    }

def rank_candidates(candidates: list) -> list:
    ranked = sorted(candidates, key=lambda x: x.get("match_score", 0), reverse=True)
    for i, c in enumerate(ranked):
        c["rank"] = i + 1
    return ranked