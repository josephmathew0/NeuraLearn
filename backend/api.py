import random
import json
from flask import Blueprint, jsonify, request
from models import db, User, Question, Response, Misconception
from flask_cors import cross_origin
from flask_sql_validator_api import SQLValidator  # ✅ Import the class, not the function
from utils import check_similarity, find_misconception, select_feedback  # Import similarity & feedback functions

api = Blueprint("api", __name__)

@api.route("/api/questions", methods=["GET"])
@cross_origin()
def get_questions():
    questions = Question.query.all()
    return jsonify([
        {
            "id": q.id,
            "type": q.question_type,
            "content": q.content,
            "correct_answer": q.correct_answer,
            "options": q.options.split(",") if q.options else []
        }
        for q in questions
    ])

@api.route("/api/responses", methods=["POST"])
@cross_origin()
def submit_response():
    data = request.json
    user_id = data.get("user_id")
    question_id = data.get("question_id")
    answer = data.get("answer").strip().lower()

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    correct_answers = [ans.strip().lower() for ans in json.loads(question.correct_answer)]
    
    similarity_score = check_similarity(answer, correct_answers)
    if similarity_score >= 0.8:
        correctness = True
        feedback_message = "✅ Correct!"
    else:
        correctness = False

        misconception = find_misconception(answer, question_id)
        print("🔍 Debug: Found Misconception:", misconception)  # ✅ Debug output

        feedback_message = select_feedback(misconception)
        print("🔍 Debug: Selected Feedback:", feedback_message)  # ✅ Debug output

    response = Response(user_id=user_id, question_id=question_id, answer=answer, correctness=correctness)
    db.session.add(response)
    db.session.commit()

    print("🔍 Debug: Final API Response:", {
    "correct": correctness,
    "message": "Response recorded!",
    "feedback": feedback_message
    })

    return jsonify({
        "correct": correctness,
        "message": "Response recorded!",
        "feedback": feedback_message
    })

@api.route("/api/validate_sql", methods=["POST"])
@cross_origin()
def validate_sql_query():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No SQL query provided"}), 400

    validator = SQLValidator(query)
    validation_results = validator.validate()

    return jsonify({"query": query, "validation": validation_results})


@api.route('/api/misconceptions', methods=['GET'])  # ✅ Add /api prefix
def get_misconceptions():
    misconceptions = Misconception.query.all()
    return jsonify([m.to_dict() for m in misconceptions])
