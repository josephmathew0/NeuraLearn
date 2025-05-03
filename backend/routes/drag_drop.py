# backend/routes/drag_drop.py

from flask import Blueprint, jsonify
import pandas as pd
import random
import os

drag_drop_bp = Blueprint('drag_drop', __name__)

# Path to your dataset
CSV_PATH = os.path.join("files", "train_drag_and_drop_ready.csv")

# Load once at startup
drag_data = pd.read_csv(CSV_PATH)

@drag_drop_bp.route("/api/drag", methods=["GET"])
def get_drag_question():
    row = drag_data.sample(1).iloc[0]
    draggables = eval(row["draggables"]) if isinstance(row["draggables"], str) else row["draggables"]
    return jsonify({
        "question": row["question"],
        "refined_support": row["refined_support"],
        "draggables": draggables
    })
