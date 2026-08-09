class Book:
    def __init__(self, title, author, isbn, total_copies):
        if not title or not author or not isbn:
            raise ValueError("Title, author, and ISBN are required")
        if total_copies <= 0:
            raise ValueError("Total copies must be a positive integer")
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.copies_available = total_copies

    def is_available(self):
        return self.copies_available > 0

class Member:
    max_books_allowed = 0
    borrowing_period_days = 0

    def __init__(self, name, member_id):
        if not name or not member_id:
            raise ValueError("Name and member ID are required")
        self.name = name
        self.member_id = member_id

        self.borrowed_books = []

    def __repr__(self):
        return f"Member(name='{self.name}', member_id='{self.member_id}', borrowed_books={len(self.borrowed_books)})"