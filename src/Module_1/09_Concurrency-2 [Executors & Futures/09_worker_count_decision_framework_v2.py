# ============================================================
# CONCURRENCY-2
# FILE : 09_worker_count_decision_framework_v2.py
# ============================================================

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ============================================================
# FINAL CONCEPTUAL FILE OF THE MODULE
# ============================================================

# We learned:
#
# Threads
# Processes
# GIL
# Executors
# Futures
# CPU-bound vs I/O-bound
#
# Final question:
#
# How many workers should we create?

# ============================================================
# ASK LEARNERS
# ============================================================

# If 4 workers are good,
# then 400 workers must be better?
#
# Not necessarily.

# ============================================================
# WHY MORE WORKERS IS NOT ALWAYS BETTER
# ============================================================

# Workers are not free.
#
# Threads cost memory.
# Processes cost memory.
# Scheduling costs CPU.
# Context switching costs time.

# ============================================================
# THE GOLDEN RULE
# ============================================================

# More workers may help.
#
# Too many workers may hurt.

# ============================================================
# CPU-BOUND THINKING
# ============================================================

# Examples:
#
# Image Processing
# Video Rendering
# Compression
# Scientific Computing

# ============================================================
# ASK LEARNERS
# ============================================================

# Machine has 8 CPU cores.
#
# How many CPU-heavy tasks
# can truly run at once?

# ============================================================
# ANSWER
# ============================================================

# Roughly 8.

# ============================================================
# VISUALIZATION
# ============================================================

# Core1 -> Process1
# Core2 -> Process2
# Core3 -> Process3
# Core4 -> Process4
# Core5 -> Process5
# Core6 -> Process6
# Core7 -> Process7
# Core8 -> Process8

# ============================================================
# WHAT IF WE CREATE 100 PROCESSES?
# ============================================================

# The operating system keeps
# switching between them.
#
# More overhead.
# More scheduling.
# More context switching.

# ============================================================
# CPU GUIDELINE
# ============================================================

# Typical starting point:
#
# Workers ≈ CPU core count

# ============================================================
# EXAMPLE
# ============================================================

# ProcessPoolExecutor(
#     max_workers=8
# )

# ============================================================
# I/O-BOUND THINKING
# ============================================================

# Examples:
#
# Web Scraping
# API Calls
# Database Queries
# File Downloads

# ============================================================
# ASK LEARNERS
# ============================================================

# If 100 threads exist,
# are all 100 actively computing?

# ============================================================
# ANSWER
# ============================================================

# Usually no.
#
# Many are waiting.

# ============================================================
# WAITING FOR
# ============================================================

# APIs
# Databases
# Network
# Files

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# Waiting threads are very
# different from CPU-heavy workers.

# ============================================================
# I/O GUIDELINE
# ============================================================

# ThreadPoolExecutor(
#     max_workers=50
# )
#
# may be reasonable for some
# I/O-heavy workloads.

# ============================================================
# DECISION FRAMEWORK
# ============================================================

# Step 1:
#
# CPU-bound?
#
# or
#
# I/O-bound?

# ============================================================
# IF CPU-BOUND
# ============================================================

# Prefer:
#
# ProcessPoolExecutor
#
# Start near:
#
# CPU core count

# ============================================================
# IF I/O-BOUND
# ============================================================

# Prefer:
#
# ThreadPoolExecutor
#
# Often more workers
# than available cores.

# ============================================================
# PRACTICAL SCENARIOS
# ============================================================

# 1000 Web Pages
# -> ThreadPoolExecutor
#
# 1000 Images
# -> ProcessPoolExecutor
#
# API Aggregator
# -> ThreadPoolExecutor
#
# Video Rendering
# -> ProcessPoolExecutor

# ============================================================
# BENCHMARKING MINDSET
# ============================================================

# Never assume performance.
#
# Measure:
#
# 10 workers
# 20 workers
# 50 workers
# 100 workers
#
# Real systems surprise us.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# More workers always means
# more speed.
# False.
#
# Same worker count works
# everywhere.
# False.

# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

# CPU-bound worker count?
# Roughly core count.
#
# Why can I/O workloads use
# more workers?
# Because many wait.
#
# First decision question?
# CPU-bound or I/O-bound?

# ============================================================
# MODULE WRAP-UP
# ============================================================

# Threads
# Processes
# GIL
# Executors
# Futures
# Benchmarks
# Decision Framework

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# CPU-bound:
# ProcessPoolExecutor
#
# I/O-bound:
# ThreadPoolExecutor
#
# More workers is not
# always better.
#
# Benchmark real systems.
#
# The workload decides.
