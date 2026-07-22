"""
============================================================
CONCURRENCY-2
FILE : 05_future_exception_handling_v2.py
============================================================

Topics Covered
--------------
1. Motivation
2. Revisiting Pain #2
3. Why Silent Failures Are Dangerous
4. Raw Threads vs Futures
5. Where Exceptions Go
6. Exception Propagation
7. result() and Failures
8. try/except with Futures
9. Multiple Futures
10. Success vs Failure Timelines
11. Common Misconceptions
12. Interview Questions
13. Key Takeaways

Based on Concurrency-2 Lecture Notes.
"""

from concurrent.futures import ThreadPoolExecutor
import time

# ============================================================
# MOTIVATION
# ============================================================

# In File 01 we identified two major pains.
#
# Pain #1
#
# Return values.
#
# Pain #2
#
# Exceptions.
#
# Files 03 and 04 largely solved
# the return value problem.
#
# We learned:
#
# submit()
# Future
# done()
# result()
#
# But a very important question
# remains unanswered.
#
# What happens when a worker fails?

# ============================================================
# ASK LEARNERS
# ============================================================

# Imagine:
#
# Payment service unavailable.
#
# Database timeout.
#
# Email service down.
#
# Inventory update crashes.
#
# Should the main application
# know about these failures?
#
# Of course.
#
# The challenge is:
#
# How do we communicate the failure
# from a background worker back
# to the caller?

# ============================================================
# THE RAW THREAD WORLD
# ============================================================

# Recall what we observed with
# raw threads.
#
# Worker starts.
#
# Worker crashes.
#
# Traceback appears.
#
# Main thread often continues.
#
# This feels uncomfortable.

# ============================================================
# WHY THIS FEELS WRONG
# ============================================================

# Imagine:
#
# Customer places an order.
#
# Payment processing fails.
#
# Main application never notices.
#
# Order marked successful.
#
# Business state is now incorrect.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# In production systems:
#
# Silent failures are often
# more dangerous than crashes.
#
# Crashes get attention.
#
# Silent failures may remain hidden.

# ============================================================
# SIMPLE FAILING TASK
# ============================================================

def fetch_user(user_id):

    time.sleep(1)

    if user_id == 500:

        raise ConnectionError(
            "User service unavailable"
        )

    return f"User-{user_id}"

# ============================================================
# ASK LEARNERS
# ============================================================

# Suppose:
#
# fetch_user(500)
#
# runs inside a worker.
#
# Where should the exception go?
#
# Options:
#
# A) Disappear
# B) Print only
# C) Reach the caller

# Ideally:
#
# C

# ============================================================
# THE FUTURE'S SECRET JOB
# ============================================================

# Most students think:
#
# Future stores results.
#
# That is only half the story.
#
# A Future can store:
#
# Result
#
# OR
#
# Exception

# ============================================================
# THIS IS A HUGE IDEA
# ============================================================

# Future is not just a container
# for success.
#
# Future is a container for
# the final outcome.
#
# Success outcome.
#
# Failure outcome.

# ============================================================
# FOOD TOKEN ANALOGY REVISITED
# ============================================================

# Earlier:
#
# Token #57 represented food.
#
# Let's extend the analogy.
#
# You return to collect food.
#
# Possible outcomes:
#
# Food is ready.
#
# Kitchen reports:
#
# "Sorry, machine failed."
#
# The token represents the final
# outcome, not merely success.

# ============================================================
# EXECUTOR EXAMPLE
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        500
    )

# ============================================================
# ASK LEARNERS
# ============================================================

# Did submit() fail?
#
# Think carefully.

# ============================================================
# OBSERVATION
# ============================================================

# No.
#
# submit() succeeded.
#
# The task was accepted.
#
# The failure happened later
# inside the worker.

# ============================================================
# COMMON CONFUSION
# ============================================================

# Students often think:
#
# submit()
#
# should raise the exception.
#
# But submit() merely schedules work.
#
# The work hasn't even completed yet.

# ============================================================
# WHERE IS THE EXCEPTION NOW?
# ============================================================

# Answer:
#
# Inside the Future.
#
# The Future remembers
# what happened.

# ============================================================
# VISUALIZATION
# ============================================================

# submit()
#     ↓
# Future Created
#     ↓
# Worker Runs
#     ↓
# Exception Occurs
#     ↓
# Future Stores Exception

# ============================================================
# INTRODUCING result()
# ============================================================

# We already know:
#
# result()
#
# returns the answer.
#
# But what if there is no answer?

# ============================================================
# ASK LEARNERS
# ============================================================

