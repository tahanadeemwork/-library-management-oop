# Library Management System (OOP Project)

A command-line Library Management System built in Python to practice object-oriented programming — specifically composition, inheritance, and polymorphism working together across multiple interacting classes, rather than a single class in isolation.

## Overview

The system models a library where a `Library` object manages a catalog of `Book` objects and a roster of `Member` objects, coordinating borrowing and returning between them. Two member types — `StudentMember` and `FacultyMember` — extend a base `Member` class with their own borrowing limits and loan periods, demonstrating real behavioral differences through the same shared interface.

## How to Run

Requires Python 3.x. No external dependencies — uses only the standard library (`datetime`, `json`).

```bash
python main.py
```

On startup, the program attempts to load existing data from `library_data.json`. If none exists, it starts with an empty catalog and roster. Data is automatically saved after every action that changes state (adding a book/member, borrowing, returning), so nothing is lost if the program closes unexpectedly.

## Features

- Add books to the catalog, with automatic copy-count merging if the same ISBN is added again
- Add student or faculty members
- Search books by partial title or author match (case-insensitive)
- Borrow books, enforcing both book availability and the member's own borrowing limit
- Return books, restoring availability
- View a per-member report showing borrowed books, due dates, and overdue status
- Full persistence to JSON, including correct restoration of each member's original subclass on reload

## Where OOP Concepts Show Up

**Composition** — `Library` does not inherit from `Book` or `Member`; instead it *has* a catalog (`self.books`) and a roster (`self.members`) and coordinates interactions between them. Almost all the real logic — checking availability, enforcing limits, calculating due dates — lives in `Library` methods like `borrow_book()`, because `Library` is the only object able to see both a specific book and a specific member at once. `Book` and `Member` themselves stay focused only on their own state.

**Inheritance** — `StudentMember` and `FacultyMember` both extend `Member`, inheriting its `__init__` (name, member ID, empty borrowed-books list) unchanged, since neither subclass needs extra constructor data. What they *do* override are two class-level attributes: `max_books_allowed` and `borrowing_period_days`.

**Polymorphism** — this is the core of the project, and it's concentrated in one place: `Library.borrow_book()`. The method contains no `if isinstance(member, StudentMember)` branching anywhere. It simply reads `member.max_books_allowed` and `member.borrowing_period_days` directly:

```python
if len(member.borrowed_books) >= member.max_books_allowed:
    raise ValueError(...)
...
due_date = date.today() + timedelta(days=member.borrowing_period_days)
```

The exact same two lines of code produce a limit of 3 books / 14-day loans for a `StudentMember`, and 6 books / 30-day loans for a `FacultyMember` — because Python resolves each attribute lookup against the object's *actual* class at runtime. This is verified directly in testing: borrowing is correctly blocked at 3 books for a student and would only block at 6 for faculty, using identical calling code.

## Project Structure

- `models.py` — `Book`, `Member`, `StudentMember`, `FacultyMember` class definitions
- `library.py` — `Library` class: catalog/roster management, search, borrow/return logic, member reports, JSON persistence
- `main.py` — command-line menu loop tying everything together
- `library_data.json` — generated at runtime; stores the persisted catalog, members, and active loans
- `README.md` — this file