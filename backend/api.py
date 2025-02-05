from flask import Blueprint, jsonify, request
from models import db, User, Question, Response, Misconception
from flask_cors import cross_origin

api = Blueprint("api", __name__)

# ✅ 1️⃣ Get All Questions (This was missing)
@api.route("/api/questions", methods=["GET"])
@cross_origin()  # ✅ Allow CORS for frontend access
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


# ✅ 2️⃣ Submit a User Response (Already exists)
@api.route("/api/responses", methods=["POST"])
@cross_origin()
def submit_response():
    data = request.json
    user_id = data.get("user_id")
    question_id = data.get("question_id")
    answer = data.get("answer").strip().lower()

    # ✅ 1️⃣ Get the correct answer
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    # ✅ 2️⃣ Check correctness
    correctness = (answer == question.correct_answer.strip().lower())

    # ✅ 3️⃣ If incorrect, check for misconceptions
    feedback_message = "❌ Incorrect! Try again."
    if not correctness:
        misconception = Misconception.query.filter(
            Misconception.question_id == question_id,
            Misconception.pattern.ilike(answer)  # ✅ Fix: Case-insensitive match
        ).first()
        if misconception:
            feedback_message = f"❌ Incorrect! {misconception.feedback}"

    # ✅ 4️⃣ Store response
    response = Response(user_id=user_id, question_id=question_id, answer=answer, correctness=correctness)
    db.session.add(response)
    db.session.commit()

    return jsonify({
        "correct": correctness,
        "message": "Response recorded!",
        "feedback": "✅ Correct!" if correctness else feedback_message
    })