# If a task crashes,
# what should result() do?
#
# Return None?
#
# Ignore the failure?
#
# Hide the exception?

# ============================================================
# ANSWER
# ============================================================

# result()
#
# re-raises the exception.

# ============================================================
# THIS IS THE MAGIC
# ============================================================

# Worker crashes.
#
# Future remembers.
#
# result() replays the failure
# in the caller.

# ============================================================
# TIMELINE
# ============================================================

# submit()
#     ↓
# Worker Starts
#     ↓
# Worker Crashes
#     ↓
# Future Stores Exception
#     ↓
# result()
#     ↓
# Exception Raised Again

# ============================================================
# EXAMPLE
# ============================================================

try:

    with ThreadPoolExecutor(
        max_workers=1
    ) as executor:

        future = executor.submit(
            fetch_user,
            500
        )

        answer = future.result()

        print(answer)

except Exception as e:

    print("Caught:", e)

# ============================================================
# OBSERVATION
# ============================================================

# Finally:
#
# The caller knows.
#
# This feels much more natural.

# ============================================================
# WHY THIS MATTERS
# ============================================================

# Once the exception reaches us,
# we can:
#
# Retry
# Log
# Alert
# Recover
# Notify Users

# ============================================================
# ============================================================

# Which code feels easier?
#
# Raw Thread approach
#
# or
#
# Future approach

# ============================================================
# MULTIPLE FUTURES
# ============================================================

with ThreadPoolExecutor(
    max_workers=3
) as executor:

    future1 = executor.submit(
        fetch_user,
        1
    )

    future2 = executor.submit(
        fetch_user,
        500
    )

    future3 = executor.submit(
        fetch_user,
        3
    )

# ============================================================
# PREDICTION
# ============================================================

# Suppose:
#
# future2 fails.
#
# future1 succeeds.
#
# future3 succeeds.
#
# What happens?

# ============================================================
# OBSERVATION
# ============================================================

# Each Future tracks its own state.
#
# Future 1:
# Success
#
# Future 2:
# Failure
#
# Future 3:
# Success

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# One task failing does not
# automatically destroy the
# results of other tasks.

# ============================================================
# SUCCESS TIMELINE
# ============================================================

# submit()
#     ↓
# Worker Runs
#     ↓
# Value Produced
#     ↓
# Future Stores Value
#     ↓
# result()
#     ↓
# Value Returned

# ============================================================
# FAILURE TIMELINE
# ============================================================

# submit()
#     ↓
# Worker Runs
#     ↓
# Exception Raised
#     ↓
# Future Stores Exception
#     ↓
# result()
#     ↓
# Exception Re-Raised

# ============================================================
# COMPARISON TABLE
# ============================================================

# Raw Thread
# ---------------------
# Failure difficult to manage
#
# Future
# ---------------------
# Failure captured and propagated

# ============================================================
# WHY FUTURES FEEL CLEANER
# ============================================================

# Futures unify:
#
# Success Path
#
# and
#
# Failure Path
#
# under one interface.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# submit() raises worker exceptions.
#
# Correct:
#
# Exceptions typically appear later
# when result() is called.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# Future stores only values.
#
# Correct:
#
# Future stores values
# or exceptions.

# ============================================================
# COMMON MISCONCEPTION #3
# ============================================================

# Wrong:
#
# result() always returns.
#
# Correct:
#
# result() may raise.

# ============================================================
# COMMON MISCONCEPTION #4
# ============================================================

# Wrong:
#
# Failed task means all tasks failed.
#
# Correct:
#
# Each Future tracks its own outcome.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What happens when a task
# raises an exception?
#
# Answer:
#
# The Future stores it.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# When is the exception
# typically observed?
#
# Answer:
#
# During result().

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Why are Futures better than
# raw threads for error handling?
#
# Answer:
#
# They propagate failures back
# to the caller.

# ============================================================
# INTERVIEW QUESTION #4
# ============================================================

# What can a Future store?
#
# Answer:
#
# Result
#
# or
#
# Exception

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now know:
#
# submit()
# Future
# done()
# result()
# Exception propagation
#
# New question:
#
# What if we have:
#
# 100 tasks?
#
# Do we really want:
#
# submit()
# submit()
# submit()
# ...
#
# The next file introduces:
#
# executor.map()

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Futures solve the silent
# failure problem.
#
# Futures store:
#
# Results
# or
# Exceptions.
#
# result() re-raises failures.
#
# try/except works naturally.
#
# This is one of the biggest
# advantages of Executors over
# raw threads.
