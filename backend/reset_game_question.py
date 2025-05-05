from app import app
from models import db, GameQuestion

with app.app_context():
    GameQuestion.__table__.drop(db.engine)  # 🔥 Only drops GameQuestion
    GameQuestion.__table__.create(db.engine)  # ✅ Recreate it with new structure
    print("✅ Dropped and recreated GameQuestion table.")
