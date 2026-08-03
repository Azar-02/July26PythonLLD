"""
============================================================
LLD-5 : OOP-4 (ABCs, PROTOCOLS AND MIXINS)
FILE : LLD5_01_abstract_base_classes.py
============================================================

ABSTRACT BASE CLASSES (ABC)

Topics Covered
--------------
1. Why NotImplementedError is not enough
2. Hidden Runtime Bugs
3. Zone Example
4. ABC Module
5. Abstract Base Classes
6. @abstractmethod
7. Instantiation-Time Validation
8. Abstract Classes
9. Payment Gateway Example
10. ABC as a Contract
11. ABC vs NotImplementedError
12. Interview Questions
13. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# Suppose every Zone in Uber must provide:
#
# area()
#
# We want all developers to follow
# this rule.
#
# What happens if someone forgets?

# ============================================================
# V1 - USING NOTIMPLEMENTEDERROR
# ============================================================


class ZoneV1:

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError(
            "Every zone must implement area()"
        )


# ============================================================
# NEW DEVELOPER JOINS TEAM
# ============================================================


class HexagonalZoneV1(ZoneV1):

    def __init__(self, name, side_length):
        super().__init__(name)
        self.side_length = side_length

    # Forgot area()


print("========== V1 ==========")

zone = HexagonalZoneV1(
    "Airport Zone",
    5
)

print("Object created successfully")

# Observation:
#
# No error.
#
# Python allows object creation.

# ============================================================
# BUG APPEARS LATER
# ============================================================

print("\nLate Failure")

try:
    zone.area()

except NotImplementedError as ex:
    print(ex)

# Observation:
#
# Error appears only when
# area() is called.
#
# The object survived creation.
#
# The bug remained hidden.

# ============================================================
# WHY THIS IS DANGEROUS
# ============================================================

# Imagine:
#
# Object created today.
#
# area() called:
#
# - tomorrow
# - next week
# - production environment
#
# Then the application crashes.
#
# We want failure much earlier.

# ============================================================
# INTRODUCING ABC
# ============================================================

# ABC
#
# = Abstract Base Class
#
# Python provides:
#
# ABC
#
# and
#
# @abstractmethod
#
# to solve this problem.

# ============================================================
# V2 - ABSTRACT BASE CLASS
# ============================================================


class Zone(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        pass

    def __str__(self):

        return (
            f"{self.name} "
            f"(area={self.area():.2f})"
        )


# ============================================================
# FORGETTING AGAIN
# ============================================================


class HexagonalZone(Zone):

    def __init__(self, name, side_length):
        super().__init__(name)
        self.side_length = side_length

    # Forgot area()


print("\n========== ABC ==========")

try:

    zone = HexagonalZone(
        "Airport Zone",
        5
    )

except TypeError as ex:

    print(ex)

# Observation:
#
# Error occurs immediately.
#
# Object creation fails.
#
# Bug caught much earlier.

# ============================================================
# WHAT CHANGED?
# ============================================================

# Old approach:
#
# Object created successfully
#
# Failure occurs later.
#
#
# ABC approach:
#
# Object creation itself fails.
#
# Much safer.

# ============================================================
# CORRECT IMPLEMENTATION
# ============================================================


class HexagonalZoneV2(Zone):

    def __init__(self, name, side_length):

        super().__init__(name)

        self.side_length = side_length

    def area(self):

        return (
            (3 * (3 ** 0.5)) / 2
        ) * (
            self.side_length ** 2
        )


print("\nCorrect Implementation")

zone = HexagonalZoneV2(
    "Airport Zone",
    5
)

print(zone)

# ============================================================
# ABSTRACT CLASS RULE
# ============================================================

# If a class contains
# abstract methods,
#
# it becomes an
# abstract class.
#
# Abstract classes
# cannot be instantiated.

# ============================================================
# DIRECT INSTANTIATION
# ============================================================

print("\nDirect Instantiation")

try:

    zone = Zone("Test Zone")

except TypeError as ex:

    print(ex)

# ============================================================
# PAYMENT GATEWAY EXAMPLE
# ============================================================

# Consider a payment system.
#
# Every gateway must support:
#
# charge()
# refund()


class PaymentGateway(ABC):

    @abstractmethod
    def charge(self, amount):
        pass

    @abstractmethod
    def refund(self, transaction_id):
        pass


# ============================================================
# PARTIAL IMPLEMENTATION
# ============================================================


class RazorpayGateway(PaymentGateway):

    def charge(self, amount):

        print(
            f"Charging ₹{amount}"
        )

    # Forgot refund()


print("\nPartial Implementation")

try:

    gateway = RazorpayGateway()

except TypeError as ex:

    print(ex)

# Observation:
#
# Implementing one abstract
# method is not enough.
#
# ALL abstract methods
# must be implemented.

# ============================================================
# COMPLETE IMPLEMENTATION
# ============================================================


class RazorpayGatewayV2(
    PaymentGateway
):

    def charge(self, amount):

        print(
            f"Charging ₹{amount}"
        )

    def refund(self, transaction_id):

        print(
            f"Refunding "
            f"{transaction_id}"
        )


print("\nComplete Implementation")

gateway = RazorpayGatewayV2()

gateway.charge(500)

gateway.refund("TXN-101")

# ============================================================
# ABC AS CONTRACT
# ============================================================

# Think of ABC as:
#
# A contract.
#
# PaymentGateway says:
#
# Every gateway MUST provide:
#
# charge()
# refund()
#
# Missing even one method
# violates the contract.

# ============================================================
# NOTIMPLEMENTEDERROR VS ABC
# ============================================================

# NotImplementedError
#
# Advantages:
#
# - Simple
#
# Problems:
#
# - Runtime failure
# - Late discovery
#
#
# ABC
#
# Advantages:
#
# - Early failure
# - Strong contract
# - Better team safety
#
# Trade-off:
#
# Slightly more structure.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Question:
#
# Why use ABC instead of
# NotImplementedError?
#
# Answer:
#
# ABC catches missing
# implementations during
# object creation.
#
# NotImplementedError catches
# them only when the method
# is called.

# ============================================================
# QUIZ
# ============================================================

# What happens here?
#
# class StripeGateway(
#     PaymentGateway
# ):
#
#     pass
#
# StripeGateway()
#
# Answer:
#
# TypeError
#
# Because:
#
# charge()
# refund()
#
# are missing.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ABC
# =
# Abstract Base Class
#
# @abstractmethod marks
# mandatory methods.
#
# Abstract classes cannot
# be instantiated.
#
# All abstract methods
# must be implemented.
#
# ABCs catch bugs earlier.
#
# ABCs act as contracts.
#
# Useful when:
#
# - you own the hierarchy
# - the contract is important
# - early bug detection matters
