
"""
MODULE FILE NAME ============================================================

02_race_conditions_v2.py

Topics Covered
--------------
• Shared State
• Race Conditions
• Why counter += 1 is not Atomic
• Thread Interleaving
• Lost Update
• Non-deterministic Bugs
• Need for Synchronization

===========================================================================
"""

# =============================================================================
# MOTIVATION
# =============================================================================

# Imagine two accountants updating the same bank balance.
#
# Accountant A reads:
#     Balance = ₹1000
#
# Before A writes the new balance, Accountant B also reads:
#     Balance = ₹1000
#
# Both independently calculate a new value.
#
# Whoever writes last silently overwrites the other person's work.
#
# No error is shown.
# No exception is raised.
#
# The final balance is simply... wrong.
#
# Computers suffer from exactly the same problem.
#
# This problem is called a Race Condition.

# =============================================================================
# RECAP – THREADS AND MEMORY
# =============================================================================

# Every thread owns its own stack.
#
# Local variables normally live inside that stack.
#
# However, objects created on the heap can be accessed by multiple threads.
#
# Whenever two or more threads can READ and WRITE the same object, we call that
# object Shared State.
#
#                 Heap Memory
#             +----------------+
# Thread A -->| counter = 0    |<-- Thread B
#             +----------------+
#
# Sharing data is useful...
# but it also introduces danger.

# =============================================================================
# CENTRAL QUESTION
# =============================================================================

# Suppose two threads each increment the same counter 100,000 times.
#
# Mathematical answer:
#
#     100000 + 100000 = 200000
#
# Should the computer ALWAYS produce 200000?
#
# Let's investigate.

import threading

counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1

# Uncomment to experiment.
#
# t1 = threading.Thread(target=increment)
# t2 = threading.Thread(target=increment)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(counter)

# =============================================================================
# EXPECTATION VS REALITY
# =============================================================================

# You may observe outputs such as:
#
# 200000
# 193781
# 187442
# 199998
#
# Same code.
# Same machine.
# Same input.
#
# Different answers.
#
# That should immediately raise one question:
#
# "Where did the missing increments go?"

# =============================================================================
# THE BIG MISCONCEPTION
# =============================================================================

# Most beginners believe:
#
#     counter += 1
#
# is one single operation.
#
# It LOOKS like one statement.
#
# Internally it behaves like multiple tiny steps.

# =============================================================================
# SLOW MOTION REPLAY
# =============================================================================

# Conceptually:
#
# Step 1
# READ counter
#
# Step 2
# Calculate counter + 1
#
# Step 3
# WRITE the result back
#
# Timeline
#
# READ  ---> ADD ---> WRITE
#
# Between ANY two of these steps another thread may run.

# =============================================================================
# THE LOST UPDATE
# =============================================================================

# Initial counter = 100
#
# Thread A                Thread B
# --------                --------
# READ 100
#                         READ 100
# ADD ->101
#                         ADD ->101
# WRITE 101
#                         WRITE 101
#
# Final value = 101
#
# Two increments happened.
#
# Counter increased by only ONE.
#
# One update was LOST forever.

# =============================================================================
# WHY IS THE BUG RANDOM?
# =============================================================================

# The operating system decides when threads run.
#
# It may pause one thread after READ.
#
# It may resume another thread.
#
# This changing order is called Thread Interleaving.
#
# Every execution may have a different interleaving.
#
# Therefore every execution may produce a different answer.
#
# These bugs are called Non-deterministic.
#
# Non-deterministic means:
#
# "The same program can produce different results."

# =============================================================================
# VISUALIZATION
# =============================================================================
#
# Run 1
# -----
# A READ
# A ADD
# A WRITE
# B READ
# B ADD
# B WRITE
#
# Correct
#
# Run 2
# -----
# A READ
# B READ
# A WRITE
# B WRITE
#
# Lost Update

# =============================================================================
# ANALOGY – SHARED GOOGLE DOC
# =============================================================================

# Two people open the same document.
#
# Both see the old sentence.
#
# Both edit it.
#
# Whoever saves last overwrites the previous person's work.
#
# Neither editor knows the overwrite happened.
#
# Race conditions behave exactly like this.

# =============================================================================
# WHY THIS IS DANGEROUS
# =============================================================================

# The worst race conditions do NOT fail every time.
#
# Sometimes they produce the correct answer.
#
# This creates false confidence.
#
# Developers think:
#
# "It worked on my machine."
#
# But the timing simply happened to be favourable.

# =============================================================================
# COMMON MISTAKES
# =============================================================================

# Mistake 1
#
# Assuming one Python statement equals one atomic operation.
#
# ------------------------------------------------------------
#
# Mistake 2
#
# Believing a bug that appears only occasionally is harmless.
#
# ------------------------------------------------------------
#
# Mistake 3
#
# Running the program once and concluding it is thread-safe.

# =============================================================================
# INTERVIEW DISCUSSION
# =============================================================================

# Q. What is a Race Condition?
#
# A race condition occurs when multiple threads access shared mutable state and
# the correctness of the result depends on execution timing.
#
# ------------------------------------------------------------
#
# Q. What causes the Lost Update problem?
#
# Multiple threads read the same old value before either thread writes the new
# value back.
#
# ------------------------------------------------------------
#
# Q. Why are race conditions difficult to reproduce?
#
# Because scheduling decisions change from one execution to another.

# =============================================================================
# KEY TAKEAWAYS
# =============================================================================

# ✓ Shared mutable state is the root cause.
#
# ✓ counter += 1 is conceptually READ → ADD → WRITE.
#
# ✓ Another thread can interrupt between these steps.
#
# ✓ Timing changes the final answer.
#
# ✓ Correctness should never depend on thread scheduling.
#
# ✓ We need a mechanism that allows only one thread to update the shared data
#   at a time.

# =============================================================================
# BRIDGE
# =============================================================================

# We now know WHY race conditions happen.
#
# The next question is:
#
# "Can we temporarily stop other threads from touching shared data?"
#
# Yes.
#
# The first synchronization primitive that solves this problem is a Lock.
