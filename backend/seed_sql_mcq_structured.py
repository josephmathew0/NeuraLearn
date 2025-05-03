from app import app
from models import db, SQLMCQStructured

with app.app_context():
    db.create_all()
    SQLMCQStructured.query.delete()  # ✅ Clear previous entries
    db.session.commit()

    questions = [
        # Topic 1: SQL Basics
        SQLMCQStructured(
            question="What does SELECT * FROM Students return?",
            correct_answer="All rows and columns in Students",
            distractor1="Only the first row",
            distractor2="Only the column names",
            distractor3="Only the primary key values",
            explanation="SELECT * returns all rows and columns.",
            topic="sql_basics",
            topic_order=1
        ),
        SQLMCQStructured(
            question="Which keyword is used to fetch data from a table?",
            correct_answer="SELECT",
            distractor1="FETCH",
            distractor2="RETRIEVE",
            distractor3="GET",
            explanation="SELECT is the standard SQL keyword to fetch data.",
            topic="sql_basics",
            topic_order=1
        ),
        SQLMCQStructured(
            question="Which clause specifies the table to query from?",
            correct_answer="FROM",
            distractor1="WHERE",
            distractor2="TABLE",
            distractor3="INTO",
            explanation="The FROM clause specifies the source table.",
            topic="sql_basics",
            topic_order=1
        ),

        # Topic 2: Logical Operators
        SQLMCQStructured(
            question="Which logical operator returns TRUE only if both conditions are TRUE?",
            correct_answer="AND",
            distractor1="OR",
            distractor2="XOR",
            distractor3="NOT",
            explanation="AND returns true only when both operands are true.",
            topic="logical_operators",
            topic_order=2
        ),
        SQLMCQStructured(
            question="Which SQL keyword negates a condition?",
            correct_answer="NOT",
            distractor1="EXCEPT",
            distractor2="ELSE",
            distractor3="IS NOT",
            explanation="NOT negates a condition in SQL.",
            topic="logical_operators",
            topic_order=2
        ),
        SQLMCQStructured(
            question="Which operator returns TRUE if either condition is TRUE?",
            correct_answer="OR",
            distractor1="AND",
            distractor2="ALL",
            distractor3="BETWEEN",
            explanation="OR returns true if either condition is met.",
            topic="logical_operators",
            topic_order=2
        ),

        # Topic 3: ORDER BY + LIMIT
        SQLMCQStructured(
            question="What does ORDER BY do in SQL?",
            correct_answer="Sorts the result set",
            distractor1="Removes duplicates",
            distractor2="Limits output to 10 rows",
            distractor3="Groups results",
            explanation="ORDER BY sorts rows based on specified column(s).",
            topic="order_by_limit",
            topic_order=3
        ),
        SQLMCQStructured(
            question="Which keyword is used to fetch only the first N rows?",
            correct_answer="LIMIT",
            distractor1="TOP",
            distractor2="OFFSET",
            distractor3="ROWNUM",
            explanation="LIMIT restricts the number of rows returned.",
            topic="order_by_limit",
            topic_order=3
        ),
        SQLMCQStructured(
            question="What does ORDER BY age DESC return?",
            correct_answer="Rows sorted by age in descending order",
            distractor1="Rows sorted by age ascending",
            distractor2="Only rows where age is the highest",
            distractor3="Rows with NULL age removed",
            explanation="DESC means descending order.",
            topic="order_by_limit",
            topic_order=3
        ),

        # Topic 4: Aggregate Functions
        SQLMCQStructured(
            question="What does COUNT(*) return?",
            correct_answer="The total number of rows",
            distractor1="The number of columns",
            distractor2="The number of NULL values",
            distractor3="The number of distinct rows",
            explanation="COUNT(*) counts all rows, including NULLs.",
            topic="aggregate_functions",
            topic_order=4
        ),
        SQLMCQStructured(
            question="Which aggregate function returns the average value?",
            correct_answer="AVG()",
            distractor1="MEAN()",
            distractor2="SUM()",
            distractor3="MEDIAN()",
            explanation="AVG() calculates the mean of numeric values.",
            topic="aggregate_functions",
            topic_order=4
        ),
        SQLMCQStructured(
            question="Which function returns the smallest value?",
            correct_answer="MIN()",
            distractor1="LEAST()",
            distractor2="SMALLEST()",
            distractor3="FIRST()",
            explanation="MIN() gives the minimum in a group of values.",
            topic="aggregate_functions",
            topic_order=4
        ),

        # Topic 5: GROUP BY + HAVING
        SQLMCQStructured(
            question="What is the purpose of GROUP BY in SQL?",
            correct_answer="To group rows sharing a common value",
            distractor1="To limit the result",
            distractor2="To remove duplicates",
            distractor3="To apply ordering",
            explanation="GROUP BY combines rows with the same value into summary rows.",
            topic="group_by_having",
            topic_order=5
        ),
        SQLMCQStructured(
            question="Which clause is used to filter groups after aggregation?",
            correct_answer="HAVING",
            distractor1="WHERE",
            distractor2="GROUP BY",
            distractor3="LIMIT",
            explanation="HAVING filters groups, WHERE filters rows.",
            topic="group_by_having",
            topic_order=5
        ),
        SQLMCQStructured(
            question="What does this query return? SELECT dept, COUNT(*) FROM employees GROUP BY dept;",
            correct_answer="Number of employees in each department",
            distractor1="Employees grouped by job title",
            distractor2="List of departments with salaries",
            distractor3="Total count of departments",
            explanation="This query counts rows per department.",
            topic="group_by_having",
            topic_order=5
        ),
        # Topic 1–5 (already added)...
        # Topic 6: Subqueries
        SQLMCQStructured(
            question="What does a subquery return in SQL?",
            correct_answer="A value or set of values used by the main query",
            distractor1="A new table",
            distractor2="An error",
            distractor3="Only NULL",
            explanation="A subquery returns a result used by an outer query.",
            topic="subqueries",
            topic_order=6
        ),
        SQLMCQStructured(
            question="Where can a subquery be placed in SQL?",
            correct_answer="In SELECT, FROM, or WHERE clauses",
            distractor1="Only in WHERE",
            distractor2="Only in JOIN",
            distractor3="Only in HAVING",
            explanation="Subqueries can appear in several clauses.",
            topic="subqueries",
            topic_order=6
        ),
        SQLMCQStructured(
            question="What does this do? SELECT name FROM students WHERE age = (SELECT MAX(age) FROM students);",
            correct_answer="Returns the name(s) of oldest student(s)",
            distractor1="Returns all students",
            distractor2="Returns names of youngest students",
            distractor3="Returns only MAX(age)",
            explanation="The subquery finds max age, outer query fetches name(s).",
            topic="subqueries",
            topic_order=6
        ),

        # Topic 7: JOINs
        SQLMCQStructured(
            question="What is the result of an INNER JOIN?",
            correct_answer="Only matching rows from both tables",
            distractor1="All rows from both tables",
            distractor2="Only unmatched rows",
            distractor3="All rows from left table only",
            explanation="INNER JOIN keeps only rows with matches in both tables.",
            topic="joins",
            topic_order=7
        ),
        SQLMCQStructured(
            question="Which join includes all rows from the left table and matching ones from right?",
            correct_answer="LEFT JOIN",
            distractor1="RIGHT JOIN",
            distractor2="FULL JOIN",
            distractor3="INNER JOIN",
            explanation="LEFT JOIN includes all from left + matching from right.",
            topic="joins",
            topic_order=7
        ),
        SQLMCQStructured(
            question="What happens if there's no match in RIGHT JOIN?",
            correct_answer="NULLs are filled for left table columns",
            distractor1="Row is discarded",
            distractor2="Error is thrown",
            distractor3="Data is duplicated",
            explanation="RIGHT JOIN shows all right table rows, NULL for missing left.",
            topic="joins",
            topic_order=7
        ),

        # Topic 8: NULL Handling
        SQLMCQStructured(
            question="Which SQL condition checks for NULL values?",
            correct_answer="IS NULL",
            distractor1="= NULL",
            distractor2="NULL = NULL",
            distractor3="IS NOT NULL",
            explanation="Use IS NULL to check for NULLs, not = NULL.",
            topic="null_handling",
            topic_order=8
        ),
        SQLMCQStructured(
            question="What does COALESCE(col1, 'default') do?",
            correct_answer="Returns col1 if not NULL, else 'default'",
            distractor1="Returns NULL",
            distractor2="Always returns col1",
            distractor3="Throws error if col1 is NULL",
            explanation="COALESCE returns first non-NULL argument.",
            topic="null_handling",
            topic_order=8
        ),
        SQLMCQStructured(
            question="Which function returns NULL if two values are equal?",
            correct_answer="NULLIF(val1, val2)",
            distractor1="IFNULL(val1, val2)",
            distractor2="ISNULL(val1, val2)",
            distractor3="CASE WHEN val1 = val2 THEN NULL ELSE val1 END",
            explanation="NULLIF(val1, val2) returns NULL if equal.",
            topic="null_handling",
            topic_order=8
        ),

        # Topic 9: DDL (Data Definition Language)
        SQLMCQStructured(
            question="What does CREATE TABLE do?",
            correct_answer="Defines a new table",
            distractor1="Deletes a table",
            distractor2="Inserts data",
            distractor3="Modifies a table",
            explanation="CREATE TABLE defines new structure.",
            topic="ddl",
            topic_order=9
        ),
        SQLMCQStructured(
            question="Which command removes a table completely?",
            correct_answer="DROP TABLE",
            distractor1="DELETE TABLE",
            distractor2="REMOVE TABLE",
            distractor3="TRUNCATE",
            explanation="DROP TABLE removes schema + data.",
            topic="ddl",
            topic_order=9
        ),
        SQLMCQStructured(
            question="What does ALTER TABLE do?",
            correct_answer="Modifies an existing table",
            distractor1="Creates a new table",
            distractor2="Deletes data from a table",
            distractor3="Selects specific rows",
            explanation="ALTER modifies columns, constraints, etc.",
            topic="ddl",
            topic_order=9
        ),
        # Topic 10: DML (Data Manipulation Language)
        SQLMCQStructured(
            question="Which SQL command adds a new row to a table?",
            correct_answer="INSERT",
            distractor1="UPDATE",
            distractor2="SELECT",
            distractor3="ALTER",
            explanation="INSERT is used to add new records to a table.",
            topic="dml",
            topic_order=10
        ),
        SQLMCQStructured(
            question="Which command modifies existing data in a table?",
            correct_answer="UPDATE",
            distractor1="ALTER",
            distractor2="INSERT",
            distractor3="MERGE",
            explanation="UPDATE is used to modify existing rows.",
            topic="dml",
            topic_order=10
        ),
        SQLMCQStructured(
            question="What does DELETE FROM table_name do?",
            correct_answer="Removes all rows from the table",
            distractor1="Deletes the table structure",
            distractor2="Removes only NULL rows",
            distractor3="Deletes rows from system tables",
            explanation="DELETE removes rows; table structure remains.",
            topic="dml",
            topic_order=10
        ),

        # Topic 11: Constraints
        SQLMCQStructured(
            question="What is the purpose of a PRIMARY KEY constraint?",
            correct_answer="Uniquely identifies each row",
            distractor1="Allows NULL values",
            distractor2="Creates a duplicate column",
            distractor3="Combines tables",
            explanation="PRIMARY KEY ensures row uniqueness.",
            topic="constraints",
            topic_order=11
        ),
        SQLMCQStructured(
            question="Which constraint ensures values in a column are not NULL?",
            correct_answer="NOT NULL",
            distractor1="UNIQUE",
            distractor2="CHECK",
            distractor3="FOREIGN KEY",
            explanation="NOT NULL prevents missing values.",
            topic="constraints",
            topic_order=11
        ),
        SQLMCQStructured(
            question="What does the CHECK constraint do?",
            correct_answer="Ensures values meet a condition",
            distractor1="Limits table size",
            distractor2="Assigns default value",
            distractor3="Indexes the table",
            explanation="CHECK restricts the values allowed in a column.",
            topic="constraints",
            topic_order=11
        ),

        # Topic 12: Views & Indexes
        SQLMCQStructured(
            question="What is a SQL VIEW?",
            correct_answer="A virtual table based on a query",
            distractor1="A copy of the base table",
            distractor2="A materialized report",
            distractor3="An index table",
            explanation="A VIEW is a named query treated like a table.",
            topic="views_indexes",
            topic_order=12
        ),
        SQLMCQStructured(
            question="What is the purpose of an index in SQL?",
            correct_answer="To speed up data retrieval",
            distractor1="To enforce referential integrity",
            distractor2="To store a backup copy",
            distractor3="To manage table constraints",
            explanation="Indexes make lookups faster, especially on large tables.",
            topic="views_indexes",
            topic_order=12
        ),
        SQLMCQStructured(
            question="What happens if you query a view?",
            correct_answer="The underlying query is executed",
            distractor1="The view's data is copied",
            distractor2="The view is deleted",
            distractor3="No rows are returned",
            explanation="Views execute their defining query each time.",
            topic="views_indexes",
            topic_order=12
        )
    ]


    db.session.add_all(questions)
    db.session.commit()
    print("✅ Structured SQL MCQs seeded!")