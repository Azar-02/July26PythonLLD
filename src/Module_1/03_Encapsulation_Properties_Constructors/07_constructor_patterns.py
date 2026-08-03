"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 8 - CONSTRUCTOR PATTERNS
============================================================

Topics Covered
--------------
1. Constructor Design
2. Mutable Default Argument Trap
3. Why trips=[] Is Dangerous
4. Shared State Problem
5. The None Pattern
6. Named Constructors
7. from_dict()
8. from_string()
9. from_env()
10. Constructor Best Practices

"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider a Driver.
#
# Every Driver should maintain:
#
# - name
# - rating
# - completed trips
#
# New drivers should start with:
#
# an empty trips list.
#
# Many developers write:
#
# trips=[]
#
# inside the constructor.
#
# It looks harmless.
#
# But it creates one of the most
# famous bugs in Python.

# ============================================================
# THE NAIVE IMPLEMENTATION
# ============================================================


class DriverV1:

    def __init__(self, name, trips=[]):

        self.name = name
        self.trips = trips


driver_one = DriverV1("Ramesh") 
driver_two = DriverV1("Suresh")

driver_one.trips.append("trip_101")

print("V1")

print(driver_one.trips)
print(driver_two.trips)

# Expected by most developers:
#
# ['trip_101']
# []
#
# Actual Output:
#
# ['trip_101']
# ['trip_101']

# ============================================================
# THE SURPRISE
# ============================================================

# Why does Suresh have a trip?
#
# Suresh never completed a trip.
#
# Yet both drivers show:
#
# ['trip_101']
#
# Something is wrong.

# ============================================================
# WHAT ACTUALLY HAPPENS
# ============================================================

# Important:
#
# trips=[]
#
# is created exactly once.
#
# Not every time __init__ runs.
#
# The list is created when the
# function definition executes.
#
# Therefore:
#
# DriverV1("Ramesh")
# DriverV1("Suresh")
#
# receive references to the same list.

# ============================================================
# PROVING SHARED STATE
# ============================================================

print("\nShared List Check")

print(id(driver_one.trips))
print(id(driver_two.trips))

# Same id
#
# Therefore:
#
# Same object.

# ============================================================
# VISUALIZATION
# ============================================================

# driver_one
#      |
#      v
#   [trip_101]
#      ^
#      |
# driver_two
#
# Two variables.
#
# One list.

# ============================================================
# THE CORRECT SOLUTION
# ============================================================


class DriverV2:

    def __init__(self, name, trips=None):

        self.name = name

        if trips is None:

            self.trips = []

        else:

            self.trips = trips


driver_one = DriverV2("Ramesh")
driver_two = DriverV2("Suresh")

driver_one.trips.append("trip_101")

print("\nV2")

print(driver_one.trips)
print(driver_two.trips)

# Output:
#
# ['trip_101']
# []

# ============================================================
# VERIFYING AGAIN
# ============================================================

print("\nIndependent Lists")

print(id(driver_one.trips))
print(id(driver_two.trips))

# Different ids
#
# Different objects.

# ============================================================
# BEST PRACTICE
# ============================================================

# Never use:
#
# []
# {}
# set()
#
# as default arguments.
#
# Instead use:
#
# None
#
# and create a fresh object
# inside the constructor.

# ============================================================
# CONSTRUCTOR PATTERN #2
# NAMED CONSTRUCTORS
# ============================================================

# Consider:
#
# Driver("Ramesh", 4.8)
#
# Works perfectly.
#
# But what if the data comes from:
#
# - API Response
# - CSV File
# - Environment Variables
#
# We can create helper constructors.

# ============================================================
# BASIC DRIVER CLASS
# ============================================================


class DriverV3:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating

    def __repr__(self):

        return (
            f"Driver(name='{self.name}', "
            f"rating={self.rating})"
        )


# ============================================================
# FROM DICTIONARY
# ============================================================


class DriverV4:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating

    def __repr__(self):

        return (
            f"Driver(name='{self.name}', "
            f"rating={self.rating})"
        )

    # Constructor Pattern #2
    # Named Constructor
    @classmethod
    def from_dict(cls, data):

        return cls(
            data["name"],
            data["rating"]
        )


driver = DriverV4.from_dict(
    {
        "name": "Ramesh",
        "rating": 4.8
    }
)

print("\nfrom_dict")

print(driver)

# ============================================================
# WHY CLASSMETHOD?
# ============================================================

# Question:
#
# Why not use a normal method?
#
# Answer:
#
# We need to create a new object.
#
# There is no object yet.
#
# Therefore:
#
# cls
#
# is required.

# ============================================================
# FROM STRING
# ============================================================


class DriverV5:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating

    def __repr__(self):

        return (
            f"Driver(name='{self.name}', "
            f"rating={self.rating})"
        )

    @classmethod
    def from_string(cls, text):

        name, rating = text.split(",")

        return cls(
            name,
            float(rating)
        )


driver = DriverV5.from_string(
    "Suresh,4.5"
)

print("\nfrom_string")

print(driver)

# ============================================================
# FROM ENVIRONMENT
# ============================================================

import os


class DriverV6:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating

    def __repr__(self):

        return (
            f"Driver(name='{self.name}', "
            f"rating={self.rating})"
        )

    @classmethod
    def from_env(cls):

        name = os.environ.get(
            "DRIVER_NAME",
            "TestDriver"
        )

        rating = float(
            os.environ.get(
                "DRIVER_RATING",
                "5.0"
            )
        )

        return cls(name, rating)


driver = DriverV6.from_env()

print("\nfrom_env")

print(driver)

# ============================================================
# BENEFIT OF NAMED CONSTRUCTORS
# ============================================================

# Compare:
#
# Driver(
#     api_data["name"],
#     api_data["rating"]
# )
#
# vs
#
# Driver.from_dict(api_data)
#
# The second version tells us:
#
# where the data is coming from.
#
# The intent is clearer.

# ============================================================
# MULTIPLE CONSTRUCTION PATHS
# ============================================================

# One class.
#
# Multiple ways to create it.
#
# Driver(...)
#
# Driver.from_dict(...)
#
# Driver.from_string(...)
#
# Driver.from_env(...)

# ============================================================
# SUMMARY TABLE
# ============================================================

# Constructor Pattern 1
#
# Mutable Default Protection
#
# Use:
#
# trips=None
#
# instead of:
#
# trips=[]
#
#
# Constructor Pattern 2
#
# Named Constructors
#
# Use:
#
# @classmethod
#
# to provide meaningful
# creation methods.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Never use mutable objects
# as default arguments.
#
# Use None and create a fresh
# object inside the constructor.
#
# Named constructors are usually
# implemented using @classmethod.
#
# from_dict()
# from_string()
# from_env()
#
# are examples of named constructors.
#
# They improve readability and
# make object creation explicit.
