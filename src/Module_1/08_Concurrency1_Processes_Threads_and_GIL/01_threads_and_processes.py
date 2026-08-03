"""
============================================================
CONCURRENCY-1
FILE : 01_threads_and_processes.py
============================================================

Topics Covered
--------------
1. Motivation
2. What is a Thread?
3. Main Thread
4. Program vs Process
5. Process vs Thread
6. Memory Sharing
7. Restaurant Analogy
8. Key Differences
9. Common Misconceptions
10. Interview Questions
11. Key Takeaways

"""

# ============================================================
# MOTIVATION
# ============================================================

# So far in OOP and LLD,
# we focused on organizing code.
#
# Classes
# Inheritance
# Abstraction
# Encapsulation
#
# But modern applications must also
# handle multiple tasks efficiently.
#
# Examples:
#
# - Sending notifications
# - Processing payments
# - Handling API requests
# - Downloading files
#
# To understand concurrency,
# we first need to understand:
#
# 1. Thread
# 2. Process

# ============================================================
# WHAT IS A THREAD?
# ============================================================

# Consider:

print("Step 1")
print("Step 2")
print("Step 3")

# Observation:
#
# Statements execute
# from top to bottom.
#
# Step 2 cannot execute
# before Step 1.
#
# This single path of execution
# is called a Thread.

# Definition:
#
# A Thread is a path of execution
# inside a running program.

# ============================================================
# MAIN THREAD
# ============================================================

# Every Python program starts with
# one thread automatically.
#
# This is called:
#
# Main Thread
#
# When execution begins,
# the main thread starts executing
# the file line by line.

# Observation:
#
# Every program has at least
# one thread.

# ============================================================
# PROGRAM VS PROCESS
# ============================================================

# Consider a file:
#
# app.py
#
# While sitting on disk:
#
# It is just code.
#
# It is not running.
#
# It consumes storage only.

# Definition:
#
# Program =
# Code stored on disk.

# Example:
#
# calculator.py
# zomato.py
# uber.py

# ============================================================
# WHAT IS A PROCESS?
# ============================================================

# Suppose we execute:
#
# python app.py
#
# The operating system:
#
# 1. Loads code into RAM
# 2. Allocates resources
# 3. Starts execution

# Definition:
#
# Process =
# Program in execution.

# Observation:
#
# Program -> Passive
#
# Process -> Active

# ============================================================
# PROGRAM VS PROCESS EXAMPLE
# ============================================================

# Before execution:
#
# app.py
#
# Program

# After execution:
#
# python app.py
#
# Process

# Therefore:
#
# Program is static.
#
# Process is running.

# ============================================================
# PROCESS VS THREAD
# ============================================================

# Process:
#
# A running program.
#
# Owns:
#
# - Memory
# - Resources
# - Files
# - Network connections

# Thread:
#
# A unit of execution
# inside a process.

# Important:
#
# Multiple threads can exist
# inside one process.

# ============================================================
# RESTAURANT ANALOGY
# ============================================================

# Imagine a restaurant.
#
# Restaurant:
#
# - Kitchen
# - Ingredients
# - Storage
# - Staff
#
# Entire restaurant
# represents a Process.

# Now imagine:
#
# Multiple chefs working
# inside the same kitchen.

# Chef 1:
#
# Making Pizza

# Chef 2:
#
# Making Burger

# Chef 3:
#
# Making Pasta

# These chefs represent Threads.

# Therefore:
#
# Process = Restaurant
#
# Thread = Chef

# ============================================================
# MEMORY SHARING
# ============================================================

# Threads inside the same process
# share memory.

# Example:
#
# Chef 1 and Chef 2
# use the same refrigerator.

# Similarly:
#
# Thread A and Thread B
# use the same memory.

# Advantage:
#
# Fast communication.

# Danger:
#
# One thread can accidentally
# affect another thread.

# This creates:
#
# Race Conditions
#
# (covered later)

# ============================================================
# PROCESS ISOLATION
# ============================================================

# Imagine two restaurants.
#
# Restaurant A
#
# Restaurant B
#
# Each has:
#
# - Separate kitchen
# - Separate ingredients
# - Separate storage

# One restaurant cannot directly
# use another restaurant's fridge.

# Similarly:
#
# Processes have separate memory.

# Observation:
#
# Processes do not automatically
# share memory.

# ============================================================
# PROCESS VS THREAD SUMMARY
# ============================================================

# Process:
#
# - Running program
# - Own memory
# - Heavyweight
# - Isolated

# Thread:
#
# - Path of execution
# - Shared memory
# - Lightweight
# - Exists inside process

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Wrong:
#
# Thread and Process
# are the same thing.

# Correct:
#
# A Process can contain
# multiple Threads.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What is the difference between
# a Process and a Thread?
#
# Process:
# Own memory space.
#
# Thread:
# Shares memory with
# other threads in the
# same process.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Thread:
#
# Path of execution.

# Main Thread:
#
# Default thread in every program.

# Program:
#
# Code stored on disk.

# Process:
#
# Program loaded into memory
# and executing.

# Process:
#
# Own private memory.

# Thread:
#
# Shares process memory.

# Restaurant Analogy:
#
# Restaurant -> Process
# Chef -> Thread

# Multiple threads can exist
# inside a single process.
