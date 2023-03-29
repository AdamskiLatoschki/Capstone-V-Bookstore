# ================= Class Book ================

class Book:
    """Class to create a book objects. Used to represent database records"""
    def __init__(self, title, author, qty):
        self.title = title
        self.author = author
        self.qty = qty
