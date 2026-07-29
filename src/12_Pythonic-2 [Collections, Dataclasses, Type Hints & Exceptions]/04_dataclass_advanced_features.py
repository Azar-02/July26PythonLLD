"""
===============================================================================
PART 04 - DATACLASSES
Advanced Features of @dataclass
===============================================================================

Topics Covered
--------------
1. Why basic dataclasses are not enough
2. Default values
3. Mutable default pitfalls
4. default_factory
5. frozen=True
6. order=True
7. field()
8. Practical discussions and interview observations

"""

from dataclasses import dataclass, field

# =============================================================================
# MOTIVATION
# =============================================================================
#
# Yesterday we discovered that @dataclass removes repetitive methods like:
#
#     __init__()
#     __repr__()
#     __eq__()
#
# Naturally students now ask:
#
#     "Is that all @dataclass can do?"
#
# Not at all.
#
# The basic decorator is only the starting point.
#
# Real software projects introduce new requirements:
#
# • Some values should have sensible defaults.
# • Some objects should never change.
# • Some objects should be sortable.
# • Some fields should be hidden while printing.
#
# Today's lecture is about solving each of those real-world problems.

# =============================================================================
# THEORY
# =============================================================================
#
# The philosophy has not changed.
#
# Yesterday:
#
#     Boilerplate methods
#            ↓
#     @dataclass
#
# Today:
#
#     Boilerplate configurations
#            ↓
#     Advanced dataclass options
#
# Every option exists because developers repeatedly faced the same problem.


# =============================================================================
# FEATURE 1 - DEFAULT VALUES
# =============================================================================
#
# ASK LEARNERS
#
# Imagine building a School Management System.
#
# Should every newly admitted student already have a grade?
#
# Student Thinking:
#
# No.
#
# The grade may be assigned later.
#
# Therefore the object should still be constructible.

@dataclass
class Student:
    name: str
    grade: str = "Not Assigned"

print("=== Default Values ===")
s1 = Student("Alice")
s2 = Student("Bob", "A")
print(s1)
print(s2)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Python automatically supplied the default only when no value
# was provided.
#
# Explicit values always take priority.


# =============================================================================
# SMALL EXPERIMENT
# =============================================================================

print(type(s1.grade))
print(s1.grade == "Not Assigned")

# =============================================================================
# FEATURE 2 - MUTABLE DEFAULTS
# =============================================================================
#
# This is one of the most important discussions in dataclasses.
#
# THINK BEFORE RUNNING
#
# Suppose every student has a list of enrolled subjects.
#
# Question:
#
# Should every Student object share one common list?
#
# Expected Answer:
#
# Absolutely not.
#
# Every student needs an independent list.
#
# Python therefore provides default_factory.

@dataclass
class StudentCourses:
    name: str
    subjects: list = field(default_factory=list)

alice = StudentCourses("Alice")
bob = StudentCourses("Bob")

alice.subjects.append("Python")

print("\n=== default_factory ===")
print(alice)
print(bob)

# =============================================================================
# MEMORY DIAGRAM
# =============================================================================
#
# alice.subjects --------> ['Python']
#
# bob.subjects ----------> []
#
# Different list objects.
#
# No accidental sharing.
#

print(id(alice.subjects))
print(id(bob.subjects))

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# default_factory does NOT share one object.
#
# Instead it calls list() every time a new instance is created.
#
# Every object receives its own independent list.


# =============================================================================
# COMMON MISCONCEPTION
# =============================================================================
#
# Many beginners think:
#
#     default_factory=list
#
# stores one list.
#
# It doesn't.
#
# It stores a callable that creates a fresh list whenever needed.


# =============================================================================
# FEATURE 3 - frozen=True
# =============================================================================
#
# Some objects represent values that should never change.
#
# Examples:
#
# • Coordinates
# • Employee IDs
# • Configuration
#
# Analogy:
#
# Think of a passport number.
#
# Once issued, it should remain fixed.

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

point = Coordinate(10, 20)

print("\n=== frozen=True ===")
print(point)

try:
    point.x = 99
except Exception as e:
    print(type(e).__name__, "->", e)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# frozen=True blocks attribute reassignment.
#
# It encourages immutable value objects.


# =============================================================================
# FEATURE 4 - order=True
# =============================================================================
#
# ASK LEARNERS
#
# If two Player objects exist,
# how should Python decide which one is "smaller"?
#
# Without comparison methods,
# Python cannot know.
#
# order=True generates comparison behaviour.

@dataclass(order=True)
class Player:
    score: int
    name: str

players = [
    Player(91, "Alice"),
    Player(75, "Bob"),
    Player(88, "Charlie")
]

print("\n=== order=True ===")
for p in sorted(players):
    print(p)

print(players[1] < players[0])

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Comparisons follow field declaration order.
#
# score becomes the primary comparison key.


# =============================================================================
# FEATURE 5 - field()
# =============================================================================
#
# Sometimes individual attributes require special behaviour.
#
# field() lets us customise a single field
# without affecting the rest of the dataclass.

@dataclass
class User:
    username: str
    password: str = field(repr=False)

user = User("admin", "secret123")

print("\n=== field(repr=False) ===")
print(user)
print("Password still exists:", user.password)

# =============================================================================
# DISCUSSION
# =============================================================================
#
# ASK LEARNERS
#
# Did repr=False remove the password?
#
# Student Thinking:
#
# No.
#
# It only changes how the object is represented.
#
# The data still exists.


# =============================================================================
# BEFORE vs AFTER
# =============================================================================
#
# Basic dataclass
#
#     @dataclass
#
# generates:
#
# __init__
# __repr__
# __eq__
#
#
# Advanced dataclass
#
# adds configuration:
#
# default values
# default_factory
# frozen=True
# order=True
# field()


# =============================================================================
# INTERVIEW OBSERVATION
# =============================================================================
#
# Frequently asked:
#
# Why use default_factory?
#
# Because mutable defaults should not be shared.
#
# Why frozen=True?
#
# To model immutable value objects.
#
# Why order=True?
#
# To generate ordering methods automatically.
#
# Difference between default and default_factory?
#
# default stores a value.
#
# default_factory calls a function to create a value.


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
#                 @dataclass
#                      |
#      ------------------------------------
#      |        |        |       |         |
#   default  factory   frozen   order    field
#
# Every option solves a different real-world problem.


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ Start with the simplest dataclass.
# ✓ Add advanced options only when a problem appears.
# ✓ Use default_factory for mutable objects.
# ✓ Use frozen=True for immutable models.
# ✓ Use order=True for sortable objects.
# ✓ Use field() for per-attribute customisation.


# =============================================================================
# BRIDGE TO THE NEXT TOPIC
# =============================================================================
#
# Our classes have become concise and expressive.
#
# The next question is:
#
# Can we also make our code easier for humans,
# IDEs and static analysis tools to understand?
#
# That leads naturally into Type Hints.
