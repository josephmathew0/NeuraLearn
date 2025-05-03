# -----------------------------
# File: backend/seed_sqlmcq.py
# -----------------------------
import os
from flask import Flask
from models import db, SQLMCQStructured

# Setup Flask app context
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'neuralearn.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

sample_questions = [
    {
        "question": "What does SELECT * FROM Students return?",
        "correct_answer": "All rows and columns in Students",
        "distractor1": "Only the first row",
        "distractor2": "Only the column names",
        "distractor3": "Only the primary key values",
        "explanation": "SELECT * returns all rows and columns.",
        "topic": "sql_basics",
        "topic_order": 1
    },
    {
        "question": "Which keyword is used to fetch data from a table?",
        "correct_answer": "SELECT",
        "distractor1": "FETCH",
        "distractor2": "RETRIEVE",
        "distractor3": "GET",
        "explanation": "SELECT is the standard SQL keyword to fetch data.",
        "topic": "sql_basics",
        "topic_order": 1
    },
    {
        "question": "Which clause specifies the table to query from?",
        "correct_answer": "FROM",
        "distractor1": "WHERE",
        "distractor2": "TABLE",
        "distractor3": "INTO",
        "explanation": "The FROM clause specifies the source table.",
        "topic": "sql_basics",
        "topic_order": 1
    }
]

with app.app_context():
    db.create_all()

    # 🧹 Clear existing records first
    SQLMCQStructured.query.delete()
    db.session.commit()

    # 🚀 Insert new records
    for q in sample_questions:
        entry = SQLMCQStructured(**q)
        db.session.add(entry)

    db.session.commit()
    print("✅ SQLMCQStructured table cleared and seeded.")
