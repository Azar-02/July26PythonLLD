"""
MODULE FILE NAME ============================================================

04_condition_and_event.py

Topics Covered
--------------
• Why Lock is not enough
• Waiting vs Mutual Exclusion
• threading.Condition
• wait()
• notify()
• notify_all()
• Why wait() belongs inside a while loop
• threading.Event
• set(), clear(), wait()
• Condition vs Event
• Best Practices

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# A Lock solves one important problem:
#
# "Only one thread should touch this shared data at a time."
#
# But Locks cannot answer another common question:
#
# "How can one thread WAIT until another thread finishes some work?"
#
# Waiting while repeatedly checking a variable wastes CPU time.
#
# We need a smarter mechanism.

# =============================================================================
# THE PROBLEM WITH BUSY WAITING
# =============================================================================

# Imagine a consumer thread waiting for data.
#
# Naive approach:
#
# while not data_ready:
#     pass
#
# This loop continuously checks the condition.
#
# The CPU remains busy even though no useful work is being done.
#
# This technique is called Busy Waiting (or Busy Spinning).

# Common Mistake
#
# Beginners often think this loop is harmless.
#
# In reality it wastes processor time and battery.

# Key Takeaway
#
# Waiting should be passive, not active.

# =============================================================================
# CONDITION – WAIT FOR A SITUATION
# =============================================================================

# A Condition allows a thread to:
#
# 1. Sleep efficiently.
# 2. Wake up only when another thread signals it.
#
# Think of a waiting room in a hospital.
#
# Patients do not repeatedly ask,
# "Is it my turn now?"
#
# They quietly wait until their name is called.

import threading

condition = threading.Condition()
items = []

def consumer():
    with condition:
        while not items:
            condition.wait()
        item = items.pop()
        print("Consumed:", item)

def producer():
    with condition:
        items.append("Book")
        print("Produced: Book")
        condition.notify()

# Uncomment to test.
#
# threading.Thread(target=consumer).start()
# threading.Thread(target=producer).start()

# =============================================================================
# WHAT DOES wait() DO?
# =============================================================================

# condition.wait()
#
# Step 1
# Releases the associated lock.
#
# Step 2
# Puts the thread to sleep.
#
# Step 3
# Waits for another thread to call notify().
#
# Step 4
# Re-acquires the lock before continuing execution.
#
# Visualization
#
# Lock Held
#     |
# wait()
#     |
# Release Lock
#     |
# Sleep
#     |
# notify()
#     |
# Wake Up
#     |
# Re-acquire Lock
#     |
# Continue

# =============================================================================
# WHY USE while INSTEAD OF if?
# =============================================================================

# Beginners often write:
#
# if not items:
#     condition.wait()
#
# This is unsafe.
#
# By the time the thread wakes up,
# another consumer might already have removed the item.
#
# Therefore we must CHECK AGAIN.
#
# Correct pattern:
#
# while not items:
#     condition.wait()

# Common Mistake
#
# Using if instead of while around wait().

# Interview Discussion
#
# Q. Why does wait() appear inside a while loop?
#
# Because the condition may no longer be true after the thread wakes up.

# Key Takeaway
#
# Wake up does NOT guarantee the condition is satisfied.
# Always verify again.

# =============================================================================
# notify() vs notify_all()
# =============================================================================

# notify()
#
# Wakes ONE waiting thread.
#
# notify_all()
#
# Wakes every waiting thread.
#
# Which one should you choose?
#
# notify()
# ----------
# Better when only one thread can make progress.
#
# notify_all()
# ------------
# Better when multiple waiting threads may proceed.

# =============================================================================
# EVENT – A SIMPLE SIGNAL
# =============================================================================

# Sometimes we do not need shared data.
#
# We simply need to tell threads:
#
# "Start now."
#
# "Configuration loaded."
#
# "Server is ready."
#
# This is exactly what Event provides.

start_signal = threading.Event()

def worker(worker_id):
    start_signal.wait()
    print(f"Worker {worker_id} started.")

# Later...
#
# start_signal.set()

# =============================================================================
# HOW EVENT WORKS
# =============================================================================

# Event behaves like an ON/OFF switch.
#
# Initially:
#
# OFF
#
# All waiting threads sleep.
#
# After set():
#
# ON
#
# Every waiting thread wakes immediately.

# Visualization
#
# Event OFF
# ----------
# Worker A waiting
# Worker B waiting
# Worker C waiting
#
# set()
#
# Event ON
# --------
# Worker A running
# Worker B running
# Worker C running

# =============================================================================
# EVENT METHODS
# =============================================================================

# wait()
# ------
# Block until the flag becomes True.
#
# set()
# -----
# Turn the flag ON and wake waiting threads.
#
# clear()
# -------
# Turn the flag OFF again.

# =============================================================================
# CONDITION VS EVENT
# =============================================================================

# Condition
# ---------
# Wait for a changing situation.
#
# Example:
# Queue becomes non-empty.
#
# Event
# -----
# Wait for a simple signal.
#
# Example:
# "Application has started."

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# Mistake
#
# Using busy waiting instead of Condition.
#
# ------------------------------------------------------------
#
# Mistake
#
# Forgetting to call notify().
#
# Waiting threads may sleep forever.
#
# ------------------------------------------------------------
#
# Mistake
#
# Assuming Event stores multiple signals.
#
# Event is simply a shared ON/OFF flag.

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. What problem does Condition solve?
#
# Efficient waiting for shared-state changes.
#
# ------------------------------------------------------------
#
# Q. Why is Event simpler than Condition?
#
# Event only manages a boolean flag.
# It is ideal for broadcasting "start" or "stop" signals.
#
# ------------------------------------------------------------
#
# Q. When would you choose Event over Condition?
#
# When threads only need a signal and not access to shared mutable data.

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

# ✓ Locks protect shared data.
# ✓ Conditions coordinate waiting threads.
# ✓ wait() releases the lock and sleeps.
# ✓ Always wrap wait() inside a while loop.
# ✓ notify() wakes one thread.
# ✓ notify_all() wakes everyone.
# ✓ Event is a simple signalling mechanism using an internal flag.

# =============================================================================
# BRIDGE
# =============================================================================

# Locks allow ONE thread inside.
#
# Conditions coordinate waiting.
#
# The next question is:
#
# "What if we want to allow not one, but THREE threads at the same time?"
#
# That leads us to Semaphore.
