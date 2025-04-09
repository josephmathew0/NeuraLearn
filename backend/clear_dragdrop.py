# clear_dragdrop.py
from app import app
from models import db, DragDropQuestion

with app.app_context():
    num_deleted = db.session.query(DragDropQuestion).delete()
    db.session.commit()
    print(f"🗑️ Deleted {num_deleted} existing drag-and-drop questions.")
