"""
============================================================
LLD-2 : OOP-1
PART 5 - THE THREE METHOD TYPES
============================================================

Topics Covered
--------------
1. Instance Methods
2. Why Instance Methods Need self
3. The @classmethod Problem
4. Alternative Constructors
5. Understanding cls
6. The @staticmethod Problem
7. Validation Logic
8. Comparing All Three Method Types
"""

# ============================================================
# SETUP
# ============================================================

class DriverV1:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def accept_ride(self):
        self.is_available = False

# ============================================================
# INSTANCE METHODS
# ============================================================

# So far every method we have written has looked like:
#
# def accept_ride(self):
#
# Such methods operate on a specific object.
#
# They need access to the state of that object.
#
# Therefore Python passes self automatically.

driver_one = DriverV1("Ramesh", 4.8)

print("Before:", driver_one.is_available)

driver_one.accept_ride()

print("After :", driver_one.is_available)

# Observation:
#
# accept_ride changed the state of ONE object.
#
# This is the defining characteristic of
# an instance method.

# ============================================================
# BREAK IT DEMO
# ============================================================

# The lecture recommends intentionally
# breaking things.
#
# What happens if we try:
#
# DriverV1.accept_ride()
#
# Python cannot inject self because
# there is no object available.
#
# Uncomment to see the TypeError.
#
# DriverV1.accept_ride()

# ============================================================
# THE CLASSMETHOD PROBLEM
# ============================================================

# Imagine Driver information arrives from an API.
#
# Example payload:

driver_data = {
    "name": "Mahesh",
    "rating": 4.6
}

# A common solution:

driver = DriverV1(
    driver_data["name"],
    driver_data["rating"]
)

print("\nDriver created manually:")
print(driver.name, driver.rating)

# The lecture asks:
#
# What if ten different places in the codebase
# perform this conversion?
#
# What happens when the API changes?
#
# We now need to update ten places.
#
# What if the Driver class itself knew how
# to create a Driver from a dictionary?

# ============================================================
# INTRODUCING @classmethod
# ============================================================


class DriverV2:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    @classmethod
    def from_dict(cls, data):

        # cls refers to the class itself.
        #
        # cls is to a class what self is
        # to an object.

        return cls(
            data["name"],
            data["rating"]
        )


driver = DriverV2.from_dict(driver_data)

#print((DriverV2.trial(driver).__dict__))

print("\nCreated using classmethod:")
print(driver.name, driver.rating)

# Observation:
#
# We called the method on the class:
#
# DriverV2.from_dict(...)
#
# There was no Driver object yet.
#
# Therefore self would not make sense.
#
# Python passes cls automatically.

# ============================================================
# UNDERSTANDING cls
# ============================================================

# self -> current object
#
# cls  -> current class

print("\ncls demonstration:")
print(type(driver))

# ============================================================
# SURPRISING BEHAVIOUR
# ============================================================

# The lecture explicitly points out that
# classmethods can also be called
# through an instance.

driver_again = driver.from_dict(
    {
        "name": "Suresh",
        "rating": 4.5
    }
)

print("\nCalled via instance:")
print(driver_again.name, driver_again.rating)

# Even though we called through an object,
# cls still refers to the class.

# ============================================================
# USE CASES FOR CLASSMETHODS
# ============================================================

# Use classmethods for:
#
# 1. Alternative constructors
# 2. Factory methods
# 3. Creating objects from external formats
#
# Examples:
#
# from_dict()
# from_json()
# from_csv()
# from_api_response()

# ============================================================
# THE STATICMETHOD PROBLEM
# ============================================================

# New problem.
#
# Uber wants to validate a driver's license.
#
# Does validation need:
#
# self ?
#
# No.
#
# cls ?
#
# No.
#
# It only needs the license number.

# ============================================================
# INTRODUCING @staticmethod
# ============================================================


class DriverV3:

    @staticmethod
    def is_valid_license(license_no):

        return (
            isinstance(license_no, str)
            and len(license_no) == 16
        )


print("\nStatic Method Demo")

print(
    DriverV3.is_valid_license(
        "1234567890123456"
    )
)

print(
    DriverV3.is_valid_license(
        "ABC"
    )
)

# Observation:
#
# No self.
#
# No cls.
#
# Python injects nothing.
#
# The method behaves like a normal function
# that happens to live inside the Driver class.

# ============================================================
# CALLING STATICMETHODS
# ============================================================

driver_obj = DriverV3()

print(
    driver_obj.is_valid_license(
        "1111222233334444"
    )
)

# The lecture notes highlight:
#
# staticmethods can be called using:
#
# DriverV3.is_valid_license(...)
#
# OR
#
# driver_obj.is_valid_license(...)

# ============================================================
# COMPARISON TABLE
# ============================================================

# Method Type      First Argument
# ----------------------------------
# instance         self
# classmethod      cls
# staticmethod     nothing
#
# instance
#     acts on one object
#
# classmethod
#     acts on the class
#
# staticmethod
#     utility logic related to the class

# ============================================================
# COMPLETE EXAMPLE
# ============================================================


class DriverFinal:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["rating"]
        )

    @staticmethod
    def is_valid_license(license_no):
        return (
            isinstance(license_no, str)
            and len(license_no) == 16
        )

    def display(self):
        print(
            f"Driver(name={self.name}, "
            f"rating={self.rating})"
        )


driver = DriverFinal.from_dict(
    {
        "name": "Priya",
        "rating": 4.9
    }
)

driver.display()

print(
    DriverFinal.is_valid_license(
        "1234567890123456"
    )
)

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Instance Method
# - receives self
# - acts on one object
#
# @classmethod
# - receives cls
# - acts on the class
# - commonly used for alternative constructors
#
# @staticmethod
# - receives nothing automatically
# - utility / validation logic
#
# Remember:
#
# self -> object
# cls  -> class
# staticmethod -> neither
