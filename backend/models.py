from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=True)  # Comma-separated MCQ options

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    correctness = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("responses", lazy=True))
    question = db.relationship("Question", backref=db.backref("responses", lazy=True))

class Misconception(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    pattern = db.Column(db.String(255), nullable=False)  # Stores common error
    feedback = db.Column(db.String(500), nullable=False)  # Explanation for misconception
    weight = db.Column(db.Float, default=1.0)  # ✅ Probability weight for how common the mistake is
    occurrences = db.Column(db.Integer, default=1)  # ✅ Track total times misconception was observed

    def to_dict(self):
        """Convert Misconception object to JSON-serializable format."""
        return {
            "id": self.id,
            "question_id": self.question_id,
            "pattern": self.pattern,
            "feedback": self.feedback,
            "weight": self.weight,
            "occurrences": self.occurrences
        }

    def update_weight(self, increase=True):
        """Dynamically update misconception weight using Bayesian update."""
        if increase:
            self.weight = (self.weight * self.occurrences + 1) / (self.occurrences + 1)
            self.occurrences += 1  # ✅ Track misconception frequency
        else:
            self.weight = max(1.0, self.weight - 0.5)  # Prevent weight from going too low
        db.session.commit()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    misconception_id = db.Column(db.Integer, db.ForeignKey('misconception.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    weight = db.Column(db.Float, default=1.0)  # ✅ Adaptive feedback weight
    occurrences = db.Column(db.Integer, default=1)  # ✅ Track how often this feedback is used

    def update_weight(self):
        """Bayesian update for feedback weights."""
        self.weight = (self.weight * self.occurrences + 1) / (self.occurrences + 1)
        self.occurrences += 1
        db.session.commit()
