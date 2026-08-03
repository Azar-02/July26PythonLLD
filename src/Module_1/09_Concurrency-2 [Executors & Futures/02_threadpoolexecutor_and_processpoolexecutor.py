"""
============================================================
CONCURRENCY-2
FILE : 02_threadpoolexecutor_and_processpoolexecutor.py
============================================================

Topics Covered
--------------
1. Motivation
2. What Is An Executor?
3. Worker Pool Concept
4. ThreadPoolExecutor
5. ProcessPoolExecutor
6. Same Interface, Different Engine
7. Worker Queues
8. Scheduling Jobs
9. Common Misconceptions
10. Interview Questions
11. Key Takeaways

"""

from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor
)
import time

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we discovered:
#
# Raw threads are not the problem.
#
# Managing work is the problem.
#
# We struggled with:
#
# - Return values
# - Exceptions
# - Tracking workers
#
# The natural question becomes:
#
# What tool does Python provide
# to simplify all of this?

# ============================================================
# INTRODUCING EXECUTORS
# ============================================================

# An Executor is a manager.
#
# Instead of creating workers
# one by one:
#
# Thread(...)
# Thread(...)
# Thread(...)
#
# We create a pool.
#
# Then submit jobs to it.

# ============================================================
# ANALOGY
# ============================================================

# Imagine a company.
#
# Without an Executor:
#
# You personally hire workers.
# You assign every task.
# You track every worker.
#
# Lots of manual effort.
#
# With an Executor:
#
# A manager already exists.
#
# You hand work to the manager.
#
# The manager handles workers.

# ============================================================
# THE FIRST EXECUTOR
# ============================================================

executor = ThreadPoolExecutor(
    max_workers=3
)

# Observation:
#
# We did not create:
#
# Thread 1
# Thread 2
# Thread 3
#
# manually.
#
# The Executor created and
# manages them.

executor.shutdown()

# ============================================================
# ASK LEARNERS
# ============================================================

# If max_workers=3
#
# and we submit:
#
# 100 jobs
#
# how many can execute
# immediately?

# ============================================================
# ANSWER
# ============================================================

# Only:
#
# 3 jobs.
#
# Because:
#
# Only 3 workers exist.
#
# Remaining jobs wait.

# ============================================================
# WHAT IS A WORKER POOL?
# ============================================================

# Think of:
#
# ThreadPoolExecutor(max_workers=3)
#
# as:
#
# Worker 1
# Worker 2
# Worker 3
#
# sitting idle and waiting.

# ============================================================
# VISUALIZATION
# ============================================================

# Initial State:
#
# Worker 1 -> idle
# Worker 2 -> idle
# Worker 3 -> idle

# ============================================================
# JOB ARRIVAL
# ============================================================

# Suppose:
#
# Job A
# Job B
# Job C
# Job D
# Job E
#
# arrive.

# ============================================================
# WHAT HAPPENS?
# ============================================================

# Worker 1 -> Job A
# Worker 2 -> Job B
# Worker 3 -> Job C
#
# Waiting:
#
# Job D
# Job E

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# We never create the queue.
#
# We never manage the queue.
#
# The Executor handles it.

# ============================================================
# ASK LEARNERS
# ============================================================

# Does Job D start immediately?
#
# No.
#
# It must wait until
# a worker becomes available.

# ============================================================
# WHEN A WORKER FINISHES
# ============================================================

# Suppose:
#
# Worker 1 finishes Job A.
#
# Immediately:
#
# Worker 1 picks Job D.

# ============================================================
# OBSERVATION
# ============================================================

# This feels very similar to:
#
# FixedThreadPool in Java.
#
# Limited workers.
#
# Many tasks.
#
# Waiting queue.

# ============================================================
# THREADPOOLEXECUTOR
# ============================================================

# ThreadPoolExecutor:
#
# Uses threads internally.
#
# Best for:
#
# I/O-bound work.

