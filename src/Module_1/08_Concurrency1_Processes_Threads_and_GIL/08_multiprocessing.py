"""
============================================================
CONCURRENCY-1
FILE : 08_multiprocessing.py
============================================================

Topics Covered
--------------
1. Motivation
2. Why Multiprocessing Exists
3. Real Parallelism
4. Process Class
5. Creating Processes
6. start()
7. join()
8. Process vs Thread
9. The __main__ Guard
10. Windows Spawn Problem
11. Pool
12. pool.map()
13. Returning Results
14. Pickling Overhead
15. Best Practices
16. Interview Questions
17. Key Takeaways

Based on Concurrency-1 Lecture Notes.
"""

from multiprocessing import Process, Pool

# ============================================================
# MOTIVATION
# ============================================================

# We learned:
#
# CPU-bound + Threading
#
# gives little or no speedup.
#
# Reason:
#
# The GIL allows only one thread
# to execute Python bytecode
# at a time.
#
# The natural question becomes:
#
# How do we achieve real parallelism
# for CPU-heavy work?

# ============================================================
# THE IDEA
# ============================================================

# Instead of:
#
# Multiple Threads
#
# inside one process,
#
# we create:
#
# Multiple Processes.

# Each process gets:
#
# - Its own memory
# - Its own interpreter
# - Its own GIL

# Therefore:
#
# Multiple CPU cores can be used.

# ============================================================
# REAL PARALLELISM
# ============================================================

# Threading:
#
# One process
# One interpreter
# One GIL
#
# Multiprocessing:
#
# Multiple processes
# Multiple interpreters
# Multiple GILs

# Observation:
#
# Processes can truly execute
# at the same time.

# ============================================================
# CPU-HEAVY FUNCTION
# ============================================================

def cpu_heavy(n):

    return sum(
        i * i
        for i in range(n)
    )

# ============================================================
# FIRST PROCESS
# ============================================================

# Creating a process is very similar
# to creating a thread.

# Example:
#
# Process(
#     target=cpu_heavy,
#     args=(5000000,)
# )

# ============================================================
# PROCESS OBJECT
# ============================================================

# Example:
#
# p1 = Process(
#     target=cpu_heavy,
#     args=(5000000,)
# )

# Observation:
#
# Process object is created.
#
# Work has not started yet.

# ============================================================
# STARTING PROCESSES
# ============================================================

# start()
#
# Launches the process.

# Example:
#
# p1.start()

# Observation:
#
# A completely separate process
# begins execution.

# ============================================================
# WAITING FOR COMPLETION
# ============================================================

# join()
#
# Waits until the process finishes.

# Example:
#
# p1.join()

# Similar to threading:
#
# start() -> launch
#
# join() -> wait

# ============================================================
# COMPLETE EXAMPLE
# ============================================================

