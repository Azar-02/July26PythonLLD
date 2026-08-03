
"""
MODULE FILE NAME ============================================================

01_async_intro.py

Topics Covered
--------------
1. Why threads eventually hit a scalability wall
2. Why asynchronous programming exists
3. The mental model behind async programming
4. async def
5. await
6. asyncio.run()
7. asyncio.gather()
8. Threads vs Async
9. Common misconceptions about async

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# Suppose you have already learned threading.
#
# Threads solved an important problem:
#
# Instead of waiting for one network request to finish before starting the next,
# multiple requests could overlap.
#
# This was a huge improvement for I/O-bound programs.
#
# Naturally, the next question is:
#
# "If a few threads are good...
# why not create thousands of them?"
#
# This chapter answers that question.

# =============================================================================
# CENTRAL QUESTION
# =============================================================================

# Imagine building a chat server.
#
# There are 10,000 connected users.
#
# Surprisingly, almost every connection is idle.
#
# Most users are simply waiting for someone to send a message.
#
# Should we create one thread for every waiting client?

# =============================================================================
# OBSERVATION — THREADS ARE NOT FREE
# =============================================================================

# Every operating-system thread owns its own stack memory.
#
# The operating system must also schedule every runnable thread.
#
# Constantly switching between thousands of threads takes time.
#
# This switching is called context switching.
#
# Context switching is useful, but it is not free.

# Visualization
#
# Thread A ----\
# Thread B ----- > CPU
# Thread C ----/
#
# Thousands of threads
#      ↓
# More memory
# More scheduling
# More context switching

# =============================================================================
# EXPLANATION
# =============================================================================

# The surprising observation is that most of those threads are not doing work.
#
# They are waiting.
#
# Waiting for:
#
# - Network packets
# - Database responses
# - Files
# - User input
#
# If everybody is waiting, why dedicate one operating-system worker to every
# connection?

# =============================================================================
# ANALOGY — THE WAITER
# =============================================================================

# Imagine a restaurant.
#
# Bad approach:
#
# One waiter stands beside every table waiting for food.
#
# Most waiters spend their time doing absolutely nothing.
#
# Better approach:
#
# One skilled waiter serves many tables.
#
# While one table waits for food, the waiter serves another table.
#
# Nobody wastes time standing idle.
#
# Async programming follows exactly this philosophy.

# =============================================================================
# THE IDEA OF ASYNC
# =============================================================================

# Async tries to overlap waiting instead of creating more workers.
#
# Instead of saying:
#
#     "Let's create another thread."
#
# it says:
#
#     "While I am waiting, let someone else continue."

# =============================================================================
# async def
# =============================================================================

# Motivation
#
# We need functions that are allowed to pause and later continue exactly from
# where they stopped.

# Explanation
#
# async def creates a coroutine.
#
# A coroutine is similar to a normal function, but it can voluntarily suspend
# its execution and resume later.

# Common Mistake
#
# Thinking async def immediately starts running.
#
# It does not.
#
# It merely creates a coroutine function.

# Interview Discussion
#
# Q. Is every async function automatically executed?
#
# No.
#
# It must be awaited or scheduled by the event loop.

# Key Takeaway
#
# async def defines a coroutine.
# It does not automatically execute it.

# =============================================================================
# await
# =============================================================================

# Motivation
#
# How does a coroutine temporarily stop itself?

# Explanation
#
# The answer is await.
#
# await tells the event loop:
#
# "I need to wait here.
# Please run something else until this operation completes."

# Important Observation
#
# await does NOT pause the entire program.
#
# It pauses only the current coroutine.

# Visualization
#
# Coroutine A
#      |
#   await
#      |
# Event Loop
#      |
# Coroutine B
#      |
# Coroutine C

# Common Mistake
#
# Wrong:
# await freezes Python.
#
# Correct:
# Only the current coroutine pauses.

# Interview Discussion
#
# Why is await called cooperative?
#
# Because the coroutine voluntarily gives up execution instead of being forced
# to stop by the operating system.

# Key Takeaway
#
# await is the place where a coroutine allows another coroutine to run.

# =============================================================================
# FIRST PROGRAM
# =============================================================================

import asyncio

async def fetch(name):
    print(f"{name}: start")
    await asyncio.sleep(1)
    print(f"{name}: done")


async def main():
    await asyncio.gather(
        fetch("A"),
        fetch("B"),
        fetch("C")
    )


if __name__ == "__main__":
    asyncio.run(main())

# =============================================================================
# WHAT HAPPENED?
# =============================================================================

# Step 1
# All three coroutines begin almost immediately.
#
# Step 2
# Each coroutine reaches await asyncio.sleep(1).
#
# Step 3
# Instead of blocking one another, each coroutine politely steps aside.
#
# Step 4
# The event loop keeps another coroutine running whenever one is waiting.
#
# Timeline
#
# A ---- await ---------------- done
# B ---- await ---------------- done
# C ---- await ---------------- done
#
# Total execution time is roughly one second instead of three.

# =============================================================================
# THREADS VS ASYNC
# =============================================================================

# Threads
# --------
# Multiple OS threads
# More memory
# Context switching performed by the OS
#
# Async
# -----
# Usually one thread
# Many lightweight coroutines
# Event loop switches work at await points

# =============================================================================
# COMMON MISTAKES ABOUT ASYNC
# =============================================================================

# 1. Async makes CPU-heavy programs faster.
#    It usually does not.
#
# 2. async automatically creates threads.
#    It usually does not.
#
# 3. await blocks the entire application.
#    It blocks only the current coroutine.

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. Why can async servers handle thousands of idle network connections?
#
# Because idle work does not require thousands of operating-system threads.
#
# One event loop can efficiently manage many waiting operations.

# Q. What is the biggest difference between threading and async?
#
# Threads rely on operating-system scheduling.
#
# Async relies on cooperative scheduling at await points.

# =============================================================================
# KEY TAKEAWAY
# =============================================================================

# ✔ Threads solve many I/O problems but become expensive at massive scale.
#
# ✔ Async focuses on overlapping waiting instead of creating more threads.
#
# ✔ async def defines a coroutine.
#
# ✔ await is where a coroutine voluntarily pauses.
#
# ✔ asyncio.run() starts the event loop.
#
# ✔ asyncio.gather() executes multiple coroutines concurrently.

# =============================================================================
# BRIDGE TO THE NEXT CHAPTER
# =============================================================================

# Async solves one kind of scalability problem.
#
# Our next topic is different.
#
# Even if we use ordinary threads, another dangerous problem appears:
#
# Multiple threads modifying the same shared data.
#
# That leads us to Race Conditions.
