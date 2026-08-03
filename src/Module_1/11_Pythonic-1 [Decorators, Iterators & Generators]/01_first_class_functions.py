"""
PART 1 - FIRST-CLASS FUNCTIONS

Topics Covered

1. What are first-class functions?
2. Functions are values
3. Storing functions in variables
4. Passing functions as arguments
5. Why this concept is the foundation of decorators
"""

# ============================================================
# MOTIVATION
# ============================================================

# Until today, we have mostly used functions like this:
#
#     greet("Alice")
#
# We write a function name.
# Add parentheses.
# Python executes it.
#
# This naturally makes many beginners believe that a function
# exists only to be called.
#
# Python has a much more powerful idea.
#
# A function is simply another object.
#
# Just like an integer, string or list, a function can be
# stored, passed around and later used.
#
# Once this idea clicks, decorators become much easier to
# understand because decorators receive and return functions.

# ============================================================
# THEORY
# ============================================================

# First-Class Function means:
#
# A function can be treated like any normal value.
#
# It can be:
#
# • Stored inside a variable
# • Passed into another function
# • Returned from another function (next topic)
#
# One very important distinction:
#
# greet
# -----
# Refers to the function object.
#
# greet()
# -------
# Executes the function and returns its result.

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Many beginners think:
#
#     say_hello = greet
#
# executes greet().
#
# It does NOT.
#
# Since there are no parentheses, Python simply creates another
# reference to the same function object.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# Before Assignment
#
# greet
#   │
#   ▼
# Function Object
#
#
# After Assignment
#
# greet --------┐
#               │
#               ▼
#        Function Object
#               ▲
#               │
# say_hello ----┘
#
# Two labels.
# One function object.

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# What exactly gets stored here?
#
#     say_hello = greet
#
# Is it:
#
# • the returned string?
# • the function?
# • something else?
#
# EXPECTED ANSWER
#
# The function itself.
#
# Parentheses execute.
# No parentheses simply refer to the function object.

# ============================================================
# DEMO 1 - STORING FUNCTIONS
# ============================================================

def greet(name):
    return f"Hello, {name}"

say_hello = greet

print("Original call :", greet("Alice"))
print("Variable call :", say_hello("Alice"))

print("\nSame object?")
print(greet is say_hello)

# Runtime Observation:
#
# Observe that the output is True.
#
# We never copied the function.
#
# We simply created another reference pointing to exactly the
# same function object.

print("\nMemory Addresses")
print(id(greet))
print(id(say_hello))

# ============================================================
# DEMO 2 - FUNCTIONS ARE OBJECTS
# ============================================================

print("\nType Information")
print(type(greet))

print("\nCallable Checks")
print(callable(greet))
print(callable(10))
print(callable("Hello"))

# Observe:
#
# Functions are objects.
#
# They also happen to be callable.

# ============================================================
# DEMO 3 - PASSING FUNCTIONS
# ============================================================

def shout(func, name):
    return func(name).upper()

print("\nPassing function as argument")
print(shout(greet, "Bob"))

# Why didn't we write greet()?
#
# Because shout expects a FUNCTION.
#
# greet() would execute immediately and produce a string.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Interview Question:
#
# "Are functions objects in Python?"
#
# Correct Answer:
#
# Yes.
#
# Functions are first-class objects.
#
# Therefore they can be:
#
# • Assigned
# • Passed
# • Returned
# • Decorated

# ============================================================
# BOARD SUMMARY
# ============================================================

# No Parentheses
#
#     greet
#
# Means:
#
#     The function object.
#
#
# Parentheses
#
#     greet(...)
#
# Means:
#
#     Execute the function.

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# So far we have learned that a function can be treated like
# any other value.
#
# Python goes one step further.
#
# A function can even CREATE another function.
#
# Even more interesting...
#
# The inner function can remember variables from the outer
# function long after the outer function has finished.
#
# That special ability is called a Closure.
#
# Closures are the real building blocks behind decorators.
#
# That is exactly what we study next.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Functions are objects.
# ✓ Functions are first-class values.
# ✓ Parentheses execute a function.
# ✓ Without parentheses you refer to the function object.
# ✓ Functions can be stored and passed around.
# ✓ This idea is the foundation of closures and decorators.
