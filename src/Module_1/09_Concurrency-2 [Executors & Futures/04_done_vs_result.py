"""
============================================================
CONCURRENCY-2
FILE : 04_done_vs_result.py
============================================================

Topics Covered
--------------
1. Motivation
2. Revisiting Future
3. Understanding done()
4. Understanding result()
5. Non-Blocking vs Blocking
6. Future Timelines
7. Multiple Futures
8. Polling Patterns
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

# In the previous file we learned:
#
# submit()
# Future
#
# We also learned:
#
# done()
# result()
#
# At first glance these methods
# seem very small.
#
# Just two functions.
#
# But understanding the difference
# between them is one of the most
# important parts of the Executor API.

# ============================================================
# RECAP
# ============================================================

# Future represents:
#
# Work that may finish later.
#
# Future is:
#
# NOT the final answer.
#
# Future is:
#
# A handle to the answer.

# ============================================================
# SIMPLE TASK
# ============================================================

def fetch_user(user_id):

    time.sleep(3)

    return f"User-{user_id}"

# ============================================================
# THE CENTRAL QUESTION
# ============================================================

# Once we have a Future:
#
# How do we know whether
# the work has completed?
#
# How do we retrieve the answer?

# ============================================================
# FUTURE CREATION
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        101
    )

# ============================================================
# ASK LEARNERS
# ============================================================

# Immediately after submit():
#
# Has the task finished?
#
# Probably not.
#
# So how do we check?

# ============================================================
# INTRODUCING done()
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        101
    )

    print(
        future.done()
    )

# ============================================================
# OBSERVATION
# ============================================================

# Usually:
#
# False
#
# because the task is still running.

# ============================================================
# WHAT DOES done() MEAN?
# ============================================================

# done()
#
# asks:
#
# "Has the task finished?"

# ============================================================
# IMPORTANT DETAIL
# ============================================================

# done()
#
# does NOT:
#
# Return the answer.
#
# Return partial work.
#
# Return progress.
#
# It simply returns:
#
# True
# or
# False

# ============================================================
# ANALOGY
# ============================================================

# Imagine:
#
# Restaurant token #57
#
# done() means:
#
# "Is my food ready?"
#
# Answer:
#
# Yes
# or
# No

# ============================================================
# ASK LEARNERS
# ============================================================

# Does asking:
#
# "Is my food ready?"
#
# give you the food?
#
# No.
#
# Same idea here.

# ============================================================
# INTRODUCING result()
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        500
    )

    answer = future.result()

    print(answer)

# ============================================================
# WHAT DOES result() MEAN?
# ============================================================

# result()
#
# asks:
#
# "Give me the answer."

# ============================================================
# IMPORTANT DIFFERENCE
# ============================================================

# done()
#
# asks for status.
#
# result()
#
# asks for data.

# ============================================================
# ASK LEARNERS
# ============================================================

# Suppose:
#
# Task needs:
#
# 30 seconds.
#
# We immediately call:
#
# future.result()
#
# What happens?

# ============================================================
# ANSWER
# ============================================================

# result() waits.

# ============================================================
# VERY IMPORTANT WORD
# ============================================================

# result() is:
#
# Blocking
#
# It pauses the caller until
# work completes.

# ============================================================
# TIMELINE #1
# ============================================================

# submit()
#     ↓
# Future returned
#     ↓
# result()
#     ↓
# Wait...
# Wait...
# Wait...
#     ↓
# Answer returned

# ============================================================
# OBSERVATION
# ============================================================

# The Future allowed us to
# continue working.
#
# But result() chooses to wait.

# ============================================================
# NON-BLOCKING VS BLOCKING
# ============================================================

# submit()
#
# Non-blocking
#
# returns immediately

# ============================================================

# done()
#
# Non-blocking
#
# checks status

# ============================================================

# result()
#
# Blocking
#
# waits for completion

# ============================================================
# THIS IS THE CORE LESSON
# ============================================================

# Many students remember:
#
# Future
#
# but forget:
#
# result() blocks.

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
        2
    )

    future3 = executor.submit(
        fetch_user,
        3
    )

# ============================================================
# ASK LEARNERS
# ============================================================

# What is happening now?
#
# Answer:
#
# Three tasks may be running
# simultaneously.

# ============================================================
# COMMON BEGINNER PATTERN
# ============================================================

# future1.result()
# future2.result()
# future3.result()

# ============================================================
# OBSERVATION
# ============================================================

# This works.
#
# But notice:
#
# We immediately start waiting.

# ============================================================
# BETTER MENTAL MODEL
# ============================================================

# Submit work
#     ↓
# Submit more work
#     ↓
# Do other useful work
#     ↓
# Collect results later

# ============================================================
# WHY FUTURES EXIST
# ============================================================

# Futures allow:
#
# Work
#
# and
#
# Waiting
#
# to become separate actions.

# ============================================================
# POLLING WITH done()
# ============================================================

with ThreadPoolExecutor(
    max_workers=1
) as executor:

    future = executor.submit(
        fetch_user,
        100
    )

    while not future.done():

        print(
            "Still working..."
        )

        time.sleep(0.5)

# ============================================================
# OBSERVATION
# ============================================================

# We are repeatedly asking:
#
# Finished yet?
#
# Finished yet?
#
# Finished yet?

# ============================================================
# REAL-WORLD ANALOGY
# ============================================================

# Imagine repeatedly checking:
#
# "Has my package arrived?"
#
# That's essentially polling.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# done()
#
# lets us observe.
#
# result()
#
# lets us collect.

# ============================================================
# PREDICTION EXERCISE
# ============================================================

# Which call is safer if
# you cannot afford to wait?
#
# A) done()
# B) result()

# ============================================================
# ANSWER
# ============================================================

# done()
#
# because it does not block.

# ============================================================
# COMMON MISTAKE #1
# ============================================================

# Wrong:
#
# future.done()
#
# returns the answer.
#
# Correct:
#
# Returns only True/False.

# ============================================================
# COMMON MISTAKE #2
# ============================================================

# Wrong:
#
# result() is instant.
#
# Correct:
#
# result() may wait.

# ============================================================
# COMMON MISTAKE #3
# ============================================================

# Wrong:
#
# submit()
# result()
# submit()
# result()
#
# This often destroys much of
# the concurrency benefit.

# ============================================================
# WHY THIS MATTERS
# ============================================================

# Executors help us overlap work.
#
# Calling result() too early
# often removes that advantage.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What does done() return?
#
# Answer:
#
# True or False.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# What does result() return?
#
# Answer:
#
# Final result of the task.

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Which method blocks?
#
# Answer:
#
# result()

# ============================================================
# INTERVIEW QUESTION #4
# ============================================================

# Which method simply checks
# completion status?
#
# Answer:
#
# done()

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# So far we assumed:
#
# Work succeeds.
#
# But what if:
#
# The worker crashes?
#
# API fails?
#
# Database becomes unavailable?
#
# The next file explains:
#
# Future Exception Handling

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Future represents work.
#
# done() checks status.
#
# result() retrieves answer.
#
# done() is non-blocking.
#
# result() is blocking.
#
# Futures separate:
#
# Work submission
#
# from
#
# Result collection.
#
# Next:
#
# Exception handling
# with Futures.
