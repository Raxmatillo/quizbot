import sqlite3

# SQLite bazaga ulanish
# conn = sqlite3.connect("D:\Rakhmatullo\projects\quizbot\data\main.db")  # Baza nomi
conn = sqlite3.connect("quizzes.db")
cursor = conn.cursor()

quizzes = cursor.execute("SELECT * FROM Quizzes;").fetchall()
for quiz in quizzes:
    