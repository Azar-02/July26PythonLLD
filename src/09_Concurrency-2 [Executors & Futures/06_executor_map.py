"""
============================================================
CONCURRENCY-2
FILE : 06_executor_map.py
============================================================

Topics Covered
--------------
1. Motivation
2. The submit() Repetition Problem
3. Why map() Exists
4. Basic map() Usage
5. Internal Worker Distribution
6. Ordering Guarantees
7. map() vs submit()
8. When To Use Each
9. Common Mistakes
10. Interview Questions
11. Key Takeaways

Based on Concurrency-2 Lecture Notes.
"""

from concurrent.futures import ThreadPoolExecutor
import time

# ============================================================
# MOTIVATION
# ============================================================

# So far we have learned:
#
# submit()
# Future
# done()
# result()
# Exception Handling
#
# Everything works.
#
# But a new problem appears.

# ============================================================
# THE SUBMIT REPETITION PROBLEM
# ============================================================

# Imagine:
#
# 5 tasks.
#
# Easy.
#
# We can write:
#
# submit()
# submit()
# submit()
# submit()
# submit()

# ============================================================
# ASK LEARNERS
# ============================================================

# What if we have:
#
# 100 tasks?
#
# 1,000 tasks?
#
# 100,000 tasks?
#
# Are we really going to write:
#
# submit()
# submit()
# submit()
# ...
#
# forever?

# ============================================================
# EXAMPLE PROBLEM
# ============================================================

def fetch_user(user_id):

    time.sleep(1)

    return f"User-{user_id}"

user_ids = [
    101,
    102,
    103,
    104,
    105
]

# ============================================================
# SUBMIT VERSION
# ============================================================

with ThreadPoolExecutor(
    max_workers=3
) as executor:

    future1 = executor.submit(
        fetch_user,
        101
    )

    future2 = executor.submit(
        fetch_user,
        102
    )

    future3 = executor.submit(
        fetch_user,
        103
    )

# ============================================================
# OBSERVATION
# ============================================================

# This is manageable.
#
# But imagine:
#
# 500 user IDs.
#
# This quickly becomes repetitive.

# ============================================================
# IMPORTANT QUESTION
# ============================================================

# We already know Python has:
#
# map()
#
# for normal functions.
#
# Can Executors provide
# something similar?

# ============================================================
# INTRODUCING executor.map()
# ============================================================

# Answer:
#
# Yes.
#
# Executors provide:
#
# executor.map()

# ============================================================
# BASIC EXAMPLE
# ============================================================

with ThreadPoolExecutor(
    max_workers=3
) as executor:

    results = executor.map(
        fetch_user,
        user_ids
    )

# ============================================================
# ASK LEARNERS
# ============================================================

# What happened here?
#
# Did we create:
#
# 5 workers?
#
# No.

# ============================================================
# OBSERVATION
# ============================================================

# We still have:
#
# max_workers=3
#
# Only three workers exist.
#
# Five tasks exist.

# ============================================================
# INTERNAL VISUALIZATION
# ============================================================

# Workers:
#
# Worker 1
# Worker 2
# Worker 3
#
# Tasks:
#
# 101
# 102
# 103
# 104
# 105

# ============================================================
# DISTRIBUTION
# ============================================================

# Initial Assignment:
#
# Worker 1 -> 101
# Worker 2 -> 102
# Worker 3 -> 103
#
# Waiting:
#
# 104
# 105

# ============================================================
# WHAT HAPPENS NEXT?
# ============================================================

# Suppose:
#
# Worker 2 finishes first.
#
# Immediately:
#
# Worker 2 -> 104

# ============================================================

# Suppose:
#
# Worker 1 finishes next.
#
# Immediately:
#
# Worker 1 -> 105

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# map() does NOT create
# one worker per task.
#
# map() distributes tasks
# among available workers.

# ============================================================
# ANALOGY
# ============================================================

# Imagine:
#
# Three cashiers.
#
# Five customers.
#
# Customers are not assigned
# permanent cashiers.
#
# Available cashier takes
# the next customer.

# ============================================================
# ============================================================

# What does executor.map()
# return?
#
# Think carefully.

# ============================================================
# ANSWER
# ============================================================

# It returns an iterable
# of results.

# ============================================================
# EXAMPLE
# ============================================================

with ThreadPoolExecutor(
    max_workers=3
) as executor:

    results = executor.map(
        fetch_user,
        user_ids
    )

    for result in results:

        print(result)

# ============================================================
# OBSERVATION
# ============================================================

# Output:
#
# User-101
# User-102
# User-103
# User-104
# User-105

# ============================================================
# VERY IMPORTANT QUESTION
# ============================================================

# Is that the completion order?
#
# Not necessarily.

# ============================================================
# THE ORDERING GUARANTEE
# ============================================================

# This is one of the most
# important facts about map().
#
# Results are returned in:
#
# Input Order

# ============================================================
# INPUT
# ============================================================

# [101, 102, 103, 104, 105]

# ============================================================
# OUTPUT
# ============================================================

# User-101
# User-102
# User-103
# User-104
# User-105

# ============================================================
# EVEN IF...
# ============================================================

# Worker handling:
#
# 104
#
# finishes before:
#
# 102
#
# map() still preserves
# input ordering.

# ============================================================
# ASK LEARNERS
# ============================================================

# Why might this be useful?

# ============================================================
# OBSERVATION
# ============================================================

# Many business workflows
# depend on positional matching.
#
# Input 1
# should correspond to
# Output 1.

# ============================================================
# map() VS submit()
# ============================================================

# submit():
#
# More flexible
#
# Individual Futures
#
# Individual control

# ============================================================

# map():
#
# Cleaner for batch processing
#
# Less boilerplate

# ============================================================
# WHEN TO USE map()
# ============================================================

# Same function
#
# Applied to:
#
# Many inputs

# ============================================================
# EXAMPLES
# ============================================================

# Download 100 URLs
#
# Process 100 images
#
# Validate 100 users
#
# Fetch 100 products

# ============================================================
# WHEN TO USE submit()
# ============================================================

# Different tasks
#
# Different workflows
#
# Individual Future control

# ============================================================
# EXAMPLE
# ============================================================

# Task A:
# Download File
#
# Task B:
# Generate Report
#
# Task C:
# Send Email
#
# submit() is often better.

# ============================================================
# PREDICTION EXERCISE
# ============================================================

# Suppose:
#
# Same task
#
# 10,000 inputs
#
# Which feels cleaner?
#
# submit()
#
# or
#
# map()

# ============================================================
# ANSWER
# ============================================================

# Usually:
#
# map()

# ============================================================
# COMMON MISTAKE #1
# ============================================================

# Wrong:
#
# map() creates one worker
# per input.
#
# Correct:
#
# Tasks share workers.

# ============================================================
# COMMON MISTAKE #2
# ============================================================

# Wrong:
#
# Output order equals
# completion order.
#
# Correct:
#
# Output order equals
# input order.

# ============================================================
# COMMON MISTAKE #3
# ============================================================

# Wrong:
#
# map() replaces submit()
#
# Correct:
#
# Both have different use cases.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why was map() introduced?
#
# Answer:
#
# To simplify batch task submission.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# What does map() return?
#
# Answer:
#
# Iterable of results.

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Does map() preserve ordering?
#
# Answer:
#
# Yes.
#
# Input order.

# ============================================================
# INTERVIEW QUESTION #4
# ============================================================

# When is map() preferred?
#
# Answer:
#
# Same function
# Many inputs

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now know:
#
# submit()
# Future
# map()
#
# Next:
#
# Real-world application.
#
# A web scraper.
#
# Sequential version
# vs
# ThreadPoolExecutor version.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# map() simplifies bulk work.
#
# Tasks are distributed across
# available workers.
#
# map() preserves input order.
#
# submit() offers more control.
#
# map() reduces boilerplate.
#
# Next:
#
# I/O-bound Web Scraper Lab
