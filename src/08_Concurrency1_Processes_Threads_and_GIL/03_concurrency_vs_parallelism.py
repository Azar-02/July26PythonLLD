"""
============================================================
CONCURRENCY-1
FILE : 03_concurrency_vs_parallelism.py
============================================================

Topics Covered
--------------
1. Motivation
2. Why This Distinction Matters
3. What is Concurrency?
4. What is Parallelism?
5. Support Agent Analogy
6. Single-Core Systems
7. Multi-Core Systems
8. Concurrency vs Parallelism
9. Common Misconceptions
10. Interview Questions
11. Key Takeaways

"""

# ============================================================
# MOTIVATION
# ============================================================

# Many developers use the terms:
#
# Concurrency
#
# and
#
# Parallelism
#
# interchangeably.
#
# However:
#
# They are not the same thing.
#
# Understanding the difference
# is essential before studying:
#
# - Threading
# - Multiprocessing
# - Async Programming

# ============================================================
# THE BIG QUESTION
# ============================================================

# What does it mean for a computer
# to do multiple things together?
#
# There are two possibilities:
#
# 1. Switching between tasks quickly
#
# 2. Actually executing tasks
#    at the same instant

# ============================================================
# SUPPORT AGENT ANALOGY
# ============================================================

# Imagine a support agent
# handling three chat tickets.
#
# Ticket A
# Ticket B
# Ticket C
#
# The agent:
#
# - Replies to A
# - Switches to B
# - Switches to C
# - Returns to A
#
# Progress is happening on
# all three tickets.
#
# But:
#
# The agent is still one person.

# ============================================================
# WHAT IS CONCURRENCY?
# ============================================================

# Definition:
#
# Concurrency means making
# progress on multiple tasks
# by switching between them.
#
# Important:
#
# Multiple tasks may appear
# to run together.
#
# But they are not necessarily
# executing at the exact same moment.

# Observation:
#
# Concurrency is about
# organizing work.

# ============================================================
# CONCURRENCY VISUALIZATION
# ============================================================

# Timeline
#
# Time --->
#
# Task A
# [Run]      [Run]
#
# Task B
#       [Run]
#
# Task C
#             [Run]
#
# One worker.
#
# Multiple tasks.
#
# Rapid switching.

# ============================================================
# PARALLELISM ANALOGY
# ============================================================

# Now imagine:
#
# Three support agents.
#
# Agent 1 -> Ticket A
# Agent 2 -> Ticket B
# Agent 3 -> Ticket C
#
# All three agents work
# at the same time.

# ============================================================
# WHAT IS PARALLELISM?
# ============================================================

# Definition:
#
# Parallelism means
# multiple tasks execute
# simultaneously.
#
# Work is genuinely happening
# at the same instant.

# Observation:
#
# Parallelism requires
# multiple workers.
#
# Example:
#
# Multiple CPU cores.

# ============================================================
# PARALLELISM VISUALIZATION
# ============================================================

# Timeline
#
# Time --->
#
# Task A
# [Run][Run][Run]
#
# Task B
# [Run][Run][Run]
#
# Task C
# [Run][Run][Run]
#
# All tasks progressing
# simultaneously.

# ============================================================
# SINGLE-CORE MACHINE
# ============================================================

# Suppose a machine has:
#
# One CPU Core
#
# Can it execute two instructions
# at the exact same instant?
#
# No.
#
# Therefore:
#
# True parallel execution
# is impossible.

# However:
#
# It can switch between tasks
# very quickly.
#
# Therefore:
#
# Concurrency is still possible.

# ============================================================
# MULTI-CORE MACHINE
# ============================================================

# Suppose a machine has:
#
# Four CPU Cores
#
# Core 1 -> Task A
# Core 2 -> Task B
# Core 3 -> Task C
# Core 4 -> Task D
#
# Now tasks can execute
# simultaneously.

# Therefore:
#
# Parallelism becomes possible.

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# Concurrency does NOT
# automatically mean parallelism.
#
# Example:
#
# One worker
# handling multiple tasks.
#
# Concurrency exists.
#
# Parallelism does not.

# ============================================================
# ANOTHER OBSERVATION
# ============================================================

# Parallelism almost always
# includes concurrency.
#
# Because:
#
# Multiple tasks are being
# worked on together.

# ============================================================
# THREADING AND THESE CONCEPTS
# ============================================================

# Python's threading module
# definitely provides:
#
# Concurrency
#
# Whether it also provides:
#
# Parallelism
#
# depends on the type of work
# being performed.
#
# This leads directly to
# the GIL discussion.

# ============================================================
# REAL-WORLD EXAMPLES
# ============================================================

# Example 1:
#
# Downloading files.
#
# While one request waits,
# another request can progress.
#
# Concurrency.

# Example 2:
#
# Image processing on
# multiple CPU cores.
#
# Parallelism.

# Example 3:
#
# Web server handling
# thousands of requests.
#
# Primarily concurrency.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# Concurrency and Parallelism
# are identical.
#
# Correct:
#
# They solve different problems.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# More threads always means
# more parallel execution.
#
# Correct:
#
# Depends on runtime,
# hardware,
# and workload.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Difference between
# Concurrency and Parallelism?
#
# Concurrency:
#
# Managing multiple tasks
# by switching between them.
#
# Parallelism:
#
# Executing multiple tasks
# simultaneously.

# ============================================================
# QUICK MEMORY TRICK
# ============================================================

# Concurrency:
#
# One worker
# many tasks.
#
# Parallelism:
#
# Many workers
# many tasks.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Concurrency:
#
# Progress on multiple tasks.
#
# Usually achieved through
# task switching.

# Parallelism:
#
# Simultaneous execution.
#
# Requires multiple workers.

# Single-Core Machine:
#
# Concurrency possible.
#
# Parallelism not possible.

# Multi-Core Machine:
#
# Concurrency possible.
#
# Parallelism possible.

# Concurrency:
#
# About organizing work.
#
# Parallelism:
#
# About increasing execution power.

# Python threading:
#
# Always provides concurrency.
#
# Parallelism depends on
# the workload and runtime.
