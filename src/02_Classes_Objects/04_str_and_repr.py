"""
============================================================
LLD-2 : OOP-1
PART 4 - __str__ AND __repr__
============================================================

Topics Covered
--------------
1. Default Object Representation
2. Why Default Output Is Not Useful
3. Understanding __str__
4. Understanding __repr__
5. User vs Developer View
6. Python Automatically Invokes Dunder Methods
7. Dunder Method Pattern
8. Fallback Behaviour
"""

# ============================================================
# MOTIVATION
# ============================================================

# So far we have created Driver objects.
#
# Question:
#
# What happens when we print a Driver object?
#
# Will Python automatically know what information
# we want to display?
#
# Let's find out.

# ============================================================
# DEMO 1 - DEFAULT OBJECT OUTPUT
# ============================================================


class DriverV1:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True


driver_one = DriverV1("Ramesh", 4.8)

print("Printing DriverV1 Object")
print(driver_one)

# Observation:
#
# Typical output looks like:
#
# <__main__.DriverV1 object at 0x...>
#
# This is Python's default representation.
#
# If we were debugging an Uber application,
# this output would not be very useful.
#
# We want meaningful information such as:
#
# Driver Name
# Driver Rating
# Availability

# ============================================================
# WHY DOES THIS HAPPEN?
# ============================================================

# When Python needs a string representation of an object,
# it looks for special methods.
#
# One of those special methods is:
#
# __str__
#
# If we do not provide one,
# Python falls back to its default behaviour.

# ============================================================
# DEMO 2 - FIRST __str__
# ============================================================


class DriverV2:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def __str__(self):

        # This print is intentionally included
        # to prove that Python is calling __str__.

        print("Python is calling __str__ on me!")

        return (
            f"Driver(name={self.name}, "
            f"rating={self.rating}, "
            f"available={self.is_available})"
        )


driver_two = DriverV2("Suresh", 4.6)

print("\nPrinting DriverV2 Object")
print(driver_two)

# Important Observation:
#
# We never wrote:
#
# driver_two.__str__()
#
# Instead we wrote:
#
# print(driver_two)
#
# Yet __str__ executed.
#
# Conclusion:
#
# Python automatically called __str__.

# ============================================================
# DISCUSSION
# ============================================================

# This is a recurring Python pattern.
#
# We define special methods.
#
# Python decides when to invoke them.
#
# Earlier:
#
# __init__
#
# Now:
#
# __str__
#
# Later you will see:
#
# __repr__
# __len__
# __iter__
# __getitem__
#
# and many more.

# ============================================================
# CLEANER __str__
# ============================================================

# In production code we would normally not
# keep the debug print statement.


class DriverV3:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def __str__(self):
        return (
            f"Driver(name={self.name}, "
            f"rating={self.rating}, "
            f"available={self.is_available})"
        )


driver_three = DriverV3("Mahesh", 4.9)

print("\nCleaner __str__ Example")
print(driver_three)

# ============================================================
# USER VIEW VS DEVELOPER VIEW
# ============================================================

# The lecture distinguishes between two audiences.
#
# Audience 1:
#
# Someone reading the object.
#
# Audience 2:
#
# A developer debugging the system.
#
# __str__
#
# Friendly representation.
#
# __repr__
#
# Developer-oriented representation.

# ============================================================
# DEMO 3 - UNDERSTANDING __repr__
# ============================================================


class DriverV4:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def __str__(self):
        return f"Driver(name={self.name}, rating={self.rating})"

    def __repr__(self):

        # Intentionally included to prove
        # Python is invoking __repr__.

        print("Python is calling __repr__ on me!")

        return (
            f"Driver(name='{self.name}', "
            f"rating={self.rating})"
        )


driver_four = DriverV4("Priya", 4.7)

print("\nUsing repr()")
print(repr(driver_four))
print("\nUsing print()")

# Observation:
#
# We never wrote:
#
# driver_four.__repr__()
#
# Instead we wrote:
#
# repr(driver_four)
#
# Python invoked __repr__ for us.

# ============================================================
# WHAT SHOULD __repr__ RETURN?
# ============================================================

# A common guideline:
#
# __repr__ should help a developer understand
# the object quickly.
#
# Ideally it should contain enough information
# to identify the object.
#
# It is usually more precise than __str__.

# ============================================================
# THE DUNDER METHOD PATTERN
# ============================================================

# __init__
# __str__
# __repr__
#
# All of these are examples of dunder methods.
#
# Dunder = Double Underscore.
#
# Python recognizes these method names.
#
# When specific events occur,
# Python automatically invokes them.
#
# We define behaviour.
#
# Python decides when to call it.

# ============================================================
# DEMO 4 - FALLBACK BEHAVIOUR
# ============================================================

# Important observation from the lecture.
#
# What if __str__ does not exist?
#
# Will print(obj) fail?
#
# Let's test it.


class DriverV5:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Driver(name='{self.name}')"


driver_five = DriverV5("Amit")

print("\nFallback Behaviour")
print(driver_five)

# Observation:
#
# print(driver_five) still works.
#
# Why?
#
# Python falls back to __repr__.

# ============================================================
# VISUAL SUMMARY
# ============================================================

# print(obj)
#      |
#      v
#   __str__()
#
# If __str__ missing
#      |
#      v
#   __repr__()
#
#
# repr(obj)
#      |
#      v
#   __repr__()

# ============================================================
# COMPARISON
# ============================================================

# __str__
#
# - Human readable
# - Friendly
# - Used by print()
#
#
# __repr__
#
# - Developer readable
# - More precise
# - Used by repr()
# - Fallback for print()

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# 1. Default object output is often not useful.
# 2. __str__ provides a friendly representation.
# 3. Python automatically calls __str__.
# 4. __repr__ is aimed at developers.
# 5. Python automatically calls __repr__ when needed.
# 6. Dunder methods are special methods recognized by Python.
# 7. We define the method; Python decides when to invoke it.
# 8. If __str__ is missing, Python falls back to __repr__.
