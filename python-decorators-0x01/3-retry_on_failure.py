# 3-retry_on_failure.py
import time
import sqlite3
import functools

def with_db_connection(func):
    """Decorator that opens and closes a database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Retries a database operation if it fails."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        print(f"[INFO] Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print("[ERROR] All retry attempts failed.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Attempt to fetch users
users = fetch_users_with_retry()
print(users)
