# -----------------------------
# File: backend/app.py
# -----------------------------

from flask import Flask, jsonify
from flask_cors import CORS
from models import db, MCQQuestion
import os
from models import DragDropQuestion
import random
import ast 

app = Flask(__name__)
CORS(app)  # Allow cross-origin (frontend can talk to backend)

# ----------------------------
# Configuration
# ----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'neuralearn.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ----------------------------
# Initialize DB
# ----------------------------
db.init_app(app)

# ----------------------------
# Sample Route (Test)
# ----------------------------
@app.route('/')
def index():
    return jsonify({'message': '🚀 NeuraLearn Backend is running!'})

# ----------------------------
# API Route to Get a Random MCQ
# ----------------------------
@app.route('/api/mcq')
def get_mcq():
    mcq = MCQQuestion.query.order_by(db.func.random()).first()
    if not mcq:
        return jsonify({'error': 'No questions found'}), 404
    return jsonify({
        'id': mcq.id,
        'question': mcq.question,
        'correct_answer': mcq.correct_answer,
        'options': [mcq.correct_answer, mcq.distractor1, mcq.distractor2, mcq.distractor3],
        'explanation': mcq.explanation,
        'topic': mcq.topic
    })

# ----------------------------
# API Route to Get a Random DRAG & DROP
# ----------------------------

# import ast  # 👈 Add this at the top

# @app.route('/api/drag')
# def get_drag_question():
#     total = DragDropQuestion.query.count()
#     if total == 0:
#         return jsonify({"error": "No drag-and-drop questions found"}), 404

#     random_index = random.randint(0, total - 1)
#     question = DragDropQuestion.query.offset(random_index).first()

#     # try:
#     #     draggables = ast.literal_eval(question.draggables) if isinstance(question.draggables, str) else question.draggables
#     # except Exception:
#     #     draggables = []

#     return jsonify({
#         "id": question.id,
#         "question": question.question,
#         "full_answer": question.full_answer,
#         "drag_question": question.drag_question,
#         "correct_answer": question.correct_answer,
#         "draggables": question.draggables
#     })

from models import DragDrop100Question

@app.route('/api/drag')
def get_drag_question():
    total = DragDrop100Question.query.count()
    if total == 0:
        return jsonify({"error": "No questions found"}), 404

    random_index = random.randint(0, total - 1)
    question = DragDrop100Question.query.offset(random_index).first()

    return jsonify({
        "id": question.id,
        "question": question.question,
        "full_answer": question.full_answer,
        "drag_question": question.drag_question,
        "correct_answer": question.correct_answer,
        "draggables": question.draggables  # will be split in frontend
    })


# ----------------------------
# Main Entry Point
# ----------------------------
if __name__ == '__main__':
    # Ensure instance directory exists
    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
