import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

# Book class to handle book operations
class Book:
    def __init__(self, title, author, year, genre, book_id=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

# Library class to manage the collection of books
class Library:
    def __init__(self):
        self.books = []
        self.next_id = 1

    def get_all_books(self):
        return self.books

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def add_book(self, title, author, year, genre):
        book = Book(title, author, year, genre, self.next_id)
        self.books.append(book)
        self.next_id += 1

    def update_book(self, book_id, title, author, year, genre):
        book = self.get_book_by_id(book_id)
        if book:
            book.title = title
            book.author = author
            book.year = year
            book.genre = genre

    def delete_book(self, book_id):
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)

    def search_books(self, search_term, column="title"):
        if column == "title":
            return [book for book in self.books if search_term.lower() in book.title.lower()]
        elif column == "author":
            return [book for book in self.books if search_term.lower() in book.author.lower()]
        elif column == "genre":
            return [book for book in self.books if search_term.lower() in book.genre.lower()]
        return []

# GUI class for Library Management Application
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

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by Title")
        self.search_bar.textChanged.connect(self.search_books)
        self.layout.addWidget(self.search_bar)

        # Search dropdown (filter by Title, Author, Genre)
        self.search_column_dropdown = QComboBox()
        self.search_column_dropdown.addItems(["title", "author", "genre"])
        self.layout.addWidget(self.search_column_dropdown)

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

    def load_books(self):
        books = self.library.get_all_books()
        self.table.setRowCount(len(books))
        for row_idx, book in enumerate(books):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(book.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(book.title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(book.author))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(book.year)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(book.genre))

    def search_books(self):
        search_term = self.search_bar.text()
        search_column = self.search_column_dropdown.currentText()
        books_data = self.library.search_books(search_term, search_column)
        
        self.table.setRowCount(len(books_data))
        for row_idx, book in enumerate(books_data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(book.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(book.title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(book.author))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(book.year)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(book.genre))

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

        self.library.update_book(int(book_id), title, author, year, genre)
        self.load_books()
        self.clear_inputs()

    def delete_book(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "No book selected!")
            return

        book_id = self.table.item(selected, 0).text()

        self.library.delete_book(int(book_id))
        self.load_books()

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
