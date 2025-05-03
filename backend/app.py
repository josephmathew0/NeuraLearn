# -----------------------------
# File: backend/app.py (Optimized)
# -----------------------------
# Adding comment to test
import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import torch
import os
import json
import random
import re
from nltk.tokenize import sent_tokenize
import nltk
from nltk.data import find
from models import db, MCQQuestion, DragDropQuestion, DragDrop100Question, TextAnswerQuestion, SQLMCQStructured, SQLDragDrop, SQLTextAnswerQuestion, DTDQuestion
from sqlalchemy import func
from socket_server import socketio, register_socket_events, get_lobby_players
from difflib import SequenceMatcher

# ----------------------------
# App Initialization
# ----------------------------

app = Flask(__name__)
CORS(app)

# ----------------------------
# Configuration
# ----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
nltk.data.path.append(os.path.join(BASE_DIR, 'nltk_data'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'neuralearn.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH + '?check_same_thread=False'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': None  # Disable pooling to avoid threading issues
    }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ----------------------------
# Load Models
# ----------------------------
model = SentenceTransformer(os.path.join(BASE_DIR, 'models', 'all-MiniLM-L6-v2'))

# Ensure NLTK tokenizer is available from local folder (for Render)
try:
    find('tokenizers/punkt')
except LookupError:
    print("⚠️ NLTK punkt tokenizer not found in bundled directory.")


# ----------------------------
# Routes
# ----------------------------
@app.route('/')
def index():
    return jsonify({'message': '🚀 NeuraLearn Backend is running!'})

@app.route('/api/mcq')
def get_mcq():
    mcq = MCQQuestion.query.order_by(db.func.random()).first()
    if not mcq:
        return jsonify({'error': 'No MCQ found'}), 404
    return jsonify({
        'id': mcq.id,
        'question': mcq.question,
        'correct_answer': mcq.correct_answer,
        'options': [mcq.correct_answer, mcq.distractor1, mcq.distractor2, mcq.distractor3],
        'explanation': mcq.explanation,
        'topic': mcq.topic
    })

@app.route('/api/drag')
def get_drag():
    total = DragDrop100Question.query.count()
    if total == 0:
        return jsonify({'error': 'No drag-and-drop questions'}), 404
    question = DragDrop100Question.query.offset(random.randint(0, total - 1)).first()
    return jsonify({
        "id": question.id,
        "question": question.question,
        "full_answer": question.full_answer,
        "drag_question": question.drag_question,
        "correct_answer": question.correct_answer,
        "draggables": question.draggables
    })

@app.route('/api/text')
def get_text():
    total = TextAnswerQuestion.query.count()
    if total == 0:
        return jsonify({'error': 'No text answer questions'}), 404
    q = TextAnswerQuestion.query.offset(random.randint(0, total - 1)).first()
    return jsonify({
        "id": q.id,
        "question": q.question,
        "answer": q.answer
    })

@app.route("/api/evaluate_text", methods=["POST"])
def evaluate_text():
    try:
        data = request.json
        student_answer = data.get("user_answer", "").strip()
        correct_answer = data.get("correct_answer", "").strip()

        if not student_answer or not correct_answer:
            return jsonify({"error": "Empty input received"}), 400

        score = util.cos_sim(model.encode(student_answer), model.encode(correct_answer)).item()
        correct_sents = sent_tokenize(correct_answer)
        student_embedding = model.encode(student_answer)

        highlighted = []
        for sent in correct_sents:
            sent_embedding = model.encode(sent)
            sim = util.cos_sim(sent_embedding, student_embedding).item()
            if sim < 0.75:
                highlighted.append(f"<strong>{sent}</strong>")
            else:
                highlighted.append(sent)
        final_feedback = " ".join(highlighted)

        if score > 0.95:
            level = "🌟 Excellent"
        elif score > 0.85:
            level = "👍 Good"
        elif score > 0.65:
            level = "⚠️ Needs Improvement"
        else:
            level = "❌ Try again"

        return jsonify({
            "score": round(score, 2),
            "level": level,
            "highlighted_answer": final_feedback
        })

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/api/dtd/<int:qid>")
def get_dtd_question(qid):
    question = DTDQuestion.query.get(qid)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify({
        "id": question.id,
        "prompt": question.prompt,
        "initial_lines": question.initial_lines,
        "correct_lines": question.correct_lines,
    })

@app.route("/api/debug/dtd")
def debug_dtd():
    questions = DTDQuestion.query.all()
    return jsonify([{ "id": q.id, "prompt": q.prompt, "initial_lines": q.initial_lines, "correct_lines": q.correct_lines } for q in questions])

@app.route("/api/sqlmcq/structured/<int:topic_order>")
def get_structured_sql_mcqs(topic_order):
    questions = SQLMCQStructured.query.filter_by(topic_order=topic_order).all()
    if not questions:
        return jsonify({"error": "No questions found for this topic"}), 404
    return jsonify([{ "id": q.id, "question": q.question, "correct_answer": q.correct_answer, "distractor1": q.distractor1, "distractor2": q.distractor2, "distractor3": q.distractor3, "explanation": q.explanation, "topic": q.topic, "topic_order": q.topic_order } for q in questions])

@app.route("/api/sqlmcq/structured")
def get_all_structured_sql_mcqs():
    questions = SQLMCQStructured.query.order_by(SQLMCQStructured.topic_order, SQLMCQStructured.id).all()
    return jsonify([{ "id": q.id, "question": q.question, "correct_answer": q.correct_answer, "options": [q.correct_answer, q.distractor1, q.distractor2, q.distractor3], "explanation": q.explanation, "topic": q.topic, "topic_order": q.topic_order } for q in questions])

@app.route("/api/sql/dragdrop")
def get_random_sql_dragdrop():
    question = SQLDragDrop.query.order_by(func.random()).first()
    return jsonify({ "id": question.id, "question": question.question, "correct_answer": question.correct_answer, "draggables": json.loads(question.draggables), "topic": question.topic, "topic_order": question.topic_order })

@app.route("/api/sql/dragdrop/all")
def get_all_sql_dragdrop():
    questions = SQLDragDrop.query.order_by(SQLDragDrop.topic_order).all()
    return jsonify([{ "id": q.id, "question": q.question, "correct_answer": q.correct_answer, "draggables": json.loads(q.draggables), "topic": q.topic, "topic_order": q.topic_order } for q in questions])

@app.route('/api/sql/dragdrop/<int:question_id>')
def get_sql_dragdrop_by_id(question_id):
    question = SQLDragDrop.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify({ "id": question.id, "question": question.question, "correct_answer": question.correct_answer, "draggables": json.loads(question.draggables), "topic": question.topic, "topic_order": question.topic_order })

@app.route("/api/debug/sqltext")
def debug_sql_text_questions():
    questions = SQLTextAnswerQuestion.query.all()
    return jsonify([{ "question": q.question, "correct_answer": q.correct_answer, "topic": q.topic, "topic_order": q.topic_order } for q in questions])

@app.route("/api/sql/textanswer")
def get_sql_text_answer():
    question = SQLTextAnswerQuestion.query.order_by(db.func.random()).first()
    return jsonify({ "question": question.question, "correct_answer": question.correct_answer, "topic": question.topic, "topic_order": question.topic_order })

@app.route("/api/sql/evaluate_text", methods=["POST"])
def evaluate_sql_text():
    data = request.get_json()
    user_answer = data["user_answer"]
    correct_answer = data["correct_answer"]

    model_score = util.cos_sim(model.encode(user_answer), model.encode(correct_answer)).item()
    user_tokens = set(user_answer.lower().split())
    correct_tokens = set(correct_answer.lower().split())
    token_score = len(user_tokens & correct_tokens) / len(correct_tokens)
    final_score = max(model_score, token_score)

    if final_score >= 0.95:
        feedback = "Excellent! You've nailed it."
    elif final_score >= 0.85:
        feedback = "Good job! You’re almost there."
    elif final_score >= 0.7:
        feedback = "Fair attempt. Try to include more keywords."
    else:
        feedback = "Your answer misses key concepts. Review the topic and try again."

    highlighted = " ".join([f"<span style='color:red; font-weight:bold'>{word}</span>" if word not in user_tokens else word for word in correct_answer.split()])

    return jsonify({
        "model_score": model_score,
        "token_score": token_score,
        "score": final_score,
        "feedback": feedback,
        "highlighted_answer": highlighted
    })

@app.route("/api/lobby")
def get_lobby():
    players = get_lobby_players()
    return jsonify({ "players": players })

if __name__ == '__main__':
    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
    register_socket_events(app)
    socketio.init_app(app, cors_allowed_origins=[
        "http://localhost:5173",
        "http://10.0.0.165:5173",
        "https://neuralearn-one.vercel.app"
    ])
    socketio.run(app, host='0.0.0.0', port=5000)

