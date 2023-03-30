# Capstone-V-Bookstore

<br>

## Project Description: 
The bookstore is a command-line application for managing a book inventory. The program stores information about books in a database and allows users to access and manipulate data.

<br>

## Installation

To use this program, you will need to have Python 3 and ideally PyCharm installed on your computer. 
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


- Display all books - Display a table with all the books in the inventory.

- Add a new book - Takes user inputs like title, author and qty and insert created book into database.
    
- Search books - Allows the user to search for a book in the database using its title or author and display a result in a table.
    
- Update book information - Allows the user to edit information of a book that is already within the database.
    
- Delete a book - Allows the user to delete a specific book from the database by selecting a book ID.
    
- Show low stock books - Display low stock books in the inventory.
    
- Generate a report - Generate a report to file with all the books in the inventory. Allow user to choose between CSV and TXT file.
   
- Sent an email / Order books - Allow user to enter email address and email content to send an email to order books.
    
- Exit - Exits the programme.    
    




