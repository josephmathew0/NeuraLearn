import sqlparse
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

class SQLValidator:
    def __init__(self, query):
        self.query = query.strip()
        self.tokens = sqlparse.parse(self.query)[0].tokens

    def check_missing_clauses(self):
        required_clauses = ['SELECT', 'FROM']
        missing = [clause for clause in required_clauses if clause not in self.query.upper()]
        if missing:
            return f"Error: Missing clauses - {', '.join(missing)}"
        return None
    
    def check_order_of_clauses(self):
        clause_order = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY']
        order_indices = {clause: self.query.upper().find(clause) for clause in clause_order if clause in self.query.upper()}
        sorted_indices = sorted(order_indices.values())
        if list(order_indices.values()) != sorted_indices:
            return "Error: Incorrect order of SQL clauses."
        return None
    
    def validate(self):
        errors = []
        missing_clauses = self.check_missing_clauses()
        if missing_clauses:
            errors.append(missing_clauses)
        
        order_error = self.check_order_of_clauses()
        if order_error:
            errors.append(order_error)
        
        return errors if errors else "Query is syntactically valid."

@app.route('/validate_sql', methods=['POST'])
def validate_sql():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No SQL query provided."}), 400

    validator = SQLValidator(query)
    validation_results = validator.validate()

    return jsonify({"query": query, "validation": validation_results})

if __name__ == '__main__':
    app.run(debug=True)
