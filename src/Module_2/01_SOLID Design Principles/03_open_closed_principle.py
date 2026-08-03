"""
PART 03 - OPEN / CLOSED PRINCIPLE (OCP)

Topics Covered
1. Why SRP alone is not enough
2. The Open / Closed Principle
3. Regression problem
4. Rebuilding Bird using abstraction
5. Why adding new birds should not modify old code
6. Quiz
7. Bridge to Abstract Base Classes

================================================================
This file intentionally continues from Part 02.
================================================================
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lesson we discovered an important idea:
#
# Every class should have only ONE reason to change.
#
# Splitting Bird into Pigeon, Sparrow and Eagle solved one problem.
#
# But...
#
# Stop and think.
#
# Suppose tomorrow your product manager says:
#
#     "We need to support Falcon."
#
# Ask yourself:
#
# Will you MODIFY existing code?
#
# Or will you simply ADD new code?
#
# This distinction is the heart of today's lesson.

# ============================================================
# STOP AND THINK
# ============================================================

# Imagine your house has three bedrooms.
#
# Next year your family grows.
#
# Which sounds better?
#
# Option A:
#     Break an existing bedroom,
#     remove walls,
#     rebuild the house.
#
# Option B:
#     Extend the house by building one more room.
#
# Most people naturally prefer Option B.
#
# Why?
#
# Because disturbing something that already works
# introduces unnecessary risk.

# ============================================================
# DISCUSSION
# ============================================================

# Software behaves exactly the same way.
#
# Every time we edit working code,
# we risk accidentally breaking something
# that previously worked perfectly.

# ============================================================
# THE PROBLEM
# ============================================================

class BirdV1:

    def __init__(self, bird_type):
        self.type = bird_type

    def fly(self):
        if self.type == "pigeon":
            print("Short bursts")
        elif self.type == "sparrow":
            print("Fluttering")
        elif self.type == "eagle":
            print("Long glides")

# ============================================================
# THINK BEFORE READING
# ============================================================

# Tomorrow we introduce:
#
#     Falcon
#
# Which line changes?
#
# Think carefully before scrolling.

# ============================================================
# DISCUSSION
# ============================================================

# Answer:
#
# The fly() method.
#
# We must open existing code,
# insert another elif,
# test everything again,
# and hope nothing broke.
#
# This type of change is dangerous because
# the method already had working behaviour.

# ============================================================
# WHY IS THIS DANGEROUS?
# ============================================================

# Imagine fly() has:
#
# • 600 lines
# • 15 bird types
# • 40 passing unit tests
#
# While adding Falcon,
# a small typo accidentally changes
# Eagle's behaviour.
#
# Falcon works.
#
# Eagle breaks.
#
# This is called a regression.
#
# A regression means:
#
# A new change accidentally breaks
# an old feature that previously worked.

# ============================================================
# KEY IDEA
# ============================================================

# Open / Closed Principle
#
# Software entities should be:
#
# OPEN for extension.
#
# CLOSED for modification.
#
# Read that sentence twice.
#
# It does NOT mean
# "never change code."
#
# It means:
#
# Whenever possible,
# NEW features should arrive
# by ADDING new code,
# instead of modifying stable code.

# ============================================================
# A BETTER DESIGN
# ============================================================

class Bird:
    """Contains only generic bird information."""

    def __init__(self, name):
        self.name = name


class Pigeon(Bird):

    def fly(self):
        print("Short bursts near the ground.")


class Sparrow(Bird):

    def fly(self):
        print("Quick fluttering flight.")


class Eagle(Bird):

    def fly(self):
        print("Long soaring glides.")


# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Which class should change
# if Eagle's flying style changes?

Pigeon("Oliver").fly()
Sparrow("Max").fly()
Eagle("Sky").fly()

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Every class owns its own behaviour.
#
# If tomorrow Falcon arrives,
# we simply create:
#
# class Falcon(Bird):
#     def fly(...):
#         ...
#
# Existing classes remain untouched.

# ============================================================
# SMALL EXPERIMENT
# ============================================================

class Falcon(Bird):

    def fly(self):
        print("Fast diving flight.")

Falcon("Flash").fly()

# Observation:
#
# We added a completely new bird.
#
# Did we modify:
#
# Pigeon?
# Sparrow?
# Eagle?
#
# No.
#
# We extended the system
# by adding new code.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception:
#
# OCP means old code can never change.
#
# Incorrect.
#
# Bugs will still be fixed.
#
# Refactoring will still happen.
#
# OCP simply encourages designing systems
# where new features usually arrive
# through extension rather than modification.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Very common interview question:
#
# "Explain OCP without giving the definition."
#
# Good answer:
#
# "When a new feature is introduced,
# I prefer adding new classes instead of
# editing stable classes that already work."

# ============================================================
# SELF CHECK
# ============================================================

# Scenario:
#
# Existing apply_discount()
# supports:
#
# • Student
# • Festival
# • Premium
#
# Tomorrow:
#
# Senior Citizen discount arrives.
#
# Which design follows OCP?
#
# A)
# Add another elif.
#
# B)
# Introduce a new discount strategy class.
#
# Think before reading.

# ============================================================
# ANSWER
# ============================================================

# B
#
# We extend the system.
#
# Existing implementations remain untouched.

# ============================================================
# BOARD SUMMARY
# ============================================================

# OCP
#
# OPEN
#     Add new behaviour.
#
# CLOSED
#     Avoid modifying
#     stable working code.
#
# Extension > Modification

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# We now have separate bird classes.
#
# But another question appears.
#
# What belongs in Bird?
#
# What belongs in subclasses?
#
# And how do we force every flying bird
# to provide its own fly() implementation?
#
# The answer begins with
# Abstract Base Classes.
