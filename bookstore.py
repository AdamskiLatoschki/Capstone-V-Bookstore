import functions as func
import book as bk
import database as dtbs

db = dtbs.Database()


# =============== Class BookStore ==============
class BookStore:
    """Class allows the user to modify and view records"""

    # def __init__(self, database):
    #     self.db = database

    @staticmethod
    def view_all():
        """Function displays all books available in stock if there are any, otherwise display a message saying 'No
        books to display' """
        check_all = db.get_all()
        if check_all:
            func.print_tabulate(check_all)
        else:
            func.switch_message(0)

    @staticmethod
    def add_book():
        """Taking user inputs required to create an object and add a new book to stock.
        Validating if input is empty, if it is a string or digit."""
        book_title = input('Enter the title of the new book: ').strip().title()
        while not func.check_str_input(book_title):
            func.switch_message(1)
            book_title = input('Enter the title of the new book: ').strip().title()

        book_author = input('Enter the author of the new book: ').strip().title()
        while not func.check_str_input(book_author):
            func.switch_message(1)
            book_author = input('Enter the author of the new book: ').strip().title()

        book_quantity = input('Enter the quantity of the new book you would like to add to stock: ').strip()
        while not func.check_int_input(book_quantity):
            func.switch_message(1)
            book_quantity = input('Enter the quantity of the new book you would like to add to stock: ').strip()

        book = bk.Book(book_title, book_author, book_quantity)
        db.insert_values(book)
        db.db_commit()
        print(f'\nNew book "{book.title}" has been added to stock.')

    @staticmethod
    def search_book():
        """This function allow user to search specific book by title or author and then display results."""
        while db.check_if_empty():
            choice = input('\nPlease choose from following options how would you like to search a book:\n'
                           '1 - Search by title\n'
                           '2 - Search by author\n'
                           '0 - Exit to main menu\n'
                           ':')

            if choice == '1':
                subject = 'Title'
                book_title = input('Enter the title of the book you would like to search for: ')
                func.search(subject, book_title)
            elif choice == '2':
                subject = 'Author'
                book_author = input('Enter the author of the book you would like to search for: ')
                func.search(subject, book_author)
            elif choice == '0':
                func.switch_message(2)
                break
            else:
                func.switch_message(1)
        func.switch_message(0)

    def update_info(self):
        """Function updates quantity for chosen book.If book with entered ID does not exist, then an error message
        will be displayed. """
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
                        func.switch_message(1)
                func.switch_message(3)
            except ValueError:
                func.switch_message(1)

    def delete_book(self):
        """Function deletes chosen book from stock. If book with entered ID does not exist, then an error message
        will be displayed."""
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
                        func.switch_message(2)
                        break
                    else:
                        func.switch_message(1)
                        continue
                else:
                    func.switch_message(3)
            except ValueError:
                func.switch_message(1)

    @staticmethod
    def show_low_stock():
        """Function display selected low stock books"""
        content = db.select_low_stock()
        if content:
            func.print_tabulate(content)
        else:
            func.switch_message(0)

    @staticmethod
    def generate_report():
        """Function generates reports and write data to file. User can choose between CSV and TXT file."""
        while True:
            choice = input(f'What type of the file would you like to generate a report to? :\n'
                           '1 - CSV\n'
                           '2 - TXT\n'
                           ':')
            match choice:
                case '1':
                    func.write_to_csv()
                    func.switch_message(5)
                    break
                case '2':
                    func.write_to_txt()
                    func.switch_message(5)
                    break
                case _:
                    func.switch_message(1)
                    continue

    @staticmethod
    def order_books():
        """Function allows a user to send an email"""
        while True:
            receiver_email = input('Please enter the receiver email address:')
            if func.validate_email(receiver_email):
                email_content = input('Please enter the content of the email you would like to send: ')
                print('\nSending email.....')
                func.send_email(receiver_email, email_content)
                break
