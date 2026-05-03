import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0989",
        database="books_tracker"
    )

def insert_book(title, price, rating):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO books (title, price, rating) VALUES (%s, %s, %s)"
    cursor.execute(sql, (title, price, rating))

    conn.commit()
    cursor.close()
    conn.close()
