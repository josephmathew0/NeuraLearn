from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # ✅ Import Flask-Migrate
from models import db  # ✅ Import the global `db` instance
from api import api  # ✅ Ensure API is imported
from flask_sql_validator_api import validate_sql  # ✅ Import the SQL validator


app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neuralearn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize db with Flask app
db.init_app(app)
migrate = Migrate(app, db)  # ✅ Initialize Flask-Migrate

# ✅ Enable CORS (allows React to access Flask API)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ✅ Import API AFTER initializing Flask & db to avoid circular imports
app.register_blueprint(api)

# ✅ Ensure tables are created inside app context
with app.app_context():
    db.create_all()  # ✅ This makes sure tables are created before inserting data

@app.route('/')
def home():
    return jsonify({"message": "Welcome to NeuraLearn Backend!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
