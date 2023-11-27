import mysql.connector
from mysql.connector import errorcode

from models.book import Book


class BookRepository:
    def __init__(self, host, user, password, database):
        self.conn = None
        self.cursor = None

        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            self.cursor = self.conn.cursor(buffered=True)
            print("Connected to MySQL database")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Access denied. Check your username and password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            else:
                print("Error:", err)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def add_book(self, book):
        query = "INSERT INTO Book (Title, Author, Genre) VALUES (%s, %s, %s)"
        data = (book.Title, book.Author, book.Genre)

        try:
            self.cursor.execute(query, data)
            self.conn.commit()

            # Update the Book object with the assigned BookID
            book.BookID = self.cursor.lastrowid

            print("Book added successfully. BookID:", book.BookID)
        except mysql.connector.Error as err:
            print("Error:", err)

    def update_book(self, book):
        query = "UPDATE Book SET Title = %s, Author = %s, Genre = %s WHERE BookID = %s"
        data = (book.Title, book.Author, book.Genre, book.BookID)

        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            print("Book updated successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def remove_book(self, book_id):
        query = "DELETE FROM Book WHERE BookID = %s"

        try:
            self.cursor.execute(query, (book_id,))
            self.conn.commit()
            print("Book removed successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def get_book_by_id(self, book_id):
        query = "SELECT * FROM Book WHERE BookID = %s"

        try:
            self.cursor.execute(query, (book_id,))
            book_data = self.cursor.fetchone()

            if book_data:
                book = Book(book_data[0], book_data[1], book_data[2], book_data[3])
                return book
            else:
                print("Book not found.")
                return None

        except mysql.connector.Error as err:
            print("Error:", err)
