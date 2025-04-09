import pandas as pd
from models import db, DragDrop100Question
from app import app

df = pd.read_csv("dragdrop_100.csv")

with app.app_context():
    # Optional: Clear previous data
    DragDrop100Question.query.delete()
    db.session.commit()

    # Insert new entries
    for _, row in df.iterrows():
        q = DragDrop100Question(
            question=row['question'],
            full_answer=row['full_answer'],
            drag_question=row['drag_question'],
            correct_answer=row['correct_answer'],
            draggables=row['draggables']
        )
        db.session.add(q)

    db.session.commit()
    print(f"✅ Successfully imported {len(df)} DragDrop100 questions.")
