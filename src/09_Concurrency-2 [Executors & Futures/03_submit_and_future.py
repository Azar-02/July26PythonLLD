"""
============================================================
CONCURRENCY-2
FILE : 03_submit_and_future.py
============================================================

Topics Covered
--------------
1. Motivation
2. The Problem With Raw Threads
3. submit()
4. What Is A Future?
5. Food Token Analogy
6. Future Lifecycle
7. done()
8. result()
9. Waiting Behaviour
10. Common Misconceptions
11. Interview Questions
12. Key Takeaways

Based on Concurrency-2 Lecture Notes.
"""

from concurrent.futures import ThreadPoolExecutor
import time

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file we learned:
#
# Executor
# Worker Pool
# ThreadPoolExecutor
# ProcessPoolExecutor
#
# A question still remains.
#
# We have a pool.
#
# Great.
#
# But how do we actually
# give work to that pool?

# ============================================================
# THE OLD WORLD
# ============================================================

# Earlier:
#
# t = Thread(...)
# t.start()
# t.join()
#
# We manually controlled
# individual workers.

# ============================================================
# THE EXECUTOR WORLD
# ============================================================

# Now:
#
# We do not interact directly
# with workers.
#
# Instead:
#
# We hand work to the Executor.

# ============================================================
# A SIMPLE TASK
# ============================================================

def fetch_user(user_id):

    time.sleep(2)

    return f"User-{user_id}"

# ============================================================
# INTRODUCING submit()
# ============================================================

with ThreadPoolExecutor(
    max_workers=2
) as executor:

    future = executor.submit(
        fetch_user,
        101
    )

# ============================================================
# ASK LEARNERS
# ============================================================

# What does submit() return?
#
# A) Final Answer
# B) Thread Object
# C) Something Else

# ============================================================
# ANSWER
# ============================================================

# submit() returns:
#
# Future

# ============================================================
# WHAT IS A FUTURE?
# ============================================================

# Future represents:
#
# Work that may complete
# in the future.
#
# Not completed yet.
#
# Not necessarily failed.
#
# Not necessarily successful.
#
# Simply:
#
# Work in progress.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Future is NOT:
#
# The final answer.
#
# Future is:
#
# A handle to the answer.

# ============================================================
# FOOD TOKEN ANALOGY
# ============================================================

# Imagine:
#
# You order food.
#
# Restaurant gives:
#
# Token #57
#
# Is token #57 the food?
#
# No.
#
# It represents the food.

# ============================================================
# MAPPING
# ============================================================

# Restaurant
#     ↓
# Executor
#
# Kitchen
#     ↓
# Worker Thread
#
# Food
#     ↓
# Final Result
#
# Token
#     ↓
# Future

# ============================================================
# WHY THIS ANALOGY IS IMPORTANT
# ============================================================

# Students often think:
#
# future = result
#
# Wrong.
#
# Future points to
# a future result.

# ============================================================
# EXAMPLE
# ============================================================

with ThreadPoolExecutor(
    max_workers=2
) as executor:

    future = executor.submit(
        fetch_user,
        500
    )

    print(type(future))

# ============================================================
# OBSERVATION
# ============================================================

# Output resembles:
#
# <class 'Future'>
#
# Not:
#
# User-500

# ============================================================
# ASK LEARNERS
# ============================================================

# What happens immediately
# after submit()?
#
# Does Python wait
# for completion?

# ============================================================
# ANSWER
# ============================================================

# No.
#
# submit() returns immediately.

# ============================================================
# TIMELINE
# ============================================================

# submit()
#     ↓
# Future created
#     ↓
# Work starts in background
#     ↓
# Main thread continues

# ============================================================
# THIS IS THE BIG IDEA
# ============================================================

# We can continue doing
# other work while the
# background task executes.

# ============================================================
# FUTURE LIFECYCLE
# ============================================================

# Pending
#     ↓
# Running
#     ↓
# Finished
#
# or
#
# Failed

# ============================================================
# INTRODUCING done()
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        1
    )

    print(
        "Immediately:",
        future.done()
    )

# ============================================================
# OBSERVATION
# ============================================================

# Usually:
#
# False
#
# because work has not
# completed yet.

# ============================================================
# WHAT DOES done() MEAN?
# ============================================================

# done()
#
# asks:
#
# "Has the work finished?"

# ============================================================
# IMPORTANT DETAIL
# ============================================================

# done() does NOT:
#
# Return the answer.
#
# It only reports status.

# ============================================================
# INTRODUCING result()
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        42
    )

    answer = future.result()

    print(answer)

# ============================================================
# ASK LEARNERS
# ============================================================

# What if work has not
# finished yet?
#
# What should result() do?

# ============================================================
# ANSWER
# ============================================================

# result() waits.

# ============================================================
# VERY IMPORTANT
# ============================================================

# result()
#
# blocks the caller.
#
# It waits until:
#
# Success
#
# or
#
# Failure

# ============================================================
# TIMELINE
# ============================================================

# submit()
#     ↓
# Future Returned
#     ↓
# result()
#     ↓
# Wait...
# Wait...
# Wait...
#     ↓
# Final Answer

# ============================================================
# done() VS result()
# ============================================================

# done()
#
# Question:
#
# Finished yet?
#
# Returns:
#
# True / False

# ============================================================

# result()
#
# Question:
#
# Give me the answer.
#
# Returns:
#
# Actual result.
#
# May block.

# ============================================================
# PREDICTION EXERCISE
# ============================================================

# Suppose:
#
# Task takes 30 seconds.
#
# We call:
#
# future.result()
#
# immediately.
#
# Prediction:
#
# Program waits 30 seconds.

# ============================================================
# OBSERVATION
# ============================================================

# Many beginners accidentally
# destroy concurrency by calling:
#
# result()
#
# too early.

# ============================================================
# WHY THIS MATTERS
# ============================================================

# Concurrency gives us the ability
# to overlap work.
#
# Calling result() immediately
# often removes that benefit.

# ============================================================
# BETTER PATTERN
# ============================================================

# Submit work
#     ↓
# Submit more work
#     ↓
# Do other work
#     ↓
# Collect results later

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# Future contains the answer.
#
# Correct:
#
# Future points to the answer.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# submit() waits.
#
# Correct:
#
# submit() returns immediately.

# ============================================================
# COMMON MISCONCEPTION #3
# ============================================================

# Wrong:
#
# done() gives result.
#
# Correct:
#
# done() only reports status.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What does submit() return?
#
# Answer:
#
# Future

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# What is a Future?
#
# Answer:
#
# A placeholder/handle for
# work that may finish later.

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Difference between:
#
# done()
# result()
#
# done():
# status
#
# result():
# answer

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now understand:
#
# submit()
# Future
# done()
# result()
#
# Next question:
#
# What happens when
# background work fails?
#
# How do Futures help us
# handle exceptions cleanly?

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# submit() schedules work.
#
# submit() returns Future.
#
# Future is not the answer.
#
# Future represents work
# in progress.
#
# done() checks status.
#
# result() gets answer.
#
# result() may block.
#
# Futures make result tracking
# much cleaner than raw threads.
