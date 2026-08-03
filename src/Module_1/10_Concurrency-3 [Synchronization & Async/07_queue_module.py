"""
MODULE FILE NAME ============================================================

07_queue_module.py

Topics Covered
--------------
• Why queue.Queue Exists
• Problems with Manual Synchronization
• Creating a Queue
• put() and get()
• Blocking Behavior
• Producer–Consumer using Queue
• task_done() and join()
• Queue vs List
• Queue vs Manual Condition
• Common Mistakes
• Interview Discussion

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# In the previous chapter, we solved the Producer–Consumer problem using:
#
# • Lock
# • Condition
# • wait()
# • notify()
#
# The solution worked...
#
# But notice how much synchronization code we had to write.
#
# As programmers, we should always ask:
#
# "Can this be made simpler?"
#
# The Python standard library answers that question with queue.Queue.

# =============================================================================
# THE PROBLEM WITH THE MANUAL APPROACH
# =============================================================================

# Manual synchronization requires us to manage:
#
# • Shared buffer
# • Lock
# • Condition
# • wait()
# • notify()
# • Buffer full checks
# • Buffer empty checks
#
# Forgetting even one of these can introduce subtle concurrency bugs.
#
# Python provides a safer abstraction.

# =============================================================================
# WHAT IS queue.Queue?
# =============================================================================

# queue.Queue is a thread-safe FIFO (First-In, First-Out) data structure.
#
# Thread-safe means multiple threads can safely use it at the same time.
#
# Internally, Queue already contains:
#
# • Locks
# • Condition variables
# • Synchronization logic
#
# Therefore, we usually do NOT need to write those ourselves.

import threading
import queue
import time

q = queue.Queue(maxsize=5)

# =============================================================================
# PRODUCER USING Queue
# =============================================================================

def producer():
    for item in range(1, 11):
        print(f"Producing {item}")
        q.put(item)
        time.sleep(0.3)

# =============================================================================
# CONSUMER USING Queue
# =============================================================================

def consumer():
    while True:
        item = q.get()
        print(f"Consumed {item}")

        time.sleep(0.5)

        q.task_done()

        if item == 10:
            break

# Uncomment to test.
#
# threading.Thread(target=producer).start()
# threading.Thread(target=consumer).start()

# =============================================================================
# WHAT DOES put() DO?
# =============================================================================

# q.put(item)
#
# If space exists,
# the item is inserted immediately.
#
# If the queue is already full,
# the producer automatically waits.
#
# No manual wait() call is needed.

# =============================================================================
# WHAT DOES get() DO?
# =============================================================================

# q.get()
#
# If an item exists,
# it is returned immediately.
#
# If the queue is empty,
# the consumer automatically waits.
#
# Again, no manual synchronization code is required.

# =============================================================================
# VISUALIZATION
# =============================================================================

# Capacity = 5
#
# []
#
# put(1)
#
# [1]
#
# put(2)
#
# [1][2]
#
# get()
#
# [2]
#
# Queue becomes full...
#
# Producer sleeps automatically.
#
# Consumer removes an item.
#
# Producer wakes automatically.

# =============================================================================
# WHY Queue IS THREAD-SAFE
# =============================================================================

# Queue internally protects its data using synchronization primitives.
#
# Conceptually, Queue performs operations like:
#
# Acquire internal lock
# Modify queue
# Wake waiting threads if needed
# Release lock
#
# Users of Queue do not have to write this logic manually.

# =============================================================================
# task_done() AND join()
# =============================================================================

# task_done()
# -----------
#
# Indicates that one retrieved task has been completely processed.
#
# join()
# ------
#
# Blocks until every queued task has been marked complete.
#
# Example
#
# producer thread
#
# q.join()
#
# waits until consumers call task_done() for every item.

# =============================================================================
# Queue VS LIST
# =============================================================================

# List
# ----
#
# Not inherently thread-safe.
#
# Requires manual synchronization.
#
# Queue
# -----
#
# Thread-safe.
#
# Automatically coordinates producers and consumers.

# =============================================================================
# Queue VS MANUAL CONDITION
# =============================================================================

# Manual Solution
# ---------------
#
# Buffer
# Lock
# Condition
# wait()
# notify()
#
# Queue Solution
# --------------
#
# Queue
# put()
# get()
#
# Much simpler.
#
# Fewer opportunities for bugs.

# =============================================================================
# REAL-WORLD APPLICATIONS
# =============================================================================

# Queue is widely used in:
#
# • Web servers
# • Background job systems
# • Message processing
# • Logging frameworks
# • Task schedulers
# • Thread pools
# • Print services
# • Data pipelines

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# Mistake
#
# Forgetting task_done() after get().
#
# join() may wait forever.
#
# ------------------------------------------------------------
#
# Mistake
#
# Replacing Queue with a normal list in multi-threaded code.
#
# Lists are not designed for coordinated thread communication.
#
# ------------------------------------------------------------
#
# Mistake
#
# Assuming Queue removes the need for careful program design.
#
# Queue simplifies synchronization,
# but developers must still think about workflow and termination.

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. Why should Queue be preferred over a shared list?
#
# Because Queue is thread-safe and automatically handles synchronization.
#
# ------------------------------------------------------------
#
# Q. What happens if Queue becomes full?
#
# Producers block until space becomes available.
#
# ------------------------------------------------------------
#
# Q. What happens if Queue is empty?
#
# Consumers block until new items arrive.
#
# ------------------------------------------------------------
#
# Q. What is the purpose of task_done()?
#
# It informs Queue that processing of one retrieved task has finished.

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

# ✓ Queue is a thread-safe FIFO data structure.
# ✓ put() blocks when the queue is full.
# ✓ get() blocks when the queue is empty.
# ✓ Internal synchronization is handled automatically.
# ✓ Queue dramatically simplifies Producer–Consumer implementations.
# ✓ task_done() and join() help coordinate completion of queued work.

# =============================================================================
# CHAPTER SUMMARY
# =============================================================================

# Across the last several chapters, we learned how threads communicate and
# coordinate safely.
#
# We progressed from:
#
# Race Conditions
#        ↓
# Lock / RLock
#        ↓
# Condition / Event
#        ↓
# Semaphore
#        ↓
# Manual Producer–Consumer
#        ↓
# queue.Queue
#
# This progression illustrates an important software engineering principle:
#
# Build the fundamentals first, then use higher-level abstractions that
# encapsulate those fundamentals.
