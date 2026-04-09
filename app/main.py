from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from parser import extract_text_from_pdf
from scorer import score_resume, rank_candidates

app = Flask(__name__)
CORS(app)  # allows the HTML frontend to call the API

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Resume screener is running"})

@app.route("/screen", methods=["POST"])
def screen_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
    if "job_description" not in request.form:
        return jsonify({"error": "No job description provided"}), 400

    resume_file = request.files["resume"]
    job_desc    = request.form["job_description"]

    if not resume_file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        resume_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        resume_text = extract_text_from_pdf(tmp_path)
        result      = score_resume(resume_text, job_desc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp_path)

@app.route("/rank", methods=["POST"])
def rank():
    data = request.get_json()
    if not data or "candidates" not in data:
        return jsonify({"error": "Provide a candidates list"}), 400
    ranked = rank_candidates(data["candidates"])
    return jsonify(ranked)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)