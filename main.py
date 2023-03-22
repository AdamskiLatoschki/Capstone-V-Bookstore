import sqlite3
from tabulate import tabulate


# ================= Class Book ================
class Book:
    def __init__(self, title, author, qty):
        self.title = title
        self.author = author
        self.qty = qty


# =============== Class BookStore ==============
class BookStore:
    def __init__(self, database):
        self.db = database

    @staticmethod
    def view_all():
        """Function displays all books available in stock if there are any."""

        check_all = db.get_all()
        if check_all:
            headers = ['ID', 'Title', 'Author', 'Qty']
            print(tabulate(check_all, headers=headers, tablefmt='fancy_grid'))
        else:
            switch_message(0)

    @staticmethod
    def add_book():
        """Taking user inputs required to add a new book to stock and validating if input is not empty, or it is
        not a digit."""

        book_title = input('Enter the title of the new book: ').strip().title()
        while not check_str_input(book_title):
            switch_message(1)
            book_title = input('Enter the title of the new book: ').strip().title()

        book_author = input('Enter the author of the new book: ').strip().title()
        while not check_str_input(book_author):
            switch_message(1)
            book_author = input('Enter the author of the new book: ').strip().title()

        book_quantity = input('Enter the quantity of the new book you would like to add to stock: ')
        while not check_int_input(book_quantity):
            switch_message(1)
            book_quantity = input('Enter the quantity of the new book you would like to add to stock: ')

        book = Book(book_title, book_author, book_quantity)
        db.insert_values(book)
        db.db_commit()
        print(f'\nNew book "{book.title}" has been added to stock.')

    @staticmethod
    def search_book():
        """This function allow user to search specific book by title or author."""

        while db.check_if_empty():
            choice = input('\nPlease choose from following options how would you like to search a book:\n'
                           '1 - Search by title\n'
                           '2 - Search by author\n'
                           '0 - Exit to main menu\n'
                           ':')

            if choice == '1':

                subject = 'Title'
                book_title = input('Enter the title of the book you would like to search for: ')
                search(subject, book_title)

            elif choice == '2':
                subject = 'Author'
                book_author = input('Enter the author of the book you would like to search for: ')
                search(subject, book_author)

            elif choice == '0':
                switch_message(2)
                break
            else:
                switch_message(1)

        switch_message(0)

    def delete_book(self):
        """Function deletes chosen book from stock"""

        self.view_all()
        while db.check_if_empty():
            try:
                book_to_remove = int(input('Please enter the book ID you would like to remove from stock:\n'))
                content = db.select_id(book_to_remove)

                if content:
                    choice = input('Are you sure you want to delete this item? Y / N: ').lower()

                    if choice == 'Y'.lower():
                        db.delete_id(book_to_remove)
                        print(f'\nYour chosen book with #ID {book_to_remove} has been removed.')
                        db.db_commit()
                        break

                    elif choice == 'N'.lower():
                        switch_message(2)
                        break
                    else:
                        switch_message(1)
                        continue
                else:
                    switch_message(3)
            except ValueError:
                switch_message(1)

    def update_info(self):
        """Function updates an information for chosen book"""

        self.view_all()
        while db.check_if_empty():
            try:
                chosen_id = int(input('\nPlease enter the book ID you would like to update an information for:\n'))
                content = db.select_id(chosen_id)

                if content:
                    try:
                        new_quantity = int(input('\nPlease enter the new stock quantity for this book: '))
                        db.update_book_qty(new_quantity, chosen_id)

                        print(f'\nStock quantity has been changed to {new_quantity} for your chosen book')
                        break
                    except ValueError:
                        switch_message(1)
                switch_message(3)
            except ValueError:
                switch_message(1)


# =============== Class Database ==============
class Database:
    def __init__(self):
        self.db = sqlite3.connect('bookstore_db')
        self.cursor = self.db.cursor()
        self.create_table()
        self.insert_records()

    def db_commit(self):
        self.db.commit()

    def db_close(self):
        self.db.close()

    def create_table(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS bookstore(ID INTEGER PRIMARY KEY, Title TEXT, '
            'Author TEXT, Qty \n '
            '            INTEGER )')

    def insert_records(self):
        """This function inserts all compulsory books from the list into a table."""

        compulsory_books = [(1, 'A Tale of Two Cities', 'Charles Dickens', 30),
                            (2, 'Harry Potter and the Philosopher`s Stone', 'J.K. Rowling', 40),
                            (3, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
                            (4, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
                            (5, 'Alice in Wonderland', 'Lewis Carroll', 12)]

        self.cursor.executemany(
            '''INSERT OR REPLACE INTO bookstore(ID, Title, Author, Qty) VALUES(?, ?, ?, ?)''',
            compulsory_books)

    def check_if_empty(self):
        records = len(self.get_all())
        if records == 0:
            return False
        return True

    def get_all(self):
        return self.cursor.execute(f'''SELECT * FROM bookstore''').fetchall()

    def insert_values(self, book):
        script = '''INSERT OR IGNORE INTO bookstore(Title, Author, Qty) VALUES (?, ?, 
                        ?)'''
        self.cursor.execute(script, (book.title, book.author, book.qty))

    def get_book(self, subject, word):
        content = []
        for row in self.cursor.execute(
                f'''SELECT * FROM bookstore WHERE {subject} LIKE "%{word}%" '''):
            content.append(row)
        return content

    def select_id(self, value):
        return self.cursor.execute(f'SELECT ID FROM bookstore WHERE ID = {value}').fetchall()

    def delete_id(self, book_to_remove):
        self.cursor.execute(f'''DELETE FROM bookstore WHERE ID = {book_to_remove}''')

    def update_book_qty(self, book_qty, rowid):
        self.cursor.execute(
            f'''UPDATE bookstore SET qty = {book_qty} WHERE rowid = {rowid} ''')


# ================= Functions ================
def check_str_input(value):
    if value == '' or value.isdigit():
        return False
    else:
        return True


def check_int_input(value):
    if str(value).isdigit():
        return True
    else:
        return False


def search(subject, value):
    content = db.get_book(subject, value)
    if content:
        headers = ['ID', 'Title', 'Author', 'Qty']
        print(tabulate(content, headers=headers, tablefmt='fancy_grid'))
    else:
        switch_message(4)


def switch_message(value):
    switcher = {
        0: "\n**********  No books to display.  **********\n",
        1: "\n**********  Invalid input. Please try again.  **********\n",
        2: "\n**********  You are redirecting to the main menu.  **********\n",
        3: "\n**********  This ID does not exist. Please try again.  **********\n",
        4: "\n**********  The book you are looking for cannot be found.  **********\n"
    }
    return print(switcher.get(value))


db = Database()
bookstore = BookStore(db)


def main():
    while True:
        menu = input(f'\nPlease choose an option:\n'
                     '1 - Display all books\n'
                     '2 - Add a new book\n'
                     '3 - Search books\n'
                     '4 - Update book information\n'
                     '5 - Delete a book\n'
                     '0 - Exit\n'
                     ':')
        if menu == '1':
            bookstore.view_all()
        elif menu == '2':
            bookstore.add_book()
        elif menu == '3':
            bookstore.search_book()
        elif menu == '4':
            bookstore.update_info()
        elif menu == '5':
            bookstore.delete_book()
        elif menu == '0':
            print('Thank you')
            db.db_commit()
            db.db.close()
            exit()
        else:
            print('\nInvalid input. Try again!\n')


if __name__ == "__main__":
    main()
