import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets

# Database connection functions
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",         # Your MySQL username
        password="01026671963", # Your MySQL password
        database="library"
    )

def execute_query(query, params=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    conn.commit()
    cursor.close()
    conn.close()

def fetch_query(query, params=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# CRUD Operations
def add_book(title, author, genre, year, quantity):
    query = "INSERT INTO books (title, author, genre, year, quantity) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query, (title, author, genre, year, quantity))

def update_book(book_id, title, author, genre, year, quantity):
    query = "UPDATE books SET title=%s, author=%s, genre=%s, year=%s, quantity=%s WHERE book_id=%s"
    execute_query(query, (title, author, genre, year, quantity, book_id))

def delete_book(book_id):
    query = "DELETE FROM books WHERE book_id=%s"
    execute_query(query, (book_id,))

def fetch_books():
    query = "SELECT * FROM books"
    return fetch_query(query)

# PyQt5 GUI
class LibraryApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        # Layout and Widgets
        self.layout = QtWidgets.QVBoxLayout()

        # Table View
        self.table_widget = QtWidgets.QTableWidget(self)
        self.layout.addWidget(self.table_widget)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Title", "Author", "Genre", "Year", "Quantity"])

        # Add Book Button
        self.add_button = QtWidgets.QPushButton("Add Book", self)
        self.add_button.clicked.connect(self.show_add_book_window)
        self.layout.addWidget(self.add_button)

        # Update Book Button
        self.update_button = QtWidgets.QPushButton("Update Book", self)
        self.update_button.clicked.connect(self.show_update_book_window)
        self.layout.addWidget(self.update_button)

        # Delete Book Button
        self.delete_button = QtWidgets.QPushButton("Delete Book", self)
        self.delete_button.clicked.connect(self.delete_book)
        self.layout.addWidget(self.delete_button)

        self.refresh_data()

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def refresh_data(self):
        self.table_widget.setRowCount(0)
        books = fetch_books()
        for row, book in enumerate(books):
            self.table_widget.insertRow(row)
            for col, data in enumerate(book):
                self.table_widget.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

    def show_add_book_window(self):
        self.add_book_window = AddBookWindow(self)
        self.add_book_window.show()

    def show_update_book_window(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            book_id = self.table_widget.item(selected_row, 0).text()
            self.update_book_window = UpdateBookWindow(self, book_id)
            self.update_book_window.show()

    def delete_book(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            book_id = self.table_widget.item(selected_row, 0).text()
            delete_book(book_id)
            self.refresh_data()

class AddBookWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Book")
        self.setGeometry(200, 200, 400, 300)

        layout = QtWidgets.QFormLayout()

        self.title_input = QtWidgets.QLineEdit(self)
        self.author_input = QtWidgets.QLineEdit(self)
        self.genre_input = QtWidgets.QLineEdit(self)
        self.year_input = QtWidgets.QSpinBox(self)
        self.quantity_input = QtWidgets.QSpinBox(self)

        layout.addRow("Title:", self.title_input)
        layout.addRow("Author:", self.author_input)
        layout.addRow("Genre:", self.genre_input)
        layout.addRow("Year:", self.year_input)
        layout.addRow("Quantity:", self.quantity_input)

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_book)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        year = self.year_input.value()
        quantity = self.quantity_input.value()

        add_book(title, author, genre, year, quantity)
        self.parent().refresh_data()
        self.close()

class UpdateBookWindow(QtWidgets.QWidget):
    def __init__(self, parent, book_id):
        super().__init__(parent)
        self.setWindowTitle("Update Book")
        self.setGeometry(200, 200, 400, 300)

        self.book_id = book_id

        layout = QtWidgets.QFormLayout()

        self.title_input = QtWidgets.QLineEdit(self)
        self.author_input = QtWidgets.QLineEdit(self)
        self.genre_input = QtWidgets.QLineEdit(self)
        self.year_input = QtWidgets.QSpinBox(self)
        self.quantity_input = QtWidgets.QSpinBox(self)

        layout.addRow("Title:", self.title_input)
        layout.addRow("Author:", self.author_input)
        layout.addRow("Genre:", self.genre_input)
        layout.addRow("Year:", self.year_input)
        layout.addRow("Quantity:", self.quantity_input)

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_updated_book)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_book_data()

    def load_book_data(self):
        query = "SELECT * FROM books WHERE book_id=%s"
        book_data = fetch_query(query, (self.book_id,))
        if book_data:
            book = book_data[0]
            self.title_input.setText(book[1])
            self.author_input.setText(book[2])
            self.genre_input.setText(book[3])
            self.year_input.setValue(book[4])
            self.quantity_input.setValue(book[5])

    def save_updated_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        year = self.year_input.value()
        quantity = self.quantity_input.value()

        update_book(self.book_id, title, author, genre, year, quantity)
        self.parent().refresh_data()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
