import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password =""
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",   # change if needed
            password="root", # change if needed
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(query)
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Check if record exists
                cursor.execute("SELECT * FROM user_data WHERE email=%s", (email,))
                result = cursor.fetchone()

                if not result:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")