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
            new_checkout = Checkout(None, existing_copy, existing_user, None, None)
            self.checkout_repository.add_checkout(new_checkout)
            return new_checkout.CheckoutID
        else:
            if not existing_user:
                print(f"User with id {user_id} doesn't exist.")
            if not existing_copy:
                print(f"BookCopy with id {copy_id} doesn't exist.")
            return None

    def return_book(self, checkout_id):
        self.checkout_repository.return_book_copy(checkout_id)

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
