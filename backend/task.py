from app import app  
from models import db, Question

with app.app_context():
    db.session.query(Question).delete()  # ✅ Clear old questions

    questions = [
        Question(
            question_type="MCQ",
            content="What is the primary key in SQL?",
            correct_answer='["id"]',
            options="id,name,email"
        ),
        Question(
            question_type="sql",
            content="Write a query to select all columns from the 'users' table.",
            correct_answer='["SELECT * FROM users;"]',
            options="SELECT,*,FROM,users,WHERE,id,>,100,;"  # ✅ Store Drag-and-Drop SQL elements
        ),
        Question(
            question_type="text",
            content="What is normalization in databases?",
            correct_answer='["Normalization is the process of organizing a database to reduce redundancy."]',
            options=None  # ✅ No options for text input
        )
    ]

    db.session.add_all(questions)
    db.session.commit()

    print("✅ Questions added successfully!")
