"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 01_zone_hashing_mystery_student_version.py
============================================================

Topics Covered
--------------
1. Zone Hierarchy Recap
2. Default Equality
3. Identity vs Equality
4. Business Equality
5. Implementing __eq__
6. Verifying Behaviour
7. The Set Experiment
8. The Hashing Mystery
9. Interview Question
10. Key Takeaways
"""

import math

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lecture we built a Zone hierarchy.
#
# CircularZone
# RectangularZone
# TriangularZone
#
# Each zone knows how to calculate its own area.
#
# A new requirement arrives:
#
# Two zones should be considered equal
# if their areas are equal.
#
# The requirement appears simple.
#
# After implementing it, an unexpected
# side effect appears.

# ============================================================
# ZONE HIERARCHY RECAP
# ============================================================


class Zone:

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError

    def __str__(self):
        return f"{self.name} (area={self.area():.2f})"


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


print("Zone Hierarchy Demo")

airport = CircularZone("Airport", 3)
koramangala = RectangularZone("Koramangala", 4, 5)
stadium = TriangularZone("Stadium", 6, 4)

print(airport)
print(koramangala)
print(stadium)

# Observation:
#
# The same interface is used for all zones.
#
# Each subclass provides its own area() logic.

# ============================================================
# DEFAULT EQUALITY
# ============================================================

zone_one = CircularZone("Test", 3)
zone_two = CircularZone("Test", 3)

print("\nDefault Equality")
print(zone_one == zone_two)

# Observation:
#
# Python returns False.
#
# Even though both objects contain
# the same values.

# ============================================================
# IDENTITY VS EQUALITY
# ============================================================

print("\nIdentity Check")
print(zone_one is zone_two)

print(id(zone_one))
print(id(zone_two))

# Observation:
#
# These are two different objects.
#
# By default, equality behaves like
# an identity comparison.

# ============================================================
# BUSINESS REQUIREMENT
# ============================================================

# Operations teams care about the
# represented area rather than the
# object's memory location.
#
# Requirement:
#
# Two zones are equal if their
# areas are equal.

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


# ============================================================
# VERIFYING BUSINESS EQUALITY
# ============================================================

zone_three = BetterCircularZone("Test", 3)
zone_four = BetterCircularZone("Test", 3)

print("\nBusiness Equality")
print(zone_three == zone_four)

# Observation:
#
# Equality now matches the
# business requirement.

zone_five = BetterCircularZone("Large Zone", 5)

print("\nDifferent Areas")
print(zone_three == zone_five)

# Observation:
#
# Different areas produce False.

# ============================================================
# THE SET EXPERIMENT
# ============================================================

# A set seems like a natural choice
# for storing assigned zones because:
#
# - duplicates are avoided
# - lookups are efficient

print("\nSet Experiment")

try:

    assigned_zones = {
        zone_three,
        zone_four
    }

    print(assigned_zones)

except TypeError as error:

    print(error)

# Observation:
#
# A TypeError appears.
#
# The object has become unhashable.

# ============================================================
# THE MYSTERY
# ============================================================

# We changed:
#
# __eq__
#
# We did not implement:
#
# __hash__
#
# Yet Python is now discussing
# hashability.
#
# This connection is the mystery
# that motivates the next sections.

# ============================================================
# DISCUSSION
# ============================================================

# Important Questions:
#
# Why does a set care about equality?
#
# Why is hashing involved?
#
# Why would Python disable hashing
# automatically?

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Can defining __eq__ affect whether
# objects can be stored inside a set?
#
# Yes.
#
# This example demonstrates that it can.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Default equality is identity based.
#
# __eq__ changes equality semantics.
#
# Business equality now works.
#
# A set operation unexpectedly fails.
#
# The failure is intentional and will
# be explained later.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Before understanding hashing,
# we need to understand how Python
# maps ordinary syntax to special methods.
#
# Next:
#
# 02_dunders_as_protocol.py