if __name__ == "__main__":

    p1 = Process(
        target=cpu_heavy,
        args=(5_000_000,)
    )

    p2 = Process(
        target=cpu_heavy,
        args=(5_000_000,)
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()

# Observation:
#
# Both processes can run on
# separate CPU cores.

# ============================================================
# PROCESS VS THREAD
# ============================================================

# Thread:
#
# Shares memory.
#
# Process:
#
# Own memory.

# Thread:
#
# Shares one GIL.
#
# Process:
#
# Own GIL.

# Thread:
#
# Lightweight.
#
# Process:
#
# Heavier.

# ============================================================
# THE __main__ GUARD
# ============================================================

# Very Important:
#
# Multiprocessing code should
# usually be protected using:
#
# if __name__ == "__main__":

# Example:
#
# if __name__ == "__main__":
#     p.start()

# ============================================================
# WHY IS THIS REQUIRED?
# ============================================================

# Child processes must import
# the Python file again.
#
# Without protection:
#
# Process creation code may
# execute repeatedly.

# This can create:
#
# Infinite process spawning.

# ============================================================
# WINDOWS SPAWN PROBLEM
# ============================================================

# Windows uses:
#
# Spawn
#
# instead of:
#
# Fork

# Therefore:
#
# A new Python interpreter starts
# and imports the file again.

# Without:
#
# if __name__ == "__main__"
#
# Process creation may repeat
# indefinitely.

# Observation:
#
# This is one of the most common
# multiprocessing mistakes.

# ============================================================
# PROCESS PERFORMANCE
# ============================================================

# Example benchmark:
#
# Sequential:
# 4.1s
#
# Threading:
# 4.3s
#
# Multiprocessing:
# 2.2s

# Exact values vary.
#
# Important observation:
#
# Multiprocessing can provide
# real CPU speedup.

# ============================================================
# THE PROBLEM WITH MANY PROCESSES
# ============================================================

# Suppose we need:
#
# 10 processes
#
# 20 processes
#
# 50 processes
#
# Creating each process manually
# becomes tedious.

# ============================================================
# INTRODUCTION TO POOL
# ============================================================

# multiprocessing provides:
#
# Pool
#
# A Pool manages worker processes
# automatically.

# ============================================================
# CREATING A POOL
# ============================================================

# Example:
#
# with Pool(processes=4) as pool:
#     pass

# Observation:
#
# Four worker processes
# are created.

# ============================================================
# pool.map()
# ============================================================

# Similar to built-in map().
#
# Example:
#
# pool.map(
#     cpu_heavy,
#     [5000000] * 4
# )

# Meaning:
#
# Run cpu_heavy()
# four times.

# ============================================================
# COMPLETE POOL EXAMPLE
# ============================================================

if __name__ == "__main__":

    with Pool(processes=4) as pool:

        results = pool.map(
            cpu_heavy,
            [5_000_000] * 4
        )

    print(results)

# ============================================================
# WHY POOL IS USEFUL
# ============================================================

# Pool automatically:
#
# - Creates workers
# - Distributes work
# - Waits for completion
# - Collects results

# Less code.
#
# Easier maintenance.

# ============================================================
# RETURNING RESULTS
# ============================================================

# Process objects do not directly
# return function results.
#
# Additional mechanisms are needed.
#
# Example:
#
# Queue
#
# Pipe

# Pool simplifies this by
# collecting results automatically.

# ============================================================
# PICKLING
# ============================================================

# Processes do not share memory.
#
# Therefore:
#
# Data must be transferred
# between processes.

# Python uses:
#
# Pickling
#
# to serialize data.

# Observation:
#
# Data transfer has a cost.

# ============================================================
# PICKLING OVERHEAD
# ============================================================

# Multiprocessing is not free.
#
# Costs include:
#
# - Process startup
# - Memory usage
# - Data serialization
# - Data transfer

# Therefore:
#
# Use multiprocessing when
# the workload is large enough
# to justify the cost.

# ============================================================
# WHEN TO USE MULTIPROCESSING
# ============================================================

# Good Choices:
#
# - Image processing
# - Video encoding
# - Scientific computation
# - Machine Learning inference
# - Heavy mathematical work

# Poor Choices:
#
# - API calls
# - Database queries
# - File downloads

# Those are usually I/O-bound.

# ============================================================
# BEST PRACTICES
# ============================================================

# Always:
#
# Use __main__ guard.
#
# Prefer Pool when many workers
# perform similar tasks.
#
# Measure performance instead
# of guessing.

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Wrong:
#
# Multiprocessing is always better.
#
# Correct:
#
# Multiprocessing is usually best
# for CPU-bound workloads.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Why does multiprocessing avoid
# the GIL limitation?
#
# Answer:
#
# Each process has its own
# Python interpreter and GIL.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What is the purpose of
# if __name__ == "__main__"?
#
# Answer:
#
# Prevents unwanted execution
# when child processes import
# the module.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Multiprocessing:
#
# Creates multiple processes.

# Each process has:
#
# - Own memory
# - Own interpreter
# - Own GIL

# Multiprocessing enables:
#
# Real parallel execution.

# Process:
#
# start() -> launch
#
# join() -> wait

# __main__ guard:
#
# Essential for multiprocessing.

# Pool:
#
# Simplifies worker management.

# Multiprocessing:
#
# Best suited for CPU-bound work.

# I/O-bound work:
#
# Usually better served
# by threading.
