import mysql.connector
from mysql.connector import errorcode

from models.user import User


class UserRepository:
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

    def add_user(self, user):
        query = "INSERT INTO User (UserName, UserType) VALUES (%s, %s)"
        data = (user.UserName, user.UserType)

        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            user.UserID = self.cursor.lastrowid
            print("User added successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def update_user(self, user):
        query = "UPDATE User SET UserName = %s, UserType = %s WHERE UserID = %s"
        data = (user.UserName, user.UserType, user.UserID)

        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            print("User updated successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def remove_user(self, user_id):
        query = "DELETE FROM User WHERE UserID = %s"

        try:
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
            print("User removed successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM User WHERE UserID = %s"

        try:
            self.cursor.execute(query, (user_id,))
            user_data = self.cursor.fetchone()

            if user_data:
                user = User(user_data[0], user_data[1], user_data[2])
                return user
            else:
                print("User not found.")
                return None

        except mysql.connector.Error as err:
            print("Error:", err)

