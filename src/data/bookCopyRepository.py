import mysql.connector
from mysql.connector import errorcode

from models.bookCopy import BookCopy


class BookCopyRepository:
    def __init__(self, host, user, password, database, book_repository):
        self.conn = None
        self.cursor = None
        self.book_repository = book_repository

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

    def add_book_copy(self, book_copy):
        # Check if the associated book exists
        associated_book = self.book_repository.get_book_by_id(book_copy.Book.BookID)

        if associated_book:
            query = "INSERT INTO BookCopy (BookID, Status) VALUES (%s, %s)"
            data = (associated_book.BookID, book_copy.Status)

            try:
                self.cursor.execute(query, data)
                self.conn.commit()

                # Update the BookCopy object with the assigned CopyID
                book_copy.CopyID = self.cursor.lastrowid

                print("BookCopy added successfully. CopyID:", book_copy.CopyID)
            except mysql.connector.Error as err:
                print("Error:", err)
        else:
            print("Error: Associated book not found. Unable to add BookCopy.")

    def update_book_copy(self, book_copy):
        query = "UPDATE BookCopy SET Status = %s WHERE CopyID = %s"
        data = (book_copy.Status, book_copy.CopyID)

        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            print("BookCopy updated successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def remove_book_copy(self, book_copy_id):
        query = "DELETE FROM BookCopy WHERE CopyID = %s"

        try:
            self.cursor.execute(query, (book_copy_id,))
            self.conn.commit()
            print("BookCopy removed successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def get_book_copy_by_id(self, book_copy_id):
        query = "SELECT * FROM BookCopy WHERE CopyID = %s"

        try:
            self.cursor.execute(query, (book_copy_id,))
            book_copy_data = self.cursor.fetchone()

            if book_copy_data:
                book_copy = BookCopy(book_copy_data[0], self.book_repository.get_book_by_id(book_copy_data[1]),
                                     book_copy_data[2])
                return book_copy
            else:
                print("BookCopy not found.")
                return None

        except mysql.connector.Error as err:
            print("Error:", err)

    def get_available_book_copies(self, book_id):
        query = "SELECT * FROM BookCopy WHERE BookID = %s AND Status = 'Available'"

        try:
            self.cursor.execute(query, (book_id,))
            available_book_copies = []

            for book_copy_data in self.cursor.fetchall():
                book_copy = BookCopy(book_copy_data[0], self.book_repository.get_book_by_id(book_copy_data[1]),
                                     book_copy_data[2])
                available_book_copies.append(book_copy)

            return available_book_copies
        except mysql.connector.Error as err:
            print("Error:", err)
