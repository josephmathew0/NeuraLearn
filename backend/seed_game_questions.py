# seed_game_questions.py

import eventlet
eventlet.monkey_patch()  # Must be FIRST before anything else

from app import app
from models import db, GameQuestion

with app.app_context():
    db.create_all()
    print("✅ All tables created.")

    print("⏳ Seeding game questions...")

    player_questions = [
        {
            "question": "-- Table: books(id, title, year)\n-- Q1: What is the latest year among all books?",
            "answer_query": "SELECT MAX(year) FROM books;",
            "hint": "2022"
        },
        {
            "question": "-- Table: borrowers(id, name, book_id, borrowed_year)\n-- Q2: Find the names of borrowers who borrowed books after the year you got in question 1.",
            "answer_query": "SELECT name FROM borrowers WHERE borrowed_year > 2022;",
            "hint": "John Doe"
        },
        {
            "question": "-- Table: books(id, title, year, genre)\n-- Q3: What is the genre of the book borrowed by the person you got in question 2?",
            "answer_query": "SELECT genre FROM books WHERE id IN (SELECT book_id FROM borrowers WHERE name = 'John Doe');",
            "hint": "Mystery"
        },
        {
            "question": "-- Table: authors(id, name, genre)\n-- Q4: Which authors have written books in the genre you got from question 3?",
            "answer_query": "SELECT name FROM authors WHERE genre = 'Mystery';",
            "hint": "Agatha Christie"
        },
        {
            "question": "-- Table: author_awards(id, author_name, award_name)\n-- Q5: What award was won by the author you got in question 4?",
            "answer_query": "SELECT award_name FROM author_awards WHERE author_name = 'Agatha Christie';",
            "hint": "Mystery Master Award"
        },
        {
            "question": "-- Table: awards(id, name, year, recipient)\n-- Q6: Which year did the author receive the award from question 5?",
            "answer_query": "SELECT year FROM awards WHERE name = 'Mystery Master Award' AND recipient = 'Agatha Christie';",
            "hint": "2019"
        },
        {
            "question": "-- Table: libraries(id, name, founded_year)\n-- Q7: Which libraries were founded before the year from question 6?",
            "answer_query": "SELECT name FROM libraries WHERE founded_year < 2019;",
            "hint": "Central Library"
        },
        {
            "question": "-- Table: events(id, library_name, event_name)\n-- Q8: What event was held in the library from question 7?",
            "answer_query": "SELECT event_name FROM events WHERE library_name = 'Central Library';",
            "hint": "BookFest"
        },
        {
            "question": "-- Table: event_participants(id, event_name, participant_name)\n-- Q9: Who participated in the event from question 8?",
            "answer_query": "SELECT participant_name FROM event_participants WHERE event_name = 'BookFest';",
            "hint": "Michael Smith"
        },
        {
            "question": "-- Table: suspects(id, name, occupation)\n-- Q10: Who among the suspects matches the participant from question 9?",
            "answer_query": "SELECT name FROM suspects WHERE name = 'Michael Smith';",
            "hint": "Michael Smith"
        },
    ]

    murderer_questions = [
        {
            "question": "-- Table: books(id, title, genre)\n-- Q1: Delete all books with genre 'Horror'.",
            "answer_query": "DELETE FROM books WHERE genre = 'Horror';",
            "hint": "3 rows affected"
        },
        {
            "question": "-- Table: logs(id, action, rows_affected)\n-- Q2: How many rows were affected in the last DELETE operation?",
            "answer_query": "SELECT rows_affected FROM logs WHERE action = 'DELETE_Horror';",
            "hint": "3"
        },
        {
            "question": "-- Table: books(id, title, genre)\n-- Q3: Update all remaining books of genre 'Mystery' to genre 'Thriller'.",
            "answer_query": "UPDATE books SET genre = 'Thriller' WHERE genre = 'Mystery';",
            "hint": "4 rows updated"
        },
        {
            "question": "-- Table: books(id, title, genre)\n-- Q4: Count how many books are now labeled as 'Thriller'.",
            "answer_query": "SELECT COUNT(*) FROM books WHERE genre = 'Thriller';",
            "hint": "4"
        },
        {
            "question": "-- Table: authors(id, name, genre)\n-- Q5: Update authors who wrote in 'Mystery' to 'Thriller'.",
            "answer_query": "UPDATE authors SET genre = 'Thriller' WHERE genre = 'Mystery';",
            "hint": "2 rows updated"
        },
        {
            "question": "-- Table: logs(id, action, user)\n-- Q6: What user performed the most recent update?",
            "answer_query": "SELECT user FROM logs ORDER BY id DESC LIMIT 1;",
            "hint": "admin_user"
        },
        {
            "question": "-- Table: events(id, name, status)\n-- Q7: Delete any events marked 'Cancelled'.",
            "answer_query": "DELETE FROM events WHERE status = 'Cancelled';",
            "hint": "1 event deleted"
        },
        {
            "question": "-- Table: events(id, name, status)\n-- Q8: Count how many events remain after the deletion.",
            "answer_query": "SELECT COUNT(*) FROM events;",
            "hint": "5"
        },
        {
            "question": "-- Table: audit(id, action)\n-- Q9: What was the action logged before the last delete?",
            "answer_query": "SELECT action FROM audit ORDER BY id DESC LIMIT 1 OFFSET 1;",
            "hint": "UPDATE_Thriller"
        },
        {
            "question": "-- Table: suspects(id, name, action_tag)\n-- Q10: Who matches the last logged action?",
            "answer_query": "SELECT name FROM suspects WHERE action_tag = 'UPDATE_Thriller';",
            "hint": "Michael Smith"
        },
    ]

    for i, q in enumerate(player_questions, start=1):
        db.session.add(GameQuestion(
            question=q["question"],
            answer_query=q["answer_query"],
            hint=q["hint"],
            role='player',
            question_order=i
        ))

    for i, q in enumerate(murderer_questions, start=1):
        db.session.add(GameQuestion(
            question=q["question"],
            answer_query=q["answer_query"],
            hint=q["hint"],
            role='murderer',
            question_order=i
        ))

    db.session.commit()
    print("✅ Game questions seeded.")
