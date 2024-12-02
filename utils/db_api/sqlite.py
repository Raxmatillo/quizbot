import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone VARCHAR(20) NOT NULL,
            telegram_id INTEGER UNIQUE NOT NULL,
            credit INTEGER DEFAULT 100,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(sql, commit=True)

    def create_table_payments(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            income INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        );
        """
        self.execute(sql, commit=True)

    def create_table_quizzes(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner INTEGER NOT NULL,
            title TEXT NOT NULL,
            count_test INTEGER NULL,
            credit INTEGER NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(owner) REFERENCES Users(id)
        )
        """
        self.execute(sql, commit=True)

    def create_table_tests(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer_a TEXT NOT NULL,
            answer_b TEXT NOT NULL,
            answer_c TEXT NOT NULL,
            answer_d TEXT NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY(question_id) REFERENCES Quizzes(id)
        );
        """
        self.execute(sql, commit=True)

    def create_table_results(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(quiz_id) REFERENCES Quizzes(id)
        );
        """
        self.execute(sql, execute=True)

    

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, full_name, phone, telegram_id):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(full_name, phone, telegram_id) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(full_name, phone, telegram_id), commit=True)
    
    def add_quiz(owner: int, title: str, count_test: int, credit: int):
        
        sql = """
        INSERT INTO Quizzes (owner, title, count_test, credit)
        VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(owner, title, count_test, credit), commit=True)

    def save_to_database(self, question_id: int, question: str, answers: list, correct_answer: str):
        while len(answers) < 4:
            answers.append("")

        sql = """
        INSERT INTO Quizzes (question_id, question, answer_a, answer_b, answer_c, answer_d, answer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(question_id, question, answers[0], answers[1], answers[2], answers[3], correct_answer), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")