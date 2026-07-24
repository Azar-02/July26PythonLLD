"""
MODULE FILE NAME ============================================================

08_lab_and_summary.py

Topics Covered
--------------
• Concurrency Revision
• Practical Lab Exercises
• Debugging Challenges
• Interview Checklist
• Choosing the Right Synchronization Primitive
• Final Summary

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# Learning concurrency is similar to learning to drive.
#
# Reading the rules is important, but confidence comes from practice.
#
# This chapter focuses on applying the ideas learned throughout the module.
#
# Instead of introducing new synchronization primitives, we will revise,
# compare, and practice using the existing ones.

# =============================================================================
# QUICK RECAP OF THE JOURNEY
# =============================================================================

# Async Programming
#        │
#        ▼
# Race Conditions
#        │
#        ▼
# Lock / RLock
#        │
#        ▼
# Condition / Event
#        │
#        ▼
# Semaphore
#        │
#        ▼
# Producer–Consumer
#        │
#        ▼
# queue.Queue
#
# Each topic solved a limitation discovered in the previous one.

# =============================================================================
# DECISION GUIDE
# =============================================================================

# Which tool should you use?
#
# Need exclusive access to shared data?
#     → Lock
#
# Need nested locking?
#     → RLock
#
# Need to wait until something becomes true?
#     → Condition
#
# Need to broadcast "start" or "stop"?
#     → Event
#
# Need to limit concurrent access?
#     → Semaphore
#
# Need a thread-safe producer-consumer buffer?
#     → queue.Queue

# =============================================================================
# LAB 1 – FIND THE RACE CONDITION
# =============================================================================

import threading

counter = 0

def increment():
    global counter
    for _ in range(10000):
        counter += 1

# Exercise:
# 1. Create two threads.
# 2. Run increment() in both.
# 3. Observe the final value.
# 4. Fix the bug using threading.Lock().

# =============================================================================
# LAB 2 – PROTECT THE CRITICAL SECTION
# =============================================================================

# Modify the previous program:
#
# • Create a Lock.
# • Protect only the counter update.
# • Compare the outputs before and after synchronization.
#
# Reflection:
# Why should the critical section be kept as small as possible?

# =============================================================================
# LAB 3 – CONDITION PRACTICE
# =============================================================================

# Create:
#
# • One producer
# • Two consumers
#
# Use Condition to coordinate them.
#
# Questions:
# • What happens when consumers start first?
# • What happens if notify() is removed?
# • What changes when notify_all() is used?

# =============================================================================
# LAB 4 – SEMAPHORE
# =============================================================================

import time

parking = threading.Semaphore(3)

def car(car_id):
    with parking:
        print(f"Car {car_id} entered")
        time.sleep(1)
        print(f"Car {car_id} left")

# Exercise:
# Launch 8 cars simultaneously.
#
# Observe that only three are inside the parking lot at any moment.

# =============================================================================
# LAB 5 – QUEUE
# =============================================================================

import queue

tasks = queue.Queue()

# Exercise:
#
# • Create one producer.
# • Create multiple consumers.
# • Insert ten tasks.
# • Use task_done() and join().
#
# Observe how Queue removes the need for manual wait() and notify() calls.

# =============================================================================
# DEBUGGING CHALLENGES
# =============================================================================

# Challenge 1
#
# Why does the following program sometimes produce different outputs?
#
# Hint:
# Shared mutable state.
#
# ------------------------------------------------------------
#
# Challenge 2
#
# A thread never wakes from wait().
#
# Possible causes:
# • notify() never called
# • wrong condition checked
# • deadlock
#
# ------------------------------------------------------------
#
# Challenge 3
#
# q.join() never returns.
#
# Hint:
# Was task_done() called?

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# • Protecting too much code with a Lock.
# • Forgetting to release manually acquired locks.
# • Using if instead of while before wait().
# • Forgetting notify().
# • Replacing Queue with a normal list.
# • Forgetting task_done().
# • Assuming concurrency bugs always reproduce consistently.

# =============================================================================
# INTERVIEW RAPID FIRE
# =============================================================================

# Q. What is a race condition?
#
# Q. What is a critical section?
#
# Q. Difference between Lock and RLock?
#
# Q. Why should wait() be inside a while loop?
#
# Q. Difference between Condition and Event?
#
# Q. Difference between Lock and Semaphore?
#
# Q. Why is Queue thread-safe?
#
# Q. What is the purpose of task_done()?
#
# Try answering these without looking at previous chapters.

# =============================================================================
# MINI PROJECT IDEAS
# =============================================================================

# Beginner
# --------
# Thread-safe bank account.
#
# Intermediate
# ------------
# Parking lot simulator using Semaphore.
#
# Advanced
# --------
# Producer-consumer log processing system using Queue.
#
# Challenge
# ---------
# Download manager with multiple worker threads and a bounded Queue.

# =============================================================================
# FINAL KEY TAKEAWAYS
# =============================================================================

# ✓ Concurrency improves responsiveness but introduces coordination problems.
# ✓ Shared mutable state requires synchronization.
# ✓ Locks provide mutual exclusion.
# ✓ Conditions coordinate waiting threads.
# ✓ Events broadcast simple signals.
# ✓ Semaphores limit concurrent access.
# ✓ Queue offers a safe, high-level producer-consumer abstraction.
# ✓ Correctness is always more important than parallelism.

# =============================================================================
# FINAL SUMMARY
# =============================================================================

# Congratulations!
#
# You have completed a practical introduction to Python concurrency.
#
# More importantly, you have learned an important engineering principle:
#
# Start by understanding the underlying problem.
# Then choose the simplest synchronization primitive that solves it.
#
# Great software engineers do not use advanced tools everywhere.
# They use the right tool in the right situation.
#
# Keep experimenting with the lab exercises, modify the examples,
# and observe how threads interact in real programs.
#
# That hands-on experience is what turns theory into intuition.
