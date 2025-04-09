import pandas as pd
from app import app
from models import db, DragDropQuestion

df = pd.read_csv('dragdrop_final.csv')

with app.app_context():
    db.drop_all()
    db.create_all()

    for _, row in df.iterrows():
        question = DragDropQuestion(
            question=row['question'],
            drag_question=row['drag_question'],
            full_answer=row['full_answer'],
            correct_answer=row['correct_answer'],
            draggables=row['draggables']  # already comma-separated
        )
        db.session.add(question)

    db.session.commit()
    print(f"✅ Imported {len(df)} drag-and-drop questions.")
