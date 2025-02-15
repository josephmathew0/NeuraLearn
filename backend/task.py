from app import app  
from models import db, Question

with app.app_context():
    db.session.query(Question).delete()  # ✅ Clear old questions

    questions = [
        Question(
            question_type="sql",
            content="Write a query to select all products with price greater than 100.",
            correct_answer='["SELECT * FROM products WHERE price > 100"]',
            options="SELECT,*,FROM,products,WHERE,price,>,100"
        )

    ]

    db.session.add_all(questions)
    db.session.commit()

    print("✅ Questions added successfully!")
