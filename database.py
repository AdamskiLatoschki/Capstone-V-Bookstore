import sqlite3


# =============== Class Database ==============
class Database:
    """Class to initialise SQlite database."""

    def __init__(self):
        self.db = sqlite3.connect('bookstore_db')
        self.cursor = self.db.cursor()
        self.create_table()
        self.insert_records()
        self.db.commit()

    def db_commit(self):
        self.db.commit()

    def db_close(self):
        self.db.close()

    def create_table(self):
        """Method creates a table with four attributes, like ID, Title, Author and Qty. """
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS bookstore(ID INTEGER PRIMARY KEY, Title TEXT, '
            'Author TEXT, Qty \n '
            '            INTEGER )')

    def insert_records(self):
        """This method inserts all compulsory books from the list into a table."""

        compulsory_books = [(1, 'A Tale of Two Cities', 'Charles Dickens', 30),
                            (2, 'Harry Potter and the Philosopher`s Stone', 'J.K. Rowling', 1),
                            (3, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
                            (4, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
                            (5, 'Alice in Wonderland', 'Lewis Carroll', 4)]

        self.cursor.executemany(
            '''INSERT OR REPLACE INTO bookstore(ID, Title, Author, Qty) VALUES(?, ?, ?, ?)''',
            compulsory_books)

    def check_if_empty(self):
        """Method checks if there are any records in the database"""
        records = len(self.get_all())
        if records == 0:
            return False
        return True

    def get_all(self):
        """Method selects and returns all records from database."""
        return self.cursor.execute(f'''SELECT * FROM bookstore''').fetchall()

    def insert_values(self, book):
        """Method inserts to database parameters passed from other function with user inputs"""
        script = '''INSERT OR IGNORE INTO bookstore(Title, Author, Qty) VALUES (?, ?, 
                        ?)'''
        self.cursor.execute(script, (book.title, book.author, book.qty))

    def get_book(self, subject, word):
        """Method returns a list of selected specific records from database"""
        content = []
        for row in self.cursor.execute(
                f'''SELECT * FROM bookstore WHERE {subject} LIKE "%{word}%" '''):
            content.append(row)
        return content

    def select_id(self, value):
        """Method selects ID column from a table with specified ID"""
        return self.cursor.execute(f'SELECT ID FROM bookstore WHERE ID = {value}').fetchall()

    def delete_id(self, book_to_remove):
        """Method deletes a book from database with selected by user ID"""
        self.cursor.execute(f'''DELETE FROM bookstore WHERE ID = {book_to_remove}''')

    def update_book_qty(self, book_qty, rowid):
        """Method updates qty information for the book with selected ID"""
        self.cursor.execute(
            f'''UPDATE bookstore SET qty = {book_qty} WHERE rowid = {rowid} ''')

    def select_low_stock(self):
        """Method selects books with stock lower than 5"""
        return self.cursor.execute(f'SELECT * FROM bookstore WHERE Qty < 5').fetchall()


db = Database()
