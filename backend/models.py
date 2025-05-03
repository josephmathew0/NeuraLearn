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


# ----------------------------
# SHORT ANSWER MODEL 
# ----------------------------

class TextAnswerQuestion(db.Model):
    __tablename__ = 'text_answer_question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)



# ----------------------------
# DTD QUESTION
# ----------------------------

class DTDQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    initial_lines = db.Column(db.PickleType, nullable=False)
    correct_lines = db.Column(db.PickleType, nullable=False)


# ----------------------------
# SQL MCQ
# ----------------------------
class SQLMCQStructured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String, nullable=False)
    distractor1 = db.Column(db.String, nullable=False)
    distractor2 = db.Column(db.String, nullable=False)
    distractor3 = db.Column(db.String, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    topic = db.Column(db.String, nullable=False)        # e.g., 'joins', 'group_by'
    topic_order = db.Column(db.Integer, nullable=False) # e.g., 1 for basics, 2 for WHERE


# ----------------------------
# SQL DRAG & DROP
# ----------------------------
class SQLDragDrop(db.Model):
    __tablename__ = 'sql_dragdrop'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    correct_answer = db.Column(db.String, nullable=False)
    draggables = db.Column(db.Text, nullable=False)  # Stored as JSON string
    topic = db.Column(db.String, nullable=False)
    topic_order = db.Column(db.Integer, nullable=False)


# ----------------------------
# SQL TEXT ANSWER
# ----------------------------
class SQLTextAnswerQuestion(db.Model):
    __tablename__ = 'sql_textanswer'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    topic_order = db.Column(db.Integer, nullable=False)



