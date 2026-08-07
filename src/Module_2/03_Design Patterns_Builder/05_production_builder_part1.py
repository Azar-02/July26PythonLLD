"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 05_production_builder_part1_v1.py
============================================================

Topics Covered
--------------
1. Why the First Builder Still Feels Clumsy
2. Discoverability Problem
3. Introducing Student.get_builder()
4. Why staticmethod?
5. Who Should Actually Build?
6. Moving Construction into Builder.build()
7. Runtime Flow
8. Before vs After
9. Interview Notes
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# We now have our first Builder.
#
# It solves gradual construction.
#
# It guarantees validation before a Student object exists.
#
# However, writing client code still feels awkward.
#
# The API exposes implementation details that every caller
# must remember.

class Builder:

    __slots__ = ("name", "age", "grad_year")

    def __init__(self):
        self.name = None
        self.age = None
        self.grad_year = None


class StudentV1:

    def __init__(self, builder):

        if builder.grad_year is not None and builder.grad_year > 2022:
            raise ValueError("Invalid graduation year.")

        self.name = builder.name
        self.age = builder.age
        self.grad_year = builder.grad_year

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age}, grad_year={self.grad_year})"


# ============================================================
# FIRST VERSION OF CLIENT CODE
# ============================================================

builder = Builder()
builder.name = "Naman"
builder.age = 21
builder.grad_year = 2022

student = StudentV1(builder)

print("Current Client Code")
print(student)

# ============================================================
# OBSERVATION
# ============================================================

# This works perfectly.
#
# The problem is not correctness.
#
# The problem is discoverability.
#
# Someone opening Student for the first time has no clue
# that a separate Builder object is expected.

# ============================================================
# DISCOVERABILITY
# ============================================================

# Every public API should guide developers toward the
# correct usage.
#
# At the moment, nothing inside Student hints that a
# Builder even exists.

# ============================================================
# IMPROVEMENT 1
# ============================================================

class StudentV2:

    def __init__(self, builder):

        if builder.grad_year is not None and builder.grad_year > 2022:
            raise ValueError("Invalid graduation year.")

        self.name = builder.name
        self.age = builder.age
        self.grad_year = builder.grad_year

    @staticmethod
    def get_builder():
        return Builder()

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age}, grad_year={self.grad_year})"


builder = StudentV2.get_builder()
builder.name = "Riya"
builder.age = 20
builder.grad_year = 2022

student = StudentV2(builder)

print("\nStudent.get_builder()")
print(student)

# ============================================================
# WHY staticmethod?
# ============================================================

# No Student object exists yet.
#
# Therefore there is no self.
#
# We only need a utility associated with the Student class.
#
# A staticmethod expresses exactly that idea.

print("\nBuilder Type")
print(type(StudentV2.get_builder()).__name__)

# ============================================================
# MEMORY MODEL
# ============================================================

# Student Class
#      |
#      +---- get_builder()
#                  |
#                  v
#              Builder Object
#                  |
#          Collect information
#                  |
#                  v
#         Student(builder)

# ============================================================
# ANOTHER SMALL DESIGN SMELL
# ============================================================

# Look carefully at the final line:
#
#     Student(builder)
#
# Which object is actually performing the build?
#
# Surprisingly, Builder only stores data.
#
# Student still performs the construction.

# ============================================================
# IMPROVEMENT 2
# ============================================================

class BuilderV2:

    __slots__ = ("name", "age", "grad_year")

    def __init__(self):
        self.name = None
        self.age = None
        self.grad_year = None

    def build(self):

        if self.grad_year is not None and self.grad_year > 2022:
            raise ValueError("Invalid graduation year.")

        return StudentV3(self)


class StudentV3:

    def __init__(self, builder):
        self.name = builder.name
        self.age = builder.age
        self.grad_year = builder.grad_year

    @staticmethod
    def get_builder():
        return BuilderV2()

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age}, grad_year={self.grad_year})"


builder = StudentV3.get_builder()
builder.name = "Arjun"
builder.age = 22
builder.grad_year = 2021

student = builder.build()

print("\nBuilder.build()")
print(student)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The Builder now deserves its name.
#
# It no longer behaves like a passive container.
#
# It performs the final construction step itself.

try:
    bad = StudentV3.get_builder()
    bad.name = "Bad"
    bad.grad_year = 2025
    bad.build()
except ValueError as e:
    print("\nValidation")
    print(type(e).__name__, e)

# ============================================================
# BEFORE VS AFTER
# ============================================================

# Earlier
# -------
# Builder()
# Student(builder)
#
# Now
# ---
# Student.get_builder()
# builder.build()
#
# The responsibilities are clearer.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# A Builder should generally be responsible for producing
# the finished object.
#
# Otherwise it is merely acting as a temporary data holder.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Creating a Builder but still forcing every client to
# invoke the constructor directly.
#
# A better API guides the user naturally.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Student.get_builder()
#        |
#        v
#    Builder
#        |
#   collect data
#        |
#   build()
#        |
#        v
#    Student

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# • APIs should be discoverable.
# • staticmethod exposes a Builder naturally.
# • Builder should perform the build.
# • Responsibilities become cleaner and easier to follow.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# The Builder API is now much cleaner.
#
# One annoyance still remains.
#
# Every attribute assignment requires a separate line.
#
# The next improvement introduces fluent setters and
# method chaining.
