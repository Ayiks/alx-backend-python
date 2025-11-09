# File: 0-databaseconnection.py
import sqlite3

class DatabaseConnection:
    """A custom context manager for handling SQLite database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection on exit, even if an error occurs."""
        if self.conn:
            self.conn.close()
        # Return False to propagate exceptions if any
        return False


# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)