"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 1 - THE ENCAPSULATION PROBLEM
============================================================

Topics Covered
--------------
1. Recap of OOP-1
2. Procedural Programming Problem #1
3. Procedural Programming Problem #2
4. Why OOP Helps
5. The Remaining Problem
6. Driver Rating Example
7. Motivation for Encapsulation
"""

# ============================================================
# RECAP OF OOP-1
# ============================================================

# In the previous lecture we learned:
#
# - Classes
# - Objects
# - __init__
# - self
# - Object State
# - __str__
# - __repr__
# - Instance Methods
# - Class Methods
# - Static Methods
# - Driver
# - Rider
# - Trip
#
# We also saw that OOP helps us model
# real-world entities using classes.

# ============================================================
# PROCEDURAL PROGRAMMING PROBLEM #1
# ============================================================

# Consider a Driver in a ride-sharing application.
#
# A Driver has:
#
# - name
# - rating
# - availability
#
# Question:
#
# Can any code modify the rating?
#
# Let's see.


class DriverV1:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True


driver = DriverV1("Ramesh", 4.8)

print("Original Rating:", driver.rating)

driver.rating = -999

print("Modified Rating:", driver.rating)
print("Observation:")

# Observation:
#
# Python allowed this.
#
# The Driver object had no control
# over its own data.
#
# We now have invalid state.

# ============================================================
# WHY IS THIS A PROBLEM?
# ============================================================

# Ratings are supposed to be within
# a valid range.
#
# Example:
#
# 0.0 <= rating <= 5.0
#
# But the current design allows:
#
# -999
# 1000
# "excellent"
# None
#
# Any piece of code can directly
# change the data.

# ============================================================
# PROCEDURAL PROGRAMMING PROBLEM #2
# ============================================================

# Imagine a large application.
#
# Driver-related logic exists in:
#
# file_a.py
# file_b.py
# file_c.py
# file_d.py
#
# Validation logic is duplicated
# everywhere.
#
# Whenever rules change,
# multiple places must be updated.
#
# This is difficult to maintain.

# ============================================================
# HOW OOP HELPED
# ============================================================

# OOP already helped solve part of this.
#
# Instead of spreading Driver-related
# logic everywhere, we created:
#
# Driver
#
# and moved Driver behaviour into
# the Driver class.
#
# This bundles:
#
# Data
# +
# Behaviour
#
# together.

# ============================================================
# THE REMAINING PROBLEM
# ============================================================

# Even though data and behaviour
# are now together,
#
# the data is still completely exposed.
#
# Any code can do:
#
# driver.rating = -999
#
# The Driver class cannot stop it.

# ============================================================
# A MORE REALISTIC EXAMPLE
# ============================================================


class DriverV2:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def update_rating(self, rating):

        self.rating = rating


driver = DriverV2("Priya", 4.9)

driver.update_rating(4.7)

print("\nRating Through Method:", driver.rating)

# However, the following still works:

driver.rating = -100

print("Rating After Direct Modification:", driver.rating)

# Observation:
#
# We created an update_rating method.
#
# But users can bypass it completely.

# ============================================================
# THE CORE IDEA OF ENCAPSULATION
# ============================================================

# Question:
#
# Should outside code directly manipulate
# important internal data?
#
# Encapsulation says:
#
# "No."
#
# The object should control access
# to its own state.
#
# External code should interact through
# well-defined interfaces.

# ============================================================
# WHAT DO WE WANT?
# ============================================================

# Instead of:
#
# driver.rating = -999
#
# We want:
#
# Driver decides:
#
# - what values are valid
# - what values are invalid
# - how updates happen
#
# The object protects itself.

# ============================================================
# FORMAL DEFINITION
# ============================================================

# Encapsulation is the practice of:
#
# Bundling:
#     Data
#     +
#     Behaviour
#
# and controlling how the data is accessed
# and modified.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Different languages solve Encapsulation
# differently.
#
# Java uses:
#
# private
# protected
# public
#
# Python takes a different approach.
#
# Next:
#
# Python Access Conventions
#
# - public attributes
# - _protected
# - Python's "consenting adults" philosophy

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# OOP helped group related data
# and behaviour together.
#
# However, direct access to data
# is still a problem.
#
# Invalid object state is possible.
#
# Encapsulation exists to protect
# an object's internal state.
#
# The next step is understanding how
# Python approaches Encapsulation.
