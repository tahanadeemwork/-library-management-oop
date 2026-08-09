from datetime import date, timedelta

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

    def borrow_book(self, member, book):
        if not book.is_available():
            raise ValueError(f"'{book.title}' is not available right now")

        if len(member.borrowed_books) >= member.max_books_allowed:
            raise ValueError(f"{member.name} has reached their borrowing limit of {member.max_books_allowed} books")

        book.copies_available -= 1
        due_date = date.today() + timedelta(days=member.borrowing_period_days)
        member.borrowed_books.append((book, due_date))

    def return_book(self, member, book):
        entry_to_remove = None
        for entry in member.borrowed_books:
            if entry[0] is book:
                entry_to_remove = entry
                break
        if entry_to_remove is None:
            raise ValueError(f"'{book.title}' is not borrowed by {member.name}")

        member.borrowed_books.remove(entry_to_remove)
        book.copies_available += 1
        