# ============================================================
# EXAMPLES
# ============================================================

# API calls
# Database queries
# File operations
# Network requests

# ============================================================
# WHY THREADS?
# ============================================================

# During waiting:
#
# Threads release the CPU.
#
# Other workers can run.

# ============================================================
# PROCESSPOOLEXECUTOR
# ============================================================

# ProcessPoolExecutor:
#
# Uses processes internally.
#
# Best for:
#
# CPU-bound work.

# ============================================================
# EXAMPLE
# ============================================================

# Image processing
# Video encoding
# Mathematical computation
# Large data analysis

# ============================================================
# WHY PROCESSES?
# ============================================================

# Each process has:
#
# Own memory
# Own interpreter
# Own GIL
#
# Therefore:
#
# Multiple CPU cores can
# truly work simultaneously.

# ============================================================
# THE BIG IDEA
# ============================================================

# The most important idea
# of today's lecture:
#
# Same API
#
# Different engine.

# ============================================================
# THREADPOOL VERSION
# ============================================================

thread_executor = ThreadPoolExecutor(
    max_workers=5
)

thread_executor.shutdown()

# ============================================================
# PROCESSPOOL VERSION
# ============================================================
#
process_executor = ProcessPoolExecutor(
        max_workers=5
    )

process_executor.shutdown()

# ============================================================
# ASK LEARNERS
# ============================================================

# Compare:
#
# ThreadPoolExecutor
#
# and
#
# ProcessPoolExecutor
#
# How much code changed?

# ============================================================
# OBSERVATION
# ============================================================

# Almost nothing.
#
# The class name changed.
#
# That is the major design goal.

# ============================================================
# WHY THIS IS POWERFUL
# ============================================================

# In Lecture 8:
#
# We learned:
#
# Threads -> I/O-bound
# Processes -> CPU-bound
#
# Executors let us apply
# the same rule with
# nearly identical code.

# ============================================================
# PREDICTION EXERCISE
# ============================================================

# Suppose:
#
# We write code using:
#
# ThreadPoolExecutor
#
# for a web scraper.
#
# Then replace:
#
# ThreadPoolExecutor
#
# with:
#
# ProcessPoolExecutor
#
# What changes?
#
# Keep this question in mind.
#
# The lecture will answer it later.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Executors do not decide
# whether your workload is
# CPU-bound or I/O-bound.
#
# You must make that decision.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# ProcessPoolExecutor
# is always faster.
#
# Correct:
#
# Depends on workload.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# More workers always means
# more speed.
#
# Correct:
#
# Sometimes extra workers
# add overhead.

# ============================================================
# COMMON MISCONCEPTION #3
# ============================================================

# Wrong:
#
# Executors eliminate the need
# to understand concurrency.
#
# Correct:
#
# Executors are built on top
# of concurrency concepts.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What is an Executor?
#
# Answer:
#
# A higher-level abstraction
# that manages a pool of workers.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# When should you use:
#
# ThreadPoolExecutor?
#
# Answer:
#
# I/O-bound work.

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# When should you use:
#
# ProcessPoolExecutor?
#
# Answer:
#
# CPU-bound work.

# ============================================================
# INTERVIEW QUESTION #4
# ============================================================

# What is the major design
# benefit of both executors?
#
# Answer:
#
# Same interface.
#
# Different implementation.

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now know:
#
# What an Executor is.
#
# What a worker pool is.
#
# The difference between:
#
# ThreadPoolExecutor
# ProcessPoolExecutor
#
# Next question:
#
# How do we actually submit
# work to these pools?
#
# That introduces:
#
# submit()
# Future

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Executor = manager of workers.
#
# Worker pool = reusable workers.
#
# ThreadPoolExecutor:
#
# Best for I/O-bound work.
#
# ProcessPoolExecutor:
#
# Best for CPU-bound work.
#
# Same API.
#
# Different engine.
#
# Next:
#
# submit()
# Future
