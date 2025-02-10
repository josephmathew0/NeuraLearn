import random
import sqlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datasketch import MinHash, MinHashLSH
from models import Misconception, Feedback, db

def normalize_sql(query):
    """Standardizes SQL queries for effective similarity matching."""
    parsed = sqlparse.parse(query)
    normalized = " ".join(token.value.upper() for stmt in parsed for token in stmt.tokens if not token.is_whitespace)
    return normalized

def check_similarity(user_answer, correct_answers):
    """Returns the best similarity score between user answer and correct answers."""
    normalized_correct = [normalize_sql(ans) for ans in correct_answers]
    normalized_user = normalize_sql(user_answer)

    all_answers = normalized_correct + [normalized_user]
    vectorizer = TfidfVectorizer().fit_transform(all_answers)
    vectors = vectorizer.toarray()

    # Compute cosine similarity between user response and correct answers
    similarity_matrix = cosine_similarity([vectors[-1]], vectors[:-1])
    return max(similarity_matrix[0])  # Get highest similarity score

def find_misconception(user_answer, question_id):
    """Finds the most probable misconception using Locality-Sensitive Hashing (LSH)."""
    print(f"🔍 Debug: Checking misconceptions for Q{question_id} with answer '{user_answer}'")

    misconceptions = Misconception.query.filter_by(question_id=question_id).all()
    if not misconceptions:
        print("⚠️ No misconceptions found for this question.")
        return None  # No misconception found

    # ✅ Normalize misconceptions (convert to lowercase)
    lsh = MinHashLSH(threshold=0.7, num_perm=128)
    minhashes = {}

    # ✅ Precompute MinHash signatures for misconceptions
    for m in misconceptions:
        mh = MinHash(num_perm=128)
        normalized_pattern = m.pattern.lower().strip()  # ✅ Normalize text

        for word in normalized_pattern.split():
            mh.update(word.encode('utf8'))

        minhashes[m.id] = mh
        lsh.insert(m.id, mh)
        print(f"📌 Debug: Added misconception {m.id} with normalized pattern '{normalized_pattern}' to LSH.")

    # ✅ Normalize user answer
    normalized_user = user_answer.lower().strip()  # ✅ Convert to lowercase
    user_mh = MinHash(num_perm=128)

    for word in normalized_user.split():
        user_mh.update(word.encode('utf8'))

    # ✅ Find the closest misconception using LSH
    closest_match = lsh.query(user_mh)
    print(f"🔎 Debug: LSH found closest match: {closest_match}")

    if closest_match:
        misconception = next(m for m in misconceptions if m.id == closest_match[0])
        misconception.update_weight(increase=True)
        print(f"✅ Debug: Matched misconception {misconception.id}: {misconception.pattern}")
        return misconception

    print("⚠️ No matching misconception found!")
    return None


def select_feedback(misconception):
    """Selects the best feedback dynamically based on misconception frequency."""
    if not misconception:
        print("⚠️ Debug: No misconception found, returning default feedback.")
        return "❌ Incorrect! Try again."

    feedbacks = Feedback.query.filter_by(misconception_id=misconception.id).all()
    print(f"🔍 Debug: Found {len(feedbacks)} feedback entries for misconception {misconception.id}")

    if not feedbacks:
        print("⚠️ No specific feedback found, returning generic message.")
        return "❌ Incorrect! Consider reviewing the concept."

    # ✅ Use Bayesian weighting
    weights = [(f.weight + 1) / (f.occurrences + 2) for f in feedbacks]
    selected_feedback = random.choices(feedbacks, weights=weights, k=1)[0]

    print(f"✅ Debug: Selected feedback '{selected_feedback.message}' for misconception {misconception.id}")
    
    # ✅ Update feedback weight dynamically using Bayesian method
    selected_feedback.update_weight()

    return f"❌ Incorrect! {selected_feedback.message}"

