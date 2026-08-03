"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 03_representation_methods.py
============================================================

Topics Covered
--------------
1. Why Object Representation Matters
2. Default Object Printing
3. __str__
4. __repr__
5. Difference Between __str__ and __repr__
6. __format__
7. f-Strings and Formatting
8. Best Practices
9. Interview Question
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider the following:
#
# We create a Driver object.
#
# Then we print it.
#
# Question:
#
# What should the output look like?
#
# Should Python display:
#
# <__main__.Driver object at 0x...>
#
# or
#
# Driver(name=Ramesh, rating=4.8)
#
# Good object representation
# makes debugging easier.

# ============================================================
# DEFAULT OBJECT PRINTING
# ============================================================


class Driver:

    def __init__(
        self,
        name,
        rating
    ):
        self.name = name
        self.rating = rating


driver = Driver(
    "Ramesh",
    4.8
)

print("Default Printing")
print(driver)

# Observation:
#
# Python prints a memory-oriented
# representation.
#
# Not very useful.

# ============================================================
# WHY IS THIS A PROBLEM?
# ============================================================

# Suppose an application contains:
#
# 100 Drivers
# 500 Trips
# 1000 Payments
#
# Debugging becomes difficult if
# every object prints as a memory address.

# ============================================================
# INTRODUCING __str__
# ============================================================

# __str__ controls:
#
# str(obj)
#
# and
#
# print(obj)

# ============================================================
# DRIVER WITH __str__
# ============================================================


class DriverV2:

    def __init__(
        self,
        name,
        rating
    ):
        self.name = name
        self.rating = rating

    def __str__(self):

        return (
            f"Driver(name={self.name}, "
            f"rating={self.rating})"
        )


driver = DriverV2(
    "Ramesh",
    4.8
)

print("\nUsing __str__")
print(driver)

# Observation:
#
# Much more readable.

# ============================================================
# str() EXPLICITLY
# ============================================================

print("\nstr(driver)")

print(
    str(driver)
)

# Observation:
#
# print(driver)
#
# internally uses str(driver).

# ============================================================
# INTRODUCING __repr__
# ============================================================

# __repr__ is another
# representation method.
#
# It is intended for:
#
# Developers
# Debugging
# Interactive sessions

# ============================================================
# DRIVER WITH __repr__
# ============================================================


class DriverV3:

    def __init__(
        self,
        name,
        rating
    ):
        self.name = name
        self.rating = rating

    def __repr__(self):

        return (
            f"Driver("
            f"name='{self.name}', "
            f"rating={self.rating})"
        )


driver = DriverV3(
    "Ramesh",
    4.8
)

print("\nUsing repr()")

print(
    repr(driver)
)

# Observation:
#
# repr() explicitly calls
# __repr__.

# ============================================================
# __str__ AND __repr__
# ============================================================


class DriverV4:

    def __init__(
        self,
        name,
        rating
    ):
        self.name = name
        self.rating = rating

    def __str__(self):

        return (
            f"Driver {self.name} "
            f"({self.rating})"
        )

    def __repr__(self):

        return (
            f"Driver("
            f"name='{self.name}', "
            f"rating={self.rating})"
        )


driver = DriverV4(
    "Ramesh",
    4.8
)

print("\n__str__ Example")
print(driver)

print("\n__repr__ Example")
print(repr(driver))

# Observation:
#
# __str__
#
# Human friendly.
#
# __repr__
#
# Developer friendly.

# ============================================================
# FALLBACK BEHAVIOUR
# ============================================================

# If __str__ does not exist,
# Python falls back to __repr__.

# ============================================================
# DEMONSTRATION
# ============================================================


class DriverV5:

    def __init__(
        self,
        name
    ):
        self.name = name

    def __repr__(self):

        return (
            f"DriverV5('{self.name}')"
        )


driver = DriverV5(
    "Suresh"
)

print("\nFallback Behaviour")

print(driver)

# Observation:
#
# print() used __repr__ because
# __str__ was missing.

# ============================================================
# WHY __repr__ IS IMPORTANT
# ============================================================

# Containers often rely on repr.
#
# Example:
#
# list
# set
# dictionary values

# ============================================================
# LIST EXAMPLE
# ============================================================


class Rider:

    def __init__(
        self,
        name
    ):
        self.name = name

    # def __str__(self):

    #     return (
    #         f"Rider('{self.name}')"
    #     )
    
    def __repr__(self):

        return (
            f"Rider('{self.name}')"
        )


riders = [
    Rider("Ramesh"),
    Rider("Suresh"),
    Rider("Mahesh")
]

print("\nList Representation")

print(riders)

# Observation:
#
# Lists display repr()
# of contained objects.

# ============================================================
# INTRODUCING __format__
# ============================================================

# __format__ supports:
#
# format(obj, spec)
#
# and
#
# f-strings

# ============================================================
# DRIVER WITH __format__
# ============================================================


class DriverV6:

    def __init__(
        self,
        name,
        rating
    ):
        self.name = name
        self.rating = rating

    def __str__(self):

        return (
            f"{self.name} "
            f"({self.rating})"
        )

    def __format__(
        self,
        spec
    ):

        if spec == "short":
            return (
                f"{self.name}"
            )

        if spec == "rating":
            return (
                f"{self.rating}★"
            )

        return str(self)


driver = DriverV6(
    "Ramesh",
    4.8
)

print("\nFormat Example")

print(
    f"{driver:short}"
)

print(
    f"{driver:rating}"
)

print(
    f"{driver}"
)

# Observation:
#
# __format__ allows custom
# formatting styles.

# ============================================================
# HOW f-STRINGS WORK
# ============================================================

# f"{obj:short}"
#
# becomes:
#
# obj.__format__("short")

# ============================================================
# BEST PRACTICE #1
# ============================================================

# Implement __str__
#
# when users need a clean
# readable representation.

# ============================================================
# BEST PRACTICE #2
# ============================================================

# Implement __repr__
#
# for debugging and development.

# ============================================================
# BEST PRACTICE #3
# ============================================================

# Keep representations concise.
#
# Avoid huge outputs.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Returning non-string values
# from __str__ or __repr__.
#
# These methods must return strings.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Difference between:
#
# __str__
#
# and
#
# __repr__
#
# __str__:
# User friendly.
#
# __repr__:
# Developer/debugging friendly.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# __str__ controls print().
#
# __repr__ controls developer
# representation.
#
# __repr__ is used heavily by
# containers.
#
# __format__ supports custom
# formatting.
#
# Object representation is a
# major part of usability.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We now understand how objects
# represent themselves.
#
# Next we revisit the Zone mystery
# and finally understand the
# relationship between:
#
# __eq__
# __hash__
#
# Next:
#
# 04_eq_hash_contract.py
