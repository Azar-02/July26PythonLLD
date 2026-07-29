"""
===============================================================================
PART 10 - LAB
Refactor the Library System  -  the loop closes
===============================================================================

Topics Covered
--------------
1. Loan  ->  @dataclass(frozen=True)
2. The LibraryError exception hierarchy
3. Magic strings  ->  Enum
4. search()  ->  typed with the Searchable Protocol
5. Module 1 wrap-up

The comments are the classroom lecture.
The executable code demonstrates runtime behaviour.
"""

from dataclasses import FrozenInstanceError, dataclass
from datetime import date, timedelta
from enum import Enum
from typing import Protocol

# =============================================================================
# MOTIVATION
# =============================================================================
#
# This is it.
#
# We take the Library System you built in the OOP capstone -
#
# and make it Pythonic with today's tools.
#
# Not a new system.
#
# YOUR system.
#
# The same classes you hand-wrote weeks ago.


# =============================================================================
# THE TASK
# =============================================================================
#
# 1. Refactor Loan into a @dataclass(frozen=True) -
#
#    kill the hand-written __init__ / __eq__ / __hash__ / __repr__.
#
#
# 2. Add a LibraryError exception hierarchy;
#
#    make borrow raise BookNotAvailable / BorrowLimitExceeded
#
#    instead of returning False.
#
#
# 3. Replace the book-type / loan-status magic strings with an Enum.
#
#
# 4. Add type hints to the search function using the Searchable Protocol.
#
#
# Attempt task 1 yourself before reading on.


# =============================================================================
# BEFORE - the hand-written Loan from Lecture 7
# =============================================================================
#
# class Loan:
#     def __init__(self, member, book, due_date):
#         self.member = member; self.book = book; self.due_date = due_date
#
#     def __repr__(self):
#         return f"Loan(book={self.book!r}, member={self.member!r}, ...)"
#
#     def __eq__(self, other):
#         return (self.book == other.book and self.member == other.member)
#
#     def __hash__(self):
#         return hash((self.book, self.member))
#
#
# Count it.
#
# Roughly fifteen lines.
#
# Every field named three times.
#
# And you had to remember that defining __eq__ kills __hash__.


# =============================================================================
# SOLUTION 1 - the refactored Loan
# =============================================================================


@dataclass(frozen=True)
class Loan:
    member_id: str
    isbn: str
    due_date: date

    def is_overdue(self) -> bool:
        return date.today() > self.due_date


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Compare to the OOP-lab Loan.
#
# What did we delete?
#
# Expected Answer:
#
# __init__, __repr__, __eq__, __hash__ - all of it.
#
# @dataclass(frozen=True) generates them.
#
# And is_overdue - real behaviour - stays.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Predict all four lines.
#
# Especially the set.
#

yesterday = date.today() - timedelta(days=1)
next_week = date.today() + timedelta(days=7)

overdue_loan = Loan("M-1", "978-0", yesterday)
active_loan = Loan("M-2", "978-1", next_week)
duplicate = Loan("M-1", "978-0", yesterday)

print("repr generated :", overdue_loan)
print("eq generated   :", overdue_loan == duplicate)
print("hash generated :", len({overdue_loan, duplicate}))
print("is_overdue     :", overdue_loan.is_overdue(), "/", active_loan.is_overdue())

try:
    overdue_loan.member_id = "M-9"
except FrozenInstanceError as e:
    print("frozen         : FrozenInstanceError -", e)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Four generated methods.
#
# Zero written by hand.
#
# The set collapsed two equal loans into one -
#
# which is the exact crash you predicted in the OOP capstone,
#
# now simply working.
#
# And the object refuses to change after creation.


# =============================================================================
# SOLUTION 2 - the exception hierarchy + borrow
# =============================================================================


class LibraryError(Exception): ...
class BookNotAvailable(LibraryError): ...
class BorrowLimitExceeded(LibraryError): ...


def borrow(book, member) -> None:
    if not book.is_available:
        raise BookNotAvailable(f"'{book.title}' is not available")
    if not member.can_borrow():
        raise BorrowLimitExceeded(f"{member.name} at borrow limit")
    book.is_available = False
    member.increment_borrow()


# =============================================================================
# SOLUTION 3 - Enum + typed search
# =============================================================================


