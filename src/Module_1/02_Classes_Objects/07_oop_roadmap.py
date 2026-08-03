"""
============================================================
LLD-2 : OOP-1
PART 7 - OOP ROADMAP
============================================================

Topics Covered
--------------
1. Abstraction
2. Encapsulation
3. Inheritance
4. Polymorphism
5. Where We Are Today
6. What Comes Next
"""

# ============================================================
# THE BIG PICTURE
# ============================================================

# Many books teach:
#
# OOP has 4 pillars.
#
# In this course we will use the following model:
#
# 1 Principle
#     Abstraction
#
# 3 Pillars
#     Encapsulation
#     Inheritance
#     Polymorphism
#
# A principle tells us what we are trying to achieve.
#
# A pillar tells us how we achieve it.

# ============================================================
# ABSTRACTION
# ============================================================

# Abstraction is the idea that a complex system
# can be represented using smaller concepts.
#
# Throughout this lecture we have been practising
# abstraction without even naming it.
#
# Example:
#
# Uber System
#
#     Driver
#     Rider
#     Trip
#     Vehicle
#     Payment
#
# These are abstractions.
#
# They help us think about a large system
# in manageable pieces.

# ============================================================
# WHERE WE ARE TODAY
# ============================================================

# So far we have learned:
#
# Entity
#     -> Driver
#
# Class
#     -> Driver Blueprint
#
# Object
#     -> Actual Driver in Memory
#
# We have also learned:
#
# - __init__
# - self
# - Object State
# - __dict__
# - __str__
# - __repr__
# - Instance Methods
# - Class Methods
# - Static Methods
# - type()
# - isinstance()
# - issubclass()

# ============================================================
# ENCAPSULATION PREVIEW
# ============================================================

# Let's look at a problem in our current design.
#
# We can directly modify a Driver's rating.
#
# Is that safe?
#
# Should any code in the system be allowed
# to assign any rating value it wants?


class Driver:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


driver = Driver("Ramesh", 4.8)

print("Original Rating:", driver.rating)

driver.rating = -999

print("Modified Rating:", driver.rating)

# Observation:
#
# Python allowed this.
#
# The Driver object had no control over its data.
#
# This creates a data integrity problem.
#
# Encapsulation is the mechanism that helps
# solve this problem.

# ============================================================
# INHERITANCE PREVIEW
# ============================================================

# Imagine we have:
#
# Vehicle
#     |
#     +---- Car
#     |
#     +---- Bike
#
# Car and Bike may share common behaviour.
#
# Instead of duplicating code,
# we can inherit common behaviour
# from Vehicle.
#
# This is called Inheritance.
#
# We will study it in a future lecture.

# ============================================================
# POLYMORPHISM PREVIEW
# ============================================================

# Imagine:
#
# Car.start()
# Bike.start()
# Auto.start()
#
# Different implementations.
#
# Same method name.
#
# A function could simply call:
#
# vehicle.start()
#
# without caring whether the vehicle
# is a Car, Bike, or Auto.
#
# This idea is called Polymorphism.
#
# One interface.
# Many implementations.

# ============================================================
# ROADMAP
# ============================================================

# Lecture 2
#     OOP Foundations
#
# Lecture 3
#     Encapsulation
#
# Lecture 4
#     Inheritance
#
# Lecture 5
#     Polymorphism
#
# Lecture 6
#     Deep Dive into Dunder Methods

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Principle
#     Abstraction
#
# Pillars
#     Encapsulation
#     Inheritance
#     Polymorphism
#
# Today's class established the foundation.
#
# The next lectures will build the remaining
# pieces of the OOP toolkit.
