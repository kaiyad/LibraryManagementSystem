class Books:
    def __init__(self, name=None, author=None, genre=None):
        self.name = name
        self.author = author
        self.genre = genre

    def add_book(self, name, author, genre):
        """Add Book"""

    def remove_book(self, name):
        """Remove Book"""

    def update_book(self, name):
        """Update Book Details"""

    def get_book(self, name):
        """Get book Details"""

    def list_books(self):
        """List Books"""
        return { "name" : "Python for gods", "author": "God", "genre": "Fiction"}