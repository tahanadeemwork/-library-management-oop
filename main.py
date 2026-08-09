from library import Library
from models import Book, StudentMember, FacultyMember

def main():
    library = Library()

    try:
        library.load_from_file()
        print("Loaded existing library data.")
    except FileNotFoundError:
        print("No existing data found — starting fresh.")

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Member Report")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            try:
                total_copies = int(input("Enter total copies: "))
                book = Book(title, author, isbn, total_copies)
                library.add_book(book)
                print(f"Book '{title}' added successfully.")
                library.save_to_file()
            except ValueError as e:
                print(f"Error adding book: {e}")
            
        elif choice == "2":
            name = input("Enter member name: ")
            member_id = input("Enter member ID: ")
            member_type = input("Enter member type (student/faculty): ").strip().lower()
            try:
                if member_type == "student":
                    member = StudentMember(name, member_id)
                elif member_type == "faculty":
                    member = FacultyMember(name, member_id)
                else:
                    print("Invalid member type. Must be 'student' or 'faculty'.")
                    continue
                library.add_member(member)
                print(f"Member '{name}' added successfully.")
                library.save_to_file()
            except ValueError as e:
                print(f"Error adding member: {e}")

        elif choice == "3":
            keyword = input("Enter keyword to search (title or author): ")
            results = library.search_book(keyword)
            if results:
                print("Search Results:")
                for book in results:
                    print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available Copies: {book.copies_available}")
            else:
                print("No books found matching the keyword.")

        elif choice == "4":
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN: ")
            try:
                member = library.members[member_id]
                book = library.books[isbn]
                library.borrow_book(member, book)
                print(f"Book '{book.title}' borrowed successfully by {member.name}.")
                library.save_to_file()
            except KeyError:
                print("Member ID or Book ISBN not found.")
            except ValueError as e:
                print(f"Error borrowing book: {e}")

        elif choice == "5":
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN: ")
            try:
                member = library.members[member_id]
                book = library.books[isbn]
                library.return_book(member, book)
                print(f"Book '{book.title}' returned successfully by {member.name}.")
                library.save_to_file()
            except KeyError:
                print("Member ID or Book ISBN not found.")
            except ValueError as e:
                print(f"Error returning book: {e}")

        elif choice == "6":
            member_id = input("Enter member ID: ")
            try:
                member = library.members[member_id]
                library.view_member_report(member)
            except KeyError:
                print("Member ID not found.")

        elif choice == "7":
            library.save_to_file()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()