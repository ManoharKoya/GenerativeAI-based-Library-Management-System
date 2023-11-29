from flask import Flask, render_template, request
from application.userService import UserService
from application.bookService import BookService
from application.bookCopyService import BookCopyService
from data.userRepository import UserRepository
from data.bookRepository import BookRepository
from data.bookCopyRepository import BookCopyRepository

app = Flask(__name__)

# Replace these with your MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysqlrootpassword',
    'database': 'LibraryDatabase'
}

user_repo = UserRepository(**db_config)
user_service = UserService(user_repo)

book_repo = BookRepository(**db_config)
book_service = BookService(book_repo)

book_copy_repo = BookCopyRepository(**db_config, book_repository=book_repo)
book_copy_service = BookCopyService(book_copy_repo)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_type = request.form['user_type']

        # Call the UserService method
        result = user_service.add_user(user_name, user_type)

        return render_template('add_user_result.html', result=result)

    return render_template('add_user.html')


@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        user_name = request.form['user_name']
        user_type = request.form['user_type']

        # Call the UserService method
        result = user_service.update_user(user_id, user_name)

        return render_template('update_user_result.html', result=result)

    return render_template('update_user.html')


@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])

        # Call the UserService method
        result = user_service.remove_user(user_id)

        return render_template('remove_user_result.html', result=result)

    return render_template('remove_user.html')


@app.route('/get_user', methods=['GET', 'POST'])
def get_user():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])

        # Call the UserService method
        user = user_service.get_user(user_id)

        return render_template('get_user_result.html', user=user)

    return render_template('get_user.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']

        # Call the BookService method
        result = book_service.add_book(title, author, genre)

        return render_template('add_book_result.html', result=result)

    return render_template('add_book.html')


@app.route('/get_books_by_author', methods=['GET', 'POST'])
def get_books_by_author():
    if request.method == 'POST':
        author = request.form['author']

        # Call the BookService method
        books = book_service.get_books_by_author(author)

        return render_template('get_books_by_author_result.html', books=books)

    return render_template('get_books_by_author.html')


@app.route('/get_books_by_genre', methods=['GET', 'POST'])
def get_books_by_genre():
    if request.method == 'POST':
        genre = request.form['genre']

        # Call the BookService method
        books = book_service.get_books_by_genre(genre)

        return render_template('get_books_by_genre_result.html', books=books)

    return render_template('get_books_by_genre.html')


@app.route('/update_book', methods=['GET', 'POST'])
def update_book():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        new_title = request.form['new_title']
        new_author = request.form['new_author']
        new_genre = request.form['new_genre']

        # Call the BookService method
        result = book_service.update_book(book_id, new_title, new_author, new_genre)

        return render_template('update_book_result.html', result=result)

    return render_template('update_book.html')


@app.route('/add_book_copy', methods=['GET', 'POST'])
def add_book_copy():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])

        # Call the BookCopyService method
        result = book_copy_service.add_book_copy(book_id)

        return render_template('add_book_copy_result.html', result=result)

    return render_template('add_book_copy.html')


@app.route('/get_available_copies', methods=['GET', 'POST'])
def get_available_copies():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])

        # Call the BookCopyService method
        copies = book_copy_service.get_available_copies(book_id)

        return render_template('get_available_copies_result.html', copies=copies)

    return render_template('get_available_copies.html')


@app.route('/update_book_copy', methods=['GET', 'POST'])
def update_book_copy():
    if request.method == 'POST':
        book_copy_id = int(request.form['book_copy_id'])
        book_id = int(request.form['book_id'])
        status = request.form['status']

        # Call the BookCopyService method
        result = book_copy_service.update_book_copy(book_copy_id, book_id, status)

        return render_template('update_book_copy_result.html', result=result)

    return render_template('update_book_copy.html')


if __name__ == '__main__':
    app.run(debug=True)
