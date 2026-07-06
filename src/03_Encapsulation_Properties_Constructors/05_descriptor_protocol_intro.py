"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 5 - DESCRIPTOR PROTOCOL INTRODUCTION
============================================================

Topics Covered
--------------
1. Is @property Magic?
2. Understanding property()
3. fget, fset, fdel
4. Recreating Property Manually
5. Introduction to Descriptors
6. __get__()
7. __set__()
8. __delete__()
9. Building a Simple Descriptor
10. Understanding What @property Really Is
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we learned:
#
# @property
# @rating.setter
# @rating.deleter
#
# These allowed us to write:
#
# driver.rating
#
# and
#
# driver.rating = 4.8
#
# while still executing validation logic.
#
# The natural question is:
#
# Is @property magic?
#
# Or is something else happening behind the scenes?

# ============================================================
# REVISITING @property
# ============================================================


class DriverWithProperty:

    def __init__(self, rating):
        self._rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = value


driver = DriverWithProperty(4.8)

print("Property Demo")

print(driver.rating)

driver.rating = 4.9

print(driver.rating)

# Everything appears normal.
#
# However:
#
# @property is not a language keyword.
#
# It is actually built using
# a Python class.

# ============================================================
# THE property() FUNCTION
# ============================================================

# What we write:
#
# @property
# def rating(...):
#     ...
#
# is closely related to:
#
# property(fget, fset, fdel)
#
# where:
#
# fget
#     getter function
#
# fset
#     setter function
#
# fdel
#     deleter function

# ============================================================
# BUILDING PROPERTY MANUALLY
# ============================================================


class DriverManualProperty:

    def __init__(self, rating):
        self._rating = rating

    def get_rating(self):

        print("Getter Executed")

        return self._rating

    def set_rating(self, value):

        print("Setter Executed")

        self._rating = value

    rating = property(
        get_rating,
        set_rating
    )


driver = DriverManualProperty(4.8)

print("\nManual Property")

print(driver.rating)

driver.rating = 4.7

print(driver.rating)

# Observation:
#
# We did not use:
#
# @property
#
# Yet the behaviour is the same.
#
# This is a major clue.
#
# @property is built on top of
# the property() mechanism.

# ============================================================
# WHAT DOES property() RETURN?
# ============================================================

# Question:
#
# What exactly is property() ?
#
# Answer:
#
# property is itself a class.

print("\nproperty Type")

print(type(property))

# The property class creates an object.
#
# That object participates in Python's
# attribute access machinery.

# ============================================================
# INTRODUCING DESCRIPTORS
# ============================================================

# To understand property,
# we need one new idea:
#
# Descriptor
#
# A descriptor is an object that controls
# attribute access.
#
# Descriptors can intercept:
#
# Reading
# Writing
# Deleting

# ============================================================
# THE THREE SPECIAL METHODS
# ============================================================

# Descriptors typically implement:
#
# __get__()
#
# __set__()
#
# __delete__()
#
# These methods are automatically
# invoked by Python.

# ============================================================
# BUILDING A SIMPLE DESCRIPTOR
# ============================================================


class SimpleDescriptor:

    def __get__(
        self,
        instance,
        owner
    ):

        print("__get__ called")

        return "Descriptor Value"

    def __set__(
        self,
        instance,
        value
    ):

        print(
            "__set__ called with:",
            value
        )

    def __delete__(
        self,
        instance
    ):

        print("__delete__ called")


# ============================================================
# USING THE DESCRIPTOR
# ============================================================


class DriverWithDescriptor:

    rating = SimpleDescriptor()

    def __init__(self, name):
        self.name = name


driver = DriverWithDescriptor(
    "Ramesh"
)

print("\nDescriptor Read")

print(driver.rating)

# Observation:
#
# We wrote:
#
# driver.rating
#
# Yet Python executed:
#
# __get__()

# ============================================================
# DESCRIPTOR WRITE
# ============================================================

driver.rating = 4.8

# Observation:
#
# We wrote:
#
# driver.rating = 4.8
#
# Yet Python executed:
#
# __set__()

# ============================================================
# DESCRIPTOR DELETE
# ============================================================

del driver.rating

# Observation:
#
# We wrote:
#
# del driver.rating
#
# Yet Python executed:
#
# __delete__()

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Earlier:
#
# @property
#
# intercepted:
#
# Read
# Write
# Delete
#
# Descriptors do exactly the same thing.
#
# This is not a coincidence.

# ============================================================
# THE CONNECTION TO PROPERTY
# ============================================================

# property objects are descriptors.
#
# Internally they participate in
# the same attribute access system.
#
# The property class implements
# descriptor behaviour.
#
# This is why:
#
# driver.rating
#
# can execute code.

# ============================================================
# VISUAL FLOW
# ============================================================

# driver.rating
#
#        |
#        v
#
#     __get__()
#
#
# driver.rating = 4.8
#
#        |
#        v
#
#     __set__()
#
#
# del driver.rating
#
#        |
#        v
#
#    __delete__()

# ============================================================
# A SLIGHTLY MORE REALISTIC EXAMPLE
# ============================================================


class PositiveNumber:

    def __init__(self):
        self.value = 0

    def __get__(
        self,
        instance,
        owner
    ):
        return self.value

    def __set__(
        self,
        instance,
        value
    ):

        if value < 0:

            raise ValueError(
                "Only positive values allowed"
            )

        self.value = value


class BankAccount:

    balance = PositiveNumber()


account = BankAccount()

account.balance = 1000

print("\nValidated Descriptor")

print(account.balance)

# Uncomment:
#
# account.balance = -500

# ============================================================
# WHY SHOULD WE CARE?
# ============================================================

# Most Python developers never write
# custom descriptors.
#
# However:
#
# Understanding descriptors helps explain:
#
# @property
# ORM frameworks
# Dataclasses
# Validation libraries
#
# and many advanced Python features.

# ============================================================
# WHAT HAVE WE LEARNED?
# ============================================================

# @property is not magic.
#
# property(...) exists.
#
# property objects behave like descriptors.
#
# Descriptors intercept:
#
# Reading
# Writing
# Deleting
#
# through:
#
# __get__()
# __set__()
# __delete__()

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# So far we have focused on:
#
# Attribute Access
#
# The next section of the lecture
# shifts to object creation itself.
#
# Question:
#
# What happens before __init__?
#
# Is __init__ responsible for creating
# the object?
#
# The answer introduces:
#
# __new__()

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# @property is built on top of
# the property() mechanism.
#
# property objects are descriptors.
#
# Descriptors control attribute access.
#
# __get__    -> read
# __set__    -> write
# __delete__ -> delete
#
# This is the machinery that makes
# properties work.
