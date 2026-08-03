"""
============================================================
CONCURRENCY-1
FILE : 05_understanding_the_gil_part1.py
============================================================

Topics Covered
--------------
1. Motivation
2. The Talking Stick Analogy
3. What is the GIL?
4. One Thread at a Time
5. Why the GIL Exists
6. Reference Counting
7. Memory Corruption Problem
8. Lost Update Example
9. What the GIL Protects
10. Common Misconceptions
11. Interview Questions
12. Key Takeaways

"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we saw:
#
# Sequential  : ~4.0s
# Threaded    : ~4.1s
#
# Exact numbers do not matter.
#
# The important observation:
#
# Threaded ≈ Sequential
#
# The natural question becomes:
#
# Why can't multiple Python threads
# fully utilize multiple CPU cores?

# ============================================================
# THE TALKING STICK ANALOGY
# ============================================================

# Imagine a meeting.
#
# Only the person holding a
# talking stick is allowed
# to speak.
#
# Everyone else must wait.
#
# Even if:
#
# - They are ready
# - They know the answer
# - They want to speak
#
# Only one person may speak
# at a time.

# ============================================================
# APPLYING THE ANALOGY
# ============================================================

# Imagine:
#
# Thread A
# Thread B
# Thread C
#
# All are ready to run.
#
# However:
#
# Only the thread holding
# the talking stick can
# execute Python code.

# Observation:
#
# Multiple threads may exist.
#
# But only one can execute
# Python code at a given moment.

# ============================================================
# WHAT IS THE GIL?
# ============================================================

# GIL =
#
# Global Interpreter Lock

# Definition:
#
# A lock inside CPython that allows
# only one thread to execute Python
# bytecode at a time.

# Important:
#
# CPython is the standard Python
# interpreter used by most developers.

# ============================================================
# ONE THREAD AT A TIME
# ============================================================

# Visualization
#
# Tick --->
#
# 1   2   3   4   5
#
# A  RUN
# B      RUN
# C          RUN
# A              RUN
#
# Observation:
#
# At every instant,
# exactly one thread
# owns the GIL.

# ============================================================
# WHY DOES THE GIL EXIST?
# ============================================================

# Many developers ask:
#
# Why not simply remove it?
#
# The answer involves
# Python's memory management.

# Python performs a huge amount
# of bookkeeping internally.
#
# One important mechanism is:
#
# Reference Counting.

# ============================================================
# WHAT IS REFERENCE COUNTING?
# ============================================================

# Example:

some_list = [1, 2, 3]

another_name = some_list

del another_name

# Conceptually:
#
# some_list      -> count becomes 1
#
# another_name   -> count becomes 2
#
# del            -> count becomes 1

# Observation:
#
# Python continuously tracks
# how many references point
# to an object.

# ============================================================
# THE DANGER
# ============================================================

# Suppose:
#
# Object count = 2
#
# Two threads try to update
# the count simultaneously.

# Thread A:
#
# Reads 2

# Thread B:
#
# Reads 2

# Thread A:
#
# Writes 1

# Thread B:
#
# Writes 1

# Expected:
#
# 2 -> 1 -> 0

# Actual:
#
# 2 -> 1

# One update is lost.

# ============================================================
# WHY IS THIS BAD?
# ============================================================

# Incorrect bookkeeping may cause:
#
# - Memory leaks
# - Corrupted state
# - Crashes
# - Hard-to-reproduce bugs

# Python needs a mechanism
# to prevent its internal
# memory structures from
# becoming corrupted.

# ============================================================
# HOW THE GIL HELPS
# ============================================================

# The GIL ensures:
#
# Only one thread can execute
# Python bytecode at a time.
#
# Therefore:
#
# Internal bookkeeping operations
# are protected from simultaneous
# modification.

# Observation:
#
# The GIL primarily exists to
# protect Python's interpreter
# internals.

# ============================================================
# WHAT THE GIL PROTECTS
# ============================================================

# GIL protects:
#
# - Internal interpreter state
# - Reference counting
# - Memory management operations

# It reduces the chance of
# corruption inside Python itself.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Many beginners assume:
#
# "If the GIL exists,
# my variables are safe."
#
# This is incorrect.

# The GIL protects Python's
# internal structures.
#
# It does NOT automatically make
# your application data safe.

# This topic is explored in
# the next file.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# GIL exists to make
# programs faster.
#
# Correct:
#
# GIL exists primarily to make
# interpreter internals safer.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# Multiple threads can always
# execute Python code together.
#
# Correct:
#
# Only one thread executes
# Python bytecode at a time.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What is the GIL?
#
# The Global Interpreter Lock.
#
# A lock in CPython that allows
# only one thread to execute
# Python bytecode at a time.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# GIL:
#
# Global Interpreter Lock.

# Only one thread executes
# Python bytecode at a time.

# Talking Stick Analogy:
#
# One stick.
#
# One speaker.

# Reference Counting:
#
# Tracks references to objects.

# GIL helps protect:
#
# - Reference counting
# - Memory management
# - Interpreter internals

# GIL exists for correctness,
# not for performance.

# Next:
#
# Why counter += 1 can still fail
# even when the GIL exists.
