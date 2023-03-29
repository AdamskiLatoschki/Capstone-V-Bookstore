import yagmail
import re
from tabulate import tabulate
import csv
import database as dtbs
import bookstore as bkst


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
    """Function takes arguments from other function, search book by Author or Title, depends on the user requirements
    and display results in tabulate """
    content = db.get_book(subject, value)
    if content:
        print_tabulate(content)
    else:
        switch_message(4)


def write_to_txt():
    """Function generates and write data to TXT file in tabulate"""
    with open('Report.txt', 'w', encoding="utf-8") as output_file:
        headers = ['ID', 'Title', 'Author', 'Qty']
        content = db.get_all()
        output_file.write((tabulate(content, headers=headers, tablefmt='fancy_grid')))


def write_to_csv():
    """Function generates and write data to CSV file"""
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


def send_email(receiver, email_content):
    """Function uses yagmail.SMTP protocol allowing user to send an email"""
    user_email = "bookstore.hyperion@gmail.com"
    password = "nwbyaqxmqhpjnbfd"
    msg_header = "Bookstore order"

    receiver_email = receiver
    msg_content = email_content

    try:
        yag = yagmail.SMTP(user_email, password)
        yag.send(receiver_email, msg_header, msg_content)
        print('\nEmail has been sent successfully!\n')
    except ConnectionError:
        print('Failure, email cannot be sent. Please try again.')


def validate_email(email):
    """Function validates entered user email address"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pattern, email):
        return True
    else:
        print("Invalid email address. Please try again.")


db = dtbs.Database()
bookstore = bkst.BookStore(db)
