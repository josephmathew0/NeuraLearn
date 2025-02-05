from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db  # ✅ Import the global `db` instance

app = Flask(__name__)
app.config.from_object('config.Config')

# ✅ Initialize db with Flask app
db.init_app(app)

# ✅ Enable CORS (allows React to access Flask API)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ✅ Import API AFTER initializing Flask & db to avoid circular imports
from api import api
app.register_blueprint(api)

# ✅ Ensure tables are created inside app context
with app.app_context():
    db.create_all()  # ✅ This makes sure tables are created before inserting data

@app.route('/')
def home():
    return jsonify({"message": "Welcome to NeuraLearn Backend!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
