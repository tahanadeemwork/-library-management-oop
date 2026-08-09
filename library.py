class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book):
        if book.isbn in self.books:
            existing_book = self.books[book.isbn]
            existing_book.total_copies += book.total_copies
            existing_book.copies_available += book.total_copies
        else:
            self.books[book.isbn] = book

    def add_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Member with ID already exists")
        self.members[member.member_id] = member

    def search_book(self, keyword):
        results = []
        for book in self.books.values():
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        return results