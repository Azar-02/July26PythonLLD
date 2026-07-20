"""
============================================================
CONCURRENCY-1
FILE : 06_understanding_the_gil_part2.py
============================================================

Topics Covered
--------------
1. Motivation
2. The Shared Counter Problem
3. Race Conditions
4. Why the GIL Is Not Enough
5. Bytecode
6. The dis Module
7. Breaking Down counter += 1
8. Lost Update Problem
9. What the GIL Actually Guarantees
10. What the GIL Does NOT Guarantee
11. Locks Preview
12. Common Misconceptions
13. Interview Questions
14. Key Takeaways

"""

import threading
import dis

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we learned:
#
# The GIL allows only one thread
# to execute Python bytecode
# at a time.
#
# Many developers hear this and think:
#
# "Great.
# My shared variables must be safe."
#
# Unfortunately:
#
# This conclusion is wrong.

# ============================================================
# THE SHARED COUNTER PROBLEM
# ============================================================

counter = 0

def increment():
    global counter

    for _ in range(100_000):
        counter += 1

# Imagine:
#
# Thread A runs increment()
#
# Thread B runs increment()
#
# Expected:
#
# 200,000
#
# Because:
#
# 100,000 + 100,000

# ============================================================
# THE SURPRISING RESULT
# ============================================================

# In practice:
#
# The final result may be:
#
# 187,421
# 194,812
# 198,102
#
# Numbers vary from run to run.
#
# Observation:
#
# Some increments are lost.

# ============================================================
# WHAT IS A RACE CONDITION?
# ============================================================

# Definition:
#
# A Race Condition occurs when
# multiple threads access and
# modify shared data and the
# final result depends on timing.
#
# Different timing.
#
# Different result.

# Observation:
#
# Race conditions often produce:
#
# - Incorrect values
# - Random bugs
# - Difficult debugging sessions

# ============================================================
# THE BIG QUESTION
# ============================================================

# If only one thread executes
# Python bytecode at a time,
#
# how can increments be lost?
#
# The answer lies in:
#
# Bytecode.

# ============================================================
# SOURCE CODE VS BYTECODE
# ============================================================

# We write:

# counter += 1

# It looks like:
#
# One operation.
#
# Python sees:
#
# Multiple operations.

# ============================================================
# THE dis MODULE
# ============================================================

# Python provides:
#
# dis
#
# short for:
#
# disassemble

def add_one():
    global counter
    counter += 1

# Example:
#
# dis.dis(add_one)

# This shows the bytecode
# instructions generated
# by Python.

# ============================================================
# BYTECODE BREAKDOWN
# ============================================================

# Depending on Python version,
# instruction names may differ.
#
# The important idea remains:
#
# counter += 1
#
# becomes multiple steps.

# Example:

# LOAD_GLOBAL counter
# LOAD_CONST 1
# INPLACE_ADD
# STORE_GLOBAL counter

# Observation:
#
# One line of Python code
# becomes multiple bytecode
# instructions.

# ============================================================
# THE REAL PROBLEM
# ============================================================

# Suppose:
#
# counter = 500000

# Thread A:
#
# LOAD_GLOBAL
#
# Reads:
#
# 500000

# Before Thread A finishes,
# execution switches.

# Thread B:
#
# LOAD_GLOBAL
#
# Reads:
#
# 500000

# Thread B:
#
# Adds 1
#
# Stores:
#
# 500001

# Thread A resumes.
#
# It still remembers:
#
# 500000

# Thread A:
#
# Adds 1
#
# Stores:
#
# 500001

# ============================================================
# LOST UPDATE
# ============================================================

# Expected:
#
# 500000
# 500001
# 500002

# Actual:
#
# 500000
# 500001

# Two increments happened.
#
# Counter moved only once.

# Observation:
#
# One update disappeared.
#
# This is called:
#
# Lost Update.

# ============================================================
# DID THE GIL FAIL?
# ============================================================

# Surprisingly:
#
# No.
#
# The GIL worked correctly.

# The GIL guarantees:
#
# One bytecode instruction
# executes at a time.

# It does NOT guarantee:
#
# Multiple instructions
# execute as one unit.

# ============================================================
# IMPORTANT DISTINCTION
# ============================================================

# GIL protects:
#
# Individual bytecode instructions.

# GIL does NOT protect:
#
# Logical operations that require
# multiple instructions.

# Example:
#
# counter += 1

# Looks like:
#
# One operation.
#
# Actually:
#
# Several operations.

# ============================================================
# WHAT THE GIL ACTUALLY GUARANTEES
# ============================================================

# GIL Guarantee:
#
# One bytecode instruction
# runs uninterrupted.
#
# Example:
#
# LOAD_GLOBAL completes.
#
# Then a switch may occur.

# Observation:
#
# Thread switching can happen
# between bytecode instructions.

# ============================================================
# WHAT THE GIL DOES NOT GUARANTEE
# ============================================================

# The GIL does NOT guarantee:
#
# - Thread-safe counters
# - Thread-safe balances
# - Thread-safe shared variables
#
# Shared data can still suffer
# from race conditions.

# ============================================================
# EXAMPLE
# ============================================================

balance = 1000

# Two threads execute:
#
# balance -= 100
#
# simultaneously.
#
# Expected:
#
# 800
#
# Actual:
#
# Result may be incorrect
# without synchronization.

# ============================================================
# LOCKS PREVIEW
# ============================================================

# The proper solution is:
#
# Lock
#
# A Lock allows developers
# to protect an entire block
# of operations.
#
# Example:
#
# Read
# Modify
# Write
#
# as one indivisible unit.

# Locks are covered in the
# next concurrency lecture.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# GIL makes Python code
# thread-safe.
#
# Correct:
#
# GIL protects interpreter
# internals, not your data.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# counter += 1
#
# is atomic.
#
# Correct:
#
# It expands into multiple
# bytecode instructions.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Why can race conditions occur
# even when the GIL exists?
#
# Answer:
#
# Because the GIL protects
# individual bytecode instructions,
# not entire logical operations.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What tool can be used to inspect
# Python bytecode?
#
# Answer:
#
# dis
#
# Example:
#
# dis.dis(function_name)

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Race Condition:
#
# Result depends on timing.

# counter += 1
#
# Is NOT atomic.

# Python converts source code
# into bytecode instructions.

# dis module:
#
# Displays bytecode.

# Lost Update:
#
# Multiple modifications
# overwrite each other.

# GIL protects:
#
# Individual bytecode instructions.

# GIL does NOT protect:
#
# Your shared variables.

# Correct solution:
#
# Synchronization tools
# such as Locks.
