"""
PART 05 - DECORATORS WITH ARGUMENTS 
"""

from functools import wraps

# ============================================================
# MOTIVATION
# ============================================================

# Last class we learned ordinary decorators.
#
# They always behaved the same way.
#
# But imagine we want different behaviour...
#
# @repeat(2)
# @repeat(5)
# @repeat(10)
#
# The decorator itself now needs some configuration.
#
# Question:
#
# How can we pass data to a decorator?

# ============================================================
# QUICK REVISION
# ============================================================

# Previous lecture:
#
# Outer Function
#      │
# returns
#      ▼
# Inner Function
#
# Today's lecture asks:
#
# What if the OUTER function itself also needs arguments?

# ============================================================
# THINK BEFORE CODING
# ============================================================

# Suppose we write:
#
# @repeat(3)
#
# What do you think Python does FIRST?
#
# A) Calls the decorated function
# B) Calls repeat(3)
# C) Calls wrapper()
#
# Keep your answer in mind.

# ============================================================
# DEMO 1
# ============================================================

def repeat(times):
    print(f"[Layer 1] Creating decorator (times={times})")

    def decorator(func):
        print(f"[Layer 2] Decorating {func.__name__}")

        @wraps(func)
        def wrapper(*args, **kwargs):
            print("[Layer 3] Wrapper executing")
            result = None
            for i in range(times):
                print(f"Iteration {i+1}")
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def say_hello():
    print("Hello!")

print("\nCalling function...\n")
say_hello()

# ============================================================
# CLASS DISCUSSION
# ============================================================

# Ask learners:
#
# 1. Which print happened first?
# 2. Which prints happened only once?
# 3. Which print happens every function call?
#
# Observation:
#
# Layer 1 and Layer 2 execute during decoration.
# Layer 3 executes whenever the decorated function is called.

# ============================================================
# WHY THREE FUNCTIONS?
# ============================================================

# We have three different jobs happening at three different times.
#
# Job 1:
# Receive decorator arguments.
#
# repeat(3)
#
# -------------------------
#
# Job 2:
# Receive the function being decorated.
#
# decorator(say_hello)
#
# -------------------------
#
# Job 3:
# Execute when someone later calls say_hello().
#
# wrapper()
#
# Because these events happen at different times,
# Python naturally needs three nested functions.

# ============================================================
# TIMELINE
# ============================================================

# Program Starts
#        │
#        ▼
# repeat(3)
#        │
#        ▼
# decorator(say_hello)
#        │
#        ▼
# say_hello becomes wrapper
#
# ---------------------------------
# Much later...
#
# say_hello()
#        │
#        ▼
# wrapper executes

# ============================================================
# MEMORY VIEW
# ============================================================

# repeat(3)
#      │
#      ▼
# decorator
# remembers
# times = 3
#      │
#      ▼
# wrapper
# remembers
# func + times

# ============================================================
# DEMO 2
# ============================================================

@repeat(2)
def add(a, b):
    print(f"Adding {a} + {b}")
    return a + b

print("\nReturn value demo")
print(add(10, 20))

# ============================================================
# EXPERIMENTS
# ============================================================

print("\nExperiment 1")
print(type(repeat))

print("\nExperiment 2")
d = repeat(5)
print(callable(d))

print("\nExperiment 3")
wrapped = d(say_hello)
print(callable(wrapped))


# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# X All three functions execute together.
#
# X repeat() runs every time.
#
# X wrapper is created every function call.
#
# Reality:
#
# repeat() -> once
# decorator() -> once
# wrapper() -> every invocation

# ============================================================
# INTERVIEW NOTES
# ============================================================

# Q. Why can't two nested functions solve this?
#
# Because decorator configuration,
# decoration,
# and execution
# happen at different times.

# ============================================================
# BRIDGE
# ============================================================

# Today:
# One decorator
#
# Next:
# Multiple decorators.
#
# What happens if we write:
#
# @A
# @B
# @C
#
# Which executes first?
#
# That is the next mystery.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Parameterized decorators extend ordinary decorators.
# ✓ Three different moments require three functions.
# ✓ Layer 1 stores configuration.
# ✓ Layer 2 receives the function.
# ✓ Layer 3 executes during function calls.
# ✓ The wrapper remembers both func and configuration through closures.
