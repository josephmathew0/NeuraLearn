# import_clean_dragdrop.py

import pandas as pd
import ast
from models import db, DragDropQuestion
from app import app

df = pd.read_csv('final_dragdrop_dataset_clean.csv')

def parse_draggables(cell):
    try:
        # Convert string representation of list into actual list
        return ','.join(ast.literal_eval(cell))
    except:
        # If parsing fails, fall back to split and strip
        return ','.join([x.strip() for x in cell.strip("[]").replace("'", "").split(",") if x.strip()])

with app.app_context():
    # Delete existing data
    DragDropQuestion.query.delete()
    db.session.commit()

    for _, row in df.iterrows():
        draggables_clean = parse_draggables(row['draggables'])

        q = DragDropQuestion(
            question=row['question'],
            full_answer=row['full_answer'],
            drag_question=row['drag_question'],
            correct_answer=row['correct_answer'],
            draggables=draggables_clean
        )
        db.session.add(q)

    db.session.commit()
    print(f"✅ Reimported {len(df)} drag-and-drop questions successfully.")
