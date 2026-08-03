"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 02_dunders_as_protocol.py
============================================================

Topics Covered
--------------
1. What Are Dunder Methods?
2. Why Built-in Functions Work Everywhere
3. Dunders As Protocols
4. len() -> __len__()
5. + -> __add__()
6. == -> __eq__()
7. [] -> __getitem__()
8. for -> __iter__()
9. Python Data Model
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider the following:
#
# len([1, 2, 3])
# len("Bengaluru")
# len({1, 2, 3})
#
# The same function works on:
#
# - list
# - string
# - set
#
# Question:
#
# How is that possible?
#
# Did Python write separate versions
# of len() for every possible type?

# ============================================================
# WARM UP
# ============================================================

drivers = [
    "Ramesh",
    "Suresh",
    "Mahesh",
    "Ganesh"
]

city = "Bengaluru"

active_trip_ids = {
    101,
    102,
    103
}

print("len() Examples")
print(len(drivers))
print(len(city))
print(len(active_trip_ids))

# Observation:
#
# Same function.
#
# Different types.
#
# Correct result every time.

# ============================================================
# THE WRONG DESIGN
# ============================================================

# Imagine Python internally doing:
#
# def len(obj):
#
#     if type(obj) == list:
#         ...
#
#     elif type(obj) == str:
#         ...
#
#     elif type(obj) == set:
#         ...
#
# This approach does not scale.
#
# Every new type would require
# modifying Python itself.

# ============================================================
# THE BETTER IDEA
# ============================================================

# Instead of Python knowing every type,
# each object can answer a question:
#
# "What is your length?"
#
# Python simply asks the object.

# ============================================================
# __len__
# ============================================================

print("\n__len__ Example")

print(
    drivers.__len__()
)

print(
    len(drivers)
)

# Observation:
#
# Both return the same value.

# ============================================================
# FIRST BIG IDEA
# ============================================================

# len(obj)
#
# is translated into:
#
# obj.__len__()
#
# This is our first example of
# the Python Data Model.

# ============================================================
# CUSTOM CLASS WITHOUT __len__
# ============================================================


class Fleet:

    def __init__(self):
        self.drivers = [
            "Ramesh",
            "Suresh",
            "Mahesh"
        ]


fleet = Fleet()

print("\nFleet Without __len__")

try:
    print(len(fleet))
except TypeError as error:
    print(error)

# Observation:
#
# Python does not know how to
# calculate the length.

# ============================================================
# CUSTOM CLASS WITH __len__
# ============================================================


class BetterFleet:

    def __init__(self):
        self.drivers = [
            "Ramesh",
            "Suresh",
            "Mahesh"
        ]

    def __len__(self):
        return len(self.drivers)


better_fleet = BetterFleet()

print("\nFleet With __len__")

print(
    len(better_fleet)
)

# Observation:
#
# len() now works naturally.

# ============================================================
# DUNDERS AS PROTOCOLS
# ============================================================

# A protocol is simply:
#
# "If you implement a specific method,
# Python will provide specific behaviour."
#
# Example:
#
# Implement __len__
#
# get len()

# ============================================================
# ANOTHER PROTOCOL : __add__
# ============================================================


class Fare:

    def __init__(self, amount):
        self.amount = amount


base_fare = Fare(120)
surge_fare = Fare(45)

print("\nFare Without __add__")

try:
    print(base_fare + surge_fare)
except TypeError as error:
    print(error)

# Observation:
#
# Python does not know how to add
# two Fare objects.

# ============================================================
# IMPLEMENTING __add__
# ============================================================


class BetterFare:

    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return BetterFare(
            self.amount + other.amount
        )


base_fare = BetterFare(120)
surge_fare = BetterFare(45)

total_fare = base_fare + surge_fare

print("\nFare With __add__")

print(
    total_fare.amount
)

# Observation:
#
# + now works for our own class.

# ============================================================
# SECOND BIG IDEA
# ============================================================

# x + y
#
# becomes:
#
# x.__add__(y)

# ============================================================
# EQUALITY PROTOCOL
# ============================================================


class Driver:

    def __init__(
        self,
        name,
        rating
    ):
        self.name = name
        self.rating = rating

    def __eq__(
        self,
        other
    ):
        return (
            self.name == other.name
            and
            self.rating == other.rating
        )


driver_one = Driver(
    "Ramesh",
    4.8
)

driver_two = Driver(
    "Ramesh",
    4.8
)

print("\nEquality Protocol")

print(
    driver_one == driver_two
)

# Observation:
#
# == now uses our logic.

# ============================================================
# THIRD BIG IDEA
# ============================================================

# x == y
#
# becomes:
#
# x.__eq__(y)

# ============================================================
# SUBSCRIPTING PROTOCOL
# ============================================================


class TripHistory:

    def __init__(self):
        self.trips = [
            "TRIP-101",
            "TRIP-102",
            "TRIP-103"
        ]

    def __getitem__(
        self,
        index
    ):
        return self.trips[index]


history = TripHistory()

print("\nSubscript Protocol")

print(
    history[0]
)

# Observation:
#
# [] becomes possible through
# __getitem__.

# ============================================================
# ITERATION PROTOCOL
# ============================================================


class DriverCollection:

    def __init__(self):
        self.drivers = [
            "Ramesh",
            "Suresh",
            "Mahesh"
        ]

    def __iter__(self):
        return iter(self.drivers)


collection = DriverCollection()

print("\nIteration Protocol")

for driver in collection:
    print(driver)

# Observation:
#
# for loop works because
# __iter__ exists.

# ============================================================
# COMMON MAPPINGS
# ============================================================

# len(x)
# -> x.__len__()
#
# x + y
# -> x.__add__(y)
#
# x == y
# -> x.__eq__(y)
#
# x[0]
# -> x.__getitem__(0)
#
# for item in x
# -> x.__iter__()

# ============================================================
# PYTHON DATA MODEL
# ============================================================

# These special methods form
# the Python Data Model.
#
# Python provides behaviour.
#
# We provide implementations.
#
# This is a protocol based design.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What is a dunder method?
#
# A special method surrounded
# by double underscores that
# Python calls automatically
# in response to specific syntax.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Dunder means:
# Double Underscore.
#
# Python translates syntax
# into special method calls.
#
# Implementing a dunder method
# enables specific behaviour.
#
# Dunders form protocols.
#
# The collection of these protocols
# is called the Python Data Model.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Now that we understand
# how Python invokes dunder methods,
# we can study representation methods.
#
# Next:
#
# 03_representation_methods.py
