import yagmail
import re


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