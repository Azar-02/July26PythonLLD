"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 04_eq_hash_contract.py
============================================================

Topics Covered
--------------
1. Hashable vs Unhashable Objects
2. Revisiting the Zone Mystery
3. Default Equality
4. Implementing __eq__
5. Why Sets Need Hashing
6. The __eq__ / __hash__ Contract
7. Why Python Disables Hashing
8. Implementing __hash__
9. Verifying The Fix
10. Mutable Object Dangers
11. __lt__ and Sorting
12. Interview Questions
13. Key Takeaways
"""

import math

# ============================================================
# MOTIVATION
# ============================================================

# In File 01 we encountered a mystery.
#
# We added:
#
#     __eq__
#
# Equality started working.
#
# Then:
#
#     set()
#
# suddenly stopped working.
#
# Python reported:
#
#     unhashable type
#
# This file explains why.

# ============================================================
# HASHABLE VS UNHASHABLE
# ============================================================

print("Hashable Objects")

print(hash("Bengaluru"))
print(hash((1, 2, 3)))

# Observation:
#
# Strings are hashable.
#
# Tuples are hashable.

print("\nUnhashable Object")

try:
    print(hash([1, 2, 3]))
except TypeError as error:
    print(error)

# Observation:
# 
# Lists are not hashable.

# ============================================================
# FIRST QUESTION
# ============================================================

# Why would Python allow:
#
# tuple
#
# but reject:
#
# list
#
# We will return to this later.

# ============================================================
# ZONE HIERARCHY RECAP
# ============================================================


class Zone:

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError

    def __str__(self):
        return f"{self.name} ({self.area():.2f})"


class CircularZone(Zone):

    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class RectangularZone(Zone):

    def __init__(self, name, width, height):
        super().__init__(name)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class TriangularZone(Zone):

    def __init__(self, name, base, height):
        super().__init__(name)
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


# ============================================================
# DEFAULT EQUALITY
# ============================================================

zone_one = CircularZone("Airport", 3)
zone_two = CircularZone("Airport", 3)

print("\nDefault Equality")
print(zone_one == zone_two)

# Observation:
#
# False.
#
# Equality is identity based.

# ============================================================
# BUSINESS REQUIREMENT
# ============================================================

# Operations Requirement:
#
# Two zones should be equal
# if their areas are equal.

# ============================================================
# IMPLEMENTING __eq__
# ============================================================


class BetterZone:

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.area() == other.area()


class BetterCircularZone(BetterZone):

    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


zone_three = BetterCircularZone("Airport", 3)
zone_four = BetterCircularZone("Airport", 3)

print("\nBusiness Equality")
print(zone_three == zone_four)

# Observation:
#
# Equality now works.

# ============================================================
# THE FAILURE RETURNS
# ============================================================

print("\nSet Failure")

try:
    assigned = {zone_three, zone_four}
    print(assigned)
except TypeError as error:
    print(error)

# Observation:
#
# The same failure returns.

# ============================================================
# WHY SETS EXIST
# ============================================================

# Imagine a set containing
# ten million objects.
#
# To answer:
#
#     x in some_set
#
# Python cannot compare
# every object one by one.
#
# That would be O(n).
#
# Instead Python uses hashing.

# ============================================================
# HASHING INTUITION
# ============================================================

# Simplified View:
#
# Step 1
#
# Compute hash(value)
#
# Step 2
#
# Jump to a bucket
#
# Step 3
#
# Use equality to confirm match
#
# Hash first.
#
# Equality second.

# ============================================================
# IMPORTANT DISCUSSION
# ============================================================

# Equality and hashing
# are not independent.
#
# They must cooperate.

# ============================================================
# THE CONTRACT
# ============================================================

# Core Rule:
#
# If:
#
#     a == b
#
# Then:
#
#     hash(a) == hash(b)
#
# MUST be true.
#
# This is the contract.

# ============================================================
# WHY THIS MATTERS
# ============================================================

# Suppose:
#
# a == b
#
# but
#
# hash(a) != hash(b)
#
# Then:
#
# a and b land in
# different buckets.
#
# The set can no longer
# find matching objects reliably.

# ============================================================
# VISUAL MODEL
# ============================================================

# Bucket A
# |
# +---- hash 100
#
# Bucket B
# |
# +---- hash 200
#
# If equal objects land
# in different buckets,
# lookups break.

# ============================================================
# PYTHON'S SAFETY MECHANISM
# ============================================================

# When Python sees:
#
# __eq__
#
# but does not see:
#
# __hash__
#
# it assumes:
#
# "I cannot guarantee
# the contract."
#
# Therefore Python disables
# hashing automatically.

# ============================================================
# IMPORTANT
# ============================================================

# The error is not a bug.
#
# The error is protection.

# ============================================================
# IMPLEMENTING __hash__
# ============================================================


class SafeZone:

    def __init__(self, name, radius):
        self.name = name
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def __eq__(self, other):
        return self.area() == other.area()

    def __hash__(self):
        return hash(self.area())


zone_five = SafeZone("Airport", 3)
zone_six = SafeZone("Airport", 3)

# ============================================================
# VERIFYING THE CONTRACT
# ============================================================

print("\nEquality")
print(zone_five == zone_six)

print("\nHashes")
print(hash(zone_five))
print(hash(zone_six))

# Observation:
#
# Equal objects.
#
# Equal hashes.

# ============================================================
# VERIFYING THE FIX
# ============================================================

print("\nSet After Fix")

assigned = {
    zone_five,
    zone_six
}

print(len(assigned))

# Observation:
#
# Set works again.

# ============================================================
# HASH COLLISIONS
# ============================================================

# Important:
#
# Equal objects
# must have equal hashes.
#
# Reverse is NOT required.
#
# Unequal objects may
# share the same hash.
#
# This is called
# a collision.

# ============================================================
# MUTABLE OBJECT DANGER
# ============================================================

# Consider:
#
# Object enters a set.
#
# Hash is calculated.
#
# Later the object changes.
#
# Now the hash changes.
#
# The object may be sitting
# in the wrong bucket.

mutable_zone = SafeZone(
    "Airport",
    3
)

zone_set = {mutable_zone}

print("\nBefore Mutation")
print(mutable_zone in zone_set)

mutable_zone.radius = 10

print("\nAfter Mutation")
print(mutable_zone in zone_set)

# Observation:
#
# Behaviour becomes dangerous.
#
# Hashable objects should
# generally be immutable.

# ============================================================
# RETURN TO THE WARMUP
# ============================================================

# Why was tuple hashable?
#
# Because tuples are intended
# to be immutable.
#
# Why was list unhashable?
#
# Lists are mutable.
#
# Mutable objects are dangerous
# in hashed collections.

# ============================================================
# ORDERING OBJECTS
# ============================================================

# Equality is not enough
# for sorting.
#
# Sorting requires ordering.

# ============================================================
# IMPLEMENTING __lt__
# ============================================================


class SortableZone:

    def __init__(self, name, area_value):
        self.name = name
        self.area_value = area_value

    def __lt__(self, other):
        return self.area_value < other.area_value

    def __repr__(self):
        return (
            f"{self.name}"
            f"({self.area_value})"
        )


zones = [
    SortableZone("Airport", 28.27),
    SortableZone("Koramangala", 20),
    SortableZone("Stadium", 12)
]

print("\nBefore Sorting")
print(zones)

print("\nAfter Sorting")
print(sorted(zones))

# Observation:
#
# sorted() relies on __lt__.

# ============================================================
# SUMMARY OF SPECIAL METHODS
# ============================================================

# __eq__
#
# Equality
#
# __hash__
#
# Hashing
#
# __lt__
#
# Ordering

# ============================================================
# QUIZ
# ============================================================

# Which operation requires __lt__?
#
# A) ==
# B) set()
# C) sorted()
# D) hash()
#
# Answer:
#
# C) sorted()

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why does defining __eq__
# sometimes make an object
# unhashable?
#
# Because Python protects
# the equality/hash contract.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Complete the rule:
#
# If:
#
#     a == b
#
# Then:
#
#     ?
#
# Answer:
#
# hash(a) == hash(b)

# ============================================================
# COMMON MISTAKE
# ============================================================

# Implementing __eq__
#
# but forgetting __hash__.

# ============================================================
# BEST PRACTICE
# ============================================================

# Only hash data that
# should not change after
# object creation.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Sets and dictionaries
# depend on hashing.
#
# Equality and hashing
# must remain consistent.
#
# a == b implies:
#
# hash(a) == hash(b)
#
# Python automatically
# protects this contract.
#
# Hashable objects should
# usually be immutable.
#
# __lt__ enables ordering
# and sorting.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We now understand:
#
# __eq__
# __hash__
# __lt__
#
# Next we explore another
# powerful protocol:
#
# Context Managers.
#
# Next:
#
# 05_context_managers.py
