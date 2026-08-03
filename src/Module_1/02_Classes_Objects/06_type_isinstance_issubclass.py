"""
============================================================
LLD-2 : OOP-1
PART 6 - type(), isinstance(), issubclass()
============================================================

Topics Covered
--------------
1. Understanding type()
2. Exact Type Checking
3. Understanding isinstance()
4. Why isinstance() is Preferred
5. The bool and int Surprise
6. Understanding issubclass()
7. Comparing All Three
"""

# ============================================================
# MOTIVATION
# ============================================================

# Imagine our Uber system contains:
#
# Car
# Bike
# Auto
# Driver
# Rider
#
# At some point a function receives an object.
#
# How do we determine what kind of object it is?
#
# Python provides three important tools:
#
# type()
# isinstance()
# issubclass()

# ============================================================
# SETUP
# ============================================================

class Driver:
    pass


driver_one = Driver()

# ============================================================
# UNDERSTANDING type()
# ============================================================

# type() tells us the exact class of an object.

print("type(driver_one)")
print(type(driver_one))

# Typical Output:
#
# <class '__main__.Driver'>

# ============================================================
# USING type() FOR COMPARISON
# ============================================================

if type(driver_one) == Driver:
    print("\nIt's a Driver")

# This works.
#
# However, the lecture notes warn that there
# is a better tool that becomes important
# when inheritance enters the picture.

# ============================================================
# INTRODUCING isinstance()
# ============================================================

# isinstance() checks whether an object
# is an instance of a class.
#
# More importantly:
#
# It also considers inheritance relationships.

print("\nisinstance(driver_one, Driver)")
print(isinstance(driver_one, Driver))

# In real projects this is usually what
# you actually want.

# ============================================================
# THE SURPRISE DEMO
# ============================================================

# running this live 

print("\nThe bool/int surprise")

print(isinstance(True, int))
print(isinstance(True, bool))

# Question:
#
# Why is True an instance of int?
#
# Answer:
#
# In Python:
#
# bool inherits from int
#
# True behaves like 1
# False behaves like 0

# ============================================================
# WHY isinstance() IS PREFERRED
# ============================================================

print("\nComparing type() and isinstance()")

print(type(True) == int)
print(isinstance(True, int))

# Observation:
#
# type(True) == int
#     False
#
# isinstance(True, int)
#     True
#
# isinstance understands inheritance.
#
# type() only checks the exact type.

# ============================================================
# UNDERSTANDING issubclass()
# ============================================================

# issubclass() works with classes,
# not objects.

print("\nissubclass examples")

print(issubclass(bool, int))

# Everything in Python ultimately
# inherits from object.

print(issubclass(Driver, object))

# ============================================================
# CLASS RELATIONSHIPS VS OBJECTS
# ============================================================

# isinstance()
#
# Works with objects.
#
# Example:
#
# isinstance(driver_one, Driver)
#
#
# issubclass()
#
# Works with classes.
#
# Example:
#
# issubclass(bool, int)

# ============================================================
# VISUAL SUMMARY
# ============================================================

# driver_one
#      |
#      v
#    Driver
#
# isinstance(driver_one, Driver)
#
#
# bool
#      |
#      v
#     int
#
# issubclass(bool, int)

# ============================================================
# COMPARISON TABLE
# ============================================================

# type(obj)
#
# - Exact class only
# - Use sparingly
#
#
# isinstance(obj, Class)
#
# - Checks object relationship
# - Handles inheritance
# - Usually preferred
#
#
# issubclass(A, B)
#
# - Checks class relationship
# - Works on classes


# ============================================================
# KEY TAKEAWAYS
# ============================================================

# type(obj)
#     exact class
#
# isinstance(obj, Class)
#     object relationship
#     preferred in most situations
#
# issubclass(A, B)
#     class relationship
#
# Remember:
#
# type()       -> object's exact class
# isinstance() -> object relationship
# issubclass() -> class relationship
