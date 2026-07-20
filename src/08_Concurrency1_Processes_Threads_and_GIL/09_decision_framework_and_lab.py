"""
============================================================
CONCURRENCY-1
FILE : 09_decision_framework_and_lab.py
============================================================

Topics Covered
--------------
1. Motivation
2. The Concurrency Decision Framework
3. Threading vs Multiprocessing
4. CPU-bound vs I/O-bound Matrix
5. Real-World Examples
6. Benchmark Lab
7. Performance Comparison Table
8. Choosing the Right Tool
9. Homework
10. Interview Questions
11. Key Takeaways

Based on Concurrency-1 Lecture Notes.
"""

# ============================================================
# MOTIVATION
# ============================================================

# Throughout this lecture we learned:
#
# - Threads
# - Processes
# - Concurrency
# - Parallelism
# - GIL
# - CPU-bound Work
# - I/O-bound Work
# - Multiprocessing
#
# The final question becomes:
#
# Which tool should we choose
# for a given problem?

# ============================================================
# THE DECISION FRAMEWORK
# ============================================================

# Before writing code,
# ask one question:
#
# Is the workload:
#
# CPU-bound
#
# or
#
# I/O-bound ?

# This single decision often
# determines the correct solution.

# ============================================================
# CPU-BOUND WORK
# ============================================================

# CPU-bound work spends most
# of its time performing
# calculations.
#
# Examples:
#
# - Image processing
# - Video encoding
# - Data analysis
# - Machine Learning inference
# - Mathematical computation

# Observation:
#
# CPU is busy continuously.

# ============================================================
# I/O-BOUND WORK
# ============================================================

# I/O-bound work spends most
# of its time waiting.
#
# Examples:
#
# - API calls
# - Database queries
# - File operations
# - Network communication
# - Downloading data

# Observation:
#
# CPU spends significant time idle
# while waiting for external systems.

# ============================================================
# THREADING VS MULTIPROCESSING
# ============================================================

# Threading:
#
# - Shared memory
# - Lightweight
# - Subject to GIL
# - Excellent for I/O-bound tasks

# Multiprocessing:
#
# - Separate memory
# - Multiple interpreters
# - Separate GILs
# - Excellent for CPU-bound tasks

# ============================================================
# THE DECISION MATRIX
# ============================================================

# +----------------+--------------------+--------------------+
# |                | I/O-bound          | CPU-bound          |
# +----------------+--------------------+--------------------+
# | Use            | Threading          | Multiprocessing    |
# +----------------+--------------------+--------------------+
# | Why            | Waits overlap      | Real parallelism   |
# +----------------+--------------------+--------------------+
# | Cost           | Low                | Higher             |
# +----------------+--------------------+--------------------+
# | Examples       | APIs, DB, Files    | ML, Images, Math   |
# +----------------+--------------------+--------------------+

# ============================================================
# WHY THREADING FOR I/O?
# ============================================================

# Waiting operations release
# the GIL.
#
# Therefore:
#
# Multiple waits can overlap.
#
# Example:
#
# Five API calls.
#
# Instead of:
#
# Wait
# Wait
# Wait
# Wait
# Wait
#
# Threading allows many waits
# to occur simultaneously.

# ============================================================
# WHY MULTIPROCESSING FOR CPU?
# ============================================================

# CPU-heavy work spends most
# of its time computing.
#
# The GIL prevents Python threads
# from executing bytecode in parallel.
#
# Multiprocessing avoids this
# limitation by creating
# separate processes.

# ============================================================
# REAL-WORLD EXAMPLE #1
# ============================================================

# Uber Dispatch System
#
# Checking multiple drivers.
#
# Mostly:
#
# Network communication.
#
# Therefore:
#
# I/O-bound.
#
# Recommended:
#
# Threading.

# ============================================================
# REAL-WORLD EXAMPLE #2
# ============================================================

# Zomato Notifications
#
# Sending:
#
# - Push notifications
# - SMS messages
# - Emails
#
# Mostly waiting.
#
# Therefore:
#
# I/O-bound.
#
# Recommended:
#
# Threading.

# ============================================================
# REAL-WORLD EXAMPLE #3
# ============================================================

