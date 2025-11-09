# 4-cache_query.py
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator to handle database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache query results."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Returning cached result for query.")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Query result cached.")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call uses cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
