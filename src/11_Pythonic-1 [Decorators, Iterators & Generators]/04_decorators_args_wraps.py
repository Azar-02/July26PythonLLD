
"""
PART 4 - DECORATORS WITH *ARGS, **KWARGS AND functools.wraps

Topics Covered

1. Why simple decorators fail
2. Generic wrappers using *args and **kwargs
3. Returning values
4. Metadata problem
5. functools.wraps
"""

# ============================================================
# MOTIVATION
# ============================================================

# Our previous decorator worked only for functions with
# no parameters.
#
# Real applications have functions with different numbers
# of positional and keyword arguments.
#
# We need one decorator that works for ALL of them.

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Many beginners think:
#
# "I'll just add more parameters to wrapper()."
#
# That quickly becomes impossible because every function has
# a different signature.

# ============================================================
# DEMO 1 - THE PROBLEM
# ============================================================

def simple_logger(func):
    def wrapper():
        print("[START]")
        func()
        print("[END]")
    return wrapper

# @simple_logger
# def add(a, b):
#     return a + b
#
# add(10, 20)
#
# Expected:
# TypeError because wrapper() accepts no arguments.

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# Can one wrapper accept ANY number of arguments?
#
# Yes.
#
# Python already provides exactly that mechanism.

# ============================================================
# THEORY
# ============================================================

# *args
# collects positional arguments into a tuple.
#
# **kwargs
# collects keyword arguments into a dictionary.

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# Will this decorator work for both:
#
# greet()
# add(10, 20)
# introduce(name="Alice")

# ============================================================
# DEMO 2 - GENERIC DECORATOR
# ============================================================

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished {func.__name__}")
        return result
    return wrapper

@logger
def greet():
    print("Hello!")

@logger
def add(a, b):
    return a + b

@logger
def introduce(name, city="Unknown"):
    print(f"{name} lives in {city}")

print("Greeting Demo")
greet()

print("\nAddition Demo")
print(add(12, 8))

print("\nKeyword Argument Demo")
introduce(name="Alice", city="Jaipur")

# Runtime Observation:
#
# The same wrapper handled three completely different
# function signatures.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# wrapper(*args, **kwargs)
#          │
#          ▼
#     func(*args, **kwargs)
#
# Arguments simply flow through the wrapper.

# ============================================================
# DEMO 3 - RETURN VALUES
# ============================================================

@logger
def square(x):
    return x * x

print("\nReturn Value Demo")
print(square(9))

# Runtime Observation:
#
# A decorator should usually return the original result,
# otherwise callers may unexpectedly receive None.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Forgetting:
#
# return result
#
# is one of the most common decorator bugs.

# ============================================================
# DEMO 4 - THE METADATA PROBLEM
# ============================================================

print("\nMetadata Before wraps")
print(greet.__name__)

# Observe:
#
# The decorated function no longer reports its original
# metadata.

# ============================================================
# THEORY
# ============================================================

# The wrapper replaced the original function reference.
#
# Therefore attributes like:
#
# __name__
# __doc__
#
# now belong to wrapper.

# ============================================================
# DEMO 5 - functools.wraps
# ============================================================

from functools import wraps

def better_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[BETTER LOGGER]")
        return func(*args, **kwargs)

    return wrapper

@better_logger
def multiply(a, b):
    """Multiply two numbers."""
    return a * b

print("\nUsing functools.wraps")
print(multiply(6, 7))
print(multiply.__name__)
print(multiply.__doc__)

# Runtime Observation:
#
# wraps copies important metadata from the original function.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

print("\nExperiments")
print(callable(multiply))
print(type(multiply))

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Why use *args and **kwargs?
#
# To create decorators that work with arbitrary function
# signatures.
#
# Why use functools.wraps?
#
# To preserve metadata such as __name__, __doc__ and other
# attributes of the wrapped function.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Decorator
#      │
#      ▼
# wrapper(*args, **kwargs)
#      │
#      ▼
# func(*args, **kwargs)
#      │
#      ▼
# return result
#
# Always prefer:
#
# @wraps(func)

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# So far our decorator itself accepts no configuration.
#
# What if we want:
#
# @repeat(3)
# @retry(5)
# @permission("ADMIN")
#
# Next we will learn decorators that accept arguments.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Use *args and **kwargs for generic decorators.
# ✓ Always return the wrapped function's result.
# ✓ Forgetting return is a common bug.
# ✓ Decorated functions lose metadata unless wraps is used.
# ✓ functools.wraps is considered best practice.
