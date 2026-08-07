"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 08_builder_summary_and_usage_v1.py
============================================================

Topics Covered
--------------
1. The Complete Evolution
2. When Builder Should Be Used
3. When Builder Should Not Be Used
4. Comparing All Versions
5. Builder vs Telescoping Constructors
6. Builder vs Factory
7. Common Design Mistakes
8. AI Pitfalls
9. Interview Discussion
10. Final Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# We did not begin this journey by introducing Builder.
#
# Instead we started with ordinary object creation and
# allowed each weakness to naturally reveal itself.
#
# The final pattern is easier to remember because every
# design decision now has a reason behind it.

# ============================================================
# THE COMPLETE EVOLUTION
# ============================================================

# Version 1
# ---------
# Empty object + attribute assignment
#
# ✔ Gradual construction
# ✘ Invalid objects may exist
#
# Version 2
# ---------
# Giant constructor
#
# ✔ Validation
# ✔ Safe creation
# ✘ Long parameter list
# ✘ Difficult to read
#
# Version 3
# ---------
# Keyword arguments
#
# ✔ Better readability
# ✘ Still one large constructor
#
# Version 4
# ---------
# Dictionary
#
# ✔ Gradual construction
# ✘ Typo-prone
# ✘ Weak structure
#
# Version 5
# ---------
# Helper + __slots__
#
# ✔ Gradual construction
# ✔ Typo protection
#
# Version 6
# ---------
# Builder
#
# ✔ Gradual construction
# ✔ Validation
# ✔ Discoverable API
# ✔ Fluent interface

# ============================================================
# COMPLETE EXAMPLE
# ============================================================

class Student:

    def __init__(self, builder):
        self.name = builder._name
        self.age = builder._age
        self.grad_year = builder._grad_year

    @staticmethod
    def get_builder():
        return Builder()

    def __repr__(self):
        return (
            f"Student(name={self.name!r}, "
            f"age={self.age}, grad_year={self.grad_year})"
        )


class Builder:

    __slots__ = ("_name", "_age", "_grad_year")

    def __init__(self):
        self._name = None
        self._age = None
        self._grad_year = None

    def set_name(self, value):
        self._name = value
        return self

    def set_age(self, value):
        self._age = value
        return self

    def set_grad_year(self, value):
        self._grad_year = value
        return self

    def build(self):
        if self._name is None:
            raise ValueError("name is required")
        if self._age is None:
            raise ValueError("age is required")
        if self._grad_year is not None and self._grad_year > 2022:
            raise ValueError("invalid graduation year")
        return Student(self)

student = (
    Student.get_builder()
    .set_name("Naman")
    .set_age(21)
    .set_grad_year(2022)
    .build()
)

print("Final Builder")
print(student)

# ============================================================
# WHY THIS DESIGN WORKS
# ============================================================

# The Builder collects information.
#
# build() validates information.
#
# Student represents only valid business state.
#
# Each class has one clear responsibility.

# ============================================================
# MEMORY MODEL
# ============================================================

# Client
#   |
# Student.get_builder()
#   |
# Builder
#   |
# set_name()
# set_age()
# set_grad_year()
#   |
# build()
#   |
# Student

# ============================================================
# WHEN BUILDER MAKES SENSE
# ============================================================

# Builder shines when:
#
# • many optional fields exist
# • construction occurs over time
# • validation is substantial
# • readability is important
# • multiple construction steps exist

# ============================================================
# WHEN BUILDER IS UNNECESSARY
# ============================================================

# Builder is usually unnecessary when:
#
# • the class has only two or three fields
# • construction is always immediate
# • there is little or no validation
# • a constructor already communicates intent clearly

# ============================================================
# BUILDER VS FACTORY
# ============================================================

# Factory answers:
#
# "Which object should be created?"
#
# Builder answers:
#
# "How should one complex object be created?"

# ============================================================
# COMMON MISTAKES
# ============================================================

# • Exposing half-built Student objects.
# • Validating inside every setter.
# • Forgetting build().
# • Putting unrelated business logic inside Builder.
# • Using Builder for tiny classes.

# ============================================================
# AI PITFALL
# ============================================================

# AI-generated examples frequently introduce Builder
# for every class.
#
# That increases complexity instead of reducing it.
#
# Patterns solve specific problems.
#
# They should not be applied automatically.

# ============================================================
# INTERVIEW DISCUSSION
# ============================================================

# Typical interview questions:
#
# • Why Builder instead of constructors?
# • Why return self?
# • Why validate in build()?
# • Why use Builder instead of Factory?
# • Can Builder create immutable objects?
#
# A strong answer always connects the discussion back
# to gradual construction and validation.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Problem
#    |
# Giant Constructor
#    |
# Gradual Construction
#    |
# Helper
#    |
# Builder
#    |
# Fluent Builder
#    |
# Production Builder

# ============================================================
# FINAL TAKEAWAYS
# ============================================================

# • Builder separates construction from representation.
# • Validation occurs once during build().
# • Fluent setters improve readability.
# • Builders simplify creation of complex objects.
# • Use Builder because the problem demands it,
#   not because the pattern exists.

# ============================================================
# END OF BUILDER PATTERN
# ============================================================

# The Builder pattern completes the discussion on
# constructing complex objects safely and readably.
#
# Future design patterns will solve different kinds
# of design problems rather than object construction.
