import sqlite3
from tabulate import tabulate
import csv


# TODO Check if entered book title already exists in database.
# TODO Separate classes to modules.
# TODO Use Sphinx to create a documentations
# TODO Create a function to send an email and order more books ( use smtplib library ) - in progress.
# TODO Create GUI using Tkinter.


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

    def view_all(self):
        """Function displays all books available in stock if there are any."""
        check_all = self.db.get_all()
        if check_all:
            print_tabulate(check_all)
        else:
            switch_message(0)

    def add_book(self):
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

        book_quantity = input('Enter the quantity of the new book you would like to add to stock: ').strip()
        while not check_int_input(book_quantity):
            switch_message(1)
            book_quantity = input('Enter the quantity of the new book you would like to add to stock: ').strip()

        book = Book(book_title, book_author, book_quantity)
        self.db.insert_values(book)
        self.db.db_commit()
        print(f'\nNew book "{book.title}" has been added to stock.')

    def search_book(self):
        """This function allow user to search specific book by title or author."""

        while self.db.check_if_empty():
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
                        print(f'\nYour chosen book with #ID{book_to_remove} has been removed.')
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

    @staticmethod
    def show_low_stock():
        """Function prints selected low stock books and write to file"""
        content = db.select_low_stock()
        if content:
            print_tabulate(content)
        else:
            switch_message(0)

    @staticmethod
    def generate_report():
        while True:
            choice = input(f'What type of the file would you like to generate a report to? :\n'
                           '1 - CSV\n'
                           '2 - TXT\n'
                           ':')
            match choice:
                case '1':
                    write_to_csv()
                    switch_message(5)
                    break
                case '2':
                    write_to_txt()
                    switch_message(5)
                    break
                case _:
                    switch_message(2)
                    break


# =============== Class Database ==============
class Database:
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
        """Method returns a list of selected records from database"""
        content = []
        for row in self.cursor.execute(
                f'''SELECT * FROM bookstore WHERE {subject} LIKE "%{word}%" '''):
            content.append(row)
        return content

    def select_id(self, value):
        """Method selects ID column from a table with specified ID"""
        return self.cursor.execute(f'SELECT ID FROM bookstore WHERE ID = {value}').fetchall()

    def delete_id(self, book_to_remove):
        self.cursor.execute(f'''DELETE FROM bookstore WHERE ID = {book_to_remove}''')

    def update_book_qty(self, book_qty, rowid):
        """Method updates qty information for the book with selected ID"""
        self.cursor.execute(
            f'''UPDATE bookstore SET qty = {book_qty} WHERE rowid = {rowid} ''')

    def select_low_stock(self):
        """Method selects books with stock lower than 5"""
        return self.cursor.execute(f'SELECT * FROM bookstore WHERE Qty < 5').fetchall()

    # def if_exists(self):
    #     return self.cursor.execute(f'SELECT Title FROM bookstore WHERE Title =  5').fetchall()


# ================= Functions ================
def check_str_input(value):
    """Function checks/validate user input"""
    if value == '' or value.isdigit():
        return False
    else:
        return True


def check_int_input(value):
    """Function checks/validate user input"""
    if str(value).isdigit() and int(value) > 0:
        return True
    else:
        return False


def search(subject, value):
    """Function takes arguments from other function and display them in tabulate"""
    content = db.get_book(subject, value)
    if content:
        print_tabulate(content)
    else:
        switch_message(4)


def write_to_txt():
    """Function generate and write data to TXT file in tabulate"""
    with open('Report.txt', 'w', encoding="utf-8") as output_file:
        headers = ['ID', 'Title', 'Author', 'Qty']
        content = db.get_all()
        output_file.write((tabulate(content, headers=headers, tablefmt='fancy_grid')))
def write_to_csv():
    """Function generate and write data to CSV file"""
    with open('Report.csv', 'w', encoding="utf-8", newline='') as output_file:
        headers = ['ID', 'Title', 'Author', 'Qty']
        content = db.get_all()
        writer = csv.writer(output_file)
        writer.writerow(headers)
        writer.writerows(content)

def print_tabulate(content):
    """Function prints selected books in tabulate mode"""
    headers = ['ID', 'Title', 'Author', 'Qty']
    print(tabulate(content, headers=headers, tablefmt='fancy_grid'))


def switch_message(value):
    """Function contains different print messages and use them in various parts of the program."""
    switcher = {
        0: "\n**********  No books to display.  **********\n",
        1: "\n**********  Invalid input. Please try again.  **********\n",
        2: "\n**********  You are redirecting to the main menu.  **********\n",
        3: "\n**********  This ID does not exist. Please try again.  **********\n",
        4: "\n**********  The book you are looking for cannot be found.  **********\n",
        5: "\n**********  Report file has been generated.  **********\n"
    }
    return print(switcher.get(value))


db = Database()
bookstore = BookStore(db)


# ================= Main Program ================

def option_one():
    bookstore.view_all()


def option_two():
    bookstore.add_book()


def option_three():
    bookstore.search_book()


def option_four():
    bookstore.update_info()


def option_five():
    bookstore.delete_book()


def option_six():
    bookstore.show_low_stock()


def option_seven():
    bookstore.generate_report()

def option_eight():
    pass
def option_zero():
    print('Thank you')
    db.db_commit()
    db.db.close()
    exit()


def menu():
    print('\n**********  Welcome in the Bookstore  **********')
    print(f'\n1 - Display all books\n'
          '2 - Add a new book\n'
          '3 - Search books\n'
          '4 - Update book information\n'
          '5 - Delete a book\n'
          '6 - Show low stock books only\n'
          '7 - Generate a report\n'
          '8 - Order books\n'
          '0 - Exit\n')


def main():
    while True:
        menu()
        menu_choice = input('Please choose one of the following options:\n')

        match menu_choice:
            case '1':
                option_one()
            case '2':
                option_two()
            case '3':
                option_three()
            case '4':
                option_four()
            case '5':
                option_five()
            case '6':
                option_six()
            case '7':
                option_seven()
            case '8':
                option_eight()
            case '0':
                option_zero()
            case _:
                switch_message(1)


if __name__ == "__main__":
    main()
