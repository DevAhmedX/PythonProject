# import sys
# import mysql.connector
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
#     QPushButton, QLineEdit, QHBoxLayout, QMessageBox
# )

# # Database class to handle database operations
# class Database:
#     def __init__(self, host="localhost", user="root", password="", db_name="library"):
#         self.db_name = db_name
#         self.connection = mysql.connector.connect(
#             host=host, user=user, password=password, database=db_name
#         )
#         self.cursor = self.connection.cursor()
#         self.setup_database()

#     def setup_database(self):
#         # Create the Books table if it doesn't exist
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS Books (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 title VARCHAR(255) NOT NULL,
#                 author VARCHAR(255) NOT NULL,
#                 year INT,
#                 genre VARCHAR(100)
#             )
#         """)
#         self.connection.commit()

#     def execute_query(self, query, params=()):
#         self.cursor.execute(query, params)
#         self.connection.commit()

#     def fetch_all(self, query, params=()):
#         self.cursor.execute(query, params)
#         return self.cursor.fetchall()

#     def close(self):
#         self.connection.close()

# # Book class to handle book operations
# class Book:
#     def __init__(self, title, author, year, genre, book_id=None):
#         self.id = book_id
#         self.title = title
#         self.author = author
#         self.year = year
#         self.genre = genre

#     def save(self, db):
#         if self.id:
#             db.execute_query("""
#                 UPDATE Books
#                 SET title = ?, author = ?, year = ?, genre = ?
#                 WHERE id = ?
#             """, (self.title, self.author, self.year, self.genre, self.id))
#         else:
#             db.execute_query("""
#                 INSERT INTO Books (title, author, year, genre)
#                 VALUES (%s, %s, %s, %s)
#             """, (self.title, self.author, self.year, self.genre))

#     def delete(self, db):
#         if self.id:
#             db.execute_query("DELETE FROM Books WHERE id = %s", (self.id,))

# # Library class to manage the library system
# class Library:
#     def __init__(self):
#         self.db = Database()

#     def get_all_books(self):
#         books_data = self.db.fetch_all("SELECT * FROM Books")
#         return [Book(*book_data) for book_data in books_data]

#     def get_book_by_id(self, book_id):
#         book_data = self.db.fetch_all("SELECT * FROM Books WHERE id = %s", (book_id,))
#         if book_data:
#             return Book(*book_data[0])
#         return None

#     def add_book(self, title, author, year, genre):
#         book = Book(title, author, year, genre)
#         book.save(self.db)

#     def update_book(self, book_id, title, author, year, genre):
#         book = self.get_book_by_id(book_id)
#         if book:
#             book.title = title
#             book.author = author
#             book.year = year
#             book.genre = genre
#             book.save(self.db)

#     def delete_book(self, book_id):
#         book = self.get_book_by_id(book_id)
#         if book:
#             book.delete(self.db)

# # GUI class to handle user interface
# class LibraryManagementApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Library Management System")
#         self.setGeometry(200, 200, 800, 600)
#         self.library = Library()
#         self.initUI()
#         self.load_books()

#     def initUI(self):
#         # Main layout
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout(self.central_widget)

#         # Table to display books
#         self.table = QTableWidget()
#         self.table.setColumnCount(5)
#         self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Year", "Genre"])
#         self.layout.addWidget(self.table)

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

#         # Form for adding/updating books
#         self.title_input = QLineEdit()
#         self.title_input.setPlaceholderText("Title")
#         self.layout.addWidget(self.title_input)

#         self.author_input = QLineEdit()
#         self.author_input.setPlaceholderText("Author")
#         self.layout.addWidget(self.author_input)

#         self.year_input = QLineEdit()
#         self.year_input.setPlaceholderText("Year")
#         self.layout.addWidget(self.year_input)

#         self.genre_input = QLineEdit()
#         self.genre_input.setPlaceholderText("Genre")
#         self.layout.addWidget(self.genre_input)

#     # Load books into the table
#     def load_books(self):
#         books = self.library.get_all_books()
#         self.table.setRowCount(len(books))
#         for row_idx, book in enumerate(books):
#             self.table.setItem(row_idx, 0, QTableWidgetItem(str(book.id)))
#             self.table.setItem(row_idx, 1, QTableWidgetItem(book.title))
#             self.table.setItem(row_idx, 2, QTableWidgetItem(book.author))
#             self.table.setItem(row_idx, 3, QTableWidgetItem(str(book.year)))
#             self.table.setItem(row_idx, 4, QTableWidgetItem(book.genre))

#     # Add book to the database
#     def add_book(self):
#         title = self.title_input.text()
#         author = self.author_input.text()
#         year = self.year_input.text()
#         genre = self.genre_input.text()

#         if not title or not author:
#             QMessageBox.warning(self, "Error", "Title and Author cannot be empty!")
#             return

#         self.library.add_book(title, author, year, genre)
#         self.load_books()
#         self.clear_inputs()

#     # Update selected book
#     def update_book(self):
#         selected = self.table.currentRow()
#         if selected < 0:
#             QMessageBox.warning(self, "Error", "No book selected!")
#             return

#         book_id = self.table.item(selected, 0).text()
#         title = self.title_input.text()
#         author = self.author_input.text()
#         year = self.year_input.text()
#         genre = self.genre_input.text()

#         self.library.update_book(book_id, title, author, year, genre)
#         self.load_books()
#         self.clear_inputs()

#     # Delete selected book
#     def delete_book(self):
#         selected = self.table.currentRow()
#         if selected < 0:
#             QMessageBox.warning(self, "Error", "No book selected!")
#             return

#         book_id = self.table.item(selected, 0).text()

#         self.library.delete_book(book_id)
#         self.load_books()

#     # Clear input fields
#     def clear_inputs(self):
#         self.title_input.clear()
#         self.author_input.clear()
#         self.year_input.clear()
#         self.genre_input.clear()

# # Main application
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LibraryManagementApp()
#     window.show()
#     sys.exit(app.exec_())




















# import sys
# import mysql.connector
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
#     QPushButton, QLineEdit, QHBoxLayout, QComboBox, QMessageBox
# )
# from PyQt5.QtCore import Qt

# # Database class to handle all database operations
# class Database:
#     def __init__(self, host="localhost", user="root", password="", db_name="library"):
#         self.db_name = db_name
#         self.connection = mysql.connector.connect(
#             host=host, user=user, password=password, database=db_name
#         )
#         self.cursor = self.connection.cursor()
#         self.setup_database()

#     def setup_database(self):
#         # Create the Books table if it doesn't exist
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS Books (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 title VARCHAR(255) NOT NULL,
#                 author VARCHAR(255) NOT NULL,
#                 year INT,
#                 genre VARCHAR(100)
#             )
#         """)
#         self.connection.commit()

#     def execute_query(self, query, params=()):
#         self.cursor.execute(query, params)
#         self.connection.commit()

#     def fetch_all(self, query, params=()):
#         self.cursor.execute(query, params)
#         return self.cursor.fetchall()

#     def close(self):
#         self.connection.close()

# # Book class to handle book operations
# class Book:
#     def __init__(self, title, author, year, genre, book_id=None):
#         self.id = book_id
#         self.title = title
#         self.author = author
#         self.year = year
#         self.genre = genre

#     def save(self, db):
#         if self.id:
#             db.execute_query("""
#                 UPDATE Books
#                 SET title = %s, author = %s, year = %s, genre = %s
#                 WHERE id = %s
#             """, (self.title, self.author, self.year, self.genre, self.id))
#         else:
#             db.execute_query("""
#                 INSERT INTO Books (title, author, year, genre)
#                 VALUES (%s, %s, %s, %s)
#             """, (self.title, self.author, self.year, self.genre))

#     def delete(self, db):
#         if self.id:
#             db.execute_query("DELETE FROM Books WHERE id = %s", (self.id,))

# # Library class to manage the collection of books
# class Library:
#     def __init__(self):
#         self.db = Database()

#     def get_all_books(self):
#         books_data = self.db.fetch_all("SELECT * FROM Books")
#         return [Book(*book_data) for book_data in books_data]

#     def get_book_by_id(self, book_id):
#         book_data = self.db.fetch_all("SELECT * FROM Books WHERE id = %s", (book_id,))
#         if book_data:
#             return Book(*book_data[0])
#         return None

#     def add_book(self, title, author, year, genre):
#         book = Book(title, author, year, genre)
#         book.save(self.db)

#     def update_book(self, book_id, title, author, year, genre):
#         book = self.get_book_by_id(book_id)
#         if book:
#             book.title = title
#             book.author = author
#             book.year = year
#             book.genre = genre
#             book.save(self.db)

#     def delete_book(self, book_id):
#         book = self.get_book_by_id(book_id)
#         if book:
#             book.delete(self.db)

#     def search_books(self, search_term, column="title"):
#         search_query = f"SELECT * FROM Books WHERE {column} LIKE %s"
#         return self.db.fetch_all(search_query, ('%' + search_term + '%',))

# # GUI class for Library Management Application
# class LibraryManagementApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Library Management System")
#         self.setGeometry(200, 200, 800, 600)
#         self.library = Library()
#         self.initUI()
#         self.load_books()

#     def initUI(self):
#         # Main layout
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout(self.central_widget)

#         # Table to display books
#         self.table = QTableWidget()
#         self.table.setColumnCount(5)
#         self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Year", "Genre"])
#         self.layout.addWidget(self.table)

#         # Search bar
#         self.search_bar = QLineEdit()
#         self.search_bar.setPlaceholderText("Search by Title")
#         self.search_bar.textChanged.connect(self.search_books)
#         self.layout.addWidget(self.search_bar)

#         # Search dropdown (filter by Title, Author, Genre)
#         self.search_column_dropdown = QComboBox()
#         self.search_column_dropdown.addItems(["title", "author", "genre"])
#         self.layout.addWidget(self.search_column_dropdown)

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

#         # Form for adding/updating books
#         self.title_input = QLineEdit()
#         self.title_input.setPlaceholderText("Title")
#         self.layout.addWidget(self.title_input)

#         self.author_input = QLineEdit()
#         self.author_input.setPlaceholderText("Author")
#         self.layout.addWidget(self.author_input)

#         self.year_input = QLineEdit()
#         self.year_input.setPlaceholderText("Year")
#         self.layout.addWidget(self.year_input)

#         self.genre_input = QLineEdit()
#         self.genre_input.setPlaceholderText("Genre")
#         self.layout.addWidget(self.genre_input)

#     def load_books(self):
#         books = self.library.get_all_books()
#         self.table.setRowCount(len(books))
#         for row_idx, book in enumerate(books):
#             self.table.setItem(row_idx, 0, QTableWidgetItem(str(book.id)))
#             self.table.setItem(row_idx, 1, QTableWidgetItem(book.title))
#             self.table.setItem(row_idx, 2, QTableWidgetItem(book.author))
#             self.table.setItem(row_idx, 3, QTableWidgetItem(str(book.year)))
#             self.table.setItem(row_idx, 4, QTableWidgetItem(book.genre))

#     def search_books(self):
#         search_term = self.search_bar.text()
#         search_column = self.search_column_dropdown.currentText()
#         books_data = self.library.search_books(search_term, search_column)
        
#         self.table.setRowCount(len(books_data))
#         for row_idx, book in enumerate(books_data):
#             self.table.setItem(row_idx, 0, QTableWidgetItem(str(book[0])))
#             self.table.setItem(row_idx, 1, QTableWidgetItem(book[1]))
#             self.table.setItem(row_idx, 2, QTableWidgetItem(book[2]))
#             self.table.setItem(row_idx, 3, QTableWidgetItem(str(book[3])))
#             self.table.setItem(row_idx, 4, QTableWidgetItem(book[4]))

#     def add_book(self):
#         title = self.title_input.text()
#         author = self.author_input.text()
#         year = self.year_input.text()
#         genre = self.genre_input.text()

#         if not title or not author:
#             QMessageBox.warning(self, "Error", "Title and Author cannot be empty!")
#             return

#         self.library.add_book(title, author, year, genre)
#         self.load_books()
#         self.clear_inputs()

#     def update_book(self):
#         selected = self.table.currentRow()
#         if selected < 0:
#             QMessageBox.warning(self, "Error", "No book selected!")
#             return

#         book_id = self.table.item(selected, 0).text()
#         title = self.title_input.text()
#         author = self.author_input.text()
#         year = self.year_input.text()
#         genre = self.genre_input.text()

#         self.library.update_book(book_id, title, author, year, genre)
#         self.load_books()
#         self.clear_inputs()

#     def delete_book(self):
#         selected = self.table.currentRow()
#         if selected < 0:
#             QMessageBox.warning(self, "Error", "No book selected!")
#             return

#         book_id = self.table.item(selected, 0).text()

#         self.library.delete_book(book_id)
#         self.load_books()

#     def clear_inputs(self):
#         self.title_input.clear()
#         self.author_input.clear()
#         self.year_input.clear()
#         self.genre_input.clear()

# # Main application
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LibraryManagementApp()
#     window.show()
#     sys.exit(app.exec_())























###############################################################################################
# import sys
# import mysql.connector
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
#     QPushButton, QLineEdit, QHBoxLayout, QComboBox, QMessageBox, QDialog, QDialogButtonBox,
#     QLabel, QFormLayout, QDateEdit
# )
# from PyQt5.QtCore import QDate

# # Database class to handle all database operations
# class Database:
#     def __init__(self, host="localhost", user="root", password="", db_name="library"):
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

# # User class to manage user operations
# class User:
#     def __init__(self, username, password, user_id=None):
#         self.id = user_id
#         self.username = username
#         self.password = password

#     def save(self, db):
#         if self.id:
#             db.execute_query("""
#                 UPDATE Users
#                 SET username = ?, password = ?
#                 WHERE id = ?
#             """, (self.username, self.password, self.id))
#         else:
#             db.execute_query("""
#                 INSERT INTO Users (username, password)
#                 VALUES (?, ?)
#             """, (self.username, self.password))

#     def delete(self, db):
#         if self.id:
#             db.execute_query("DELETE FROM Users WHERE id = ?", (self.id,))

#     @staticmethod
#     def get_user_by_username(db, username):
#         user_data = db.fetch_one("SELECT * FROM Users WHERE username = ?", (username,))
#         if user_data:
#             return User(user_data[1], user_data[2], user_data[0])
#         return None

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
#                 SET title = ?, author = ?, year = ?, genre = ?, available = ?
#                 WHERE id = ?
#             """, (self.title, self.author, self.year, self.genre, self.available, self.id))
#         else:
#             db.execute_query("""
#                 INSERT INTO Books (title, author, year, genre, available)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (self.title, self.author, self.year, self.genre, self.available))

#     def delete(self, db):
#         if self.id:
#             db.execute_query("DELETE FROM Books WHERE id = ?", (self.id,))

#     @staticmethod
#     def get_all_books(db):
#         books_data = db.fetch_all("SELECT * FROM Books")
#         return [Book(*book_data) for book_data in books_data]

#     @staticmethod
#     def search_books(db, search_term, column="title"):
#         search_query = f"SELECT * FROM Books WHERE {column} LIKE %s"
#         books_data = db.fetch_all(search_query, ('%' + search_term + '%',))
#         return [Book(*book_data) for book_data in books_data]

# # BorrowedBook class to manage borrowing
# class BorrowedBook:
#     def __init__(self, book_id, user_id, borrow_date, due_date, return_date=None, borrowed_id=None):
#         self.id = borrowed_id
#         self.book_id = book_id
#         self.user_id = user_id
#         self.borrow_date = borrow_date
#         self.due_date = due_date
#         self.return_date = return_date

#     def save(self, db):
#         if self.id:
#             db.execute_query("""
#                 UPDATE BorrowedBooks
#                 SET book_id = ?, user_id = ?, borrow_date = ?, due_date = ?, return_date = ?
#                 WHERE id = ?
#             """, (self.book_id, self.user_id, self.borrow_date, self.due_date, self.return_date, self.id))
#         else:
#             db.execute_query("""
#                 INSERT INTO BorrowedBooks (book_id, user_id, borrow_date, due_date, return_date)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (self.book_id, self.user_id, self.borrow_date, self.due_date, self.return_date))

#     @staticmethod
#     def get_all_borrowed_books(db):
#         borrowed_books_data = db.fetch_all("SELECT * FROM BorrowedBooks")
#         return [BorrowedBook(*data) for data in borrowed_books_data]

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

#     def borrow_book(self, user_id, book_id, due_date):
#         borrow_date = QDate.currentDate().toString("yyyy-MM-dd")
#         borrowed_book = BorrowedBook(book_id, user_id, borrow_date, due_date)
#         borrowed_book.save(self.db)

#     def return_book(self, borrowed_id):
#         return_date = QDate.currentDate().toString("yyyy-MM-dd")
#         self.db.execute_query("""
#             UPDATE BorrowedBooks
#             SET return_date = ?
#             WHERE id = ?
#         """, (return_date, borrowed_id))

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

#         self.borrow_button = QPushButton("Borrow Book")
#         self.borrow_button.clicked.connect(self.borrow_book)
#         button_layout.addWidget(self.borrow_button)

#         self.layout.addLayout(button_layout)

#     def load_books(self):
#         self.table.setRowCount(0)
#         books = self.library.get_all_books()
#         for row, book in enumerate(books):
#             self.table.insertRow(row)
#             self.table.setItem(row, 0, QTableWidgetItem(str(book.id)))
#             self.table.setItem(row, 1, QTableWidgetItem(book.title))
#             self.table.setItem(row, 2, QTableWidgetItem(book.author))
#             self.table.setItem(row, 3, QTableWidgetItem(str(book.year)))
#             self.table.setItem(row, 4, QTableWidgetItem(book.genre))
#             self.table.setItem(row, 5, QTableWidgetItem("Yes" if book.available else "No"))

#     def search_books(self):
#         search_term = self.search_bar.text()
#         books = self.library.search_books(search_term)
#         self.table.setRowCount(0)
#         for row, book in enumerate(books):
#             self.table.insertRow(row)
#             self.table.setItem(row, 0, QTableWidgetItem(str(book.id)))
#             self.table.setItem(row, 1, QTableWidgetItem(book.title))
#             self.table.setItem(row, 2, QTableWidgetItem(book.author))
#             self.table.setItem(row, 3, QTableWidgetItem(str(book.year)))
#             self.table.setItem(row, 4, QTableWidgetItem(book.genre))
#             self.table.setItem(row, 5, QTableWidgetItem("Yes" if book.available else "No"))

#     def add_book(self):
#         # Show dialog for adding a new book
#         pass

#     def update_book(self):
#         # Show dialog for updating a selected book
#         pass

#     def delete_book(self):
#         # Show dialog for deleting a selected book
#         pass

#     def borrow_book(self):
#         # Show dialog for borrowing a book
#         pass

# # Main code to run the application
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = LibraryManagementApp()
#     window.show()
#     sys.exit(app.exec_())

