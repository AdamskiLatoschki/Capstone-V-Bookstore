# Capstone-V-Bookstore

<br>

## Project Description: 
The bookstore is command-line software that allows you to manage your book inventory. 
The programme saves book information in a database and allows users to access and change the data within a bookstore.

<br>

## Installation

To run this program, you must have Python 3 and, preferably, PyCharm installed on your computer.
You may also need to install the following libraries:

```bash
pip install re
pip install tabulate
pip install yagmail
```
<br>

## Libraries Used

The following libraries are used in this project:

- `sqlite3`: Provides an interface to work with SQLite databases.
- `tabulate`: A library used for displaying the book inventory in a formatted table.
- `re`: The Python 're' module provides regular expression support.
- `yagmail`: yagmail is a GMAIL/SMTP client that aims to make it as simple as possible to send emails.
- `csv`: The csv module implements classes to read and write tabular data in CSV format
<br>

## Download the Source Code

You can download the source code from the GitHub repository.

<br>

## Run the Application

To run the application, navigate to the directory where you downloaded the source code and run the following command:

```bash
python main.py
```

<br>

## Menu

From this menu, the user is able to enter the number of the option that they wish to access. This will then prompt additional options to appear:


- Display all books - Display a table containing all of the books in the inventory.

- Add a new book - Takes user inputs such as title, author, and quantity and inserts the resulting book into a database.
    
- Search books - Allows the user to search for a book in the database by title or author and display the results in a table.
    
- Update book information - Allows the user to edit information about a book that is already in the database.
    
- Delete a book - Allows the user to delete a specific book from the database by specifying a book ID.
    
- Show low stock books - Display low-stock books in the inventory.
    
- Generate a report - Create a report to be filed with all of the books in the inventory. Allows the user to select between a CSV and a TXT file.
   
- Sent an email / Order books - Allows the user to enter their email address and email content to send an email to order books.
    
- Exit - Exits the programme.    
    





