"""
===============================================================================
PART 03 - DATACLASSES
The Evolution Towards @dataclass
===============================================================================

Topics
------
1. Why data classes become repetitive
2. Evolution from a normal class to @dataclass
3. Generated methods
4. dataclass vs namedtuple
5. Interview discussions
"""

from dataclasses import dataclass

# =============================================================================
# MOTIVATION
# =============================================================================
#
# Up to now we have studied specialised containers:
#
#     namedtuple
#     defaultdict
#     Counter
#     deque
#
# Notice a common theme.
#
# Python keeps removing repetitive code.
#
# Today we ask a similar question:
#
# "Can Python remove repetitive CLASS code as well?"
#
# Surprisingly...
#
# Yes.
#
# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Think about these classes:
#
# Student
# Employee
# Address
# Product
# Point
# Book
#
# Question:
#
# Do these classes contain lots of business logic?
#
# Usually no.
#
# Their primary responsibility is simply storing related data.
#
# Such classes are commonly called "data classes".
#
# Unfortunately we still keep rewriting the same plumbing.
#

# =============================================================================
# VERSION 1 — ONLY __init__
# =============================================================================
#
# Let's build a Student class from scratch.
#

class StudentV1:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

s = StudentV1("Alice", 95)

print("StudentV1 object:", s)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# That output is not very useful.
#
# Python prints the object's address because we never explained
# how the object should represent itself.
#
# New requirement:
#
# We want meaningful printing.
#

# =============================================================================
# VERSION 2 — ADD __repr__
# =============================================================================

class StudentV2:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def __repr__(self):
        return f"StudentV2(name={self.name!r}, marks={self.marks})"

print("\nStudentV2:", StudentV2("Alice", 95))

# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Problem solved?
#
# Not completely.
#
# What if we compare two students?
#

# =============================================================================
# VERSION 3 — EQUALITY
# =============================================================================

class StudentV3:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def __repr__(self):
        return f"StudentV3({self.name!r}, {self.marks})"

    def __eq__(self, other):
        if not isinstance(other, StudentV3):
            return NotImplemented
        return self.name == other.name and self.marks == other.marks

a = StudentV3("Bob", 80)
b = StudentV3("Bob", 80)

print("StudentV3 equality:", a == b)

# =============================================================================
# DISCUSSION
# =============================================================================
#
# Notice the pattern.
#
# Every new requirement forces us to write another special method.
#
# __init__
# __repr__
# __eq__
#
# Tomorrow we may also need:
#
# __lt__
# __hash__
#
# The class grows...
#
# but the BUSINESS LOGIC hardly changes.
#
# We're mostly writing boilerplate.
#

# =============================================================================
# ANALOGY
# =============================================================================
#
# Imagine filling admission forms.
#
# Every form asks for:
#
# - Name
# - Address
# - Date of Birth
#
# Instead of rewriting the format every year,
# we create a reusable template.
#
# @dataclass is Python's template for common data objects.
#

# =============================================================================
# VERSION 4 — DATACLASS
# =============================================================================

@dataclass
class Student:
    name: str
    marks: int

alice = Student("Alice", 95)
print("\nDataclass object:", alice)

bob1 = Student("Bob", 80)
bob2 = Student("Bob", 80)

print("Dataclass equality:", bob1 == bob2)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# We never wrote:
#
# __init__()
# __repr__()
# __eq__()
#
# Yet all of them work.
#
# Python generated them automatically.
#

# =============================================================================
# WHAT DOES @dataclass GENERATE?
# =============================================================================
#
# By default Python generates methods similar to:
#
# ✓ __init__
# ✓ __repr__
# ✓ __eq__
#
# Depending on decorator arguments, it can also generate ordering,
# hashing and other helper methods.
#

# =============================================================================
# SMALL EXPERIMENT
# =============================================================================
#
# Observe the readable representation.
#

print("Readable:", alice)
print("Type    :", type(alice))

# =============================================================================
# dataclass vs namedtuple
# =============================================================================
#
# Students often ask:
#
# "If dataclass exists, why learn namedtuple?"
#
# namedtuple
# ----------
# • immutable
# • lightweight
# • tuple behaviour
#
# dataclass
# ---------
# • richer customisation
# • intended for modelling objects
# • can easily evolve with behaviour
#
# Both solve different problems.
#

# =============================================================================
# COMMON MISCONCEPTIONS
# =============================================================================
#
# Misconception:
#
# Every class should be a dataclass.
#
# Incorrect.
#
# Use dataclasses when the class primarily stores data.
#
# Heavy business logic classes can remain ordinary classes.
#

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================
#
# Why prefer @dataclass?
#
# • Less boilerplate
# • Better readability
# • Easier maintenance
# • Generated comparison methods
#
# Follow-up:
#
# When would you avoid it?
#
# Discuss classes whose main purpose is behaviour rather than state.
#

# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# V1
#   __init__
#
#        ↓
#
# V2
#   + __repr__
#
#        ↓
#
# V3
#   + __eq__
#
#        ↓
#
# @dataclass
#
# Python generates common methods automatically.
#

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ dataclass removes repetitive class boilerplate.
# ✓ Think about the problem before memorising the decorator.
# ✓ Python generates common methods automatically.
# ✓ dataclass complements, not replaces, normal classes.
#

# =============================================================================
# BRIDGE TO THE NEXT FILE
# =============================================================================
#
# We have only scratched the surface.
#
# Next we will study advanced dataclass features:
#
# • default values
# • default_factory
# • frozen=True
# • order=True
# • field()
#
# Those features make dataclasses production-ready.
