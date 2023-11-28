import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

from models.book import Book
from models.bookCopy import BookCopy
from models.checkout import Checkout
from models.user import User


class CheckoutRepository:
    def __init__(self, host, user, password, database, book_copy_repository, user_repository):
        self.conn = None
        self.cursor = None
        self.book_copy_repository = book_copy_repository
        self.user_repository = user_repository

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

    def add_checkout(self, checkout):
        # Check if the associated book copy exists
        book_copy = self.book_copy_repository.get_book_copy_by_id(checkout.Copy.CopyID)

        if book_copy and book_copy.Status == "Available":
            # Calculate the return date (7 days from the current date)
            return_date = datetime.now() + timedelta(days=7)

            query = "INSERT INTO Checkout (CopyID, UserID, ReturnDate) VALUES (%s, %s, %s)"
            data = (checkout.Copy.CopyID, checkout.User.UserID, return_date)

            try:
                self.cursor.execute(query, data)
                self.conn.commit()

                # Update the book copy status to 'Checked out'
                book_copy.Status = "Checked Out"
                self.book_copy_repository.update_book_copy(book_copy)

                print("Checkout added successfully. CheckoutID:", self.cursor.lastrowid)
            except mysql.connector.Error as err:
                print("Error:", err)
        elif book_copy and book_copy.Status == "Checked Out":
            print("Error: BookCopy already checked out.")
        else:
            print("Error: Associated book copy not found. Unable to add Checkout.")

    def get_last_borrower(self, book_copy_id):
        query = "SELECT User.* FROM Checkout \
                 JOIN User ON Checkout.UserID = User.UserID \
                 WHERE Checkout.CopyID = %s \
                 ORDER BY Checkout.CheckoutDate DESC \
                 LIMIT 1"

        try:
            self.cursor.execute(query, (book_copy_id,))
            user_data = self.cursor.fetchone()

            if user_data:
                user = User(user_data[0], user_data[1], user_data[2])
                return user
            else:
                print("No recent borrower found.")
                return None

        except mysql.connector.Error as err:
            print("Error:", err)

    def get_checkout_by_id(self, checkout_id):
        query = "SELECT * FROM Checkout WHERE CheckoutID = %s"

        try:
            self.cursor.execute(query, (checkout_id,))
            checkout_data = self.cursor.fetchone()

            if checkout_data:
                checkout = Checkout(checkout_data[0],
                                    self.book_copy_repository.get_book_copy_by_id(checkout_data[1]),
                                    self.user_repository.get_user_by_id(checkout_data[2]),
                                    checkout_data[3], checkout_data[4])
                return checkout
            else:
                return None

        except mysql.connector.Error as err:
            print("Error:", err)
            return None

    def get_active_checkouts_by_user(self, user_id):
        query = "SELECT Checkout.* FROM Checkout \
                 JOIN BookCopy ON Checkout.CopyID = BookCopy.CopyID \
                 WHERE Checkout.UserID = %s AND Checkout.ReturnDate >= CURDATE() AND BookCopy.Status = 'Checked Out'"

        try:
            self.cursor.execute(query, (user_id,))
            active_checkouts_dict = {}  # Dictionary to store the latest checkout for each book_copy_id

            for checkout_data in self.cursor.fetchall():
                checkout_id = checkout_data[0]
                book_copy_id = checkout_data[1]
                checkout_date = checkout_data[3]

                # Check if the book_copy_id is not in the dictionary or if the checkout_date is later
                if book_copy_id not in active_checkouts_dict or checkout_date > active_checkouts_dict[book_copy_id][3]:
                    active_checkouts_dict[book_copy_id] = checkout_data

            # Convert the dictionary values back to check out objects
            active_checkouts = [Checkout(checkout_data[0],
                                         self.book_copy_repository.get_book_copy_by_id(checkout_data[1]),
                                         self.user_repository.get_user_by_id(checkout_data[2]),
                                         checkout_data[3], checkout_data[4]) for checkout_data in
                                active_checkouts_dict.values()]

            return active_checkouts

        except mysql.connector.Error as err:
            print("Error:", err)

    def return_book_copy(self, book_copy_id):
        # Update the book copy status to 'Available'
        book_copy = self.book_copy_repository.get_book_copy_by_id(book_copy_id)
        book_copy.Status = "Available"
        self.book_copy_repository.update_book_copy(book_copy)

    def get_checkout_history_by_user(self, user_id):
        query = "SELECT * FROM Checkout WHERE UserID = %s"

        try:
            self.cursor.execute(query, (user_id,))
            checkout_history = []

            for checkout_data in self.cursor.fetchall():
                checkout = Checkout(checkout_data[0], self.book_copy_repository.get_book_copy_by_id(checkout_data[1]),
                                    self.user_repository.get_user_by_id(checkout_data[2]),
                                    checkout_data[3], checkout_data[4])
                checkout_history.append(checkout)

            return checkout_history
        except mysql.connector.Error as err:
            print("Error:", err)
