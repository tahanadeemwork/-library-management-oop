from datetime import date, timedelta
from models import Book, StudentMember, FacultyMember
import json

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

    def view_member_report(self, member):
        if not member.borrowed_books:
            print(f"{member.name} has no books currently borrowed.")
            return

        print(f"Report for {member.name} ({member.member_id}):")
        for book, due_date in member.borrowed_books:
            is_overdue = due_date < date.today()
            status = "OVERDUE" if is_overdue else "on time"
            print(f"  - {book.title} | Due: {due_date} | Status: {status}")

    def save_to_file(self, filepath="library_data.json"):
        data = {
            "books": {},
            "members": {}
        }

        for isbn, book in self.books.items():
            data["books"][isbn] = {
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "total_copies": book.total_copies,
                "copies_available": book.copies_available
            }

        for member_id, member in self.members.items():
            data["members"][member_id] = {
                "type": type(member).__name__,
                "name": member.name,
                "member_id": member.member_id,
                "borrowed_books": [
                    {"isbn": book.isbn, "due_date": due_date.isoformat()}
                    for book, due_date in member.borrowed_books
                ]
            }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath="library_data.json"):
        with open(filepath, "r") as f:
            data = json.load(f)

        self.books = {}
        self.members = {}

        for isbn, book_data in data["books"].items():
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                isbn=book_data["isbn"],
                total_copies=book_data["total_copies"]
            )
            
            book.copies_available = book_data["copies_available"]
            self.books[isbn] = book

        member_classes = {
            "StudentMember": StudentMember,
            "FacultyMember": FacultyMember
        }

        for member_id, member_data in data["members"].items():
            cls = member_classes[member_data["type"]]
            member = cls(member_data["name"], member_data["member_id"])

            for entry in member_data["borrowed_books"]:
                book = self.books[entry["isbn"]]
                due_date = date.fromisoformat(entry["due_date"])
                member.borrowed_books.append((book, due_date))

            self.members[member_id] = member