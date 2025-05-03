# File: seed_textanswer_biology.py
import pandas as pd
from models import db, TextAnswerQuestion
from app import app

# Load the dataset
df = pd.read_csv("text_answer_100.csv")  # Replace with actual path

with app.app_context():
    # ✅ Only clear the relevant table — not the whole DB
    TextAnswerQuestion.query.delete()
    db.session.commit()

    for _, row in df.iterrows():
        q = TextAnswerQuestion(
            question=row["question"].strip(),
            answer=row["answer"].strip()
        )
        db.session.add(q)

    db.session.commit()
    print(f"✅ Imported {len(df)} Biology text answer questions.")
