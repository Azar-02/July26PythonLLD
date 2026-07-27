"""
PART 6 - STACKED AND CLASS-BASED DECORATORS

Topics Covered

1. Why stack decorators?
2. Decoration order vs execution order
3. ASCII call-flow diagrams
4. Class-based decorators
5. __call__ method
6. CountCalls example
"""

# ============================================================
# MOTIVATION
# ============================================================

# One decorator may not be enough.
#
# Imagine we want to:
# - Log every call.
# - Measure execution time.
# - Check permissions.
#
# Should we combine everything into one huge decorator?
#
# No.
#
# We can stack decorators to keep each responsibility separate.

# ============================================================
# THEORY
# ============================================================

# Multiple decorators can be applied to the same function.
#
# Example:
#
# @A
# @B
# def work():
#     ...
#
# Python decorates from the bottom upwards.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# work
#   │
#   ▼
# B(work)
#   │
#   ▼
# A(wrapper_from_B)
#   │
#   ▼
# Final callable

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# Which decorator is applied first?
# Which message prints first?

from functools import wraps

def stars(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("***** START *****")
        result = func(*args, **kwargs)
        print("***** END *****")
        return result
    return wrapper

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[LOG] Before")
        result = func(*args, **kwargs)
        print("[LOG] After")
        return result
    return wrapper

# ============================================================
# DEMO 1 - STACKED DECORATORS
# ============================================================

@stars
@logger
def greet():
    print("Hello from greet()")

print("Stacked Decorator Demo")
greet()

# Runtime Observation:
#
# Decoration order:
# logger -> stars
#
# Execution enters the outermost wrapper first,
# eventually reaching the original function.

# ============================================================
# EXECUTION FLOW
# ============================================================

# @stars
# @logger
# def greet():
#
# is equivalent to:
#
# greet = stars(logger(greet))

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception:
#
# Decorators execute from top to bottom.
#
# Reality:
#
# Decoration occurs bottom to top.
#
# Calls pass through the outer wrapper first.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

print("\nMetadata")
print(greet.__name__)
print(callable(greet))

# ============================================================
# WHY CLASS-BASED DECORATORS?
# ============================================================

# So far every decorator has been a function.
#
# But objects can also behave like functions if they implement
# __call__().
#
# That allows us to keep state inside the decorator object.

# ============================================================
# THEORY
# ============================================================

# __call__()
#
# Makes an object callable just like a function.

# ============================================================
# DEMO 2 - CLASS DECORATOR
# ============================================================

class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"[CountCalls] Call #{self.calls}")
        return self.func(*args, **kwargs)

@CountCalls
def add(a, b):
    return a + b

print("\nClass Decorator Demo")
print(add(2, 3))
print(add(10, 20))
print(add(7, 8))

# Runtime Observation:
#
# The CountCalls object stores state.
#
# The call count increases every invocation.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# add
#  │
#  ▼
# CountCalls Object
#      │
#      ├── func
#      └── calls

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# Why use a class instead of a function?
#
# Expected Answer:
#
# A class naturally stores state using instance attributes.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Q: Can decorators be classes?
#
# Yes.
#
# Any callable object can act as a decorator.
#
# Implement __call__().

# ============================================================
# BOARD SUMMARY
# ============================================================

# Function Decorator
#     Function -> Wrapper
#
# Class Decorator
#     Object + __call__()
#
# Stacked decorators:
#
# greet = stars(logger(greet))

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# We have now explored several decorator styles.
#
# Next we will build a practical Singleton decorator using
# closures and dictionaries to ensure only one instance of
# a class is ever created.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Decorators can be stacked.
# ✓ Decoration order is bottom to top.
# ✓ @A @B is A(B(function)).
# ✓ Classes can also be decorators.
# ✓ __call__ makes objects callable.
# ✓ Class decorators can easily maintain state.
