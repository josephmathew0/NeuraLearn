# -----------------------------
# File: models.py
# -----------------------------
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ----------------------------
# USER MODEL
# ----------------------------
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)  # Nullable for OAuth users
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



# ----------------------------
# MURDER MYSTERY GAME
# ----------------------------
class GameQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer_query = db.Column(db.Text, nullable=False)
    hint = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)  # 'player' or 'murderer'
    question_order = db.Column(db.Integer, nullable=False)  # instead of 'number'



# ----------------------------
# PLAYER TABLE (for Mystery Game)
# ----------------------------
class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    character = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Player {self.username} - {self.character} ({self.role})>"



