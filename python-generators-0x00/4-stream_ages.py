#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """Generator that yields user ages one by one"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # replace if needed
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:
            yield age

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")


def compute_average_age():
    """Compute average age using the generator"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
if __name__ == "__main__":
    compute_average_age()
      