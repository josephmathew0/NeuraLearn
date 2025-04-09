# -----------------------------
# File: import_mcqs.py
# -----------------------------
import pandas as pd
from app import app
from models import db, MCQQuestion

# Path to your cleaned CSV
CSV_PATH = 'clean_mcq_dataset.csv'

# Load the data
df = pd.read_csv(CSV_PATH)

# Insert into database
with app.app_context():
    for _, row in df.iterrows():
        mcq = MCQQuestion(
            question=row['question'],
            correct_answer=row['correct_answer'],
            distractor1=row['distractor1'],
            distractor2=row['distractor2'],
            distractor3=row['distractor3'],
            explanation=row.get('explanation', ''),
            topic=None  # You can later populate this via topic tagging logic
        )
        db.session.add(mcq)

    db.session.commit()
    print(f"✅ Inserted {len(df)} MCQs into the database.")
