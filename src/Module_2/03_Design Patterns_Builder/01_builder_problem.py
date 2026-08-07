"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 01_builder_problem_v2.py
============================================================

Topics Covered
--------------
1. Why Builder Exists
2. Creating Objects Incrementally
3. Invalid Object States
4. Constructor Validation
5. Giant Constructors
6. Keyword Arguments
7. Remaining Limitations
8. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# Creating objects looks easy when a class has only
# two or three attributes.
#
# Real business objects rarely stay that small.
#
# A Student, User, Order or Employee object may contain
# ten, fifteen or even twenty attributes.
#
# As the object grows, object creation itself becomes
# a design problem.
#

# ============================================================
# VERSION 1 : CREATE AN EMPTY OBJECT
# ============================================================

class StudentV1:

    def __init__(self):
        self.name = None
        self.age = None
        self.psp = None
        self.batch = None
        self.student_id = None
        self.university_name = None
        self.grad_year = None
        self.phone_number = None


student = StudentV1()
student.name = "Naman"
student.age = 21
student.psp = 89.21
student.batch = "April"

print("StudentV1")
print(student.__dict__)

# ============================================================
# OBSERVATION
# ============================================================

# This approach provides maximum flexibility.
#
# Every attribute can be assigned whenever information
# becomes available.
#
# Unfortunately, the object exists long before anyone
# verifies whether it is valid.

# ============================================================
# THE INVALID OBJECT PROBLEM
# ============================================================

# Suppose the business introduces the rule:
#
#     Graduation year must not exceed 2022.
#
# Nothing currently forces that rule to be checked.

incomplete = StudentV1()
incomplete.name = "Riya"

print("\nIncomplete Object")
print(incomplete.__dict__)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Python happily creates an incomplete object.
#
# Validation depends entirely on the programmer
# remembering to perform it later.
#
# This means invalid objects can exist inside the system.

# ============================================================
# MEMORY MODEL
# ============================================================

# incomplete ------------+
#                         |
#                         v
#                Student Object
#          name  -> "Riya"
#          age   -> None
#          grad  -> None
#
# The object already occupies memory even though it
# violates business expectations.

# ============================================================
# VERSION 2 : VALIDATE INSIDE THE CONSTRUCTOR
# ============================================================

class StudentV2:

    def __init__(
        self,
        name,
        age,
        psp,
        batch,
        student_id,
        university_name,
        grad_year,
        phone_number,
    ):

        if grad_year > 2022:
            raise ValueError("Graduation year cannot exceed 2022.")

        self.name = name
        self.age = age
        self.psp = psp
        self.batch = batch
        self.student_id = student_id
        self.university_name = university_name
        self.grad_year = grad_year
        self.phone_number = phone_number


student = StudentV2(
    "Naman",
    21,
    89.21,
    "April",
    101,
    "ABC University",
    2022,
    "9999999999",
)

print("\nValidated Student")
print(student.__dict__)

# ============================================================
# OBSERVATION
# ============================================================

# Validation now occurs during construction.
#
# Invalid Student objects are rejected before the caller
# receives a usable object.
#
# This is a much safer design.

# ============================================================
# THE NEXT PROBLEM
# ============================================================

print("\nLong Positional Constructor")

student = StudentV2(
    "Naman",
    21,
    89.21,
    "April",
    101,
    "ABC University",
    2022,
    "9999999999",
)

print(student.name)

# Reading this constructor requires remembering the
# meaning of every position.
#
# As more fields are added, readability steadily declines.

# ============================================================
# KEYWORD ARGUMENTS
# ============================================================

student = StudentV2(
    name="Naman",
    age=21,
    psp=89.21,
    batch="April",
    student_id=101,
    university_name="ABC University",
    grad_year=2022,
    phone_number="9999999999",
)

print("\nKeyword Constructor")
print(student.name)

# ============================================================
# OBSERVATION
# ============================================================

# Keyword arguments solve the readability problem.
#
# Every value is now labelled.
#
# Accidentally swapping arguments becomes much less likely.

# ============================================================
# THE PROBLEM STILL REMAINS
# ============================================================

# Constructors execute exactly once.
#
# Either every value is available at construction time,
# or object creation cannot proceed.
#
# Modern applications frequently receive information from
# databases, APIs and background services at different
# points in time.
#
# A constructor cannot naturally support gradual
# object construction.

# ============================================================
# COMPARISON
# ============================================================

# Empty Object
# ------------
# ✔ Flexible
# ✔ Gradual construction
# ✘ Invalid objects can exist
#
# Constructor
# -----------
# ✔ Centralised validation
# ✔ Safe creation
# ✔ Better correctness
# ✘ Large parameter list
# ✘ Difficult to extend
# ✘ Cannot construct gradually

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Long constructors are commonly referred to as the
# telescoping constructor problem.
#
# The Builder pattern is one of the most common solutions.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Object creation deserves as much attention as object design.
#
# Constructor validation solves correctness but introduces
# maintainability issues.
#
# Keyword arguments improve readability but do not solve
# gradual construction.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Next:
#
# 02_default_values_and_constructor_limits.py
