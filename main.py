import sqlite3
import tabulate

# ================= Class Book ================
class Book:
    def __init__(self, Title, Author, Qty):
        self.Title = Title
        self.Author = Author
        self.Qty = Qty


# =============== Class BookStore ==============
class BookStore:
    def __init__(self, database):
        self.db = database

    def view_all(self):
        """Function displays all books available in stock if there are any."""

        check_all = db.get_all()
        # headers = ['ID', 'Title', 'Author', 'Qty']
        # print(tabulate(check_all, headers=headers, tablefmt='fancy_grid'))
        if not check_all:
            print('\nNothing to display')
        else:
            for row in check_all:
                print(row)

    def add_book(self):
        """Taking user inputs required to add a new book to stock and validating if input is not empty, or it is
        not a digit."""

        book_title = input('Enter the title of the new book: ').strip().title()
        while check_str_input(book_title) is False:
            print('Invalid input. Please try again.')
            book_title = input('Enter the title of the new book: ').strip().title()

        book_author = input('Enter the author of the new book: ').strip().title()
        while check_str_input(book_author) is False:
            print('Invalid input. Please try again.')
            book_author = input('Enter the author of the new book: ').strip().title()

        book_quantity = input('Enter the quantity of the new book you would like to add to stock: ')
        while check_int_input(book_quantity) is False:
            print('Invalid input. Please try again.')
            book_quantity = input('Enter the quantity of the new book you would like to add to stock: ')

        book = Book(book_title, book_author, book_quantity)
        db.insert_values(book)

        print(f'\nNew book "{book.Title}" has been added to stock.')

    def search_book(self):
        """This function allow user to search specific book by title or author."""

        while db.check_if_empty() is True:
            choice = input('\nPlease choose from following options how would you like to search a book:\n'
                           '1 - Search by title\n'
                           '2 - Search by author\n'
                           '0 - Exit to main menu\n'
                           ':')

            if choice == '1':
                book_title = input('Enter the title of the book you would like to search for: ')
                search_book_by_title(book_title)

            elif choice == '2':
                book_author = input('Enter the author of the book you would like to search for: ')
                search_book_by_author(book_author)

            elif choice == '0':
                print('You are redirecting to the main menu')
                break

            else:
                print('\nInvalid input. Try again!\n')

    def delete_book(self):
        """Function deletes chosen book from stock"""

        self.view_all()
        while db.check_if_empty() is True:
            try:
                book_to_remove = int(input('Please enter the book ID you would like to remove from stock:\n'))
                content = db.select_id(book_to_remove)

                if content:
                    choice = input('Are you sure you want to delete this item? Y / N: ').lower()

                    if choice == 'Y'.lower():
                        db.delete_id(book_to_remove)
                        print(f'\nYour chosen book with #ID {book_to_remove} has been removed.')
                        break

                    elif choice == 'N'.lower():
                        print('\nYou have decided to not delete any book. You are redirecting to the main menu')
                        break

                    else:
                        print('Invalid input! Try again!')
                        continue

                else:
                    print('This ID does not exist. Please try again!')

            except ValueError:
                print('\nInvalid input. Try again!\n')

    def update_info(self):
        """Function takes user input and update an information for chosen book"""

        self.view_all()
        while db.check_if_empty() is True:
            try:
                chosen_id = int(input('\nPlease enter the book ID you would like to update an information for:\n'))
                # check_int_input(chosen_id)
                content = db.select_id(chosen_id)

                if content:
                    try:
                        new_quantity = int(input('\nPlease enter the new stock quantity for this book: '))

                        db.update_book_qty(new_quantity, chosen_id)
                        print(f'\nStock quantity has been changed to {new_quantity} for your chosen book')
                        break
                    except ValueError:
                        print('Invalid input. Please try again!')

            except ValueError:
                print('This ID does not exist. Please try again!')

# =============== Class Database ==============
class Database:
    def __init__(self):
        self.db = sqlite3.connect('bookstore_db')
        self.cursor = self.db.cursor()
        self.create_table()
        self.insert_records()
        self.db.commit()

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
        records = len(self.cursor.execute(f'''SELECT * FROM bookstore''').fetchall())
        if records == 0:
            return False
        return True

    def get_all(self):
        return self.cursor.execute(f'''SELECT * FROM bookstore''').fetchall()

    def insert_values(self, book):
        script = '''INSERT OR IGNORE INTO bookstore(Title, Author, Qty) VALUES (?, ?, 
                        ?)'''
        self.cursor.execute(script, (book.Title, book.Author, book.Qty))

    def get_title(self, value):
        content = []
        for row in self.cursor.execute(
                f'''SELECT * FROM bookstore WHERE Title LIKE "%{value}%" '''):
            content.append(row)
        return content

    def get_author(self, value):
        content = []
        for row in self.cursor.execute(
                f'''SELECT * FROM bookstore WHERE Author LIKE "%{value}%" '''):
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

def search_book_by_title(value):
    content = db.get_title(value)
    headers = ['ID', 'Title', 'Author', 'Qty']
    print(tabulate(content, headers=headers, tablefmt='fancy_grid'))
    if not content:
        print('\nThe book you are looking for cannot be found.\n')

def search_book_by_author(value):
    content = db.get_author(value)
    headers = ['ID', 'Title', 'Author', 'Qty']
    print(tabulate(content, headers=headers, tablefmt='fancy_grid'))
    if not content:
        print('\nThe book you are looking for cannot be found.\n')


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
            exit()
        else:
            print('\nInvalid input. Try again!\n')


if __name__ == "__main__":
    main()
