"""
===============================================================================
PART 07 - EXCEPTIONS
Protecting Your Data
===============================================================================

Topics Covered
--------------
1. try / except / else / finally
2. The exception hierarchy
3. Catch specific before broad
4. Custom exceptions - the LibraryError family
5. EAFP vs LBYL

"""

import os

# =============================================================================
# MOTIVATION
# =============================================================================
#
# Everything so far described our data.
#
# @dataclass gave it structure.
#
# Type hints gave it labels.
#
# Protocol gave it contracts.
#
# But description is not protection.
#
# Recall borrow() from the Library lab.
#
# It returned False on failure.
#
# And lend_item raised a raw TypeError.
#
# Today we fix both.


# =============================================================================
# THEORY - the four blocks
# =============================================================================
#
# You know try and except.
#
# There are two more blocks worth knowing.
#
#     try       the attempt
#     except    runs ONLY if an error happened
#     else      runs ONLY if NO error happened
#     finally   runs no matter what - cleanup
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Predict, for each call below,
#
# which blocks print something.
#


def attempt(a: int, b: int) -> None:
    print(f"\n--- attempt({a}, {b}) ---")
    try:
        result = a / b            # attempt
    except ZeroDivisionError as e:
        print("except  : failed:", e)      # runs ONLY if an error happened
    else:
        print("else    : worked:", result) # runs ONLY if NO error happened
    finally:
        print("finally : always runs")     # runs no matter what - cleanup


attempt(10, 2)
attempt(10, 0)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Success run  ->  else ran, except was skipped.
#
# Failure run  ->  except ran, else was skipped.
#
# finally ran BOTH times.


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Difference between else and finally?
#
# Expected Answer:
#
# else runs only on success.
#
# finally runs always - success or failure.
#
# finally is for cleanup.
#
# Close a file. Release a connection.
#


# =============================================================================
# BOARD SUMMARY - what runs when
# =============================================================================
#
#              success      failure
#
#  try         runs         runs (until error)
#
#  except      ✗ skipped    ✓ runs
#
#  else        ✓ runs       ✗ skipped
#
#  finally     ✓ runs       ✓ runs
#


# =============================================================================
# THEORY - the exception hierarchy
# =============================================================================
#
# Exceptions form a family tree.
#
# Exception is the root.
#
# Specific ones inherit from it.
#
# Which gives one rule:
#
# Catching a PARENT catches all its CHILDREN.
#
# So the order of your except blocks matters.
#
# Catch SPECIFIC before BROAD.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# A ValueError is raised below.
#
# Two blocks could catch it.
#
# Predict which one wins.
#

try:
    int("not a number")
except ValueError as e:           # specific - catch this first
    print("\ncaught by : ValueError (specific) -", e)
except Exception as e:            # broad - catches everything else
    print("\ncaught by : Exception (broad) -", e)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# The FIRST matching block wins.
#
# Python checks top to bottom and stops at the first match.
#
# Reverse those two blocks and the ValueError block
#
# becomes unreachable - Exception would swallow everything first.


# =============================================================================
# COMMON MISCONCEPTIONS
# =============================================================================
#
# Misconception 1:
#
# "except Exception is the safe default."
#
# It catches almost everything.
#
# Use it sparingly - a swallowed error is a bug you find in production.
#
#
# Misconception 2:
#
# "The order of except blocks doesn't matter."
#
# It decides which one runs. Specific before broad.
#


# =============================================================================
# THEORY - custom exceptions
# =============================================================================
#
# An exception is just a class inheriting from Exception.
#
# But do not create a flat pile of unrelated exceptions.
#
# Create a FAMILY with one base class.
#
# Specific alarm bells instead of one generic siren.
#


class LibraryError(Exception):
    """Base for all library errors."""


class BookNotAvailable(LibraryError):
    pass


class BorrowLimitExceeded(LibraryError):
    pass


class NotBorrowable(LibraryError):
    pass


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# borrow() now RAISES instead of returning False.
#
# Predict the message each call below produces.
#


class Book:
    def __init__(self, title: str, is_available: bool = True) -> None:
        self.title = title
        self.is_available = is_available


class Member:
    def __init__(self, name: str, borrowed: int = 0, limit: int = 3) -> None:
        self.name = name
        self.borrowed = borrowed
        self.limit = limit

    def can_borrow(self) -> bool:
        return self.borrowed < self.limit


def borrow(book, member):
    if not book.is_available:
        raise BookNotAvailable(f"'{book.title}' is already loaned out")
    if not member.can_borrow():
        raise BorrowLimitExceeded(f"{member.name} is at their borrow limit")
    book.is_available = False


grace = Member("Grace", borrowed=0)
ada = Member("Ada", borrowed=3)

available = Book("Clean Code")
loaned_out = Book("Fluent Python", is_available=False)
another = Book("The Pragmatic Programmer")

