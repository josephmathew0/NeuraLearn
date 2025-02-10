from app import app  # Import Flask app instance
from models import db, Question, Feedback

# ✅ Ensure we're running inside the Flask app context
with app.app_context():
    # ✅ Add a sample MCQ question
    q1 = Question(
        question_type="MCQ",
        content="What is the primary key in SQL?",
        correct_answer='["id"]',
        options="id,name,email"
    )

    # ✅ Add a sample SQL validation question
    q2 = Question(
        question_type="sql",
        content="Write a query to select all columns from the 'users' table.",
        correct_answer='["SELECT * FROM users;"]',
        options=None
    )

    db.session.add(q1)
    db.session.add(q2)
    db.session.commit()

    print("✅ Sample questions added!")

    # ✅ Add feedback for Misconception 2
    feedback_entry = Feedback(
        misconception_id=2,  # Ensure this ID exists in the database
        message="Avoid redundant conditions in WHERE clauses.",
        weight=0.8
    )

    db.session.add(feedback_entry)
    db.session.commit()

    print("✅ Feedback for misconception 2 added!")
