# Assuming User and UserRepository classes are defined in the respective files.
from models.user import User
from data.userRepository import UserRepository


class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def add_user(self, new_user_name, new_user_type):
        # Validate new_user_type
        if new_user_type not in ('Student', 'Admin'):
            print("Error: Invalid user type. User type must be 'Student' or 'Admin'.")
            return

        # Validate new_user_name
        if not all(char.isalpha() or char.isspace() for char in new_user_name):
            print("Error: Invalid user name. User name must consist of alphabetical characters.")
            return

        new_user = User(None, new_user_name, new_user_type)
        self.user_repository.add_user(new_user)

    def update_user(self, user_id, new_user_name):
        # Validate new_user_name
        if not all(char.isalpha() or char.isspace() for char in new_user_name):
            print("Error: Invalid user name. User name must consist of alphabetical characters.")
            return

        existing_user = self.user_repository.get_user_by_id(user_id)

        if existing_user:
            existing_user.UserName = new_user_name
            self.user_repository.update_user(existing_user)
        else:
            print("Error: User not found.")

    def remove_user(self, user_id):
        self.user_repository.remove_user(user_id)

    def get_user(self, user_id):
        return self.user_repository.get_user_by_id(user_id)
