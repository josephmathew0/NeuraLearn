# -----------------------------
# File: models.py
# -----------------------------
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ----------------------------
# USER MODEL
# ----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    responses = db.relationship('UserResponse', backref='user', lazy=True)


# ----------------------------
# MCQ QUESTION MODEL
# ----------------------------
class MCQQuestion(db.Model):
    __tablename__ = 'mcq_question'  # 👈 Ensures proper table name

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(256), nullable=False)
    distractor1 = db.Column(db.String(256), nullable=False)
    distractor2 = db.Column(db.String(256), nullable=False)
    distractor3 = db.Column(db.String(256), nullable=False)
    explanation = db.Column(db.Text)
    topic = db.Column(db.String(128), nullable=True)

    responses = db.relationship('UserResponse', backref='mcq', lazy=True)


# ----------------------------
# USER RESPONSE MODEL
# ----------------------------
class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mcq_id = db.Column(db.Integer, db.ForeignKey('mcq_question.id'), nullable=False)
    selected_answer = db.Column(db.String(256))
    is_correct = db.Column(db.Boolean)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)


# ----------------------------
# DRAG & DROP QUESTION MODEL
# ----------------------------
class DragDropQuestion(db.Model):
    __tablename__ = 'dragdrop_question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)  # sentence with blanks
    full_answer = db.Column(db.Text, nullable=False)  # original sentence
    drag_question = db.Column(db.Text, nullable=False)  # sentence with ___
    correct_answer = db.Column(db.Text, nullable=False)  # list of words (joined)
    draggables = db.Column(db.Text, nullable=False)  # comma-separated draggables


# ----------------------------
# DRAG & DROP QUESTION MODEL 100
# ----------------------------

class DragDrop100Question(db.Model):
    __tablename__ = 'dragdrop100_question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    full_answer = db.Column(db.Text, nullable=False)
    drag_question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    draggables = db.Column(db.Text, nullable=False)  # Stored as comma-separated
