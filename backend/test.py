from utils import find_misconception

question_id = 2  # The ID of the SQL question
user_input = "WHERE 1=1"

misconception = find_misconception(user_input, question_id)
print(misconception)
