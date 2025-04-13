# -----------------------------
# File: backend/app.py
# -----------------------------

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, MCQQuestion, DragDropQuestion, DragDrop100Question, TextAnswerQuestion
from sentence_transformers import SentenceTransformer, util
from transformers import BertTokenizer, BertModel
import torch
import os
import random
import re
from nltk.tokenize import sent_tokenize
import nltk
from nltk.data import find

try:
    find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# ----------------------------
# App Initialization
# ----------------------------

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# ----------------------------
# Configuration
# ----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'neuralearn.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ----------------------------
# Load Models
# ----------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")
bert_model.eval()

# ----------------------------
# Helper Function: Highlight Missing Tokens
# ----------------------------
def highlight_missing_tokens(correct, user):
    correct_tokens = bert_tokenizer.tokenize(correct)
    user_tokens = bert_tokenizer.tokenize(user)

    with torch.no_grad():
        correct_ids = torch.tensor([bert_tokenizer.convert_tokens_to_ids(correct_tokens)])
        user_ids = torch.tensor([bert_tokenizer.convert_tokens_to_ids(user_tokens)])

        correct_embeds = bert_model(correct_ids)[0][0]
        user_embeds = bert_model(user_ids)[0][0]

    highlighted = []
    for i, c_embed in enumerate(correct_embeds):
        sim = torch.nn.functional.cosine_similarity(c_embed.unsqueeze(0), user_embeds).max().item()
        word = correct_tokens[i]
        if sim < 0.8:
            highlighted.append(f"<strong>{word}</strong>")
        else:
            highlighted.append(word)

    final = []
    for token in highlighted:
        if token.startswith("##") and final:
            final[-1] += token[2:]
        else:
            final.append(token)

    return " ".join(final)

# ----------------------------
# Sample Route
# ----------------------------
@app.route('/')
def index():
    return jsonify({'message': '🚀 NeuraLearn Backend is running!'})

# ----------------------------
# API: MCQ
# ----------------------------
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

# ----------------------------
# API: Drag and Drop
# ----------------------------
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

# ----------------------------
# API: Text Answer Question
# ----------------------------
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

# ----------------------------
# API: Evaluate Text Answer
# ----------------------------
# ----------------------------
# API: Evaluate Text Answer (Sentence-level BERT-based)
# ----------------------------
# @app.route("/api/evaluate_text", methods=["POST"])
# def evaluate_text():
#     try:
#         data = request.json
#         student_answer = data.get("user_answer", "").strip()
#         correct_answer = data.get("correct_answer", "").strip()

#         print("📨 Evaluation Request Received")
#         print("User Answer:", repr(student_answer))
#         print("Correct Answer:", repr(correct_answer))

#         if not student_answer or not correct_answer:
#             return jsonify({"error": "Empty input received"}), 400

#         # Similarity score using sentence-transformer
#         score = util.cos_sim(model.encode(student_answer), model.encode(correct_answer)).item()

#         # Sentence-level highlighting using BERT
#         correct_sents = sent_tokenize(correct_answer)
#         student_embedding = model.encode(student_answer)

#         highlighted = []
#         for sent in correct_sents:
#             sent_embedding = model.encode(sent)
#             sim = util.cos_sim(sent_embedding, student_embedding).item()
#             if sim < 0.75:
#                 highlighted.append(f"<strong>{sent}</strong>")
#             else:
#                 highlighted.append(sent)
#         final_feedback = " ".join(highlighted)

#         # Score level
#         if score > 0.95:
#             level = "🌟 Excellent"
#         elif score > 0.85:
#             level = "👍 Good"
#         elif score > 0.65:
#             level = "⚠️ Needs Improvement"
#         else:
#             level = "❌ Try again"

#         return jsonify({
#             "score": round(score, 2),
#             "level": level,
#             "highlighted_answer": final_feedback
#         })

#     except Exception as e:
#         print("❌ Evaluation Error:", e)
#         return jsonify({"error": "Internal Server Error"}), 500

@app.route("/api/evaluate_text", methods=["POST"])
def evaluate_text():
    try:
        data = request.json
        student_answer = data.get("user_answer", "").strip()
        correct_answer = data.get("correct_answer", "").strip()

        print("📨 Evaluation Request Received")
        print("User Answer:", repr(student_answer))
        print("Correct Answer:", repr(correct_answer))

        if not student_answer or not correct_answer:
            return jsonify({"error": "Empty input received"}), 400

        # Compute main similarity score safely
        try:
            sim_score = util.cos_sim(model.encode(student_answer), model.encode(correct_answer)).item()
        except Exception as e:
            print("⚠️ Similarity score error:", e)
            sim_score = 0.0

        # Sentence-level feedback
        correct_sents = sent_tokenize(correct_answer)
        student_emb = model.encode(student_answer)

        highlighted = []
        for sent in correct_sents:
            sent = sent.strip()
            if not sent:
                continue

            try:
                sim = util.cos_sim(model.encode(sent), student_emb).item()
            except Exception as e:
                print(f"⚠️ Could not compare sentence: {sent}", e)
                sim = 0.0

            # Only bold if NOT present and NOT semantically close
            if sent.lower() not in student_answer.lower() and sim < 0.75:
                highlighted.append(f"<strong>{sent}</strong>")
            else:
                highlighted.append(sent)

        final_feedback = " ".join(highlighted)

        # Score level
        if sim_score > 0.95:
            level = "🌟 Excellent"
        elif sim_score > 0.85:
            level = "👍 Good"
        elif sim_score > 0.65:
            level = "⚠️ Needs Improvement"
        else:
            level = "❌ Try again"

        return jsonify({
            "score": round(sim_score, 2),
            "level": level,
            "highlighted_answer": final_feedback
        })

    except Exception as e:
        print("❌ Evaluation Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500



# ----------------------------
# Main Entry
# ----------------------------
if __name__ == '__main__':
    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
