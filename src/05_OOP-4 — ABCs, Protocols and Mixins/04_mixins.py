"""
============================================================
LLD-5 : OOP-4 (ABCs, PROTOCOLS AND MIXINS)
FILE : 04_mixins.py
============================================================

Topics Covered
--------------
1. What is a Mixin?
2. Why Mixins Exist
3. LoggingMixin
4. SerializationMixin
5. TimestampMixin
6. Combining Mixins
7. MRO Impact
8. Ordering Matters
9. Best Practices
10. Common Mistakes

Based on Lecture 5 Notes.
"""

import json
from datetime import datetime

# ============================================================
# MOTIVATION
# ============================================================

# Suppose we have:
#
# Driver
# Rider
# Vehicle
#
# and all of them need:
#
# Logging
#
# Should we copy-paste
# logging code everywhere?
#
# No.
#
# Mixins solve this problem.

# ============================================================
# WHAT IS A MIXIN?
# ============================================================

# A Mixin is:
#
# A small reusable class.
#
# It provides a specific feature.

# A Mixin is a small, reusable class designed to provide specific 
# functionality that can be "mixed into" other classes via 
# multiple inheritance. \
# It's not a complete business entity—it's a feature provider.
#
# Examples:
#
# LoggingMixin
# SerializationMixin
# TimestampMixin
#
# Mixins are NOT usually
# complete business entities.

# ============================================================
# FIRST MIXIN
# ============================================================


class LoggingMixin:

    def log(
        self,
        message
    ):

        print(
            f"[LOG] {message}"
        )


# ============================================================
# USING THE MIXIN
# ============================================================


class Driver(LoggingMixin):

    def accept_ride(self):

        self.log(
            "Ride Accepted"
        )


print("LoggingMixin")

driver = Driver()

print(isinstance(driver, LoggingMixin))

driver.accept_ride()

# Observation:
#
# Driver gets logging
# without implementing it.

# ============================================================
# WHY NOT INHERITANCE?
# ============================================================

# Question:
#
# Is Driver a LoggingMixin?
#
# No.
#
# Driver IS NOT a type of
# LoggingMixin.
#
# Logging is merely a feature.
#
# Therefore:
#
# Mixin inheritance is different
# from domain inheritance.

# ============================================================
# SERIALIZATION MIXIN
# ============================================================


class SerializationMixin:

    def to_json(self):

        return json.dumps(
            self.__dict__
        )


class Rider(
    SerializationMixin
):

    def __init__(
        self,
        name,
        rating
    ):

        self.name = name
        self.rating = rating


print("\nSerializationMixin")

rider = Rider(
    "Ramesh",
    4.8
)

print(
    rider.to_json()
)

# ============================================================
# TIMESTAMP MIXIN
# ============================================================


class TimestampMixin:

    def created_at(self):

        return (
            datetime.now()
        )


class Vehicle(
    TimestampMixin
):

    pass


print("\nTimestampMixin")

vehicle = Vehicle()

print(
    vehicle.created_at()
)

# ============================================================
# MULTIPLE MIXINS
# ============================================================

# Mixins are often combined.


class DriverV2(
    LoggingMixin,
    SerializationMixin,
    TimestampMixin
):

    def __init__(
        self,
        name
    ):

        self.name = name


print("\nMultiple Mixins")

driver = DriverV2(
    "Suresh"
)

driver.log("Driver Created")

print(
    driver.to_json()
)

print(
    driver.created_at()
)

# ============================================================
# MRO REVISITED
# ============================================================

# Multiple Mixins means:
#
# Multiple Inheritance.
#
# Therefore:
#
# MRO becomes important.

# ============================================================
# MRO EXAMPLE
# ============================================================

print("\nDriverV2 MRO")

print(
    [
        cls.__name__
        for cls
        in DriverV2.mro()
    ]
)

# ============================================================
# ORDERING MATTERS
# ============================================================

# Mixins should usually
# appear before the
# main business class.
#
# Example:
#
# class Driver(
#     LoggingMixin,
#     DriverBase
# )
#
# rather than:
#
# class Driver(
#     DriverBase,
#     LoggingMixin
# )

# ============================================================
# METHOD COLLISION
# ============================================================


class MixinA:

    def process(self):

        print(
            "MixinA"
        )


class MixinB:

    def process(self):

        print(
            "MixinB"
        )


class Service(
    MixinA,
    MixinB
):

    pass


print("\nMethod Collision")

service = Service()

service.process()

# Observation:
#
# MRO decides.
#
# First match wins.

# ============================================================
# VERIFYING MRO
# ============================================================

print(
    [
        cls.__name__
        for cls
        in Service.mro()
    ]
)

# ============================================================
# COMMON MISTAKE #1
# ============================================================

# Creating huge Mixins.
#
# Bad:
#
# DatabaseMixin
#
# containing 100 methods.
#
# Good:
#
# Small focused Mixins.

# ============================================================
# COMMON MISTAKE #2
# ============================================================

# Treating Mixins as
# business entities.
#
# Example:
#
# Customer inherits
# LoggingMixin
#
# does NOT mean:
#
# Customer IS-A LoggingMixin

# ============================================================
# COMMON MISTAKE #3
# ============================================================

# Ignoring MRO.
#
# Multiple Mixins
# always involve MRO.

# ============================================================
# MIXIN BEST PRACTICES
# ============================================================

# Keep Mixins:
#
# - Small
# - Reusable
# - Focused
#
# Avoid:
#
# - Large state
# - Business logic
#
# Use Mixins for:
#
# - Logging
# - Serialization
# - Auditing
# - Timestamping

# ============================================================
# MIXINS VS ABC
# ============================================================

# ABC
#
# Defines a contract.
#
#
# Mixin
#
# Provides reusable
# implementation.

# ============================================================
# MIXINS VS PROTOCOLS
# ============================================================

# Protocol
#
# Defines expected behaviour.
#
#
# Mixin
#
# Provides actual code.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What is a Mixin?
#
# A reusable feature class
# intended to be combined
# with other classes using
# multiple inheritance.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Mixins provide reusable
# functionality.
#
# LoggingMixin
# SerializationMixin
# TimestampMixin
#
# are common examples.
#
# Mixins are not domain models.
#
# Mixins rely on
# multiple inheritance.
#
# Therefore:
#
# MRO matters.
#
# Keep Mixins small
# and focused.
