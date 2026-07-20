"""
============================================================
CONCURRENCY-1
FILE : 07_cpu_vs_io_bound.py
============================================================

Topics Covered
--------------
1. Motivation
2. What is CPU-bound Work?
3. What is I/O-bound Work?
4. Why Threading Fails for CPU-bound Tasks
5. CPU-bound Timeline
6. Why Threading Helps I/O-bound Tasks
7. I/O-bound Timeline
8. GIL Release During Waiting
9. Real Benchmark
10. Choosing the Right Tool
11. Common Misconceptions
12. Interview Questions
13. Key Takeaways

Based on Concurrency-1 Lecture Notes.
"""

import threading
import time

# ============================================================
# MOTIVATION
# ============================================================

# We learned:
#
# CPU-heavy work does not gain much
# from Python threading.
#
# The natural question becomes:
#
# If threading cannot speed up
# CPU-bound work,
#
# why does threading exist?

# ============================================================
# THE ANSWER
# ============================================================

# Not all tasks are the same.
#
# Some tasks spend most of their time:
#
# Computing.
#
# Other tasks spend most of their time:
#
# Waiting.

# Therefore:
#
# We divide workloads into:
#
# 1. CPU-bound
# 2. I/O-bound

# ============================================================
# WHAT IS CPU-BOUND WORK?
# ============================================================

# CPU-bound work means:
#
# The CPU spends most of its time
# performing calculations.
#
# Examples:
#
# - Mathematical computation
# - Image processing
# - Video encoding
# - Data analysis
# - Machine Learning inference

# Observation:
#
# CPU is busy continuously.
#
# Very little waiting occurs.

# ============================================================
# CPU-BOUND EXAMPLE
# ============================================================

def cpu_heavy(n):

    return sum(
        i * i
        for i in range(n)
    )

# Observation:
#
# This function continuously
# performs calculations.
#
# CPU remains busy.

# ============================================================
# CPU-BOUND TIMELINE
# ============================================================

# Tick --->
#
# 1   2   3   4   5   6
#
# Thread A
# COMP COMP COMP COMP
#
# Thread B
#                 COMP COMP COMP COMP

# Observation:
#
# Thread A keeps the GIL.
#
# Thread B waits.
#
# Total Time:
#
# Work A + Work B

# Therefore:
#
# Threading provides little
# or no speedup.

# ============================================================
# CPU-BOUND RULE
# ============================================================

# CPU-bound + Threading
#
# Usually:
#
# No significant speedup.

# ============================================================
# WHAT IS I/O-BOUND WORK?
# ============================================================

# I/O means:
#
# Input / Output
#
# These tasks spend most of their
# time waiting for external systems.

# Examples:
#
# - API calls
# - Database queries
# - Reading files
# - Downloading data
# - Network communication

# Observation:
#
# CPU is often idle.
#
# Program spends most of its time
# waiting.

# ============================================================
# I/O-BOUND EXAMPLE
# ============================================================

def fetch_driver_location(driver_id):

    time.sleep(1)

    return (
        f"Location for {driver_id}"
    )

# Note:
#
# sleep() represents:
#
# - Network delay
# - API response time
# - Database waiting time

# ============================================================
# IMPORTANT GIL BEHAVIOR
# ============================================================

# While waiting for I/O,
#
# Python releases the GIL.
#
# This allows:
#
# Another thread
#
# to execute.

# Observation:
#
# Waiting threads do not hold
# the GIL for the entire duration.

# ============================================================
# I/O-BOUND TIMELINE
# ============================================================

# Tick --->
#
# 1   2   3   4   5
#
# Thread A
# SETUP WAIT WAIT WAIT DONE
#
# Thread B
#     SETUP WAIT WAIT WAIT DONE

# Observation:
#
# Both waits overlap.
#
# Multiple threads can be waiting
# simultaneously.

# This is where threading shines.

# ============================================================
# WHY THREADING HELPS I/O
# ============================================================

# Thread A:
#
# Makes network request.
#
# Then waits.

# During the wait:
#
# Thread B gets a chance
# to execute.

# Then:
#
# Thread B waits too.

# Both waits happen
# at nearly the same time.

# ============================================================
# REAL BENCHMARK
# ============================================================

drivers = [
    "D101",
    "D102",
    "D103",
    "D104",
    "D105"
]

# Sequential

start = time.perf_counter()

for driver in drivers:

    fetch_driver_location(
        driver
    )

sequential_time = (
    time.perf_counter() - start
)

print(
    f"Sequential: "
    f"{sequential_time:.2f}s"
)

# ============================================================
# THREADED VERSION
# ============================================================

start = time.perf_counter()

threads = []

for driver in drivers:

    t = threading.Thread(
        target=fetch_driver_location,
        args=(driver,)
    )

    threads.append(t)

    t.start()

for t in threads:

    t.join()

threaded_time = (
    time.perf_counter() - start
)

print(
    f"Threaded: "
    f"{threaded_time:.2f}s"
)

# ============================================================
# EXPECTED RESULT
# ============================================================

# Example:
#
# Sequential:
# 5.0s
#
# Threaded:
# 1.0s

# Exact numbers vary.
#
# Important observation:
#
# Threaded version is much faster.

# Why?
#
# All waits overlap.

# ============================================================
# VISUALIZING THE DIFFERENCE
# ============================================================

# CPU-bound:
#
# Compute
# Compute
# Compute
#
# Thread A blocks progress.

# I/O-bound:
#
# Wait
# Wait
# Wait
#
# Waiting overlaps nicely.

# ============================================================
# DECISION RULE
# ============================================================

# If work is:
#
# CPU-bound
#
# Threading is usually not useful.

# If work is:
#
# I/O-bound
#
# Threading is often very useful.

# ============================================================
# REAL-WORLD EXAMPLES
# ============================================================

# Uber:
#
# Calling multiple driver devices.
#
# I/O-bound

# Zomato:
#
# Sending notifications.
#
# I/O-bound

# Image Processing:
#
# CPU-bound

# Fraud Detection Math:
#
# CPU-bound

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# Threading always improves speed.
#
# Correct:
#
# Depends on workload type.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# More threads always means
# better performance.
#
# Correct:
#
# Excessive threads may even
# reduce performance.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Why does threading help
# I/O-bound tasks?
#
# Answer:
#
# Because waiting operations
# release the GIL.
#
# Multiple waits can overlap.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Why does threading usually fail
# to speed up CPU-bound work?
#
# Answer:
#
# CPU-bound threads spend most of
# their time holding the GIL.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# CPU-bound:
#
# Heavy computation.
#
# Examples:
#
# Image processing
# Data analysis
# ML inference

# I/O-bound:
#
# Waiting for external systems.
#
# Examples:
#
# APIs
# Databases
# File operations

# CPU-bound + Threading:
#
# Little or no speedup.

# I/O-bound + Threading:
#
# Significant speedup.

# Waiting operations:
#
# Release the GIL.

# Decision Rule:
#
# CPU-bound -> Multiprocessing
#
# I/O-bound -> Threading
