"""
PART 02 - CLOSURES AND NONLOCAL (MASTER EDITION)

This teaching script is intentionally verbose.
Read it from top to bottom exactly like a classroom session.

Topics
------
1. Nested Functions
2. Closures
3. Why Closures Exist
4. Closure Cells
5. __closure__ and cell_contents
6. nonlocal
7. Multiple Closures
8. Independent State
9. Interview Questions
10. Bridge to Decorators
"""

# ============================================================
# MOTIVATION
# ============================================================

# Until today every function you wrote behaved similarly:
#
#   Input ---> Function ---> Output
#
# Once the function finished, all of its local variables
# disappeared.
#
# Today we are going to challenge that belief.
#
# Imagine I ask:
#
# "Can a function remember something AFTER it has finished?"
#
# Most beginners answer:
#
# "Impossible."
#
# Let's verify that assumption instead of accepting it.

# ============================================================
# REVISION
# ============================================================

# A function is an object.
# It can be:
#
# ✓ Stored in a variable
# ✓ Passed to another function
# ✓ Returned from another function
#
# Today we use the third property.

# ============================================================
# THEORY : NESTED FUNCTIONS
# ============================================================

# Python allows defining a function inside another function.
#
# This inner function is called a nested function.
#
# Question:
#
# Why would anyone do that?
#
# The answer becomes clear after today's demos.


# ============================================================
# DEMO 1
# ============================================================

def make_multiplier(factor):
    print(f"Creating multiplier using factor={factor}")

    def multiply(number):
        return number * factor

    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print("\nOutputs")
print(double(10))
print(triple(10))

print(make_multiplier(5)(10))

# Pause here while teaching.
#
# Ask:
#
# "Where did factor come from?"

# ============================================================
# DISCOVERY
# ============================================================

# make_multiplier() already finished.
#
# Normally local variables disappear.
#
# Yet factor is still available.
#
# This is the mystery that closures solve.

# ============================================================
# BACKPACK ANALOGY
# ============================================================

# Imagine every returned function carries a backpack.
#
# Before leaving the outer function Python packs every variable
# the inner function still needs.
#
# That backpack travels together with the function forever.

# ============================================================
# MEMORY BOARD
# ============================================================

# make_multiplier(2)
#
# factor=2
#
#        │
#        ▼
#   multiply()
#        │
#        ▼
# Closure Cell
# factor=2
#
# make_multiplier frame disappears.
#
# Closure Cell survives.

# ============================================================
# EXPERIMENT 1
# ============================================================

print("\nInspect Closure")
print(double.__closure__)
print(double.__closure__[0].cell_contents)

print("\nSecond Closure")
print(triple.__closure__)
print(triple.__closure__[0].cell_contents)

print("\nCell ids")
print(id(double.__closure__[0]))
print(id(triple.__closure__[0]))

# Observation:
#
# Different closure cells.
#
# Same code.
#
# Different remembered state.


# ============================================================
# COMMON MISTAKES
# ============================================================

# X Assuming closures copy values.
# X Assuming all closures share state.
# X Confusing global with nonlocal.

# ============================================================
# DEMO 2 - nonlocal
# ============================================================

def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

c1 = counter()
c2 = counter()

print("\nCounter A")
print(c1(), c1(), c1())

print("\nCounter B")
print(c2(), c2())

# Ask learners:
#
# Why didn't Counter B start from 4?
#
# Because each call created an independent closure.

# ============================================================
# DEEP DIVE
# ============================================================

# Reading outer variables:
# Allowed.
#
# Modifying outer variables:
# Requires nonlocal.
#
# global changes module variables.
# nonlocal changes enclosing-function variables.

# ============================================================
# REAL WORLD USE CASES
# ============================================================

# ✓ Decorators
# ✓ Logger builders
# ✓ Configuration factories
# ✓ Authentication wrappers
# ✓ Rate limiters
# ✓ Retry utilities
# ✓ Memoization
# ✓ Dependency injection helpers

# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

# Q. What is a closure?
#
# A function that remembers variables from its enclosing scope
# after that scope has returned.
#
# Q. What attribute stores captured variables?
#
# __closure__
#
# Q. How do we inspect values?
#
# cell_contents
#
# Q. Why use nonlocal?
#
# To modify captured variables.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Nested Function
#      │
# returns
#      ▼
# Closure
#      │
# remembers variables
#      ▼
# Closure Cell
#      │
# nonlocal
#      ▼
# Mutable remembered state

# ============================================================
# BRIDGE
# ============================================================

# Decorators are simply closures wrapped around functions.
#
# Once closures become clear,
# decorators become much easier.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Nested functions create closures.
# ✓ Closures preserve required variables.
# ✓ Captured variables live in closure cells.
# ✓ __closure__ exposes captured cells.
# ✓ cell_contents reveals remembered values.
# ✓ nonlocal modifies enclosing variables.
# ✓ Closures power decorators and many advanced Python patterns.
