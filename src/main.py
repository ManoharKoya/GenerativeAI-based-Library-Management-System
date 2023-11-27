from data.bookCopyRepository import BookCopyRepository
from data.checkoutRepository import CheckoutRepository
from data.userRepository import UserRepository
from data.bookRepository import BookRepository
from models.bookCopy import BookCopy
from models.checkout import Checkout
from models.user import User
from models.book import Book

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysqlrootpassword',
    'database': 'LibraryDatabase'
}


def startApp():
    pass


if __name__ == "__main__":
    # Example UserRepository
    user_repo = UserRepository(**db_config)

    # Example BookRepository
    book_repo = BookRepository(**db_config)

    # Example BookCopyRepository
    book_copy_repo = BookCopyRepository(**db_config, book_repository=book_repo)

    # Example CheckoutRepository
    checkout_repo = CheckoutRepository(**db_config, book_copy_repository=book_copy_repo, user_repository=user_repo)

    # Example User
    new_user = User(None, "John Doe", "Student")
    user_repo.add_user(new_user)

    # Example Book
    new_book = Book(None, "The Catcher in the Rye", "J.D. Salinger", "Fiction")
    book_repo.add_book(new_book)

    # Example BookCopy
    new_book_copy = BookCopy(None, new_book, "Available")
    book_copy_repo.add_book_copy(new_book_copy)

    # Example Checkout
    new_checkout = Checkout(None, new_book_copy, new_user, None, None)
    checkout_repo.add_checkout(new_checkout)

    # Example getLastBorrower
    last_borrower = checkout_repo.get_last_borrower(new_book_copy.CopyID)
    print("Last Borrower:", last_borrower.__dict__)

    # Example getCheckoutBookCopiedByUser
    active_checkouts = checkout_repo.get_active_checkouts_by_user(new_user.UserID)
    print("Active Checkouts:", [checkout.__dict__ for checkout in active_checkouts])

    # Example returnBookCopy
    checkout_repo.return_book_copy(new_book_copy.CopyID)

    # Example getCheckoutHistoryByUser
    checkout_history = checkout_repo.get_checkout_history_by_user(new_user.UserID)
    print("Checkout History:", [checkout.__dict__ for checkout in checkout_history])

    book_copy_repo.close_connection()
    book_repo.close_connection()
    user_repo.close_connection()
    checkout_repo.close_connection()
    # # Replace these with your MySQL database credentials
    # db_config = {
    #     'host': 'localhost',
    #     'user': 'root',
    #     'password': 'mysqlrootpassword',
    #     'database': 'LibraryDatabase'
    # }
    #
    # # Example BookRepository
    # book_repo = BookRepository(**db_config)
    #
    # # Example BookCopyRepository
    # book_copy_repo = BookCopyRepository(**db_config, book_repository=book_repo)
    #
    # # Example Book
    # new_book = Book(None, "The Catcher in the Rye", "J.D. Salinger", "Fiction")
    # book_repo.add_book(new_book)
    #
    # # Example BookCopy
    # new_book_copy = BookCopy(None, new_book, "Available")
    #
    # # Add book copy
    # book_copy_repo.add_book_copy(new_book_copy)
    #
    # # Update book copy
    # new_book_copy.Status = "Checked Out"
    # book_copy_repo.update_book_copy(new_book_copy)
    #
    # # Get book copy by ID
    # retrieved_book_copy = book_copy_repo.get_book_copy_by_id(new_book_copy.CopyID)
    # print("Retrieved BookCopy:", retrieved_book_copy.__dict__)
    #
    # # Get available book copies for a book
    # available_copies = book_copy_repo.get_available_book_copies(new_book.BookID)
    # print("Available BookCopies:", [copy.__dict__ for copy in available_copies])
    #
    # # Remove book copy
    # # book_copy_repo.remove_book_copy(new_book_copy.CopyID)
    #
    # book_copy_repo.close_connection()
    # book_repo.close_connection()

    # book_repo = BookRepository(**db_config)
    #
    # # Example Book
    # new_book = Book(None, "The Catcher in the Rye", "J.D. Salinger", "Fiction")
    #
    # # Add book
    # book_repo.add_book(new_book)
    #
    # # Update book
    # new_book.Title = "New Title"
    # book_repo.update_book(new_book)
    #
    # # Get book by ID
    # retrieved_book = book_repo.get_book_by_id(new_book.BookID)
    # print("Retrieved Book:", retrieved_book.__dict__)
    #
    # # Remove book
    # book_repo.remove_book(new_book.BookID)
    #
    # book_repo.close_connection()

    # user_repo = UserRepository(**db_config)
    #
    # # Example User
    # new_user = User(None, "John Doe", "Student")
    #
    # # Add user
    # user_repo.add_user(new_user)
    #
    # # Update user
    # new_user.UserName = "Updated Name"
    # user_repo.update_user(new_user)
    #
    # # Get user by ID
    # retrieved_user = user_repo.get_user_by_id(new_user.UserID)
    # print("Retrieved User:", retrieved_user.__dict__)
    #
    # # Remove user
    # user_repo.remove_user(new_user.UserID)
    #
    # user_repo.close_connection()
