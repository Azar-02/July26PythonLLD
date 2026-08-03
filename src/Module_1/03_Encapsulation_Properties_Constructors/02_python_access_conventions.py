"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 2 - PYTHON ACCESS CONVENTIONS
============================================================

Topics Covered
--------------
1. Access Modifiers in Other Languages
2. Python's Philosophy
3. Public Attributes
4. The Single Underscore Convention
5. Why _protected Is Not Protection
6. Consenting Adults Principle
7. Preparing for Name Mangling
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we discovered a problem.
#
# Any code could do:
#
# driver.rating = -999
#
# and place the object into an invalid state.
#
# Naturally, many students coming from Java ask:
#
# Can we make rating private?
#
# Before answering that question,
# we need to understand how Python thinks
# about access control.

# ============================================================
# ACCESS MODIFIERS IN OTHER LANGUAGES
# ============================================================

# In Java we commonly see:
#
# private
# protected
# public
#
# Example:
#
# private double rating;
#
# The language enforces the restriction.
#
# Outside code cannot directly access it.
#
# Many developers expect Python
# to work the same way.

# ============================================================
# PYTHON'S PHILOSOPHY
# ============================================================

# Python takes a different approach.
#
# Python follows a philosophy often described as:
#
# "We are all consenting adults here."
#
# The language assumes that developers
# will act responsibly.
#
# Instead of aggressively blocking access,
# Python prefers conventions.

# ============================================================
# PUBLIC ATTRIBUTES
# ============================================================

# By default every attribute is public.


class DriverV1:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


driver = DriverV1("Ramesh", 4.8)

print("Public Attribute Access")

print(driver.name)
print(driver.rating)

driver.rating = 4.9

print(driver.rating)

# Observation:
#
# Reading is allowed.
# Writing is allowed.
#
# Nothing is restricted.

# ============================================================
# THE SINGLE UNDERSCORE CONVENTION
# ============================================================

# Python developers often use:
#
# _attribute
#
# to communicate intent.
#
# Example:
#
# _rating
#
# This does NOT make the attribute private.
#
# It simply tells other developers:
#
# "This is considered internal.
#  Please be careful."


class DriverV2:

    def __init__(self, name, rating):
        self.name = name
        self._rating = rating


driver = DriverV2("Priya", 4.9)

print("\nSingle Underscore Example")

print(driver._rating)

# The attribute is still accessible.
#
# Python does not stop us.

# ============================================================
# IMPORTANT QUESTION
# ============================================================

#
# If Python allows access anyway,
# then what is the purpose of _rating?
#
# Answer:
#
# Communication.
#
# It communicates intent.
#
# It tells other developers:
#
# "This attribute is internal."
#
# Conventions are an important part
# of Python culture.

# ============================================================
# PROVING IT IS NOT PROTECTION
# ============================================================

driver._rating = -999

print("\nModified Internal Attribute")

print(driver._rating)

# Observation:
#
# Python allowed it.
#
# Therefore:
#
# _rating is NOT private.
#
# _rating is NOT protected.
#
# It is merely a naming convention.

# ============================================================
# WHY DOES PYTHON DO THIS?
# ============================================================

# Python values simplicity.
#
# The language avoids unnecessary restrictions.
#
# The assumption is:
#
# If you intentionally access an internal
# attribute, you probably know what you are doing.
#
# This idea is often summarized as:
#
# "Consenting Adults"

# ============================================================
# A REAL-WORLD ANALOGY
# ============================================================

# Imagine a room with a sign:
#
# "Employees Only"
#
# The sign communicates intent.
#
# Most people respect it.
#
# There may not be a locked door.
#
# The underscore convention works similarly.
#
# It says:
#
# "Please don't use this unless you
# understand what you're doing."

# ============================================================
# CLASS DESIGN EXAMPLE
# ============================================================


class DriverV3:

    def __init__(self, name, rating):
        self.name = name
        self._rating = rating

    def display(self):
        print(
            f"Driver(name={self.name}, "
            f"rating={self._rating})"
        )


driver = DriverV3("Amit", 4.7)

driver.display()

# Inside the class,
# using _rating is completely normal.
#
# The convention primarily affects
# code outside the class.

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Many developers assume:
#
# _attribute
#
# means:
#
# protected
#
# That is not true.
#
# Python does not enforce such a rule.
#
# The underscore is only a convention.

# ============================================================
# WHAT PROBLEM REMAINS?
# ============================================================

# We still have the same issue.
#
# Outside code can do:
#
# driver._rating = -999
#
# So the object still cannot fully
# protect its own state.
#
# This raises a new question:
#
# Does Python provide a stronger mechanism?

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Python does provide another mechanism:
#
# __attribute
#
# Double underscore names behave differently.
#
# They trigger something called:
#
# Name Mangling
#
# Many beginners think this creates
# true private attributes.
#
# In the next file we will investigate
# exactly what happens.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# By default attributes are public.
#
# _attribute is a convention.
#
# The single underscore does NOT create:
#
# - private attributes
# - protected attributes
#
# It simply communicates intent.
#
# Python prefers conventions over
# strict enforcement.
#
# Next:
#
# Name Mangling
# and double underscore attributes.
