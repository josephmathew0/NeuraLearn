from app import app, db
from models import Question, Misconception

# ✅ Run inside Flask app context
with app.app_context():
    # ✅ 1️⃣ Clear old data
    db.session.query(Misconception).delete()
    db.session.query(Question).delete()
    db.session.commit()

    # ✅ 2️⃣ Insert fresh questions
    questions = [
        Question(question_type="MCQ", content="What is a primary key?", correct_answer="A unique identifier", options="A unique identifier,Foreign Key,Candidate Key"),
        Question(question_type="MCQ", content="What is the default port for PostgreSQL?", correct_answer="5432", options="3306,1521,5432,1433"),
        Question(question_type="Short Answer", content="Define a foreign key.", correct_answer="A reference to a primary key")
    ]

    db.session.add_all(questions)
    db.session.commit()

    # ✅ 3️⃣ Add misconceptions
    misconceptions = [
        Misconception(question_id=1, pattern="Foreign Key", feedback="A foreign key references a primary key but is not the same."),
        Misconception(question_id=1, pattern="Candidate Key", feedback="Candidate keys are unique identifiers, but only one is chosen as the primary key."),
        Misconception(question_id=3, pattern="Unique Key", feedback="A foreign key links two tables but does not enforce uniqueness like a unique key.")
    ]

    db.session.add_all(misconceptions)
    db.session.commit()

    print("✅ Database reset and new misconceptions added!")
