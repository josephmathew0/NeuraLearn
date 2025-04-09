import pandas as pd
from app import app
from models import db, MCQQuestion

# Path to your CSV file
CSV_FILE = "clean_mcq_dataset.csv"

def load_questions():
    df = pd.read_csv(CSV_FILE)

    with app.app_context():
        for _, row in df.iterrows():
            question = MCQQuestion(
                question=row['question'],
                correct_answer=row['correct_answer'],
                distractor1=row['distractor1'],
                distractor2=row['distractor2'],
                distractor3=row['distractor3'],
                explanation=row.get('explanation', ''),
                topic=row.get('topic', None)
            )
            db.session.add(question)

        db.session.commit()
        print(f"✅ Loaded {len(df)} questions into the database.")

if __name__ == "__main__":
    load_questions()
