"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 4 - PROPERTIES, GETTERS AND SETTERS
============================================================

Topics Covered
--------------
1. The Validation Problem
2. Traditional Getters
3. Traditional Setters
4. Validation Through Setters
5. Why Getter/Setter Style Feels Clunky
6. Introduction to @property
7. Introduction to @setter
8. Validation with Properties
9. Introduction to @deleter
10. The Pythonic Solution
"""

# ============================================================
# MOTIVATION
# ============================================================

# From the previous files we discovered:
#
# driver.rating = -999
#
# is possible.
#
# This creates invalid object state.
#
# Question:
#
# How can a Driver object protect itself?
#
# How can it ensure that rating always
# remains between:
#
# 0.0 and 5.0 ?

# ============================================================
# ATTEMPT 1 - DIRECT ACCESS
# ============================================================


class DriverV1:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


driver = DriverV1("Ramesh", 4.8)

driver.rating = -999

print("Invalid Rating:", driver.rating)

# Observation:
#
# Direct access gives us no opportunity
# to validate the value.

# ============================================================
# ATTEMPT 2 - TRADITIONAL GETTER
# ============================================================

# Many OOP languages introduce:
#
# getRating()
#
# as a way to access internal state.


class DriverV2:

    def __init__(self, name, rating):
        self._rating = rating

    def get_rating(self):
        return self._rating


driver = DriverV2("Ramesh", 4.8)

print("\nGetter Example")

print(driver.get_rating())

# Observation:
#
# The actual data is hidden behind
# a method call.

# ============================================================
# ATTEMPT 3 - TRADITIONAL SETTER
# ============================================================

# If reading goes through a method,
# then writing can also go through
# a method.


class DriverV3:

    def __init__(self, name, rating):
        self._rating = rating

    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        self._rating = rating


driver = DriverV3("Ramesh", 4.8)

driver.set_rating(4.9)

print("\nSetter Example")

print(driver.get_rating())

# ============================================================
# ADDING VALIDATION
# ============================================================

# Now we finally have a place where
# validation can happen.


class DriverV4:

    def __init__(self, name, rating):
        self._rating = rating

    def get_rating(self):
        return self._rating

    def set_rating(self, rating):

        if 0 <= rating <= 5:

            self._rating = rating

        else:

            print("Invalid Rating Ignored")


driver = DriverV4("Ramesh", 4.8)

driver.set_rating(4.5)

print("\nValid Update")

print(driver.get_rating())

driver.set_rating(-100)

print(driver.get_rating())

# Observation:
#
# Validation now works.
#
# Invalid values are rejected.

# ============================================================
# THE NEW PROBLEM
# ============================================================

# Ask Students:
#
# Is this syntax pleasant?
#
# Reading:
#
# driver.get_rating()
#
# Writing:
#
# driver.set_rating(4.5)
#
# Compare this with:
#
# driver.rating
#
# driver.rating = 4.5
#
# The getter/setter style feels verbose.
#
# Can we have:
#
# Clean attribute syntax
#
# AND
#
# Validation?
#
# Python says:
#
# Yes.

# ============================================================
# INTRODUCING @property
# ============================================================

# @property allows a method to behave
# like an attribute.


class DriverV5:

    def __init__(self, name, rating):
        self._rating = rating

    @property
    def rating(self):

        print("Property Getter Invoked")

        return self._rating


driver = DriverV5("Ramesh", 4.8)

print("\n@property Example")

print(driver.rating)

# Important Observation:
#
# We wrote:
#
# driver.rating
#
# Not:
#
# driver.rating()
#
# Yet a method executed.
#
# This is the key idea behind properties.

# ============================================================
# INTRODUCING @setter
# ============================================================

# Reading is solved.
#
# What about writing?


class DriverV6:

    def __init__(self, name, rating):
        self._rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):

        print("Property Setter Invoked")

        self._rating = value


driver = DriverV6("Ramesh", 4.8)

driver.rating = 4.9

print("\nSetter Property Example")

print(driver.rating)

# Observation:
#
# We wrote:
#
# driver.rating = 4.9
#
# Yet Python executed a method.

# ============================================================
# ADDING VALIDATION TO PROPERTY
# ============================================================

# This is where properties become powerful.


class DriverV7:

    def __init__(self, name, rating):
        self._rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):

        if 0 <= value <= 5:

            self._rating = value

        else:

            print("Invalid Rating Ignored")


driver = DriverV7("Ramesh", 4.8)

print("\nValidation Through Properties")

driver.rating = 4.6

print(driver.rating)

driver.rating = -500

print(driver.rating)

# Observation:
#
# We achieved:
#
# Clean Syntax
#
# AND
#
# Validation

# ============================================================
# VISUAL SUMMARY
# ============================================================

# Without Property:
#
# driver.set_rating(4.5)
#
#
# With Property:
#
# driver.rating = 4.5
#
#
# Looks like an attribute.
#
# Behaves like a method.

# ============================================================
# INTRODUCING @deleter
# ============================================================

# Properties can also intercept deletion.


class DriverV8:

    def __init__(self, rating):
        self._rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = value

    @rating.deleter
    def rating(self):

        print("Deleting Rating")

        del self._rating


driver = DriverV8(4.8)

print("\nDeleting Property")

del driver.rating

# ============================================================
# THE FINAL PYTHONIC VERSION
# ============================================================


class DriverFinal:

    def __init__(self, name, rating):

        self.name = name

        self._rating = rating

    @property
    def rating(self):

        return self._rating

    @rating.setter
    def rating(self, value):

        if not isinstance(value, (int, float)):
            raise ValueError(
                "Rating must be numeric"
            )

        if not (0 <= value <= 5):
            raise ValueError(
                "Rating must be between 0 and 5"
            )

        self._rating = value

    def __str__(self):

        return (
            f"Driver(name={self.name}, "
            f"rating={self.rating})"
        )


driver = DriverFinal("Priya", 4.9)

print("\nFinal Version")

print(driver)

driver.rating = 4.7

print(driver)

# Uncomment to see validation.
#
driver.rating = -100
print(driver)

# ============================================================
# WHAT JUST HAPPENED?
# ============================================================

# To the outside world:
#
# driver.rating
#
# looks like a normal attribute.
#
# Internally:
#
# Python executes methods.
#
# This gives us:
#
# 1. Encapsulation
# 2. Validation
# 3. Clean Syntax
#
# all at the same time.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Question:
#
# What exactly is @property ?
#
# Is it magic?
#
# Is it a special keyword?
#
# In the next file we will discover:
#
# property(...)
#
# and the Descriptor Protocol.
#
# This reveals how properties actually work.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Traditional OOP solution:
#
# get_rating()
# set_rating()
#
# Pythonic solution:
#
# @property
# @rating.setter
#
# Properties allow:
#
# - Validation
# - Encapsulation
# - Clean syntax
#
# Attributes can look like fields
# while behaving like methods.