class LoanStatus(Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class BookType(Enum):
    NOVEL = "novel"
    TEXTBOOK = "textbook"
    REFERENCE = "reference"


class Searchable(Protocol):
    def matches(self, query: str) -> bool: ...


def search(items: list[Searchable], query: str) -> list[Searchable]:
    return [it for it in items if it.matches(query)]


# =============================================================================
# SCAFFOLDING - Book and Member
# =============================================================================
#
# borrow() and search() need something to operate on.
#
# These two are deliberately MINIMAL - just enough to run the lab.
#
# Refactoring them properly is your take-home.
#


@dataclass
class Book:
    title: str
    isbn: str
    book_type: BookType = BookType.NOVEL
    is_available: bool = True

    def matches(self, query: str) -> bool:
        return query.lower() in self.title.lower()


@dataclass
class Member:
    name: str
    member_id: str
    borrowed: int = 0
    limit: int = 2

    def can_borrow(self) -> bool:
        return self.borrowed < self.limit

    def increment_borrow(self) -> None:
        self.borrowed += 1

    def matches(self, query: str) -> bool:
        return query.lower() in self.name.lower()


# =============================================================================
# THINK BEFORE RUNNING - the whole system together
# =============================================================================
#
# Grace borrows twice, then tries a third time.
#
# Her limit is 2.
#
# Predict which line fails, and with which exception.
#

catalog = [
    Book("Clean Code", "978-0", BookType.TEXTBOOK),
    Book("Fluent Python", "978-1", BookType.TEXTBOOK),
    Book("World Atlas", "978-2", BookType.REFERENCE),
    Book("The Python Novel", "978-3", BookType.NOVEL, is_available=False),
]

grace = Member("Grace Hopper", "M-1")

print()
for book in catalog:
    try:
        borrow(book, grace)
    except BorrowLimitExceeded as e:
        print("limit reached  :", e)
    except LibraryError as e:
        print("library error  :", type(e).__name__, "-", e)
    else:
        print("borrowed       :", book.title)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Two successes.
#
# Then a BorrowLimitExceeded - Grace hit her limit of 2.
#
# Then a BookNotAvailable - that title was already loaned out.
#
# Every failure named itself.
#
# Compare with the original:
#
#     False
#     False
#
# Same behaviour. Completely different amount of information.


# =============================================================================
# SMALL EXPERIMENT - the typed search
# =============================================================================
#
# search() is hinted with the Searchable Protocol.
#
# Book and Member both have matches() - and neither inherits anything.
#

print("\nsearch books   :", [b.title for b in search(catalog, "python")])
print("search members :", [m.name for m in search([grace], "grace")])
print("status enum    :", LoanStatus.ACTIVE, "/", LoanStatus.ACTIVE.value)
print("book type enum :", catalog[0].book_type, "/", catalog[0].book_type.value)

# Runtime Observation
#
# One search function.
#
# Two unrelated classes.
#
# Judged by shape, not by family.


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Across the whole refactor -
#
# which was the single biggest line-count saving?
#
# Expected Answer:
#
# The Loan dataclass.
#
# ~15 lines of dunder boilerplate
#
#        ↓
#
# 4 lines of field declarations.
#


# =============================================================================
# BOARD SUMMARY - what changed
# =============================================================================
#
# Loan
#
# hand-written __init__ / __repr__ / __eq__ / __hash__
#
#        ↓
#
# @dataclass(frozen=True)
#
#
# borrow()
#
# return False
#
#        ↓
#
# raise BookNotAvailable / BorrowLimitExceeded
#
#
# status = "active"
#
#        ↓
#
# LoanStatus.ACTIVE
#
#
# def search(items, query)
#
#        ↓
#
# def search(items: list[Searchable], query: str) -> list[Searchable]
#


# =============================================================================
# MODULE 1 WRAP-UP
# =============================================================================
#
# Now zoom all the way out.
#
# This is the end of Module 1.
#
#
# OOP
#
#        ↓
#
# model the world as entities.
#
# (Uber, then the Library capstone.)
#
#
# Concurrency
#
#        ↓
#
# threads -> processes -> the GIL -> executors -> locks & queues
#
# -> a glimpse of async.
#
#
# Pythonic
#
#        ↓
#
# decorators & generators - write functions beautifully.
#
# dataclasses, hints, exceptions - structure data beautifully.
#
#
# You can model a system,
#
# run it concurrently,
#
# and write it cleanly, safely and Pythonically.
#
# That's the entire foundation.
#
# Everything in LLD-2 is built on this.


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ @dataclass(frozen=True) replaced ~15 lines of Loan boilerplate with 4.
# ✓ Real behaviour like is_overdue() stays - only the plumbing left.
# ✓ frozen=True also gave a safe __hash__, so Loans work in sets.
# ✓ Raising named exceptions tells the caller WHY, where False told it nothing.
# ✓ One base LibraryError lets the caller catch one failure, or the family.
# ✓ Enum replaced the magic strings for loan status and book type.
# ✓ The Searchable Protocol typed search() without forcing any inheritance.
#
# This is the same system you built by hand weeks ago.
#
# Today it is typed, validated, immutable where it should be,
#
# and it tells you why things fail.
#
#
# =============================================================================
# TAKE-HOME
# =============================================================================
#
# 1. Finish refactoring the WHOLE Library System - Member, Book, Library -
#
#    with dataclasses, hints, and the exception hierarchy.
#
#
# 2. Add __post_init__ validation:
#
#    Member - borrow limit can't be negative.
#
#    Book   - isbn can't be empty.
#
#
# 3. Replace every magic string in the system with an Enum.
#
#    Count how many you find.
#
#
# 4. Push to GitHub - branch `lecture-12-complete`.
#
#
# =============================================================================
# NEXT MODULE
# =============================================================================
#
# LLD-2: Design Principles & Patterns.
#
# You now know how to write good Python.
#
# Next we learn how to ARCHITECT it -
#
# SOLID, design patterns, and UML.
#
# And remember the @singleton decorator from the decorators lecture?
#
# In LLD-2 you'll meet the Singleton pattern properly.
#
# That's where it pays off.