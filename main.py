import functions as func
import database as dtbs
import bookstore as bkst

# TODO Create GUI using Tkinter.


db = dtbs.Database()
bookstore = bkst.BookStore()


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
    bookstore.order_books()


def option_zero():
    print('Thank you. Bye bye')
    db.db_commit()
    db.db.close()
    exit()


def menu():
    print('\n**********  MAIN MENU  **********')
    print(f'\n1 - Display all books\n'
          '2 - Add a new book\n'
          '3 - Search books\n'
          '4 - Update book information\n'
          '5 - Delete a book\n'
          '6 - Show low stock books\n'
          '7 - Generate a report\n'
          '8 - Sent an email / Order books\n'
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
                func.switch_message(1)


if __name__ == "__main__":
    main()
