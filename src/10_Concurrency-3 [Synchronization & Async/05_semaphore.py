"""
MODULE FILE NAME ============================================================

05_semaphore.py

Topics Covered
--------------
• Why Lock is Sometimes Too Restrictive
• What is a Semaphore?
• Binary vs Counting Semaphore
• threading.Semaphore
• acquire() and release()
• Real-world Use Cases
• Semaphore vs Lock
• Common Mistakes
• Best Practices

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# In the previous chapter, we learned that a Lock allows only ONE thread to
# enter a critical section at any given time.
#
# This guarantees correctness, but sometimes it is more restrictive than
# necessary.
#
# Consider these situations:
#
# • A database has 10 available connections.
# • A web server can process 50 requests simultaneously.
# • A parking lot has 100 parking spaces.
#
# In all these cases, allowing only ONE thread to proceed would waste
# available resources.
#
# We need a mechanism that allows a LIMITED number of threads to enter
# simultaneously.
#
# That mechanism is called a Semaphore.

# =============================================================================
# RESTAURANT ANALOGY
# =============================================================================

# Imagine a restaurant with five tables.
#
# Customers arrive continuously.
#
# If a table is available, the customer is seated immediately.
#
# If all tables are occupied, new customers must wait.
#
# As soon as a customer leaves, another waiting customer is allowed in.
#
# The restaurant does NOT allow unlimited customers.
#
# It also does NOT allow only one customer.
#
# It allows exactly as many customers as resources permit.
#
# This is precisely how a Semaphore works.

# ASCII Diagram
#
# Capacity = 3
#
# Thread A ---> Inside
# Thread B ---> Inside
# Thread C ---> Inside
# Thread D ---> Waiting
# Thread E ---> Waiting

# =============================================================================
# WHAT IS A SEMAPHORE?
# =============================================================================

# A Semaphore maintains an internal counter.
#
# The counter represents the number of available permits.
#
# Before entering the protected section, a thread must acquire a permit.
#
# When the thread finishes its work, it releases the permit.
#
# Another waiting thread may then continue.

# =============================================================================
# CREATING A SEMAPHORE
# =============================================================================

import threading
import time

semaphore = threading.Semaphore(3)

def worker(worker_id):
    print(f"Worker {worker_id} waiting...")

    with semaphore:
        print(f"Worker {worker_id} entered.")
        time.sleep(2)
        print(f"Worker {worker_id} leaving.")

# Uncomment to experiment.
#
# for i in range(1, 8):
#     threading.Thread(target=worker, args=(i,)).start()

# =============================================================================
# WHAT HAPPENS INTERNALLY?
# =============================================================================

# Initial permits = 3
#
# Worker 1 acquires a permit.
# Remaining permits = 2
#
# Worker 2 acquires a permit.
# Remaining permits = 1
#
# Worker 3 acquires a permit.
# Remaining permits = 0
#
# Worker 4 attempts to enter.
#
# No permits remain.
#
# Worker 4 automatically waits.
#
# When Worker 2 finishes:
#
# release()
#
# Remaining permits = 1
#
# Worker 4 immediately wakes and acquires that permit.

# =============================================================================
# acquire() AND release()
# =============================================================================

# Internally, a semaphore provides two important operations.
#
# acquire()
# ----------
# Request one permit.
#
# If a permit is available, continue immediately.
#
# Otherwise, wait.
#
# release()
# ----------
# Return one permit.
#
# Waiting threads may now continue.
#
# Using "with semaphore:" automatically performs both operations safely.

# =============================================================================
# VISUALIZATION
# =============================================================================

# Permits = 2
#
# Initial
#
# [Permit] [Permit]
#
# Thread A enters
#
# [Used] [Permit]
#
# Thread B enters
#
# [Used] [Used]
#
# Thread C waits
#
# Thread A leaves
#
# [Permit] [Used]
#
# Thread C enters

# =============================================================================
# BINARY VS COUNTING SEMAPHORE
# =============================================================================

# Binary Semaphore
# ----------------
#
# Maximum permits = 1
#
# Behaves similarly to a Lock.
#
# Counting Semaphore
# ------------------
#
# Maximum permits > 1
#
# Multiple threads may enter simultaneously.

# =============================================================================
# REAL-WORLD USE CASES
# =============================================================================

# Database Connection Pool
#
# Suppose only five database connections are available.
#
# A semaphore initialized with five permits ensures that no more than five
# threads use the database simultaneously.
#
# ------------------------------------------------------------
#
# File Download Manager
#
# Limit downloads to three concurrent files.
#
# ------------------------------------------------------------
#
# API Rate Limiting
#
# Allow only a fixed number of requests to execute in parallel.
#
# ------------------------------------------------------------
#
# Parking Lot
#
# Number of permits equals available parking spaces.

# =============================================================================
# SEMAPHORE VS LOCK
# =============================================================================

# Lock
# ----
#
# Only ONE thread enters.
#
# Suitable for protecting shared mutable data.
#
# Semaphore
# ---------
#
# Limited number of threads may enter.
#
# Suitable for managing finite resources.

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# Mistake
#
# Using a Semaphore when exclusive access is required.
#
# If only one thread should modify shared data,
# use a Lock instead.
#
# ------------------------------------------------------------
#
# Mistake
#
# Forgetting to release a permit.
#
# Waiting threads may block forever because permits are never returned.
#
# ------------------------------------------------------------
#
# Mistake
#
# Assuming Semaphores eliminate race conditions automatically.
#
# A Semaphore limits concurrency.
#
# It does NOT automatically make shared data thread-safe.

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. What problem does a Semaphore solve?
#
# It limits how many threads may access a finite resource simultaneously.
#
# ------------------------------------------------------------
#
# Q. How is Semaphore different from Lock?
#
# A Lock permits exactly one thread.
#
# A Semaphore permits a configurable number of threads.
#
# ------------------------------------------------------------
#
# Q. Give practical uses of Semaphore.
#
# Database connection pools
# Thread pools
# Parking lots
# API rate limiting
# Resource allocation

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

# ✓ A Semaphore manages a fixed number of permits.
# ✓ Threads acquire permits before entering.
# ✓ Threads release permits after completing their work.
# ✓ Counting Semaphores allow limited concurrency.
# ✓ Locks provide exclusive access.
# ✓ Semaphores manage limited shared resources.

# =============================================================================
# BRIDGE
# =============================================================================

# We have now explored several synchronization primitives:
#
# • Lock
# • RLock
# • Condition
# • Event
# • Semaphore
#
# The next step is to combine these ideas to solve one of the most famous
# concurrency problems:
#
# The Producer–Consumer Problem.
