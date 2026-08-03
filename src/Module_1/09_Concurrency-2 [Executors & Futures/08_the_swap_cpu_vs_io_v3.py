
"""
============================================================
CONCURRENCY-2
FILE : 08_the_swap_cpu_vs_io_v3.py
============================================================

CLIMAX OF THE MODULE

Topics Covered
--------------
1. Motivation
2. The Dangerous Conclusion
3. Why The Web Scraper Won
4. The Great Swap
5. I/O-Bound vs CPU-Bound
6. ThreadPoolExecutor Experiment
7. Revisiting The GIL
8. ProcessPoolExecutor Experiment
9. Same Code, Different Result
10. Decision Framework Preview
11. Common Misconceptions
12. Interview Questions
13. Key Takeaways
"""

from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor
)

# ============================================================
# MOTIVATION
# ============================================================

# The previous lecture produced
# a very dangerous outcome.
#
# Students saw:
#
# Sequential Scraper
#      vs
# ThreadPoolExecutor Scraper
#
# and the difference looked huge.
#
# Naturally many students conclude:
#
# "Threads are amazing."
#
# Then:
#
# "Threads are always better."
#
# Then:
#
# "Use ThreadPoolExecutor
# everywhere."
#
# Today's lecture exists to
# destroy that conclusion.

# ============================================================
# ============================================================

# Suppose tomorrow your manager says:
#
# "Forget web scraping."
#
# "I need image processing."
#
# "I need heavy calculations."
#
# "I need machine-learning
# preprocessing."
#
# Would you still choose:
#
# ThreadPoolExecutor ?

# ============================================================
# PAUSE AND THINK
# ============================================================

# Many students answer:
#
# Yes.
#
# Because:
#
# Threads were faster yesterday.
#
# That reasoning feels logical.
#
# Unfortunately:
#
# It is wrong.

# ============================================================
# THE BIG LESSON
# ============================================================

# There is no universally
# best executor.
#
# The workload decides.

# ============================================================
# REVISITING THE WEB SCRAPER
# ============================================================

# Let's remember what happened.
#
# We had:
#
# Network Requests
#
# Each request spent most of
# its life waiting.
#
# Waiting for:
#
# DNS
# Network
# Server Response
# Data Transfer

# ============================================================
# IMPORTANT QUESTION
# ============================================================

# What was the CPU doing
# most of the time?
#
# Heavy mathematics?
#
# Complex calculations?
#
# No.

# ============================================================
# ANSWER
# ============================================================

# Mostly waiting.

# ============================================================
# VISUALIZATION
# ============================================================

# Request 1
#     ↓
# Wait
#
# Request 2
#     ↓
# Wait
#
# Request 3
#     ↓
# Wait

# ============================================================
# WHAT THREADS DID
# ============================================================

# Threads did NOT make
# waiting faster.
#
# Threads overlapped
# the waiting periods.

# ============================================================
# SEQUENTIAL TIMELINE
# ============================================================

# Wait
# Wait
# Wait
# Wait
# Wait

# ============================================================
# THREADPOOL TIMELINE
# ============================================================

# Wait
# Wait
# Wait
# Wait
# Wait
#
# Simultaneously

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# The victory came from:
#
# Overlapping waiting.
#
# Not from:
#
# Faster computation.

# ============================================================
# THE GREAT SWAP
# ============================================================

# Let's change only one thing.
#
# Remove waiting.
#
# Add computation.

# ============================================================
# OLD WORLD
# ============================================================

# I/O-Bound
#
# Waiting dominates.

# ============================================================
# NEW WORLD
# ============================================================

# CPU-Bound
#
# Computation dominates.

# ============================================================
# CPU HEAVY TASK
# ============================================================

def cpu_heavy(n):

    total = 0

    for i in range(n):

        total += i * i

    return total

# ============================================================
# ASK LEARNERS
# ============================================================

# Look carefully.
#
# Where is the waiting?
#
# Network?
#
# Database?
#
# Sleep?
#
# None.

# ============================================================
# OBSERVATION
# ============================================================

# CPU is busy continuously.
#
# This workload is completely
# different from the scraper.

# ============================================================
# THREADPOOL EXPERIMENT
# ============================================================

# with ThreadPoolExecutor(
#     max_workers=4
# ) as executor:
#
#     results = list(
#         executor.map(
#             cpu_heavy,
#             [5_000_000] * 4
#         )
#     )

# ============================================================
# PREDICTION EXERCISE
# ============================================================

# Four workers.
#
# Four CPU-heavy tasks.
#
# Four CPU cores available.
#
# Prediction:
#
# Massive speedup?

# ============================================================
# WHAT STUDENTS IMAGINE
# ============================================================

# Core 1 -> Thread 1
# Core 2 -> Thread 2
# Core 3 -> Thread 3
# Core 4 -> Thread 4
#
# All running simultaneously.

# ============================================================
# THIS WOULD BE NICE
# ============================================================

# If that happened,
# threads would dominate
# CPU workloads too.

# ============================================================
# BUT THERE IS A PROBLEM
# ============================================================

