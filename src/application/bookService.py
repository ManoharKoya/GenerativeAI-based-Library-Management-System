# Assuming Book and BookRepository classes are defined in the respective files.
from models.book import Book
from data.bookRepository import BookRepository


class BookService:
    def __init__(self, book_repository):
        self.book_repository = book_repository

    def add_book(self, title, author, genre):
        new_book = Book(None, title, author, genre)
        self.book_repository.add_book(new_book)

    def remove_book(self, book_id):
        self.book_repository.remove_book(book_id)

    def get_books_by_author(self, author):
        books_by_author = self.book_repository.get_books_by_author(author)

        if not books_by_author:
            print(f"There is no book authored by {author}")
        return books_by_author

    def get_books_by_genre(self, genre):
        books_by_genre = self.book_repository.get_books_by_genre(genre)

        if not books_by_genre:
            print(f"There is no book in {genre} genre")
        return books_by_genre

    def update_book(self, book_id, new_title, new_author, new_genre):
        existing_book = self.book_repository.get_book_by_id(book_id)

        if existing_book:
            existing_book.Title = new_title
            existing_book.Author = new_author
            existing_book.Genre = new_genre
            self.book_repository.update_book(existing_book)
        else:
            print("There is no book with id:", book_id)
