import seed


def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()


def compute_average_age():
    """Compute average age without loading all data"""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")
