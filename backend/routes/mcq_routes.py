# File: routes/mcq_routes.py

from flask import Blueprint, jsonify, request
from models import db, MCQQuestion, UserResponse, User
import random

mcq_bp = Blueprint('mcq', __name__)

# ----------------------------
# GET: Fetch Random MCQ
# ----------------------------
@mcq_bp.route('/api/mcq/random', methods=['GET'])
def get_random_mcq():
    mcq = MCQQuestion.query.order_by(db.func.random()).first()
    if not mcq:
        return jsonify({'error': 'No MCQs available'}), 404

    options = [
        mcq.correct_answer,
        mcq.distractor1,
        mcq.distractor2,
        mcq.distractor3
    ]
    random.shuffle(options)

    return jsonify({
        'id': mcq.id,
        'question': mcq.question,
        'options': options
    })

# ----------------------------
# POST: Submit Answer
# ----------------------------
@mcq_bp.route('/api/mcq/<int:mcq_id>/answer', methods=['POST'])
def submit_answer(mcq_id):
    data = request.json
    selected_answer = data.get('answer')
    user_id = data.get('user_id')

    mcq = MCQQuestion.query.get(mcq_id)
    if not mcq:
        return jsonify({'error': 'MCQ not found'}), 404

    is_correct = selected_answer.strip().lower() == mcq.correct_answer.strip().lower()

    response = UserResponse(
        user_id=user_id,
        mcq_id=mcq_id,
        selected_answer=selected_answer,
        is_correct=is_correct
    )
    db.session.add(response)
    db.session.commit()

    return jsonify({
        'is_correct': is_correct,
        'explanation': mcq.explanation,
        'correct_answer': mcq.correct_answer
    })
