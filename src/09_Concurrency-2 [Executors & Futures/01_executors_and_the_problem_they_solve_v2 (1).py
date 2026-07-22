"""
============================================================
CONCURRENCY-2
FILE : 01_executors_and_the_problem_they_solve_v2.py
============================================================

Topics Covered
--------------
1. Motivation
2. Lecture 8 Recap
3. The Return Value Problem
4. Shared List Workaround
5. Silent Exceptions
6. Why Raw Threads Become Painful
7. Scaling Problems
8. Why Executors Exist
9. Common Misconceptions
10. Interview Questions
11. Key Takeaways

Based on Concurrency-2 Lecture Notes.
"""

import threading
import time

# ============================================================
# MOTIVATION
# ============================================================

# Last lecture was about:
#
# Thread
# Process
# start()
# join()
#
# We learned how concurrency works.
#
# We learned:
#
# - CPU-bound work
# - I/O-bound work
# - GIL
# - Multiprocessing
#
# Everything seemed complete.
#
# But today begins with an uncomfortable question:
#
# If we already know threads and processes,
# why do we need Executors?

# ============================================================
# ASK LEARNERS
# ============================================================

# Imagine:
#
# You create:
#
# 5 threads
#
# and everything works.
#
# Tomorrow:
#
# Your manager asks for:
#
# 500 concurrent tasks.
#
# Which part becomes difficult?
#
# A) Creating workers
# B) Managing workers
#
# Think before continuing.

# ============================================================
# RECAP OF LECTURE 8
# ============================================================

# We manually created:
#
# threading.Thread(...)
#
# and:
#
# multiprocessing.Process(...)
#
# We manually called:
#
# start()
# join()
#
# We manually managed workers.

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# Creating workers was not
# particularly difficult.
#
# The difficulty appeared later:
#
# Collecting results
# Handling failures
# Managing many workers

# ============================================================
# SIMPLE DRIVER EXAMPLE
# ============================================================

def fetch_driver_location(driver_id):

    time.sleep(1)

    return f"Location for {driver_id}"

drivers = [
    "D101",
    "D102",
    "D103",
    "D104",
    "D105"
]

# ============================================================
# THE FIRST PAIN
# ============================================================

# Suppose we need:
#
# [
#   "Location for D101",
#   "Location for D102",
#   ...
# ]
#
# after all workers finish.
#
# Question:
#
# How do we get the values back?

# ============================================================
# NATURAL EXPECTATION
# ============================================================

# Normally:
#
# result = function()
#
# gives us a return value.
#
# Humans naturally expect:
#
# Work
# ↓
# Result
#
# But threads feel different.

# ============================================================
# SHARED LIST WORKAROUND
# ============================================================

results = []

def fetch_and_store(driver_id):

    location = fetch_driver_location(
        driver_id
    )

    results.append(location)

threads = [
    threading.Thread(
        target=fetch_and_store,
        args=(d,)
    )
    for d in drivers
]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Results:", results)


# What did we build
# just to get answers back?
#
# Answer:
#
# A shared list.

# ============================================================
# OBSERVATION
# ============================================================

# The worker computed a value.
#
# But it did not naturally
# return that value to us.
#
# Instead:
#
# We created:
#
# results = []
#
# and every worker manually
# inserted data into it.

# ============================================================
# WHY THIS FEELS AWKWARD
# ============================================================

# Imagine:
#
# 5 workers
#
# Not bad.
#
# Imagine:
#
# 500 workers.
#
# Still building custom
# result collection logic?
#
# That does not scale well.

# ============================================================
# SCALING THE PROBLEM
# ============================================================

#
# What if we need:
#
# Locations
# Driver ratings
# Driver earnings
# Driver status
#
# simultaneously?
#
# Soon we may create:
#
# Multiple shared lists.
#
# Multiple queues.
#
# Multiple coordination rules.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Creating threads is easy.
#
# Managing results becomes harder.

# ============================================================
# THE SECOND PAIN
# ============================================================

# What happens when
# a worker fails?

# ============================================================
# FAILURE EXAMPLE
# ============================================================

def broken_fetch_driver_location(driver_id):

    if driver_id == "D103":

        raise ConnectionError(
            "Driver app unreachable"
        )

    return f"Location for {driver_id}"

# ============================================================
# RAW THREAD VERSION
# ============================================================

# Uncomment to test:
#
# t = threading.Thread(
#     target=broken_fetch_driver_location,
#     args=("D103",)
# )
#
# t.start()
# t.join()
#
# print("Main thread finished")

# ============================================================
# ASK LEARNERS
# ============================================================

# Predict:
#
# Does the main thread crash?
#
# Does execution stop?
#
# What happens?

# ============================================================
# OBSERVATION
# ============================================================

# Usually:
#
# Python prints a traceback.
#
# Then:
#
# Main thread continues.
#
# The failure happened inside
# the worker thread.

# ============================================================
# WHY THIS IS A PROBLEM
# ============================================================

# Imagine:
#
# Payment processing failed.
#
# Inventory update failed.
#
# Notification sending failed.
#
# If the main program never
# notices:
#
# Business state can become wrong.

# ============================================================
# SILENT EXCEPTIONS FEEL DANGEROUS
# ============================================================
#
# Which is worse?
#
# A) Program crashes loudly.
#
# B) Program silently ignores
#    an important failure.
#
# In many systems:
#
# B is actually more dangerous.

# ============================================================
# THE REAL PAIN
# ============================================================

# Threads are not the problem.
#
# Processes are not the problem.
#
# The problem is:
#
# Managing work.

# ============================================================
# WHAT DOES MANAGING WORK MEAN?
# ============================================================

# We care about:
#
# Has work started?
#
# Has work finished?
#
# Did work succeed?
#
# Did work fail?
#
# What value was produced?
#
# These questions become
# more important than the
# worker itself.

# ============================================================
# ANALOGY
# ============================================================

# Imagine a manager.
#
# Raw Thread approach:
#
# Hire workers yourself.
# Track workers yourself.
# Collect reports yourself.
# Investigate failures yourself.
#
# Lots of manual work.

# ============================================================
# BETTER ANALOGY
# ============================================================

# Imagine a restaurant.
#
# Raw Threads:
#
# You personally coordinate
# every waiter.
#
# Every chef.
#
# Every order.
#
# Every problem.
#
# This becomes exhausting.

# ============================================================
# THE CENTRAL QUESTION
# ============================================================

# Can Python provide:
#
# A manager?
#
# Something that tracks:
#
# Results
# Exceptions
# Completion
#
# automatically?

# ============================================================
# THE IDEA BEHIND EXECUTORS
# ============================================================

# Instead of:
#
# Create Thread
# Start Thread
# Join Thread
# Build Result Storage
# Handle Exceptions
#
# What if one object handled
# all of that?

# ============================================================
# EXECUTORS
# ============================================================

# Executors are a higher-level
# abstraction.
#
# They sit above:
#
# Threads
# Processes
#
# and provide a cleaner API.

# ============================================================
# WHAT EXECUTORS SOLVE
# ============================================================

# Executors help with:
#
# Worker pools
# Result collection
# Exception handling
# Task tracking
#
# These are exactly the pains
# discovered earlier.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Executors do not replace
# concurrency.
#
# Executors use concurrency.
#
# They simply make it easier
# to manage.

# ============================================================
# WHY THIS MATTERS
# ============================================================

# Real systems rarely run:
#
# 2 tasks
#
# or:
#
# 3 tasks.
#
# Real systems may run:
#
# Hundreds
# Thousands
# Millions
#
# of operations over time.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# Executors are faster.
#
# Correct:
#
# Executors are usually
# more convenient.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# Executors eliminate bugs.
#
# Correct:
#
# Shared-state bugs can still exist.

# ============================================================
# COMMON MISCONCEPTION #3
# ============================================================

# Wrong:
#
# Creating workers is hard.
#
# Correct:
#
# Managing workers is harder.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Before Executors,
# what two major problems
# did we face?
#
# Answer:
#
# Return values
# Exception handling

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Why were Executors introduced?
#
# Answer:
#
# To provide a cleaner way
# to submit work, collect
# results, and handle failures.

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Do Executors replace
# threads and processes?
#
# Answer:
#
# No.
#
# Executors are built on top of them.

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now understand:
#
# The pain.
#
# The motivation.
#
# The need.
#
# Next question:
#
# What exactly is an Executor?
#
# What is:
#
# ThreadPoolExecutor?
#
# What is:
#
# ProcessPoolExecutor?
#
# How can both share the
# same interface?

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Raw threads execute work.
#
# Getting results back is awkward.
#
# Error handling is awkward.
#
# Shared lists are workarounds.
#
# Worker management becomes
# harder as systems grow.
#
# Executors provide a cleaner API.
#
# Executors help track:
#
# Results
# Exceptions
# Completion
#
# Next:
#
# ThreadPoolExecutor
# ProcessPoolExecutor