# Image Processing Pipeline
#
# Performing:
#
# - Filtering
# - Compression
# - Resizing
#
# Heavy calculations.
#
# Therefore:
#
# CPU-bound.
#
# Recommended:
#
# Multiprocessing.

# ============================================================
# REAL-WORLD EXAMPLE #4
# ============================================================

# Fraud Detection
#
# Large amount of computation.
#
# Complex calculations.
#
# Therefore:
#
# CPU-bound.
#
# Recommended:
#
# Multiprocessing.

# ============================================================
# BENCHMARK LAB
# ============================================================

# To truly understand concurrency,
# benchmark different approaches.
#
# Compare:
#
# Sequential
#
# Threading
#
# Multiprocessing

# ============================================================
# CPU-BOUND BENCHMARK TABLE
# ============================================================

# Example Results
#
# +-------------------+----------+
# | Approach          | Time     |
# +-------------------+----------+
# | Sequential        | 4.1s     |
# | Threading         | 4.3s     |
# | Multiprocessing   | 2.2s     |
# +-------------------+----------+

# Observation:
#
# Threading provides little
# improvement.
#
# Multiprocessing achieves
# real speedup.

# ============================================================
# I/O-BOUND BENCHMARK TABLE
# ============================================================

# Example Results
#
# +-------------------+----------+
# | Approach          | Time     |
# +-------------------+----------+
# | Sequential        | 5.0s     |
# | Threading         | 1.0s     |
# | Multiprocessing   | 1.3s     |
# +-------------------+----------+

# Observation:
#
# Threading performs very well.
#
# Multiprocessing works,
# but incurs additional overhead.

# ============================================================
# PERFORMANCE INSIGHT
# ============================================================

# Faster is not always better.
#
# Consider:
#
# - Memory usage
# - Startup cost
# - Complexity
#
# Choose the simplest tool
# that solves the problem.

# ============================================================
# MIXED WORKLOADS
# ============================================================

# Some systems perform:
#
# I/O
#
# followed by
#
# CPU work.
#
# Example:
#
# Call Payment API
#
# Then:
#
# Run Fraud Detection.
#
# Such systems may use
# both techniques together.

# ============================================================
# CHOOSING THE RIGHT TOOL
# ============================================================

# Ask:
#
# "Where is time being spent?"
#
# If time is spent:
#
# Waiting
#
# -> Threading
#
# If time is spent:
#
# Computing
#
# -> Multiprocessing

# ============================================================
# FINAL SUMMARY
# ============================================================

# Program:
#
# Code on disk.
#
# Process:
#
# Running program.
#
# Thread:
#
# Path of execution.
#
# Concurrency:
#
# Multiple tasks making progress.
#
# Parallelism:
#
# Multiple tasks executing
# simultaneously.
#
# GIL:
#
# One thread executes Python
# bytecode at a time.

# ============================================================
# HOMEWORK
# ============================================================

# Homework 1
#
# Take the shared counter example.
#
# Research:
#
# threading.Lock()
#
# Use it to make the counter
# produce the correct answer
# every time.

# ------------------------------------------------------------

# Homework 2
#
# Create a mixed workload:
#
# sleep(0.5)
#
# followed by
#
# cpu_heavy()
#
# Compare:
#
# - Sequential
# - Threading
# - Multiprocessing

# ------------------------------------------------------------

# Homework 3
#
# Use dis.dis()
#
# Find another statement that
# expands into multiple bytecode
# instructions.

# ------------------------------------------------------------

# Homework 4
#
# Push all lecture work
# to GitHub.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What is the decision rule for
# choosing between threading and
# multiprocessing?
#
# Answer:
#
# I/O-bound
# -> Threading
#
# CPU-bound
# -> Multiprocessing

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Why is multiprocessing effective
# for CPU-heavy work?
#
# Answer:
#
# Each process has its own
# interpreter and GIL.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Concurrency:
#
# Multiple tasks making progress.

# Parallelism:
#
# Multiple tasks executing
# simultaneously.

# GIL:
#
# Limits Python threads for
# CPU-bound work.

# Threading:
#
# Best for I/O-bound workloads.

# Multiprocessing:
#
# Best for CPU-bound workloads.

# Decision Rule:
#
# Waiting
# -> Threading
#
# Computing
# -> Multiprocessing

# Benchmark before optimizing.
#
# Measure first.
#
# Then choose the correct tool.
