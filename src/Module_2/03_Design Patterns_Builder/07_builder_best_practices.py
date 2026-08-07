"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 07_builder_best_practices_v1.py
============================================================

Topics Covered
--------------
1. A Production Builder
2. Required vs Optional Fields
3. Centralising Validation
4. Builder Reuse
5. Immutable Thinking
6. Common Mistakes
7. AI Pitfalls
8. Real-world Usage
9. Interview Notes
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# The Builder now provides a pleasant API.
#
# The remaining questions are practical rather than
# syntactic.
#
# How much validation should Builder perform?
#
# Can the same Builder build multiple objects?
#
# Which fields should be mandatory?
#
# These are the questions that appear in production code.

# ============================================================
# A PRODUCTION-STYLE BUILDER
# ============================================================

class Student:

    def __init__(self, builder):
        self.name = builder._name
        self.age = builder._age
        self.grad_year = builder._grad_year

    def __repr__(self):
        return (
            f"Student(name={self.name!r}, "
            f"age={self.age}, grad_year={self.grad_year})"
        )

    @staticmethod
    def get_builder():
        return StudentBuilder()


class StudentBuilder:

    __slots__ = ("_name","_age","_grad_year")

    def __init__(self):
        self._name=None
        self._age=None
        self._grad_year=None

    def set_name(self,name):
        self._name=name
        return self

    def set_age(self,age):
        self._age=age
        return self

    def set_grad_year(self,year):
        self._grad_year=year
        return self

    def build(self):
        if self._name is None:
            raise ValueError("name is required")
        if self._age is None:
            raise ValueError("age is required")
        if self._grad_year is not None and self._grad_year>2022:
            raise ValueError("graduation year cannot exceed 2022")
        return Student(self)

# ============================================================
# REQUIRED VS OPTIONAL
# ============================================================

print("Required Fields")

student=(Student.get_builder()
         .set_name("Naman")
         .set_age(21)
         .build())

print(student)

# ============================================================
# OBSERVATION
# ============================================================

# Required fields are verified only once.
#
# The Builder freely collects information.
#
# The build() method decides whether enough
# information has been collected.

# ============================================================
# BUILD FAILURE
# ============================================================

try:
    Student.get_builder().set_age(18).build()
except ValueError as e:
    print("\nMissing Required Field")
    print(type(e).__name__, e)

# ============================================================
# WHY VALIDATE IN build()?
# ============================================================

# A Builder frequently remains incomplete for most
# of its lifetime.
#
# Rejecting assignments too early would prevent
# gradual construction.
#
# build() is the first moment when we know the
# client expects a finished object.

# ============================================================
# BUILDER REUSE
# ============================================================

builder=(Student.get_builder()
         .set_name("Riya")
         .set_age(20)
         .set_grad_year(2022))

first=builder.build()
second=builder.build()

print("\nBuilder Reuse")
print(first)
print(second)
print(first is second)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# build() creates a fresh Student every time.
#
# The Builder stores configuration.
#
# The Student stores business state.

# ============================================================
# MEMORY MODEL
# ============================================================

# Builder
#    |
#    +----------+
#    |          |
#    v          v
# Student1   Student2
#
# One Builder may produce multiple objects.

# ============================================================
# SHOULD A BUILDER BE REUSED?
# ============================================================

# It depends on the design.
#
# Some APIs encourage reuse.
#
# Others discard the Builder immediately after
# one successful build.
#
# Both approaches exist in real systems.

# ============================================================
# COMMON MISTAKES
# ============================================================

# • Performing business work inside every setter.
# • Forgetting to validate required fields.
# • Returning partially constructed business objects.
# • Mixing Builder state with Student state.

# ============================================================
# AI PITFALL
# ============================================================

# AI-generated Builder examples often validate inside
# every setter.
#
# That appears reasonable but usually destroys the
# flexibility that motivated Builder in the first place.
#
# Gradual construction should remain possible until
# build() is invoked.

# ============================================================
# REAL-WORLD USAGE
# ============================================================

# Builder is common when:
#
# • Many optional fields exist.
# • Object construction spans multiple steps.
# • Validation is expensive.
# • Readability matters more than minimizing lines.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# A frequent follow-up question:
#
# "Why not expose Student.__init__ directly?"
#
# The Builder provides a clearer API, supports
# gradual construction and centralizes validation.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Collect
#   |
# Validate once
#   |
# Build
#   |
# Business Object

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# • build() is the validation checkpoint.
# • Builders collect data; business objects represent
#   valid state.
# • Required and optional fields are handled naturally.
# • Builder improves readability and maintainability.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# The Builder pattern is now complete.
#
# The final file revisits the complete journey,
# summarizes the pattern and discusses when Builder
# should and should not be used.
