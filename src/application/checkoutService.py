# Assuming Checkout and CheckoutRepository classes are defined in the respective files.
from models.checkout import Checkout
from data.checkoutRepository import CheckoutRepository


class CheckoutService:
    def __init__(self, checkout_repository):
        self.checkout_repository = checkout_repository

    def checkout_book(self, user_id, copy_id):
        # Check if the associated user and book copy exist
        existing_user = self.checkout_repository.user_repository.get_user_by_id(user_id)
        existing_copy = self.checkout_repository.book_copy_repository.get_book_copy_by_id(copy_id)

        if existing_user and existing_copy:
            # Check if the book copy is available
            if existing_copy.Status == 'Available':
                # Check if the user has reached the maximum number of checkouts (e.g., 5)
                active_checkouts = self.checkout_repository.get_active_checkouts_by_user(user_id)
                if len(active_checkouts) >= 5:
                    print(f"Max limit of 5 checkouts is attained for the user {existing_user.UserName}")
                    return f"Max limit of 5 checkouts is attained for the user {existing_user.UserName}"

                new_checkout = Checkout(None, existing_copy, existing_user, None, None)
                self.checkout_repository.add_checkout(new_checkout)
                return 'Checkout successful!'
            else:
                print(f"The book with copy id {copy_id} is already checked out.")
                return f"The book with copy id {copy_id} is already checked out."
        else:
            if not existing_user:
                print(f"User with id {user_id} doesn't exist.")
                return f"User with id {user_id} doesn't exist."
            if not existing_copy:
                print(f"BookCopy with id {copy_id} doesn't exist.")
                return f"BookCopy with id {copy_id} doesn't exist."
        return 'Checkout successful!'

    def return_book(self, book_copy_id):
        book_copy = self.checkout_repository.book_copy_repository.get_book_copy_by_id(book_copy_id)

        if book_copy:
            # Check if the book copy is not already available
            if book_copy.Status != 'Available':
                self.checkout_repository.return_book_copy(book_copy_id)
                return 'Book returned successfully!'
            else:
                print("Error: The book is already available. Cannot return.")
                return "The book is already available. Cannot return."
        else:
            print(f"Checkout with book copy id {book_copy_id} doesn't exist.")
            return f"Checkout with book copy id {book_copy_id} doesn't exist."

    def get_checkout_history_by_user(self, user_id):
        # Check if the associated user exists
        existing_user = self.checkout_repository.user_repository.get_user_by_id(user_id)

        if existing_user:
            return self.checkout_repository.get_checkout_history_by_user(user_id)
        else:
            print(f"User with id {user_id} doesn't exist.")
            return []

    def get_active_checkouts_by_user(self, user_id):
        # Check if the associated user exists
        existing_user = self.checkout_repository.user_repository.get_user_by_id(user_id)

        if existing_user:
            return self.checkout_repository.get_active_checkouts_by_user(user_id)
        else:
            print(f"User with id {user_id} doesn't exist.")
            return []
