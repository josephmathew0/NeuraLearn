from app import app
from models import db, SQLTextAnswerQuestion

with app.app_context():
    db.create_all()
    SQLTextAnswerQuestion.query.delete()

    questions = [
        SQLTextAnswerQuestion(
            question="What are the different types of SQL JOINs?",
            correct_answer="The types of SQL JOINs are INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN.",
            topic="joins",
            topic_order=1
        ),
        SQLTextAnswerQuestion(
            question="Explain the difference between WHERE and HAVING clauses in SQL.",
            correct_answer="WHERE is used to filter rows before grouping and HAVING is used to filter groups after aggregation.",
            topic="filtering",
            topic_order=2
        ),
        SQLTextAnswerQuestion(
            question="Describe the role of GROUP BY in SQL.",
            correct_answer="GROUP BY is used to arrange identical data into groups for aggregation.",
            topic="aggregation",
            topic_order=3
        ),
        SQLTextAnswerQuestion(
            question="How does an INNER JOIN differ from a LEFT JOIN?",
            correct_answer="An INNER JOIN returns only matching rows from both tables, while a LEFT JOIN returns all rows from the left table and matching rows from the right.",
            topic="joins",
            topic_order=1
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to find the names of students who scored above 80 in Math.",
            correct_answer="SELECT name FROM Students WHERE subject = 'Math' AND score > 80;",
            topic="query_writing",
            topic_order=4
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to find the average salary of employees in each department.",
            correct_answer="SELECT department, AVG(salary) FROM Employees GROUP BY department;",
            topic="aggregation",
            topic_order=3
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to list departments with more than 10 employees.",
            correct_answer="SELECT department FROM Employees GROUP BY department HAVING COUNT(*) > 10;",
            topic="aggregation",
            topic_order=3
        ),
        SQLTextAnswerQuestion(
            question="What is the difference between DELETE and TRUNCATE in SQL?",
            correct_answer="DELETE removes rows based on a condition and can be rolled back. TRUNCATE removes all rows and is faster but cannot be rolled back.",
            topic="deletion",
            topic_order=5
        ),
        SQLTextAnswerQuestion(
            question="What is a primary key in SQL?",
            correct_answer="A primary key uniquely identifies each row in a table and cannot have NULL values.",
            topic="constraints",
            topic_order=6
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to join Students and Departments on dept_id.",
            correct_answer="SELECT * FROM Students JOIN Departments ON Students.dept_id = Departments.dept_id;",
            topic="joins",
            topic_order=1
        ),
        SQLTextAnswerQuestion(
            question="What is the purpose of the WHERE clause in SQL?",
            correct_answer="The WHERE clause is used to filter records based on specific conditions in SQL queries.",
            topic="sql_where",
            topic_order=2
        ),
        SQLTextAnswerQuestion(
            question="What is a JOIN operation in SQL?",
            correct_answer="A JOIN operation in SQL is used to combine rows from two or more tables based on a related column.",
            topic="sql_joins",
            topic_order=4
        ),
        SQLTextAnswerQuestion(
            question="When would you use an INNER JOIN instead of an OUTER JOIN?",
            correct_answer="An INNER JOIN is used when only matching rows from both tables should be returned, whereas an OUTER JOIN returns all rows from one or both tables even if there is no match.",
            topic="sql_joins",
            topic_order=4
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to retrieve the names of employees earning more than $50,000.",
            correct_answer="SELECT name FROM Employees WHERE salary > 50000;",
            topic="sql_where",
            topic_order=2
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to count the number of departments in the Departments table.",
            correct_answer="SELECT COUNT(*) FROM Departments;",
            topic="sql_aggregate",
            topic_order=3
        ),
        SQLTextAnswerQuestion(
            question="Write an SQL query to display student names in descending order of their marks.",
            correct_answer="SELECT name FROM Students ORDER BY marks DESC;",
            topic="sql_order_by",
            topic_order=4
        )
    ]

    db.session.add_all(questions)
    db.session.commit()
    print("✅ SQL Answer Type questions seeded!")
