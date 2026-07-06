"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 3 - NAME MANGLING
============================================================

Topics Covered
--------------
1. The Double Underscore Convention
2. Is __attribute Really Private?
3. AttributeError Demonstration
4. Inspecting __dict__
5. Understanding Name Mangling
6. Accessing Mangled Names
7. Privacy vs Discouragement
8. Python's Design Philosophy
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we saw:
#
# _rating
#
# The single underscore was only
# a convention.
#
# Python still allowed direct access.
#
# Naturally the next question is:
#
# What about:
#
# __rating
#
# Does double underscore finally create
# a truly private attribute?
#
# Let's investigate.

# ============================================================
# FIRST EXPERIMENT
# ============================================================


class DriverV1:

    def __init__(self, name, rating):
        self.name = name
        self.__rating = rating


driver = DriverV1("Ramesh", 4.8)

print("Driver Created")

# Question:
#
# Can we access:
#
# driver.__rating
#
# Uncomment and run:
#
# print(driver.__rating)

# Expected Result:
#
# AttributeError

# ============================================================
# STUDENT OBSERVATION
# ============================================================

# Many students see the AttributeError
# and conclude:
#
# "__rating is private"
#
# But before reaching that conclusion,
# let's investigate further.

# ============================================================
# LOOKING INSIDE THE OBJECT
# ============================================================

# Earlier we learned:
#
# __dict__
#
# shows an object's state.

print("\nInspecting __dict__")

print(driver.__dict__)
print("Observation:")

# Carefully inspect the output.
#
# Do you see:
#
# __rating
#
# Probably not.
#
# Instead you should see something like:
#
# _DriverV1__rating

# ============================================================
# THE BIG REVEAL
# ============================================================

# Python did not remove the attribute.
#
# Python did not encrypt the attribute.
#
# Python did not create true privacy.
#
# Python renamed the attribute.
#
# This process is called:
#
# Name Mangling

# ============================================================
# WHAT IS NAME MANGLING?
# ============================================================

# Python transforms:
#
# __rating
#
# into:
#
# _DriverV1__rating
#
# internally.
#
# The goal is to reduce accidental access
# and accidental name collisions.

# ============================================================
# PROVING IT EXISTS
# ============================================================

print("\nAccessing Mangled Name")

print(driver._DriverV1__rating)

# Observation:
#
# The value is still accessible.
#
# Therefore:
#
# Double underscore is not true privacy.

# ============================================================
# MODIFYING THE MANGLED ATTRIBUTE
# ============================================================

driver._DriverV1__rating = 2.1

print("\nAfter Modification")

print(driver._DriverV1__rating)

# Observation:
#
# We successfully modified the value.
#
# So the data is not protected.
#
# It is merely hidden behind
# a transformed name.

# ============================================================
# WHY DOES PYTHON DO THIS?
# ============================================================

# The purpose is not security.
#
# The purpose is:
#
# 1. Avoid accidental access
# 2. Avoid accidental overriding
# 3. Communicate intent
#
# It is a stronger signal than
# a single underscore.

# ============================================================
# COMPARING SINGLE VS DOUBLE UNDERSCORE
# ============================================================

# _rating
#
# Convention only
#
# Still directly accessible
#
#
# __rating
#
# Triggers name mangling
#
# Renamed internally
#
# Still accessible if you know
# the mangled name

# ============================================================
# A SMALL EXPERIMENT
# ============================================================


class DriverV2:

    def __init__(self):
        self._rating = 4.8
        self.__balance = 1000


driver = DriverV2()

print("\nInspecting Another Object")

print(driver.__dict__)

# Observation:
#
# _rating remains unchanged.
#
# __balance becomes:
#
# _DriverV2__balance

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Myth:
#
# "__attribute makes data private"
#
# Reality:
#
# "__attribute triggers name mangling"
#
# These are not the same thing.

# ============================================================
# JAVA VS PYTHON
# ============================================================

# In Java:
#
# private
#
# is enforced by the language.
#
# In Python:
#
# __attribute
#
# is primarily a name-mangling mechanism.
#
# Python deliberately chooses
# a more flexible approach.

# ============================================================
# PYTHON'S PHILOSOPHY
# ============================================================

# Python still follows:
#
# "We are all consenting adults."
#
# Double underscore is a stronger warning.
#
# But it is not an impenetrable wall.

# ============================================================
# WHY IS THIS USEFUL?
# ============================================================

# Name mangling becomes especially useful
# when inheritance enters the picture.
#
# It helps avoid accidental name clashes
# between parent and child classes.
#
# We will revisit this idea when studying
# inheritance.

# ============================================================
# WHAT PROBLEM STILL REMAINS?
# ============================================================

# We still cannot properly control:
#
# Reading
# Writing
# Validation
#
# Example:
#
# Rating should remain between:
#
# 0.0 and 5.0
#
# We need a cleaner mechanism.
#
# One that allows us to intercept
# attribute access and updates.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Traditional OOP languages often use:
#
# getRating()
# setRating()
#
# Python provides something better:
#
# @property
#
# @setter
#
# @deleter
#
# These allow validation while preserving
# clean syntax.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# __attribute does NOT create
# true privacy.
#
# It triggers:
#
# Name Mangling
#
# Example:
#
# __rating
#
# becomes:
#
# _DriverV1__rating
#
# The attribute still exists.
#
# It can still be accessed.
#
# Name mangling helps prevent
# accidental access and collisions.
#
# Next:
#
# Properties
# Getters
# Setters
# Validation
