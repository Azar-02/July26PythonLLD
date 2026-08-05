"""
============================================================
PART 03
SINGLETON THREAD SAFETY
============================================================

Topics Covered

1. Eager Loading
2. Lazy Loading
3. Why concurrency breaks Singleton
4. Race Condition
5. Lock-based Singleton
6. Double Checked Locking
7. Important observations
8. Interview notes
9. Board summary
"""

import threading
import time

# ============================================================
# MOTIVATION
# ============================================================

# Our Singleton from the previous class works perfectly...
#
# ...only if one thread creates the object.
#
# Modern backend applications handle many requests
# simultaneously.
#
# Multiple requests often mean multiple threads.
#
# Today we discover why that breaks our Singleton.

# ============================================================
# EAGER LOADING
# ============================================================

# One simple idea is:
#
# Create the Singleton immediately when the module loads.
#
# This avoids race conditions because the object already
# exists before any request arrives.

class EagerDBConnection:
    def __init__(self):
        print("Creating expensive DB connection...")

instance = EagerDBConnection()

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# If nobody ever uses the database,
# was creating this object useful?
#
# Expected Answer
#
# No.
#
# We paid the cost during application startup.

# ============================================================
# THEORY
# ============================================================

# Eager Loading
#
# + Very simple
# + No race during creation
#
# -
# Slower application startup.
#
# -
# Runtime configuration cannot influence creation.

# ============================================================
# LAZY LOADING
# ============================================================

# Lazy Loading waits until the first user actually
# needs the object.

class LazyConnection:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# ============================================================
# ============================================================

# Looks perfect.
#
# But what happens if two requests arrive
# at exactly the same moment?

# ============================================================
# DISCOVERING THE RACE CONDITION
# ============================================================

# Imagine this timeline:
#
# Thread A
# checks _instance
#
#             None
#
# Before A creates the object...
#
# Thread B also checks _instance.
#
# It also sees None.
#
# Both threads now create objects.
#
# Singleton broken.

# ============================================================
# MEMORY TIMELINE
# ============================================================

# Tick 1
#
# Thread A -> None
# Thread B -> None
#
# Tick 2
#
# Thread A creates Object 1
#
# Tick 3
#
# Thread B creates Object 2
#
# Result:
#
# Two Singleton objects!


# ============================================================
# DEMO
# ============================================================

class UnsafeSingleton:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            time.sleep(0.01)
            cls._instance = super().__new__(cls)

        return cls._instance

objects = []

def worker():
    objects.append(UnsafeSingleton())

threads = [threading.Thread(target=worker) for _ in range(8)]

for t in threads:
    t.start()

for t in threads:
    t.join()

unique = len({id(x) for x in objects})

print("="*60)
print("Unsafe Singleton")
print("Unique Objects:", unique)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Depending on scheduling you may occasionally observe
# more than one object.
#
# Race conditions are timing problems.
#
# They are difficult to reproduce consistently.

# ============================================================
# ============================================================

# What simple tool allows only one thread
# to execute a critical section?

# --
#
# threading.Lock()

# ============================================================
# LOCK BASED SINGLETON
# ============================================================

class SafeSingleton:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

safe = [SafeSingleton() for _ in range(2)]

print()
print("Lock Based Singleton")
print(safe[0] is safe[1])

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Correct.
#
# But every constructor call acquires the lock,
# even after the object already exists.

# ============================================================
# DOUBLE CHECKED LOCKING
# ============================================================

class BetterSingleton:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        if cls._instance is None: 

            with cls._lock:

                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

a = BetterSingleton()
b = BetterSingleton()

print()
print("Double Checked Locking")
print(a is b)

# ============================================================
# DISCUSSION
# ============================================================

# Why do we check twice?
#
# Student Thinking
#
# "The first check should be enough."
#
# Reveal
#
# Another thread may have created the object while
# this thread was waiting for the lock.
#
# The second check prevents duplicate creation.

# ============================================================
# TICK BY TICK
# ============================================================

# Tick 1
# A -> outer check -> None
# B -> outer check -> None
#
# Tick 2
# A acquires lock
# B waits
#
# Tick 3
# A creates object
#
# Tick 4
# A releases lock
#
# Tick 5
# B acquires lock
# Inner check -> object exists
# Reuse existing object

# Animation
#
# Play:
# Double Checked Locking animation.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# The GIL does NOT make this automatically safe.
#
# The GIL prevents simultaneous bytecode execution.
#
# It does not make multiple bytecode instructions
# behave as one atomic operation.

# ============================================================
# INTERVIEW OBSERVATIONS
# ============================================================

# Frequently Asked
#
# Explain race condition.
#
# Why isn't the GIL enough?
#
# Why is the second check necessary?
#
# Difference between simple locking and
# double checked locking.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Lazy Singleton
#        |
# Race Condition
#        |
# Lock
#        |
# Double Checked Locking
#        |
# Thread Safe Singleton

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# We now have a production-safe Singleton.
#
# But modern engineers increasingly rely on AI to
# generate such code.
#
# Can AI always generate a correct Singleton?
#
# That is our next discussion.