for book, member in [(available, grace), (loaned_out, grace), (another, ada)]:
    try:
        borrow(book, member)
    except BorrowLimitExceeded as e:
        print("\nLimit issue     :", e)          # handle this one specially
    except LibraryError as e:
        print("\nSome library problem :", e)     # catch-all for the family
    else:
        print(f"\nBorrowed        : {book.title} by {member.name}")

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Look at what the caller now knows.
#
# Not "it failed".
#
# Each failure has a NAME and a MESSAGE.
#
# And notice the two except blocks.
#
# The first handles one specific failure.
#
# The second catches the whole family in one line.
#
# Specific before broad - the same rule,
#
# now applied to exceptions we designed ourselves.


# =============================================================================
# THEORY - EAFP vs LBYL
# =============================================================================
#
# Two styles of handling "what if this fails".
#
#
# LBYL - "Look Before You Leap"
#
# Check everything first, then act.
#
#
# EAFP - "Easier to Ask Forgiveness than Permission"
#
# Just try it, catch the failure.
#

d = {"a": 1}

# LBYL - look, then leap
if "key" in d:                    # look
    value = d["key"]              # then leap
else:
    value = "default"

print("\nLBYL value :", value)

# EAFP - just do it
try:
    value = d["key"]              # just do it
except KeyError:
    value = "default"             # handle failure if it comes

print("EAFP value :", value)


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Remember Lecture 1 -
#
# "we're all consenting adults",
#
# conventions over hard walls,
#
# trust over enforcement?
#
# Expected Answer:
#
# Yes - Python trusts you rather than building defensive walls.
#
#
# EAFP is that same philosophy applied to errors.
#
# Instead of defensively checking everything up front,
#
# you trust it'll usually work,
#
# and handle the rare failure.


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# And there's a real reason to prefer it.
#
# LBYL has a GAP.
#
#     if os.path.exists(path):    # check...
#         open(path)              # ...file could be deleted RIGHT HERE
#
# Below we simulate exactly that gap.
#
# Predict what happens.
#

path = "demo_file.txt"

with open(path, "w") as f:
    f.write("hello")

# LBYL - the check passes...
if os.path.exists(path):
    print("\nLBYL : check passed - file exists")
    os.remove(path)                       # ...something changes in the GAP
    try:
        open(path)
    except FileNotFoundError:
        print("LBYL : crashed anyway - the check bought no safety")

# EAFP - no gap to exploit
try:
    open(path)
except FileNotFoundError:
    print("EAFP : failed cleanly, no check/act gap")

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# The LBYL check PASSED.
#
# And the code crashed anyway.
#
# Because the world changed between the check and the action.
#
# EAFP has no such gap.
#
# It just tries, and catches.


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# What's the risk between the check and the action in LBYL?
#
# Expected Answer:
#
# Something can change in that gap.
#
# The file gets deleted.
#
# EAFP has no gap - you just try, and catch if it fails.
#


# =============================================================================
# INTERVIEW OBSERVATION
# =============================================================================
#
# Frequently asked:
#
# - "else vs finally?"             -> else on success only, finally always.
# - "Why not except Exception?"    -> It hides real bugs. Use it sparingly.
# - "Why a base exception class?"  -> Caller catches one, or the whole family.
# - "raise vs return False?"       -> An error carries a reason. False carries none.
# - "EAFP or LBYL?"                -> Python leans EAFP - no check/act gap.
#
# In design reviews, "what does this method raise, and who catches it?"
#
# is a standard question about any service boundary.
#


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# The four blocks
#
# try / except / else / finally
#
#        ↓
#
# else = success only.  finally = ALWAYS.
#
#
# Hierarchy
#
#        ↓
#
# Catch SPECIFIC before BROAD.
#
# except Exception catches almost everything - use sparingly.
#
#
# Custom hierarchy
#
# LibraryError
#   BookNotAvailable
#   BorrowLimitExceeded
#   NotBorrowable
#
#        ↓
#
# Catch the exact one you care about,
#
# or the whole family with one line.
#
#
# LBYL  -> check first, then act.   (defensive)
#
# EAFP  -> try it, catch the failure.  (Pythonic - no check/act gap)
#
# Python leans EAFP.
#


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ else runs only on success; finally runs always - finally is for cleanup.
# ✓ Catching a parent catches all its children.
# ✓ Order except blocks specific before broad; the first match wins.
# ✓ A silent False tells the caller nothing about why it failed.
# ✓ A raw TypeError looks like a bug, not a business rule.
# ✓ Give the project one base exception, then build a family under it.
# ✓ The caller then chooses: one specific failure, or the whole family.
# ✓ Python leans EAFP - same "trust, don't wall off" spirit as Lecture 1.
#
#
# =============================================================================
# BRIDGE TO THE NEXT TOPIC
# =============================================================================
#
# Our failures now have names.
#
# But our VALUES still don't.
#
#     loan.status = "active"
#
# What if someone writes "activ"?
#
# Or "Active"?
#
# Nothing errors. The logic just quietly fails.
#
# Next: Enum - killing the magic strings.