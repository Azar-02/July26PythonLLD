"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 06_callable_objects.py
============================================================

Topics Covered
--------------
1. Functions As Objects
2. The callability concept
3. callable()
4. __call__
5. Building Callable Objects
6. Function-like Classes
7. Stateful Callables
8. Real World Use Cases
9. Interview Questions
10. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider a normal function.
#
# We can invoke it using:
#
# ()
#
# Example:
#
# greet()
#
# Question:
#
# Why does Python allow this?
#
# What makes an object callable?
#
# This lecture explores that idea.

# ============================================================
# A NORMAL FUNCTION
# ============================================================


def greet():

    print("Welcome To LLD")


greet()

# Observation:
#
# Functions can be called
# using parentheses.

# ============================================================
# FUNCTIONS ARE OBJECTS
# ============================================================

# In Python:
#
# Functions are objects.
#
# They can be:
#
# Assigned
# Stored
# Passed around
# Returned


def welcome():

    print("Welcome")


another_reference = welcome

print("\nFunction Object")

another_reference()

# Observation:
#
# Both variables refer to
# the same function object.

# ============================================================
# THE CALLABILITY QUESTION
# ============================================================

# Question:
#
# How does Python know that
# an object can be called?

# ============================================================
# callable()
# ============================================================

print("\ncallable() Examples")

print(callable(welcome))

print(callable("Bengaluru"))

print(callable([1, 2, 3]))

# Observation:
#
# Functions are callable.
#
# Strings are not.
#
# Lists are not.

# ============================================================
# DUNDER CONNECTION
# ============================================================

# Just like:
#
# len(x)
# -> __len__
#
# x + y
# -> __add__
#
# x == y
# -> __eq__
#
# Function call syntax
# also maps to a dunder.

# ============================================================
# INTRODUCING __call__
# ============================================================

# If an object implements:
#
# __call__
#
# it becomes callable.

# ============================================================
# FIRST CALLABLE OBJECT
# ============================================================


class Greeter:

    def __call__(self):

        print("Welcome To Python LLD")


greeter = Greeter()

print("\nCallable Object")

greeter()

# Observation:
#
# Instance behaves
# like a function.

# ============================================================
# VERIFYING CALLABILITY
# ============================================================

print("\ncallable(greeter)")

print(callable(greeter))

# Observation:
#
# Python now considers
# the object callable.

# ============================================================
# WHAT ACTUALLY HAPPENS?
# ============================================================

# greeter()
#
# becomes:
#
# greeter.__call__()

# ============================================================
# PARAMETERS IN __call__
# ============================================================


class FareCalculator:

    def __call__(
        self,
        distance,
        rate
    ):

        return (
            distance * rate
        )


calculator = FareCalculator()

fare = calculator(
    12,
    15
)

print("\nFare Calculation")

print(fare)

# Observation:
#
# __call__ can accept
# parameters exactly like
# a normal function.

# ============================================================
# RETURN VALUES
# ============================================================

# __call__ can also
# return values.

# Already demonstrated above.
#
# The object behaved exactly
# like a function.

# ============================================================
# STATEFUL CALLABLES
# ============================================================

# Functions often have
# no persistent state.
#
# Objects do.
#
# Callable objects combine
# both ideas.

# ============================================================
# EXAMPLE
# ============================================================


class RideCounter:

    def __init__(self):

        self.total_rides = 0

    def __call__(self):

        self.total_rides += 1

        return self.total_rides


counter = RideCounter()

print("\nRide Counter")

print(counter())
print(counter())
print(counter())
print(counter())

# Observation:
#
# State persists between calls.

# ============================================================
# WHY THIS IS INTERESTING
# ============================================================

# Normal functions do not
# naturally carry object state.
#
# Callable objects do.

# ============================================================
# ANOTHER EXAMPLE
# ============================================================


class DiscountEngine:

    def __init__(
        self,
        discount_percent
    ):

        self.discount_percent = (
            discount_percent
        )

    def __call__(
        self,
        amount
    ):

        return (
            amount
            *
            (100 - self.discount_percent)
            / 100
        )


discount = DiscountEngine(20)

print("\nDiscount Engine")

print(discount(1000))
print(discount(2500))

# Observation:
#
# Configuration is stored
# inside the object.
#
# Behaviour feels like
# a function.

# ============================================================
# REAL WORLD USE CASES
# ============================================================

# Validation Engines
#
# Pricing Engines
#
# Recommendation Engines
#
# Machine Learning Models
#
# Command Objects
#
# Strategy Objects

# ============================================================
# CALLABLE OBJECTS VS FUNCTIONS
# ============================================================

# Function:
#
# Simple
# Lightweight
#
#
# Callable Object:
#
# State
# Configuration
# Encapsulation

# ============================================================
# COMMON PATTERN
# ============================================================

# Create once.
#
# Configure once.
#
# Call many times.

# ============================================================
# CALLABLE CLASS INSTANCE
# ============================================================


class TripMatcher:

    def __init__(
        self,
        city
    ):

        self.city = city

    def __call__(
        self,
        driver_name
    ):

        return (
            f"{driver_name} "
            f"matched in "
            f"{self.city}"
        )


matcher = TripMatcher(
    "Bengaluru"
)

print("\nTrip Matcher")

print(
    matcher("Ramesh")
)

print(
    matcher("Suresh")
)

# Observation:
#
# Same configuration.
#
# Multiple calls.

# ============================================================
# callable() REVISITED
# ============================================================

print("\nCallable Checks")

print(callable(matcher))

print(callable(counter))

print(callable(discount))

# Observation:
#
# All objects implement
# __call__.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What makes an object callable?
#
# Answer:
#
# Implementing __call__.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# What does:
#
# obj()
#
# become internally?
#
# Answer:
#
# obj.__call__()

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Why use callable objects
# instead of functions?
#
# Answer:
#
# They combine behaviour
# with state.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Forgetting that callable()
# checks for __call__.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# __call__ makes objects callable.
#
# obj()
#
# becomes:
#
# obj.__call__()
#
# Callable objects behave
# like functions.
#
# They can maintain state.
#
# They are common in LLD
# and framework design.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We have explored:
#
# __len__
# __eq__
# __hash__
# __enter__
# __exit__
# __call__
#
# Next we combine several
# protocols together while
# building a custom container.
#
# Next:
#
# 07_deck_container_protocol.py
