from db.models import Books


class Library():
    """"""
    def __init__(self):
        pass

    def list_books(self):
        return Books().list_books()