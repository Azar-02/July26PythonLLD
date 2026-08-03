"""
MODULE FILE NAME ============================================================

06_producer_consumer_manual.py

Topics Covered
--------------
• The Producer–Consumer Problem
• Shared Buffer
• Why Synchronization is Needed
• Producer and Consumer Roles
• Manual Coordination using Lock + Condition
• wait() and notify()
• Buffer Full / Buffer Empty
• Common Mistakes
• Interview Discussion

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# Imagine a restaurant kitchen.
#
# The chef prepares food.
# The waiter serves food.
#
# The waiter cannot serve dishes that have not been cooked.
#
# Likewise, the chef cannot keep preparing dishes forever if there is no space
# left on the serving counter.
#
# The chef and waiter must coordinate.
#
# This is the Producer–Consumer Problem.

# =============================================================================
# THE PROBLEM
# =============================================================================

# Producer
# --------
# Creates data.
#
# Consumer
# --------
# Uses data.
#
# Both access the SAME shared buffer.
#
# If the producer writes while the consumer removes data, race conditions may
# occur.
#
# If the buffer becomes empty, consumers should WAIT.
#
# If the buffer becomes full, producers should WAIT.

# ASCII Diagram
#
# Producer ---> [ Buffer ] ---> Consumer
#                  ^
#              Shared Resource

# =============================================================================
# BUILDING THE SOLUTION
# =============================================================================

import threading
import time

BUFFER_SIZE = 5
buffer = []

condition = threading.Condition()

def producer():
    item = 1

    while item <= 10:
        with condition:

            while len(buffer) == BUFFER_SIZE:
                print("Producer waiting (buffer full)")
                condition.wait()

            buffer.append(item)
            print(f"Produced: {item}")

            item += 1

            condition.notify()

        time.sleep(0.3)


def consumer():

    while True:

        with condition:

            while not buffer:
                print("Consumer waiting (buffer empty)")
                condition.wait()

            value = buffer.pop(0)
            print(f"Consumed: {value}")

            condition.notify()

        time.sleep(0.5)

        if value == 10:
            break

# Uncomment to run.
#
# threading.Thread(target=producer).start()
# threading.Thread(target=consumer).start()

# =============================================================================
# WALKTHROUGH
# =============================================================================

# Initial State
#
# Buffer = []
#
# Consumer starts first.
#
# Buffer empty.
#
# Consumer executes:
#
# condition.wait()
#
# Consumer sleeps.
#
# Producer arrives.
#
# Produces first item.
#
# Calls notify().
#
# Consumer wakes, re-acquires the lock, checks the condition again, consumes
# the item and continues.

# =============================================================================
# WHY TWO while LOOPS?
# =============================================================================

# Producer
#
# while len(buffer) == BUFFER_SIZE:
#     wait()
#
# Consumer
#
# while not buffer:
#     wait()
#
# These loops prevent:
#
# • Producing into a full buffer
# • Consuming from an empty buffer
#
# They also protect against spurious wake-ups and changing conditions.

# =============================================================================
# VISUALIZATION
# =============================================================================

# Capacity = 5
#
# []
#
# Producer
#
# [1]
#
# Producer
#
# [1][2]
#
# Consumer
#
# [2]
#
# Producer
#
# [2][3]
#
# Buffer reaches capacity...
#
# Producer waits.
#
# Consumer removes one item.
#
# Producer wakes and continues.

# =============================================================================
# WHY USE Condition?
# =============================================================================

# Could we repeatedly check the buffer?
#
# while not buffer:
#     pass
#
# Yes...
#
# But that wastes CPU time.
#
# Condition allows threads to sleep efficiently until progress becomes
# possible.

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# Mistake
#
# Using if instead of while before wait().
#
# ------------------------------------------------------------
#
# Mistake
#
# Forgetting to call notify().
#
# Waiting threads may never wake.
#
# ------------------------------------------------------------
#
# Mistake
#
# Accessing the shared buffer without holding the Condition's lock.
#
# Every shared buffer operation should occur inside:
#
# with condition:

# =============================================================================
# REAL-WORLD APPLICATIONS
# =============================================================================

# Producer–Consumer appears almost everywhere.
#
# Examples:
#
# • Web servers receiving requests
# • Logging systems
# • Print queues
# • Video streaming
# • Audio playback
# • Message brokers
# • Background job processing

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. What problem does Producer–Consumer solve?
#
# It coordinates threads that generate and process shared data.
#
# ------------------------------------------------------------
#
# Q. Why is Condition used?
#
# To allow producers and consumers to sleep efficiently until work becomes
# available.
#
# ------------------------------------------------------------
#
# Q. Why should wait() always be inside a while loop?
#
# Because the condition may change before the thread resumes execution.

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

# ✓ Producer creates data.
# ✓ Consumer processes data.
# ✓ Both share the same buffer.
# ✓ Condition coordinates waiting and waking.
# ✓ Producers wait when the buffer is full.
# ✓ Consumers wait when the buffer is empty.
# ✓ notify() wakes waiting threads after progress is made.

# =============================================================================
# BRIDGE
# =============================================================================

# Although this solution is correct, it requires us to manually manage:
#
# • Buffer
# • Lock
# • Condition
# • wait()
# • notify()
#
# Python provides a higher-level solution that does this for us:
#
# queue.Queue
#
# That is the focus of the next chapter.
