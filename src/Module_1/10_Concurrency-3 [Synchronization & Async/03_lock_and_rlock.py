"""
MODULE FILE NAME ============================================================

03_lock_and_rlock.py

Topics Covered
--------------
• Why race conditions need synchronization
• Critical Section
• threading.Lock
• with lock
• Lock lifecycle
• Deadlock
• threading.RLock
• Lock vs RLock
• Best Practices

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# In the previous chapter we discovered that multiple threads can corrupt
# shared data.
#
# The obvious question is:
#
# "Can we allow only ONE thread to update the shared data at a time?"
#
# The answer is Yes.
#
# Python provides synchronization primitives for exactly this purpose.
#
# The most fundamental one is Lock.

# =============================================================================
# THE IDEA OF A LOCK
# =============================================================================

# Imagine a room that contains important company documents.
#
# Only one employee may enter at a time.
#
# Whoever enters first takes the key.
#
# Everyone else waits outside until the key is returned.
#
# A Lock behaves exactly like this key.

# ASCII Visualization
#
#        Lock
#         🔑
#          |
#  Thread A ---> Critical Section
#  Thread B ---> Waiting...
#  Thread C ---> Waiting...

# =============================================================================
# WHAT IS A CRITICAL SECTION?
# =============================================================================

# A Critical Section is the part of the program that accesses shared data.
#
# Only one thread should execute this section at a time.
#
# Everything outside the critical section can usually execute concurrently.

# =============================================================================
# FIRST EXAMPLE
# =============================================================================

import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter

    for _ in range(100_000):
        with lock:
            counter += 1

# Uncomment to test.
#
# t1 = threading.Thread(target=increment)
# t2 = threading.Thread(target=increment)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(counter)

# =============================================================================
# WHAT DOES "with lock:" DO?
# =============================================================================

# Entering the with-block:
#
#     lock.acquire()
#
# Exiting the with-block:
#
#     lock.release()
#
# The context manager guarantees that the lock is released even if an exception
# occurs.
#
# This is why using "with lock:" is preferred over manually calling
# acquire() and release().

# =============================================================================
# EXECUTION TIMELINE
# =============================================================================

# Thread A          Thread B
# --------          --------
#
# acquire()
# update counter
# release()
#                   acquire()
#                   update counter
#                   release()
#
# Notice that both threads execute.
#
# They simply do not execute the critical section simultaneously.

# =============================================================================
# WHY DOES THE ANSWER BECOME CORRECT?
# =============================================================================

# Earlier:
#
# READ
# ADD
# WRITE
#
# could be interrupted.
#
# Now the entire sequence executes while holding the lock.
#
# Other threads must wait until the lock becomes available.
#
# Therefore no Lost Update occurs.

# =============================================================================
# PERFORMANCE TRADE-OFF
# =============================================================================

# Locks improve correctness.
#
# However, locking also reduces parallelism.
#
# While one thread holds the lock, every other thread waits.
#
# Therefore:
#
# Lock ONLY the code that actually needs protection.
#
# Smaller critical sections generally lead to better performance.

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# Mistake
#
# Locking an entire function when only one statement modifies shared data.
#
# ------------------------------------------------------------
#
# Mistake
#
# Forgetting to release a manually acquired lock.
#
# Use "with lock:" whenever possible.
#
# ------------------------------------------------------------
#
# Mistake
#
# Assuming locks make every program faster.
#
# Locks improve correctness, not speed.

# =============================================================================
# A NEW PROBLEM
# =============================================================================

# Consider this situation.
#
# A function acquires a lock.
#
# Inside that function, another function is called.
#
# The second function also tries to acquire the SAME lock.
#
# What happens?

# =============================================================================
# DEADLOCK
# =============================================================================

lock = threading.Lock()

def inner():
    with lock:
        print("Inside inner()")

def outer():
    with lock:
        inner()

# Calling outer() would hang forever because the same thread attempts to
# acquire a Lock that it already owns.

# =============================================================================
# WHY DOES IT HAPPEN?
# =============================================================================

# A normal Lock does not remember who owns it.
#
# It only knows whether it is available.
#
# Therefore the same thread waits for itself forever.
#
# This situation is called a Deadlock.

# =============================================================================
# ENTER RLOCK
# =============================================================================

# RLock stands for Reentrant Lock.
#
# It allows the SAME thread to acquire the lock multiple times.
#
# Internally it maintains:
#
# • Owner thread
# • Acquisition count
#
# The lock is completely released only when the acquisition count becomes zero.

rlock = threading.RLock()

# Replace Lock() with RLock() in nested locking scenarios.

# =============================================================================
# LOCK VS RLOCK
# =============================================================================

# Lock
# ----
# Faster
# Simpler
# Cannot be acquired twice by the same thread.
#
# RLock
# -----
# Slightly heavier
# Maintains ownership information
# Safe for nested or recursive locking.

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. What is the purpose of a Lock?
#
# To ensure that only one thread executes a critical section at a time.
#
# ------------------------------------------------------------
#
# Q. What is a Critical Section?
#
# The portion of code that accesses shared mutable data.
#
# ------------------------------------------------------------
#
# Q. When should RLock be preferred?
#
# When the same thread may need to acquire the same lock multiple times,
# such as nested or recursive function calls.
#
# ------------------------------------------------------------
#
# Q. Is RLock always better?
#
# No.
#
# Use Lock unless reentrancy is actually required.

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

# ✓ Locks prevent race conditions by protecting critical sections.
# ✓ Use "with lock:" to automatically acquire and release the lock.
# ✓ Keep critical sections as small as possible.
# ✓ Deadlock can occur if a thread waits on a lock it already owns.
# ✓ RLock solves nested locking by allowing the same thread to re-acquire
#   its own lock.

# =============================================================================
# BRIDGE
# =============================================================================

# Locks answer the question:
#
# "Who may enter?"
#
# The next synchronization primitives answer a different question:
#
# "When should a thread wake up and continue?"
#
# That leads us to Condition and Event.
