
"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 06_production_builder_part2_v1.py
============================================================

Topics Covered
--------------
1. Why Multiple Setter Calls Feel Verbose
2. Fluent Interfaces
3. Returning self
4. Method Chaining
5. Progressive Evolution
6. Readability Improvements
7. Runtime Behaviour
8. Common Mistakes
9. Interview Notes
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# The Builder API is now discoverable.
#
# Student.get_builder() tells every developer where to begin.
#
# Builder.build() makes the Builder responsible for producing
# the final object.
#
# One usability issue still remains.
#
# Every attribute assignment occupies a separate line.
#
# As the number of attributes grows, client code becomes
# longer and visually noisy.

# ============================================================
# BASE IMPLEMENTATION
# ============================================================

class Student:

    def __init__(self, builder):
        self.name = builder.name
        self.age = builder.age
        self.grad_year = builder.grad_year

    @staticmethod
    def get_builder():
        return Builder()

    def __repr__(self):
        return f"Student(name={self.name!r}, age={self.age}, grad_year={self.grad_year})"


class Builder:

    __slots__ = ("name", "age", "grad_year")

    def __init__(self):
        self.name = None
        self.age = None
        self.grad_year = None

    def build(self):
        if self.grad_year is not None and self.grad_year > 2022:
            raise ValueError("Invalid graduation year.")
        return Student(self)


# ============================================================
# VERBOSE CLIENT CODE
# ============================================================

builder = Student.get_builder()
builder.name = "Naman"
builder.age = 21
builder.grad_year = 2022

print("Verbose Builder")
print(builder.build())

# ============================================================
# OBSERVATION
# ============================================================

# Every assignment is independent.
#
# The Builder itself already knows which object is being
# modified.
#
# There is an opportunity to make the API more expressive.

# ============================================================
# FIRST SETTER
# ============================================================

class FluentBuilder:

    __slots__ = ("name", "age", "grad_year")

    def __init__(self):
        self.name = None
        self.age = None
        self.grad_year = None

    def set_name(self, name):
        self.name = name
        return self

    def build(self):
        return Student(self)


fb = FluentBuilder()

returned = fb.set_name("Riya")

print("\nReturning self")
print(returned is fb)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The setter returns exactly the same Builder object.
#
# No second Builder is created.
#
# Returning self simply hands back the current object.

print(id(fb))
print(id(returned))

# ============================================================
# MEMORY MODEL
# ============================================================

# fb -----------------------+
#                           |
# returned -----------------+
#                           |
#                           v
#                    FluentBuilder
#
# Both variables reference the same object.

# ============================================================
# ADDING MORE SETTERS
# ============================================================

class FluentBuilderV2:

    __slots__ = ("name", "age", "grad_year")

    def __init__(self):
        self.name = None
        self.age = None
        self.grad_year = None

    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self

    def set_grad_year(self, grad_year):
        self.grad_year = grad_year
        return self

    def build(self):
        if self.grad_year is not None and self.grad_year > 2022:
            raise ValueError("Invalid graduation year.")
        return Student(self)

# ============================================================
# METHOD CHAINING
# ============================================================

student = (
    FluentBuilderV2()
    .set_name("Arjun")
    .set_age(22)
    .set_grad_year(2021)
    .build()
)

print("\nMethod Chaining")
print(student)

# ============================================================
# WHY CHAINING WORKS
# ============================================================

# Each setter performs two operations.
#
# 1. Update Builder state.
# 2. Return the same Builder.
#
# The returned Builder immediately receives the next call.

# ============================================================
# FLOW MODEL
# ============================================================

# Builder
#   |
# set_name()
#   |
# return self
#   |
# set_age()
#   |
# return self
#   |
# set_grad_year()
#   |
# return self
#   |
# build()

# ============================================================
# VALIDATION STILL HAPPENS ONCE
# ============================================================

try:
    (
        FluentBuilderV2()
        .set_name("Invalid")
        .set_grad_year(2030)
        .build()
    )
except ValueError as e:
    print("\nValidation")
    print(type(e).__name__, e)

# ============================================================
# BEFORE VS AFTER
# ============================================================

# Before
#
# builder.name = ...
# builder.age = ...
# builder.grad_year = ...
#
# After
#
# Builder() \
#   .set_name(...) \
#   .set_age(...) \
#   .set_grad_year(...) \
#   .build()

# ============================================================
# COMMON MISTAKE
# ============================================================

# Forgetting to return self.
#
# If a setter returns None, chaining stops immediately.

class BrokenBuilder:

    def set_name(self, name):
        self.name = name
        # Missing: return self

broken = BrokenBuilder()
result = broken.set_name("Demo")

print("\nBroken Setter")
print(result)

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# This style is known as a Fluent Interface.
#
# Builder and Fluent Interface are different ideas,
# but they are frequently used together.

# ============================================================
# BOARD SUMMARY
# ============================================================

# set_x()
#    |
# return self
#    |
# next setter
#    |
# return self
#    |
# build()

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# • Returning self enables method chaining.
# • Chaining improves readability.
# • Validation remains centralized in build().
# • Fluent interfaces complement the Builder pattern.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Our Builder is now convenient to use.
#
# The final discussion focuses on production practices,
# common mistakes, AI pitfalls and real-world usage.
