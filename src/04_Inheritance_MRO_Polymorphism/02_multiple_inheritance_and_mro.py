"""
============================================================
LLD-4 : OOP-3 (INHERITANCE)
PART 2 - MULTIPLE INHERITANCE AND MRO
============================================================

Topics Covered
--------------
1. Why Multiple Inheritance Exists
2. Electric Vehicle Example
3. Commercial Vehicle Example
4. Electric Cab
5. Diamond Problem
6. Method Resolution Order (MRO)
7. __mro__
8. mro()
9. C3 Linearization
10. Manual MRO Derivation

NOTE:
This file continues from:

01_inheritance_and_overriding.py

This is the most important file
of Lecture 4.

Everything later depends on MRO.
"""

# ============================================================
# MOTIVATION
# ============================================================

# So far:
#
# Car -> Vehicle
# Bike -> Vehicle
#
# Single parent.
#
# Easy.
#
# But real systems are not always
# this simple.
#
# Consider:
#
# Electric Cab
#
# It is:
#
# - an Electric Vehicle
# - a Commercial Vehicle
#
# at the same time.
#
# Question:
#
# Can a class have
# multiple parents?
#
# Python says:
#
# Yes.

# ============================================================
# BUILDING THE BASE CLASS
# ============================================================


class Vehicle:

    def __init__(
        self,
        registration_number
    ):

        self.registration_number = (
            registration_number
        )

        self.is_available = True

    def start(self):

        print(
            f"{self.registration_number} "
            f"starting."
        )


# ============================================================
# FIRST SPECIALIZATION
# ============================================================


class ElectricVehicle(Vehicle):

    def get_priority_score(
        self
    ):

        # Green energy bonus

        return 20


# ============================================================
# SECOND SPECIALIZATION
# ============================================================


class CommercialVehicle(Vehicle):

    def get_priority_score(
        self
    ):

        # Reliability bonus

        return 30


# ============================================================
# MULTIPLE INHERITANCE
# ============================================================


class ElectricCab(
    ElectricVehicle,
    CommercialVehicle
):

    pass


print("Multiple Inheritance")

cab = ElectricCab(
    "KA-05-9999"
)

cab.start()

# Observation:
#
# ElectricCab inherits from:
#
# ElectricVehicle
# CommercialVehicle
#
# simultaneously.

# ============================================================
# THE DIAMOND
# ============================================================

#               Vehicle
#               /     \
#              /       \
# ElectricVehicle   CommercialVehicle
#              \       /
#               \     /
#              ElectricCab
#
# This structure is called:
#
# Diamond Problem

# ============================================================
# THE BIG QUESTION
# ============================================================

# ElectricVehicle says:
#
# get_priority_score() -> 20
#
# CommercialVehicle says:
#
# get_priority_score() -> 30
#
# ElectricCab does not
# define the method.
#
# Question:
#
# Which one should Python use?

# ============================================================
# LET PYTHON DECIDE
# ============================================================

print("\nDiamond Problem")

print(
    cab.get_priority_score()
)

# Output:
#
# 20
#
# Why?
#
# Answer:
#
# MRO

# ============================================================
# WHAT IS MRO?
# ============================================================

# MRO =
#
# Method Resolution Order
#
# It is the exact order
# Python follows while
# searching for methods.

# ============================================================
# VIEWING MRO
# ============================================================

print("\nUsing __mro__")

print(
    ElectricCab.__mro__
)

# Hard to read.
#
# Let's clean it up.

# ============================================================
# CLEANER VERSION
# ============================================================

print("\nUsing mro()")

print(
    [
        cls.__name__
        for cls
        in ElectricCab.mro()
    ]
)

# Output:
#
# [
#   ElectricCab,
#   ElectricVehicle,
#   CommercialVehicle,
#   Vehicle,
#   object
# ]

# ============================================================
# UNDERSTANDING THE SEARCH
# ============================================================

# Python searches:
#
# ElectricCab
#
# then
#
# ElectricVehicle
#
# then
#
# CommercialVehicle
#
# then
#
# Vehicle
#
# then
#
# object
#
# First match wins.

# ============================================================
# WHY 20 IS RETURNED
# ============================================================

# Search begins:
#
# ElectricCab
#
# No method found.
#
# Move to:
#
# ElectricVehicle
#
# Method found.
#
# Return 20.
#
# Search stops.

# ============================================================
# IMPORTANT RULE
# ============================================================

# The answer is NOT:
#
# "left parent wins"
#
# The real answer is:
#
# "first class in the MRO wins"
#
# Today both happen
# to be the same.

# ============================================================
# C3 LINEARIZATION
# ============================================================

# Python uses:
#
# C3 Linearization
#
# to compute MRO.
#
# The goal:
#
# Convert a hierarchy
# into one linear list.

# ============================================================
# SIMPLE LINEARIZATIONS
# ============================================================

# L[object]
#
# = [object]
#
#
# L[Vehicle]
#
# = [Vehicle, object]
#
#
# L[ElectricVehicle]
#
# =
# [ElectricVehicle,
#  Vehicle,
#  object]
#
#
# L[CommercialVehicle]
#
# =
# [CommercialVehicle,
#  Vehicle,
#  object]

# ============================================================
# ELECTRIC CAB SETUP
# ============================================================

# L[ElectricCab]
#
# =
#
# ElectricCab
#
# +
#
# MERGE(
#
#   [ElectricVehicle,
#    Vehicle,
#    object],
#
#   [CommercialVehicle,
#    Vehicle,
#    object],
#
#   [ElectricVehicle,
#    CommercialVehicle]
#
# )

# ============================================================
# MERGE RULE
# ============================================================

# Repeatedly:
#
# 1. Take a head.
#
# 2. Check if it appears
#    in any other tail.
#
# 3. If safe:
#       choose it.
#
# 4. Otherwise:
#       skip it.

# ============================================================
# RESULT
# ============================================================

# Final MRO:
#
# ElectricCab
# ElectricVehicle
# CommercialVehicle
# Vehicle
# object

# ============================================================
# VERIFYING AGAIN
# ============================================================

expected = [
    "ElectricCab",
    "ElectricVehicle",
    "CommercialVehicle",
    "Vehicle",
    "object"
]

actual = [
    cls.__name__
    for cls
    in ElectricCab.mro()
]

print("\nVerification")

print(
    expected == actual
)

# True

# ============================================================
# ANOTHER EXAMPLE
# ============================================================


class A:
    pass


class B(A):
    pass


class C(A):
    pass


class D(C, B):
    pass


print("\nAnother MRO Example")

print(
    [
        cls.__name__
        for cls
        in D.mro()
    ]
)

# Output:
#
# D
# C
# B
# A
# object

# ============================================================
# WHY A IS LAST
# ============================================================

# Rule:
#
# A parent must appear
# after all its children.
#
# Therefore:
#
# C before A
# B before A

# ============================================================
# INTERVIEW RULES
# ============================================================

# Remember:
#
# MRO determines:
#
# - method lookup
# - attribute lookup
# - super()
#
# If you know MRO,
# multiple inheritance
# becomes predictable.

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Wrong:
#
# Python simply does
# depth-first search.
#
# Wrong:
#
# Left parent always wins.
#
# Correct:
#
# Python follows
# C3 Linearization.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Multiple inheritance
# allows multiple parents.
#
# Diamond structures create
# ambiguity.
#
# MRO resolves ambiguity.
#
# MRO =
# Method Resolution Order.
#
# Python stores MRO in:
#
# __mro__
#
# or
#
# mro()
#
# First match in MRO wins.
#
# Python uses:
#
# C3 Linearization
#
# to build the order.
