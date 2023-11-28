# Assuming BookCopy and BookCopyRepository classes are defined in the respective files.
from models.bookCopy import BookCopy
from data.bookCopyRepository import BookCopyRepository


class BookCopyService:
    def __init__(self, book_copy_repository):
        self.book_copy_repository = book_copy_repository

    def add_book_copy(self, book_id):
        # Check if the associated book exists
        existing_book = self.book_copy_repository.book_repository.get_book_by_id(book_id)

        if existing_book:
            new_book_copy = BookCopy(None, existing_book, "Available")
            self.book_copy_repository.add_book_copy(new_book_copy)
            return new_book_copy.CopyID
        else:
            print(f"Book with id {book_id} doesn't exist.")
            return None

    def remove_book_copy(self, copy_id):
        existing_book_copy = self.book_copy_repository.get_book_copy_by_id(copy_id)

        if existing_book_copy:
            self.book_copy_repository.remove_book_copy(copy_id)
        else:
            print(f"BookCopy with id {copy_id} doesn't exist.")

    def get_available_copies(self, book_id):
        return self.book_copy_repository.get_available_book_copies(book_id)

    def update_book_copy(self, copy_id, book_id, status):
        # Validate status
        if status not in ('Available', 'Checked Out'):
            print("Error: Invalid status. Status must be 'Available' or 'Checked Out'.")
            return

        existing_book_copy = self.book_copy_repository.get_book_copy_by_id(copy_id)

        if existing_book_copy:
            # Validate book_id
            existing_book = self.book_copy_repository.book_repository.get_book_by_id(book_id)
            if existing_book:
                existing_book_copy.Book = existing_book
            else:
                print(f"Book with id {book_id} doesn't exist.")
                return

            existing_book_copy.Status = status
            self.book_copy_repository.update_book_copy(existing_book_copy)
        else:
            print(f"BookCopy with id {copy_id} doesn't exist.")
