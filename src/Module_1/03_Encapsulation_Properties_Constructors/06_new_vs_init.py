"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 6 - __new__ VS __init__
============================================================

Topics Covered
--------------
1. Object Creation Lifecycle
2. Common Misconception About __init__
3. Understanding __new__
4. Understanding __init__
5. Creation vs Initialization
6. Returning Different Objects
7. When __new__ Is Useful
8. Foundation for Singleton Pattern
"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider:
#
# driver = Driver("Ramesh", 4.8)
#
# Ask Students:
#
# What creates the object?
#
# Most students answer:
#
# __init__()
#
# This is one of the most common
# misconceptions in Python.
#
# Today we will discover:
#
# __init__ does NOT create objects.

# ============================================================
# THE COMMON BELIEF
# ============================================================

# Many beginners think:
#
# Step 1:
#     __init__ executes
#
# Step 2:
#     Object appears
#
# Reality:
#
# The object must already exist
# before __init__ can receive self.

# ============================================================
# PROVING THE POINT
# ============================================================

# Question:
#
# Where did self come from?
#
# If __init__ creates the object,
# then who created self?
#
# Someone must create the object first.
#
# That "someone" is:
#
# __new__()

# ============================================================
# FIRST LOOK AT __new__
# ============================================================


class DriverV1:

    def __new__(cls, *args, **kwargs):

        print("__new__ called")

        return super().__new__(cls)

    def __init__(self, name, rating):

        print("__init__ called")

        self.name = name
        self.rating = rating


print("Creating DriverV1")

driver = DriverV1("Ramesh", 4.8)

# Observation:
#
# Output:
#
# __new__ called
# __init__ called
#
# Therefore:
#
# __new__ runs first.

# ============================================================
# RESPONSIBILITIES
# ============================================================

# __new__
#
# Responsible for:
#
# Creating the object
#
#
# __init__
#
# Responsible for:
#
# Initializing the object
#
# These are two different tasks.

# ============================================================
# VISUAL FLOW
# ============================================================

# Driver(...)
#
#      |
#      v
#
# __new__()
#
#      |
#      v
#
# Object Created
#
#      |
#      v
#
# __init__()
#
#      |
#      v
#
# Object Initialized

# ============================================================
# INSPECTING THE CREATED OBJECT
# ============================================================


class DriverV2:

    def __new__(cls, *args, **kwargs):

        print("Creating object")

        obj = super().__new__(cls)

        print("Object id:", id(obj))

        return obj

    def __init__(self, name):

        print("Initializing object")

        print("Object id:", id(self))

        self.name = name


print("\nObject Identity Demo")

driver = DriverV2("Priya")

# Observation:
#
# The object created by __new__
# is the same object received by __init__.

# ============================================================
# THE SURPRISING EXPERIMENT
# ============================================================

# Ask Students:
#
# What happens if __new__
# returns something else?
#
# Most students expect an error.
#
# Let's test it.


class DriverV3:

    def __new__(cls, *args, **kwargs):

        print("Returning a string")

        return "I am not a Driver"

    def __init__(self):

        print("__init__ called")


print("\nReturning Non-Driver Object")

result = DriverV3()

print(result)

print(type(result))

# Observation:
#
# __init__ never executes.
#
# Why?
#
# Because no Driver object was created.

# ============================================================
# IMPORTANT RULE
# ============================================================

# __init__ executes only if:
#
# __new__
#
# returns an instance of the class
# (or a compatible object).
#
# Otherwise Python skips __init__.

# ============================================================
# ANOTHER EXPERIMENT
# ============================================================


class DriverV4:

    def __new__(cls, *args, **kwargs):

        print("Returning integer")

        return 100

    def __init__(self):

        print("__init__ called")


print("\nReturning Integer")

value = DriverV4()

print(value)

print(type(value))

# Again:
#
# __init__ never runs.

# ============================================================
# WHY WOULD ANYONE USE __new__?
# ============================================================

# Most applications never override __new__.
#
# However it becomes useful when:
#
# 1. Singleton Pattern
# 2. Immutable Types
# 3. Object Caching
# 4. Controlling Instance Creation
#
# In normal business applications,
# __init__ is used far more often.

# ============================================================
# A MORE REALISTIC EXAMPLE
# ============================================================


class DriverV5:

    def __new__(cls, *args, **kwargs):

        print("Allocating memory")

        return super().__new__(cls)

    def __init__(self, name, rating):

        print("Populating object state")

        self.name = name
        self.rating = rating

    def __str__(self):

        return (
            f"Driver(name={self.name}, "
            f"rating={self.rating})"
        )


print("\nRealistic Example")

driver = DriverV5("Amit", 4.7)

print(driver)

# Observation:
#
# Memory allocation and state initialization
# are separate responsibilities.

# ============================================================
# CREATION VS INITIALIZATION
# ============================================================

# Creation
#
# "Give me a new object."
#
# Handled by:
#
# __new__()
#
#
# Initialization
#
# "Populate the object's state."
#
# Handled by:
#
# __init__()

# ============================================================
# COMPARISON TABLE
# ============================================================

# __new__
#
# - Runs first
# - Creates object
# - Returns object
# - Can return something else
#
#
# __init__
#
# - Runs second
# - Initializes object
# - Returns None
# - Cannot replace the object

# ============================================================
# FOUNDATION FOR SINGLETON
# ============================================================

# The lecture introduces __new__
# because the next topic requires it.
#
# Question:
#
# What if we want:
#
# Only one object
#
# for an entire application?
#
# That requires control over
# object creation.
#
# Which method controls creation?
#
# __new__()

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# In the next file we will use:
#
# __new__()
#
# to implement:
#
# Singleton Pattern
#
# where:
#
# registry_a is registry_b
#
# evaluates to True.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# __init__ does NOT create objects.
#
# __new__ creates objects.
#
# __init__ initializes objects.
#
# __new__ runs before __init__.
#
# __new__ may return a completely
# different object.
#
# If __new__ does not return an instance,
# __init__ is skipped.
#
# Understanding this distinction is
# essential for advanced Python design.
