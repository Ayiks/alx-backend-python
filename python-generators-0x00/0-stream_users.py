import seed


def stream_users():
    """Fetch users one row at a time using a generator"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row   # YIELD returns one row at a time

    cursor.close()
    connection.close()
