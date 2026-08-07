"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 04_first_builder_v1.py
============================================================

Topics Covered
--------------
1. From Helper to Builder
2. Why the Name Matters
3. First Builder Implementation
4. Validation During Construction
5. Builder Collects, Student Validates
6. Preventing Invalid Objects
7. Runtime Flow
8. First Complete Builder Example
9. Common Mistakes
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# The previous file introduced a Helper class.
#
# It solved two important problems.
#
# 1. Values could be collected gradually.
# 2. __slots__ prevented accidental attribute names.
#
# However, one question still remains.
#
# If the Helper only stores values, who is responsible
# for deciding whether those values are valid?
#
# The answer to that question finally leads us to the
# Builder pattern.

# ============================================================
# THE HELPER HAS ONLY ONE RESPONSIBILITY
# ============================================================

# The Helper is intentionally "dumb".
#
# It simply remembers information.
#
# It should not know business rules.
#
# Otherwise every assignment would need validation,
# even though the object is still incomplete.

class Helper:

    __slots__ = (
        "name",
        "age",
        "psp",
        "batch",
        "student_id",
        "university_name",
        "grad_year",
        "phone_number",
    )

    def __init__(self):
        self.name = None
        self.age = None
        self.psp = None
        self.batch = None
        self.student_id = None
        self.university_name = None
        self.grad_year = None
        self.phone_number = None


helper = Helper()
helper.name = "Naman"
helper.age = 21
helper.psp = 89.21

print("Helper State")
for slot in Helper.__slots__:
    print(f"{slot:18} -> {getattr(helper, slot)}")

# ============================================================
# OBSERVATION
# ============================================================

# Information can arrive in any order.
#
# Nothing forces every field to be available
# immediately.

# ============================================================
# THE REAL BUSINESS OBJECT
# ============================================================

class Student:

    def __init__(self, helper):

        if helper.grad_year is not None and helper.grad_year > 2022:
            raise ValueError("Graduation year cannot exceed 2022.")

        self.name = helper.name
        self.age = helper.age
        self.psp = helper.psp
        self.batch = helper.batch
        self.student_id = helper.student_id
        self.university_name = helper.university_name
        self.grad_year = helper.grad_year
        self.phone_number = helper.phone_number

    def __repr__(self):
        return (
            f"Student(name={self.name!r}, "
            f"age={self.age}, "
            f"grad_year={self.grad_year})"
        )


# ============================================================
# WHY VALIDATION BELONGS HERE
# ============================================================

# Validation happens exactly once.
#
# Every Student object must pass through this
# constructor.
#
# There is now a single checkpoint for correctness.

# ============================================================
# SUCCESSFUL CONSTRUCTION
# ============================================================

builder = Helper()

builder.name = "Naman"
builder.age = 21
builder.psp = 89.21
builder.grad_year = 2022

student = Student(builder)

print("\nSuccessful Build")
print(student)

# ============================================================
# MEMORY MODEL
# ============================================================

# Helper Object
# ---------------------
# name ------+
# age -------+
# psp -------+-------------------+
# grad_year -+                   |
#                                 |
#                                 v
#                         Student Constructor
#                                 |
#                         Validation executes
#                                 |
#                                 v
#                         Student Object

# ============================================================
# VALIDATION FAILURE
# ============================================================

invalid = Helper()

invalid.name = "Riya"
invalid.age = 22
invalid.grad_year = 2025

print("\nValidation Failure")

try:
    Student(invalid)
except ValueError as error:
    print(type(error).__name__, error)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Notice what happened.
#
# The Helper object still exists.
#
# The Student object never comes into existence.
#
# This is exactly what we wanted from the beginning.
#
# Temporary state is allowed.
#
# Invalid business objects are not.

# ============================================================
# BEFORE VS AFTER
# ============================================================

# Empty Object
# ------------
# Validation may never happen.
#
# Giant Constructor
# -----------------
# Validation happens immediately.
# Gradual construction disappears.
#
# Helper + Student
# ----------------
# Gradual construction returns.
# Validation remains guaranteed.

# ============================================================
# WHY THE NAME "BUILDER"?
# ============================================================

# The Helper has now become more than a storage object.
#
# Its entire purpose is to help create another object.
#
# In software design literature, such an object is
# traditionally called a Builder.
#
# From this point onward we simply rename Helper to
# Builder.
#
# The behaviour remains the same.
#
# The intention becomes much clearer.

Builder = Helper

builder = Builder()
builder.name = "Arjun"
builder.age = 20
builder.grad_year = 2021

student = Student(builder)

print("\nBuilder Example")
print(student)

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Builder is not the final business object.
#
# Builder is only a construction object.
#
# It exists temporarily while information is being
# collected.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# A common interview discussion is:
#
# "Why not put validation directly inside Builder?"
#
# A good answer is that Builder frequently represents
# an incomplete object.
#
# Validation belongs at the point where the real object
# is created.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Builder
# -------
# ✔ Collect values gradually
# ✔ Temporary object
#
# Student
# -------
# ✔ Validate
# ✔ Create final business object
# ✔ Reject invalid state

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Builder separates data collection from object creation.
#
# Temporary state is acceptable inside Builder.
#
# Invalid Student objects never enter the system.
#
# This is the first complete version of the Builder idea.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Our Builder works.
#
# However, using it still feels clumsy because clients
# must create Builder manually and assign attributes one
# by one.
#
# The next file improves the API and moves toward a
# production-quality Builder.
