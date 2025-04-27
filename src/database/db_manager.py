import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self):
        self.db_path = Path(__file__).parent / "movies.db"
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            conn.execute("PRAGMA foreign_keys = ON")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS watchlist (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    imdb_id TEXT NOT NULL,
                    rating REAL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(id)
                )
            """
            )
            # Add users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    date_created TEXT NOT NULL
                )
            """
            )

    def insert_movie_into_watchlist(self, user_id, imdb_id, rating):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO watchlist (user_id, imdb_id, rating, date) VALUES (?,?,?,DATE('now'))", (user_id,imdb_id,rating)
            )
            return cursor.lastrowid

    def update_movie_in_watchlist(self, user_id, rating, imdb_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE watchlist SET rating = ? WHERE user_id = ? AND imdb_id = ?", (rating, user_id, imdb_id)
            )
            return cursor.rowcount

    def create_new_user(self, username, password, email):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if email:
                cursor.execute(
                    "INSERT INTO user (username, password, email, date_created) VALUES (?,?,?,DATE('now'))",
                    (username, password, email)
                )
            return cursor.lastrowid

    def sign_in(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM user WHERE username = ? and password = ?",(username, password)
            )
            result = cursor.fetchone()
            return dict(result) if result else result

    def get_watchlist(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM watchlist WHERE user_id = ?", (user_id,)
            )
            result = cursor.fetchall()
            return result

    def retrieve_watchlist_rating(self, imdb_id, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM watchlist WHERE imdb_id = ? and user_id = ?", (imdb_id, user_id))
            result = cursor.fetchone()
            return dict(result)
