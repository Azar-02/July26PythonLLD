"""
============================================================
CONCURRENCY-1
FILE : 04_cpu_bound_threading_surprise.py
============================================================

Topics Covered
--------------
1. Motivation
2. Waiting Work vs Real Work
3. CPU-Heavy Tasks
4. Sequential Benchmark
5. Threaded Benchmark
6. The Unexpected Result
7. Why Everyone Guesses Wrong
8. The Central Question
9. Preparing for the GIL
10. Interview Questions
11. Key Takeaways

"""

import threading
import time

# ============================================================
# MOTIVATION
# ============================================================

# So far we have seen examples using:
#
# time.sleep()
#
# Example:
#
# - Waiting for network
# - Waiting for database
# - Waiting for API response
#
# These are waiting tasks.
#
# But what about actual computation?
#
# Can threads speed up
# heavy calculations?

# ============================================================
# CPU-BOUND WORK
# ============================================================

# CPU-bound work means:
#
# The CPU spends most of its time
# performing calculations.
#
# Examples:
#
# - Image processing
# - Video encoding
# - Mathematical computation
# - Machine Learning inference
# - Data analysis

# Observation:
#
# The CPU is busy continuously.
#
# There is very little waiting.

# ============================================================
# A CPU-HEAVY FUNCTION
# ============================================================

def cpu_heavy(n):

    return sum(
        i * i
        for i in range(n)
    )

# Observation:
#
# This function performs
# a large amount of computation.
#
# The larger n becomes,
# the longer execution takes.

# ============================================================
# SEQUENTIAL EXECUTION
# ============================================================

# Running the function twice
# one after another.

start = time.perf_counter()

cpu_heavy(5_000_000)
cpu_heavy(5_000_000)

sequential_time = (
    time.perf_counter() - start
)

print(
    f"Sequential: "
    f"{sequential_time:.2f}s"
)

# Observation:
#
# Total time:
#
# Work A + Work B

# ============================================================
# THE NATURAL GUESS
# ============================================================

# Most developers guess:
#
# Two threads
#
# should be faster.
#
# Reasoning:
#
# Thread A handles Task A.
#
# Thread B handles Task B.
#
# Therefore:
#
# Both should run together.
#
# Maybe close to:
#
# Half the execution time.

# ============================================================
# THREADED EXECUTION
# ============================================================

start = time.perf_counter()

t1 = threading.Thread(
    target=cpu_heavy,
    args=(5_000_000,)
)

t2 = threading.Thread(
    target=cpu_heavy,
    args=(5_000_000,)
)

t1.start()
t2.start()

t1.join()
t2.join()

threaded_time = (
    time.perf_counter() - start
)

print(
    f"Threaded: "
    f"{threaded_time:.2f}s"
)

# ============================================================
# THE SURPRISE
# ============================================================

# Expected:
#
# Sequential : 4.0s
# Threaded   : 2.0s
#
# Actual:
#
# Sequential : ~4.0s
# Threaded   : ~4.1s
#
# Numbers vary by machine.
#
# But the pattern remains:
#
# Threaded execution is often
# very close to sequential.

# Sometimes:
#
# Threaded execution is
# slightly slower.

# ============================================================
# WHY IS THIS SHOCKING?
# ============================================================

# We have:
#
# - Multiple threads
# - Multiple CPU cores
# - Heavy work
#
# Yet:
#
# No meaningful speedup.

# This feels wrong.
#
# Many developers expect
# threading to automatically
# improve performance.

# ============================================================
# WHAT WE LEARNED
# ============================================================

# Observation:
#
# Creating more threads
# does not automatically
# create more speed.
#
# Especially for:
#
# CPU-heavy tasks.

# ============================================================
# THE BIG QUESTION
# ============================================================

# If:
#
# - Multiple threads exist
# - Multiple cores exist
#
# Then:
#
# Why are both calculations
# not running simultaneously?

# Something is preventing
# Python threads from fully
# utilizing available CPU cores.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# The problem is NOT:
#
# - Thread creation
# - start()
# - join()
#
# The problem is deeper.
#
# It exists inside
# the Python interpreter.

# ============================================================
# THE HIDDEN RULE
# ============================================================

# Python has a mechanism
# that controls how threads
# execute Python code.
#
# This mechanism is called:
#
# GIL
#
# Global Interpreter Lock

# ============================================================
# WHY THIS SECTION MATTERS
# ============================================================

# Without understanding
# this benchmark:
#
# The GIL feels unnecessary.
#
# After seeing this benchmark:
#
# We have a real problem
# that needs explanation.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# More threads always means
# more speed.
#
# Correct:
#
# Depends on the workload.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# CPU-bound work automatically
# benefits from threading.
#
# Correct:
#
# Python threads often fail
# to speed up CPU-bound work.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Two CPU-heavy calculations
# run using two Python threads.
#
# Why might execution time be
# almost identical to sequential
# execution?
#
# Answer:
#
# Because of the GIL.
#
# Only one thread can execute
# Python bytecode at a time.

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now know:
#
# Threading does not always
# improve performance.
#
# The next question becomes:
#
# What exactly is the GIL?
#
# Why does it exist?
#
# What problem does it solve?

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# CPU-bound work:
#
# Heavy computation.
#
# Examples:
#
# Image processing
# Data analysis
# Mathematical calculations

# Sequential execution:
#
# Work runs one after another.

# Threaded execution:
#
# May provide little or
# no speedup for CPU work.

# Multiple threads:
#
# Does not guarantee
# multiple calculations
# run simultaneously.

# This leads directly to:
#
# The GIL.
