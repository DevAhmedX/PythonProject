import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)

# Database class to handle database operations
class Database:
    def __init__(self, host="127.0.0.1", user="root", password="01026671963", db_name="library"):
        self.db_name = db_name
        self.host = host
        self.user = user
        self.password = password

        # Connect to MySQL server without selecting a database
        self.connection = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password
        )
        self.cursor = self.connection.cursor()

        # Ensure the database exists
        self.create_database_if_not_exists()

        # Now connect to the database
        self.connection.database = self.db_name
        self.setup_database()

    def create_database_if_not_exists(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            self.connection.commit()
            print(f"Database '{self.db_name}' is ready.")
        except mysql.connector.Error as err:
            print(f"Error creating database: {err}")
            self.connection.close()
            exit(1)

    def setup_database(self):
        try:
            # Create the Books table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    year INT,
                    genre VARCHAR(100)
                )
            """)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error setting up database tables: {err}")
            self.connection.close()
            exit(1)

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


# Book class to handle book operations
class Book:
    def __init__(self, title, author, year, genre, book_id=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def save(self, db):
        if self.id:
            db.execute_query("""
                UPDATE Books
                SET title = %s, author = %s, year = %s, genre = %s
                WHERE id = %s
            """, (self.title, self.author, self.year, self.genre, self.id))
        else:
            db.execute_query("""
                INSERT INTO Books (title, author, year, genre)
                VALUES (%s, %s, %s, %s)
            """, (self.title, self.author, self.year, self.genre))

    def delete(self, db):
        if self.id:
            db.execute_query("DELETE FROM Books WHERE id = %s", (self.id,))


# Library class to manage the library system
class Library:
    def __init__(self):
        self.db = Database()

    def get_all_books(self):
        books_data = self.db.fetch_all("SELECT * FROM Books")
        return [Book(*book_data) for book_data in books_data]

    def get_book_by_id(self, book_id):
        book_data = self.db.fetch_all("SELECT * FROM Books WHERE id = %s", (book_id,))
        if book_data:
            return Book(*book_data[0])
        return None

    def add_book(self, title, author, year, genre):
        book = Book(title, author, year, genre)
        book.save(self.db)

    def update_book(self, book_id, title, author, year, genre):
        book = self.get_book_by_id(book_id)
        if book:
            book.title = title
            book.author = author
            book.year = year
            book.genre = genre
            book.save(self.db)

    def delete_book(self, book_id):
        book = self.get_book_by_id(book_id)
        if book:
            book.delete(self.db)


# GUI class to handle user interface
class LibraryManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(200, 200, 800, 600)
        self.library = Library()
        self.initUI()
        self.load_books()

    def initUI(self):
        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Table to display books
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Year", "Genre"])
        self.layout.addWidget(self.table)

        # Buttons for CRUD operations
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Book")
        self.update_button.clicked.connect(self.update_book)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Book")
        self.delete_button.clicked.connect(self.delete_book)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)

        # Form for adding/updating books
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        self.layout.addWidget(self.title_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")
        self.layout.addWidget(self.author_input)

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year")
        self.layout.addWidget(self.year_input)

        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Genre")
        self.layout.addWidget(self.genre_input)

    # Load books into the table
    def load_books(self):
        books = self.library.get_all_books()
        self.table.setRowCount(len(books))
        for row_idx, book in enumerate(books):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(book.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(book.title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(book.author))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(book.year)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(book.genre))

    # Add book to the database
    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()
        genre = self.genre_input.text()

        if not title or not author:
            QMessageBox.warning(self, "Error", "Title and Author cannot be empty!")
            return

        self.library.add_book(title, author, year, genre)
        self.load_books()
        self.clear_inputs()

    # Update selected book
    def update_book(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "No book selected!")
            return

        book_id = self.table.item(selected, 0).text()
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()
        genre = self.genre_input.text()

        self.library.update_book(book_id, title, author, year, genre)
        self.load_books()
        self.clear_inputs()

    # Delete selected book
    def delete_book(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "No book selected!")
            return

        book_id = self.table.item(selected, 0).text()

        self.library.delete_book(book_id)
        self.load_books()

    # Clear input fields
    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.genre_input.clear()


# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryManagementApp()
    window.show()
    sys.exit(app.exec_())




# import sys
# import mysql.connector
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
#     QPushButton, QLineEdit, QHBoxLayout, QDialog, QDialogButtonBox, QFormLayout, QLabel,
#     QSpinBox, QDateEdit, QComboBox
# )
# from PyQt5.QtCore import QDate


# # Database class to handle all database operations
# class Database:
#     def __init__(self, host="127.0.0.1", user="root", password="01026671963", db_name="library"):
#         # Connect to the MySQL database
#         self.connection = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name
#         )
#         self.cursor = self.connection.cursor()
#         self.setup_database()

#     def setup_database(self):
#         # Create the necessary tables
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS Books (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 title VARCHAR(255) NOT NULL,
#                 author VARCHAR(255) NOT NULL,
#                 year INT,
#                 genre VARCHAR(255),
#                 available INT DEFAULT 1
#             )
#         """)
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS Users (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 username VARCHAR(255) NOT NULL UNIQUE,
#                 password VARCHAR(255) NOT NULL
#             )
#         """)
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS BorrowedBooks (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 book_id INT,
#                 user_id INT,
#                 borrow_date DATE,
#                 due_date DATE,
#                 return_date DATE,
#                 FOREIGN KEY (book_id) REFERENCES Books(id),
#                 FOREIGN KEY (user_id) REFERENCES Users(id)
#             )
#         """)
#         self.connection.commit()

#     def execute_query(self, query, params=()):
#         self.cursor.execute(query, params)
#         self.connection.commit()

#     def fetch_all(self, query, params=()):
#         self.cursor.execute(query, params)
#         return self.cursor.fetchall()

#     def fetch_one(self, query, params=()):
#         self.cursor.execute(query, params)
#         return self.cursor.fetchone()

#     def close(self):
#         self.connection.close()


# # Book class to handle book operations
# class Book:
#     def __init__(self, title, author, year, genre, available=True, book_id=None):
#         self.id = book_id
#         self.title = title
#         self.author = author
#         self.year = year
#         self.genre = genre
#         self.available = available

#     def save(self, db):
#         if self.id:
#             db.execute_query("""
#                 UPDATE Books
#                 SET title = %s, author = %s, year = %s, genre = %s, available = %s
#                 WHERE id = %s
#             """, (self.title, self.author, self.year, self.genre, self.available, self.id))
#         else:
#             db.execute_query("""
#                 INSERT INTO Books (title, author, year, genre, available)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (self.title, self.author, self.year, self.genre, self.available))

#     def delete(self, db):
#         if self.id:
#             db.execute_query("DELETE FROM Books WHERE id = %s", (self.id,))

#     @staticmethod
#     def get_all_books(db):
#         books_data = db.fetch_all("SELECT * FROM Books")
#         return [Book(*book_data) for book_data in books_data]

#     @staticmethod
#     def search_books(db, search_term, column="title"):
#         search_query = f"SELECT * FROM Books WHERE {column} LIKE %s"
#         books_data = db.fetch_all(search_query, ('%' + search_term + '%',))
#         return [Book(*book_data) for book_data in books_data]


# # Library class to manage the collection of books
# class Library:
#     def __init__(self):
#         self.db = Database()

#     def get_all_books(self):
#         return Book.get_all_books(self.db)

#     def search_books(self, search_term, column="title"):
#         return Book.search_books(self.db, search_term, column)

#     def add_book(self, title, author, year, genre):
#         book = Book(title, author, year, genre)
#         book.save(self.db)

#     def update_book(self, book_id, title, author, year, genre, available):
#         book = Book(title, author, year, genre, available, book_id)
#         book.save(self.db)

#     def delete_book(self, book_id):
#         book = self.get_book_by_id(book_id)
#         if book:
#             book.delete(self.db)

#     def get_book_by_id(self, book_id):
#         books = self.get_all_books()
#         for book in books:
#             if book.id == book_id:
#                 return book
#         return None


# # GUI class for Library Management Application
# class LibraryManagementApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Library Management System")
#         self.setGeometry(200, 200, 1000, 800)
#         self.library = Library()
#         self.initUI()
#         self.load_books()

#     def initUI(self):
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout(self.central_widget)

#         # Table to display books
#         self.table = QTableWidget()
#         self.table.setColumnCount(6)
#         self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Year", "Genre", "Available"])
#         self.layout.addWidget(self.table)

#         # Search bar
#         self.search_bar = QLineEdit()
#         self.search_bar.setPlaceholderText("Search by Title")
#         self.search_bar.textChanged.connect(self.search_books)
#         self.layout.addWidget(self.search_bar)

#         # Buttons for CRUD operations
#         button_layout = QHBoxLayout()

#         self.add_button = QPushButton("Add Book")
#         self.add_button.clicked.connect(self.add_book)
#         button_layout.addWidget(self.add_button)

#         self.update_button = QPushButton("Update Book")
#         self.update_button.clicked.connect(self.update_book)
#         button_layout.addWidget(self.update_button)

#         self.delete_button = QPushButton("Delete Book")
#         self.delete_button.clicked.connect(self.delete_book)
#         button_layout.addWidget(self.delete_button)

#         self.layout.addLayout(button_layout)

#     def load_books(self):
#         books = self.library.get_all_books()
#         self.table.setRowCount(len(books))
#         for i, book in enumerate(books):
#             self.table.setItem(i, 0, QTableWidgetItem(str(book.id)))
#             self.table.setItem(i, 1, QTableWidgetItem(book.title))
#             self.table.setItem(i, 2, QTableWidgetItem(book.author))
#             self.table.setItem(i, 3, QTableWidgetItem(str(book.year)))
#             self.table.setItem(i, 4, QTableWidgetItem(book.genre))
#             self.table.setItem(i, 5, QTableWidgetItem("Yes" if book.available else "No"))

#     def search_books(self):
#         search_term = self.search_bar.text()
#         books = self.library.search_books(search_term)
#         self.table.setRowCount(len(books))
#         for i, book in enumerate(books):
#             self.table.setItem(i, 0, QTableWidgetItem(str(book.id)))
#             self.table.setItem(i, 1, QTableWidgetItem(book.title))
#             self.table.setItem(i, 2, QTableWidgetItem(book.author))
#             self.table.setItem(i, 3, QTableWidgetItem(str(book.year)))
#             self.table.setItem(i, 4, QTableWidgetItem(book.genre))
#             self.table.setItem(i, 5, QTableWidgetItem("Yes" if book.available else "No"))

#     def add_book(self):
#         dialog = BookDialog(self)
#         if dialog.exec_():
#             title, author, year, genre = dialog.get_values()
#             self.library.add_book(title, author, year, genre)
#             self.load_books()

#     def update_book(self):
#         row = self.table.currentRow()
#         if row == -1:
#             return
#         book_id = int(self.table.item(row, 0).text())
#         title = self.table.item(row, 1).text()
#         author = self.table.item(row, 2).text()
#         year = int(self.table.item(row, 3).text())
#         genre = self.table.item(row, 4).text()
#         available = self.table.item(row, 5).text() == "Yes"
#         self.library.update_book(book_id, title, author, year, genre, available)
#         self.load_books()

#     def delete_book(self):
#         row = self.table.currentRow()
#         if row == -1:
#             return
#         book_id = int(self.table.item(row, 0).text())
#         self.library.delete_book(book_id)
#         self.load_books()


# class BookDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Add Book")
#         self.setGeometry(300, 300, 300, 200)
#         self.initUI()

#     def initUI(self):
#         self.form_layout = QFormLayout(self)

#         self.title_input = QLineEdit()
#         self.author_input = QLineEdit()
#         self.year_input = QSpinBox()
#         self.year_input.setRange(1900, 2024)
#         self.genre_input = QLineEdit()

#         self.form_layout.addRow("Title:", self.title_input)
#         self.form_layout.addRow("Author:", self.author_input)
#         self.form_layout.addRow("Year:", self.year_input)
#         self.form_layout.addRow("Genre:", self.genre_input)

#         button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         button_box.accepted.connect(self.accept)
#         button_box.rejected.connect(self.reject)

#         self.form_layout.addRow(button_box)

#     def get_values(self):
#         return self.title_input.text(), self.author_input.text(), self.year_input.value(), self.genre_input.text()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = LibraryManagementApp()
#     window.show()
#     sys.exit(app.exec_())
