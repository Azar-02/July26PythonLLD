"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 02_default_values_and_constructor_limits_v1.py
============================================================

Topics Covered
--------------
1. Optional Constructor Parameters
2. Default Values
3. Mutable Default Argument Trap
4. Why None Is Safer
5. Growing Constructors
6. Why Constructors Cannot Build Gradually
7. Interview Observations
8. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we moved validation into the constructor.
#
# That solved one important problem:
#
# Invalid Student objects could no longer be created.
#
# Unfortunately, another problem now appears.
#
# A real application rarely knows every piece of information
# at the exact moment an object is created.
#
# Some values arrive immediately.
# Others arrive from a database.
# Others arrive after an API call.
#
# Before looking for a completely different design, we first
# examine whether constructors themselves can be improved.

# ============================================================
# VERSION 1 : OPTIONAL PARAMETERS
# ============================================================

class StudentV1:

    def __init__(
        self,
        name,
        age,
        psp,
        subjects=[],
        phone_number=None,
    ):
        self.name = name
        self.age = age
        self.psp = psp
        self.subjects = subjects
        self.phone_number = phone_number


print("Creating first student")

s1 = StudentV1("Naman", 21, 89.21)
s1.subjects.append("Math")

print(s1.subjects)

print("\nCreating second student")

s2 = StudentV1("Riya", 20, 91.0)

print(s2.subjects)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# At first glance this looks impossible.
#
# Nobody explicitly copied "Math" into Riya's object.
#
# Yet both students appear to share the same list.

# ============================================================
# WHY THIS HAPPENS
# ============================================================

# Default argument values are evaluated only once.
#
# The list object is created when Python executes the
# function definition.
#
# Every constructor call that does not provide its own
# subjects list reuses exactly the same object.

print("\nIdentity Check")
print(id(s1.subjects))
print(id(s2.subjects))

# ============================================================
# MEMORY MODEL
# ============================================================

# s1 -------------------------+
#                             |
#                             |
# s2 -------------------------+
#                             |
#                             v
#                    ["Math"]
#
# Both objects point to one shared list.

# ============================================================
# THE SAFE APPROACH
# ============================================================

class StudentV2:

    def __init__(
        self,
        name,
        age,
        psp,
        subjects=None,
        phone_number=None,
    ):

        self.name = name
        self.age = age
        self.psp = psp
        self.subjects = [] if subjects is None else subjects
        self.phone_number = phone_number


safe_one = StudentV2("A", 21, 90)
safe_two = StudentV2("B", 22, 91)

safe_one.subjects.append("Physics")

print("\nSafe Lists")
print(safe_one.subjects)
print(safe_two.subjects)

print(id(safe_one.subjects))
print(id(safe_two.subjects))

# ============================================================
# OBSERVATION
# ============================================================

# Each Student now owns an independent list.
#
# Mutating one object no longer affects another.

# ============================================================
# A LARGER PROBLEM
# ============================================================

# Default values make constructors easier to call.
#
# They do not make constructors smaller.
#
# As the class grows, the constructor continues to
# collect more parameters, more defaults and more
# validation logic.

# Example only.

class StudentV3:

    def __init__(
        self,
        name,
        age,
        psp,
        batch=None,
        student_id=None,
        university_name=None,
        grad_year=None,
        phone_number=None,
        address=None,
        city=None,
        state=None,
    ):
        self.name = name


print("\nLarge constructor still exists.")

# ============================================================
# WHY CONSTRUCTORS STILL FAIL
# ============================================================

# Imagine the following sequence:
#
# Step 1
# ------
# Name and age arrive from a registration form.
#
# Step 2
# ------
# University arrives from another service.
#
# Step 3
# ------
# Phone number arrives after OTP verification.
#
# A constructor executes exactly once.
#
# It cannot naturally pause after Step 1,
# continue after Step 2 and finally finish
# after Step 3.

# ============================================================
# COMPARISON
# ============================================================

# Default Values
# --------------
# ✔ Fewer required arguments
# ✔ More convenient API
#
# Still Problems
# --------------
# ✘ Giant constructor
# ✘ Validation grows
# ✘ Cannot build gradually

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# One of the most common Python interview questions is:
#
# "Why should mutable objects not be used as default
# arguments?"
#
# The expected explanation is that default arguments are
# created once and reused.

# ============================================================
# COMMON MISTAKE
# ============================================================

# ❌ def __init__(..., items=[]):
#
# ✔ def __init__(..., items=None):
#       self.items = [] if items is None else items

# ============================================================
# BOARD SUMMARY
# ============================================================

# Default values solve convenience.
#
# They do not solve object construction.
#
# Constructors continue to become larger as
# business requirements grow.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# • Never use mutable default arguments.
# • Use None and create a fresh object.
# • Default values reduce mandatory parameters.
# • Constructors still become large.
# • Gradual object construction remains unsolved.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Constructors are reaching their practical limits.
#
# The next file explores a completely different idea:
#
# Collect values first.
# Build the object later.
#
# Next:
#
# 03_from_dict_to_helper.py
