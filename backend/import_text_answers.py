import pandas as pd
from models import db, TextAnswerQuestion
from app import app

df = pd.read_csv("text_answer_100.csv")  # Replace with actual path

with app.app_context():
    db.drop_all()
    db.create_all()

    for _, row in df.iterrows():
        q = TextAnswerQuestion(
            question=row["question"].strip(),
            answer=row["answer"].strip()
        )
        db.session.add(q)

    db.session.commit()
    print(f"✅ Imported {len(df)} text answer questions.")
