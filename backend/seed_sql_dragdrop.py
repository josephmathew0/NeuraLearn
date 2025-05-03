from app import app
from models import db, SQLDragDrop
import json

with app.app_context():
    # ✅ Only delete entries from the SQLDragDrop table
    db.session.query(SQLDragDrop).delete()
    db.session.commit()

    # ✅ Keep all other tables/data intact
    db.create_all()


    questions = [
        # Relational Algebra
        SQLDragDrop(
            question="Project name and salary attributes from Employees (Relational Algebra).",
            correct_answer="π name, salary (Employees)",
            draggables=json.dumps(["π", "name, salary", "(", "Employees", ")"]),
            topic="relational_algebra",
            topic_order=5
        ),
        SQLDragDrop(
            question="Select tuples where age > 18 from Students (Relational Algebra).",
            correct_answer="σ age > 18 (Students)",
            draggables=json.dumps(["σ", "age > 18", "(", "Students", ")"]),
            topic="relational_algebra",
            topic_order=5
        ),
        SQLDragDrop(
            question="Join Students and Departments on dept_id (Relational Algebra).",
            correct_answer="Students ⨝ Students.dept_id = Departments.dept_id Departments",
            draggables=json.dumps(["Students", "⨝", "Students.dept_id = Departments.dept_id", "Departments"]),
            topic="relational_algebra",
            topic_order=5
        ),
        SQLDragDrop(
            question="Select students from CS department (Relational Algebra).",
            correct_answer="σ department = 'CS' (Students)",
            draggables=json.dumps(["σ", "department = 'CS'", "(", "Students", ")"]),
            topic="relational_algebra",
            topic_order=5
        ),
        SQLDragDrop(
            question="Project name and department from Students (Relational Algebra).",
            correct_answer="π name, department (Students)",
            draggables=json.dumps(["π", "name, department", "(", "Students", ")"]),
            topic="relational_algebra",
            topic_order=5
        ),
        # SQL
        SQLDragDrop(
            question="Write an SQL query to get all student names from the Students table.",
            correct_answer="SELECT name FROM Students;",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", ";"]),
            topic="sql_select",
            topic_order=1
        ),
        SQLDragDrop(
            question="Write an SQL query to get the names of students older than 18.",
            correct_answer="SELECT name FROM Students WHERE age > 18;",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", "WHERE", "age", ">", "18", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Write an SQL query to get the number of students.",
            correct_answer="SELECT COUNT(*) FROM Students;",
            draggables=json.dumps(["SELECT", "COUNT(*)", "FROM", "Students", ";"]),
            topic="sql_aggregate",
            topic_order=3
        ),
        SQLDragDrop(
            question="List all employees with salary between 40000 and 60000, ordered by name.",
            correct_answer="SELECT * FROM Employees WHERE salary BETWEEN 40000 AND 60000 ORDER BY name ASC;",
            draggables=json.dumps(["SELECT", "*", "FROM", "Employees", "WHERE", "salary", "BETWEEN", "40000", "AND", "60000", "ORDER BY", "name", "ASC", ";"]),
            topic="sql_order_by",
            topic_order=4
        ),
        SQLDragDrop(
            question="Find the total salary of all employees.",
            correct_answer="SELECT SUM(salary) FROM Employees;",
            draggables=json.dumps(["SELECT", "SUM(salary)", "FROM", "Employees", ";"]),
            topic="sql_aggregate",
            topic_order=3
        ),
        SQLDragDrop(
            question="Find average age of students in each department.",
            correct_answer="SELECT dept_id, AVG(age) FROM Students GROUP BY dept_id;",
            draggables=json.dumps(["SELECT", "dept_id,", "AVG(age)", "FROM", "Students", "GROUP BY", "dept_id", ";"]),
            topic="sql_groupby",
            topic_order=6
        ),
        SQLDragDrop(
            question="Get departments having more than 5 students.",
            correct_answer="SELECT dept_id FROM Students GROUP BY dept_id HAVING COUNT(*) > 5;",
            draggables=json.dumps(["SELECT", "dept_id", "FROM", "Students", "GROUP BY", "dept_id", "HAVING", "COUNT(*)", ">", "5", ";"]),
            topic="sql_groupby",
            topic_order=6
        ),
        SQLDragDrop(
            question="Get names of students along with department names.",
            correct_answer="SELECT Students.name, Departments.name FROM Students INNER JOIN Departments ON Students.dept_id = Departments.dept_id;",
            draggables=json.dumps(["SELECT", "Students.name,", "Departments.name", "FROM", "Students", "INNER JOIN", "Departments", "ON", "Students.dept_id", "=", "Departments.dept_id", ";"]),
            topic="sql_join",
            topic_order=7
        ),
        SQLDragDrop(
            question="Relational Algebra: Project name and salary attributes from Employees.",
            correct_answer="π name, salary (Employees)",
            draggables=json.dumps(["π", "name,", "salary", "(", "Employees", ")"]),
            topic="relational_algebra",
            topic_order=8
        ),
        SQLDragDrop(
            question="Relational Algebra: Select employees with salary > 50000.",
            correct_answer="σ salary > 50000 (Employees)",
            draggables=json.dumps(["σ", "salary > 50000", "(", "Employees", ")"]),
            topic="relational_algebra",
            topic_order=8
        ),
        SQLDragDrop(
            question="Write an SQL query to find the average salary of employees.",
            correct_answer="SELECT AVG(salary) FROM Employees;",
            draggables=json.dumps(["SELECT", "AVG(salary)", "FROM", "Employees", ";"]),
            topic="sql_aggregate",
            topic_order=3
        ),
        SQLDragDrop(
            question="Find students who are either in CS or IT department.",
            correct_answer="SELECT * FROM Students WHERE department = 'CS' OR department = 'IT';",
            draggables=json.dumps(["SELECT", "*", "FROM", "Students", "WHERE", "department", "=", "'CS'", "OR", "department", "=", "'IT'", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Sort students by name in descending order.",
            correct_answer="SELECT * FROM Students ORDER BY name DESC;",
            draggables=json.dumps(["SELECT", "*", "FROM", "Students", "ORDER BY", "name", "DESC", ";"]),
            topic="sql_order_by",
            topic_order=4
        ),
        SQLDragDrop(
            question="List all unique departments from the Employees table.",
            correct_answer="SELECT DISTINCT department FROM Employees;",
            draggables=json.dumps(["SELECT", "DISTINCT", "department", "FROM", "Employees", ";"]),
            topic="sql_distinct",
            topic_order=6
        ),
        SQLDragDrop(
            question="Write a query to get names of students in department 10 or 12.",
            correct_answer="SELECT name FROM Students WHERE dept_id IN (10, 12);",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", "WHERE", "dept_id", "IN", "(10, 12)", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Find total salary paid by each department.",
            correct_answer="SELECT department, SUM(salary) FROM Employees GROUP BY department;",
            draggables=json.dumps(["SELECT", "department", "SUM(salary)", "FROM", "Employees", "GROUP BY", "department", ";"]),
            topic="sql_group_by",
            topic_order=7
        ),
        SQLDragDrop(
            question="Get department-wise average age of students having age > 18.",
            correct_answer="SELECT dept_id, AVG(age) FROM Students WHERE age > 18 GROUP BY dept_id;",
            draggables=json.dumps(["SELECT", "dept_id", "AVG(age)", "FROM", "Students", "WHERE", "age", ">", "18", "GROUP BY", "dept_id", ";"]),
            topic="sql_group_by",
            topic_order=7
        ),
        SQLDragDrop(
            question="Relational Algebra: Get employee names with salary over 40000.",
            correct_answer="π name (σ salary > 40000 (Employees))",
            draggables=json.dumps(["π", "name", "(", "σ", "salary > 40000", "(", "Employees", ")", ")"]),
            topic="relational_algebra",
            topic_order=5
        ),
        SQLDragDrop(
            question="Get names of students whose age is between 20 and 25.",
            correct_answer="SELECT name FROM Students WHERE age BETWEEN 20 AND 25;",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", "WHERE", "age", "BETWEEN", "20", "AND", "25", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Get name and salary from Employees ordered by salary descending.",
            correct_answer="SELECT name, salary FROM Employees ORDER BY salary DESC;",
            draggables=json.dumps(["SELECT", "name, salary", "FROM", "Employees", "ORDER BY", "salary", "DESC", ";"]),
            topic="sql_order_by",
            topic_order=4
        ),
        SQLDragDrop(
            question="Relational Algebra: Project names of employees in department 5.",
            correct_answer="π name (σ dept_id = 5 (Employees))",
            draggables=json.dumps(["π", "name", "(", "σ", "dept_id = 5", "(", "Employees", ")", ")"]),
            topic="relational_algebra",
            topic_order=5
        ),
        SQLDragDrop(
            question="Write an SQL query to get student names in ascending order of age.",
            correct_answer="SELECT name FROM Students ORDER BY age ASC;",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", "ORDER BY", "age", "ASC", ";"]),
            topic="sql_order_by",
            topic_order=4
        ),
        SQLDragDrop(
            question="Get the maximum salary from Employees table.",
            correct_answer="SELECT MAX(salary) FROM Employees;",
            draggables=json.dumps(["SELECT", "MAX(salary)", "FROM", "Employees", ";"]),
            topic="sql_aggregate",
            topic_order=3
        ),
        SQLDragDrop(
            question="Get names of students who are 18 years old.",
            correct_answer="SELECT name FROM Students WHERE age = 18;",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", "WHERE", "age", "=", "18", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Get the names of students who are not in department 5.",
            correct_answer="SELECT name FROM Students WHERE dept_id != 5;",
            draggables=json.dumps(["SELECT", "name", "FROM", "Students", "WHERE", "dept_id", "!=", "5", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Get all records from Employees who have salary greater than 50000.",
            correct_answer="SELECT * FROM Employees WHERE salary > 50000;",
            draggables=json.dumps(["SELECT", "*", "FROM", "Employees", "WHERE", "salary", ">", "50000", ";"]),
            topic="sql_where",
            topic_order=2
        ),
        SQLDragDrop(
            question="Join Students and Courses using course_id.",
            correct_answer="Students ⨝ Students.course_id = Courses.course_id Courses",
            draggables=json.dumps(["Students", "⨝", "Students.course_id = Courses.course_id", "Courses"]),
            topic="relational_algebra",
            topic_order=5
        )
    ]

    db.session.add_all(questions)
    db.session.commit()
    print("✅ SQL Drag-and-Drop questions seeded!")