# We already studied it.
#
# GIL

# ============================================================
# REVISITING THE GIL
# ============================================================

# GIL:
#
# Global Interpreter Lock
#
# CPython restriction.
#
# Only one thread executes
# Python bytecode at a time.

# ============================================================
# ASK LEARNERS
# ============================================================

# Do we have multiple threads?
#
# Yes.
#
# Do they all execute Python
# bytecode simultaneously?
#
# No.

# ============================================================
# VISUALIZATION
# ============================================================

# Thread 1 gets GIL.
#
# Thread 2 waits.
# Thread 3 waits.
# Thread 4 waits.

# ============================================================

# Scheduler switches.
#
# Thread 2 gets GIL.
#
# Others wait.

# ============================================================

# Scheduler switches.
#
# Thread 3 gets GIL.

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# Threads exist.
#
# Concurrency exists.
#
# But CPU-bound parallelism
# is limited.

# ============================================================
# THIS IS THE SURPRISE
# ============================================================

# Same ThreadPoolExecutor.
#
# Completely different outcome.
#
# Why?
#
# Because the workload changed.

# ============================================================
# VERY IMPORTANT SENTENCE
# ============================================================

# The executor stayed the same.
#
# The workload changed.

# ============================================================
# ENTER PROCESSPOOLEXECUTOR
# ============================================================

# with ProcessPoolExecutor(
#     max_workers=4
# ) as executor:
#
#     results = list(
#         executor.map(
#             cpu_heavy,
#             [5_000_000] * 4
#         )
#     )

# ============================================================
# ASK LEARNERS
# ============================================================

# What changed?
#
# Function?
# No.
#
# Input?
# No.
#
# Algorithm?
# No.
#
# Only:
#
# Executor.

# ============================================================
# WHY PROCESSES ARE DIFFERENT
# ============================================================

# Process 1:
#
# Own Memory
# Own Interpreter
# Own GIL

# ============================================================

# Process 2:
#
# Own Memory
# Own Interpreter
# Own GIL

# ============================================================

# Process 3:
#
# Own Memory
# Own Interpreter
# Own GIL

# ============================================================

# Process 4:
#
# Own Memory
# Own Interpreter
# Own GIL

# ============================================================
# VISUALIZATION
# ============================================================

# Process 1 -> Core 1
# Process 2 -> Core 2
# Process 3 -> Core 3
# Process 4 -> Core 4

# ============================================================
# OBSERVATION
# ============================================================

# Genuine parallel execution
# becomes possible.

# ============================================================
# THE SHOCKING RESULT
# ============================================================

# Same Machine
#
# Same Input
#
# Same Algorithm
#
# Same Number Of Workers
#
# Different Executor
#
# Different Result

# ============================================================
# WHY THIS LECTURE EXISTS
# ============================================================

# Students often memorize:
#
# ThreadPoolExecutor
#
# without understanding:
#
# WHY it worked.
#
# The answer was never:
#
# Threads are magic.
#
# The answer was:
#
# The workload matched the tool.

# ============================================================
# SIDE-BY-SIDE COMPARISON
# ============================================================

# I/O-Bound
#
# Waiting dominates
#
# ThreadPoolExecutor often shines

# ============================================================

# CPU-Bound
#
# Computation dominates
#
# ProcessPoolExecutor often shines

# ============================================================
# DECISION PREVIEW
# ============================================================

# New task arrives.
#
# First question:
#
# Mostly waiting?
#
# or
#
# Mostly computing?
#
# That question is often more
# important than the code itself.

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# ThreadPoolExecutor is always best.
#
# Correct:
#
# Depends on workload.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# ProcessPoolExecutor is always best.
#
# Correct:
#
# Processes have startup overhead.

# ============================================================
# COMMON MISCONCEPTION #3
# ============================================================

# Wrong:
#
# More workers always means
# more speed.
#
# Correct:
#
# Too many workers can reduce
# performance.

# ============================================================
# COMMON MISCONCEPTION #4
# ============================================================

# Wrong:
#
# GIL makes threads useless.
#
# Correct:
#
# Threads remain extremely useful
# for I/O-bound workloads.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Best executor for:
#
# Web Scraping?
#
# Answer:
#
# ThreadPoolExecutor

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Best executor for:
#
# Image Processing?
#
# Answer:
#
# ProcessPoolExecutor

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Why can CPU-bound threads
# disappoint in CPython?
#
# Answer:
#
# GIL

# ============================================================
# INTERVIEW QUESTION #4
# ============================================================

# What determines the best executor?
#
# Answer:
#
# Nature of the workload.

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# We now understand:
#
# ThreadPoolExecutor wins
# some battles.
#
# ProcessPoolExecutor wins
# others.
#
# The next file converts these
# observations into a practical
# decision framework you can use
# in interviews and real projects.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# The web scraper won because
# waiting could overlap.
#
# CPU-bound workloads change
# the rules.
#
# GIL becomes important.
#
# ProcessPoolExecutor often wins
# CPU-heavy benchmarks.
#
# There is no universal winner.
#
# The workload decides.
