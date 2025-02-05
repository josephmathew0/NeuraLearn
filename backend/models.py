from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=True)  # Comma-separated MCQ options

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    correctness = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("responses", lazy=True))
    question = db.relationship("Question", backref=db.backref("responses", lazy=True))

class Misconception(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    pattern = db.Column(db.Text, nullable=False)  # Common incorrect answer pattern
    feedback = db.Column(db.Text, nullable=False)  # Explanation for correction
