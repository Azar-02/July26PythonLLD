
"""
PART 3 - DECORATORS BASICS

Topics Covered
1. Why decorators exist
2. Manual function wrapping
3. Wrapper functions
4. @ decorator syntax
5. Manual vs @ equivalence
"""

# ============================================================
# MOTIVATION
# ============================================================

# Imagine you have a function that already works perfectly.
#
# Later, your manager asks:
#
# - Log every call.
# - Measure execution time.
# - Check permissions.
# - Retry on failure.
#
# Should we edit every existing function?
#
# That quickly becomes repetitive and error-prone.
#
# We need a way to ADD behaviour without changing the original
# business logic.
#
# That is exactly why decorators exist.

# ============================================================
# ANALOGY - GIFT WRAPPING
# ============================================================

# Think of a gift.
#
# The gift itself does not change.
#
# We simply wrap it.
#
# The wrapper adds presentation while preserving the gift.
#
# Decorators wrap functions in the same way.

# ============================================================
# THEORY
# ============================================================

# A decorator is simply a function that:
#
# 1. Receives another function.
# 2. Creates a wrapper.
# 3. Returns the wrapper.
#
# Nothing magical happens.

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# Since functions are first-class objects, can a function accept
# another function as an argument?
#
# Yes.
#
# That idea makes decorators possible.

# ============================================================
# DEMO 1 - THE ORIGINAL FUNCTION
# ============================================================

def greet():
    print("Hello!") ## 1

print("Original:")
greet()

# Runtime Observation:
# greet points directly to the original function.

# ============================================================
# DEMO 2 - MANUAL WRAPPING
# ============================================================

def decorator(func):#1
    def wrapper(): #2
        print("[LOG] Before function")
        func() #1
        print("[LOG] After function")
    return wrapper

wrapped = decorator(greet)

print("\nManual wrapping:")
wrapped()

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# greet ---------> original function
#
# decorator(greet)
#          │
#          ▼
#      wrapper ----------> original function

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# Has greet changed?
#
# Or did we simply create another function?

print("\nOriginal still works:")
greet() ##1

# Runtime Observation:
#
# The original function has not been modified.
# We merely created another function.

# ============================================================
# DEMO 3 - REPLACING THE REFERENCE
# ============================================================

greet = decorator(greet)
#1 --> #2
print("\nReference replaced:")
greet()

# Runtime Observation:
#
# The name greet now refers to wrapper().
#
# The original function still exists.
#
# The wrapper simply keeps a reference to it. Func point to original greet method

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception:
#
# Decorators modify the original function.
#
# Reality:
#
# They usually return a NEW function.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

print("\nExperiments")
print(type(greet))
print(callable(greet))
print(greet.__name__)

# Observe:
#
# The wrapper has replaced the original reference.

# ============================================================
# WHY @ EXISTS
# ============================================================

# Writing
#
# greet = decorator(greet)
#
# again and again becomes repetitive.
#
# Python therefore introduced a cleaner syntax.

# ============================================================
# DEMO 4 - @ SYNTAX
# ============================================================

def logger(func):
    def wrapper():
        print("[START]")
        func()
        print("[END]")
    return wrapper

@logger
def say_bye():
    print("Good Bye!")

print("\nUsing @ syntax:")
say_bye()

# ============================================================
# MANUAL VS @
# ============================================================

# These are identical.
#
# Version 1
#
# @logger
# def hello():
#     ...
#
# Version 2
#
# def hello():
#     ...
#
# hello = logger(hello)

# ============================================================
# MEMORY DIAGRAM
# ============================================================

#            hello
#              │
#              ▼
#         logger()
#              │
#              ▼
#          wrapper
#              │
#              ▼
#      original function

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# What is a decorator?
#
# A function that accepts another function,
# wraps additional behaviour around it,
# and returns a new callable.
#
# What does @ actually do?
#
# It is syntactic sugar for:
#
# func = decorator(func)

# ============================================================
# BOARD SUMMARY
# ============================================================

# Function
#      │
#      ▼
# Decorator
#      │
#      ▼
# Wrapper
#      │
#      ▼
# Original Function
#
# @decorator
#
# is equivalent to
#
# function = decorator(function)

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# Our wrapper currently works only for functions
# with NO parameters.
#
# Real-world functions accept many different arguments.
#
# In the next lesson we will make decorators generic using:
#
# *args
# **kwargs
#
# We will also learn why functools.wraps is important.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Decorators add behaviour without changing business logic.
# ✓ A decorator receives a function.
# ✓ A wrapper calls the original function.
# ✓ Decorators usually return a new function.
# ✓ @ is only syntactic sugar.
# ✓ @decorator is equivalent to:
#   function = decorator(function)
