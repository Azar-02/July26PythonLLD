"""
============================================================
CONCURRENCY-2
FILE : 07_io_bound_web_scraper_lab_v2.py
============================================================

Topics Covered
--------------
1. Motivation
2. The First Real Concurrency Win
3. Understanding Web Scraping
4. Why Web Scraping Is I/O-Bound
5. Sequential Scraper
6. Measuring Runtime
7. The Waiting Problem
8. ThreadPoolExecutor Solution
9. Worker Pool Visualization
10. Why Threading Helps
11. Relation To The GIL
12. Common Misconceptions
13. Interview Questions
14. Key Takeaways

Based on Concurrency-2 Lecture Notes.
"""

from concurrent.futures import ThreadPoolExecutor
import time

# ============================================================
# MOTIVATION
# ============================================================

# Up until now we have learned:
#
# Thread
# Process
# GIL
# ThreadPoolExecutor
# ProcessPoolExecutor
# Future
# submit()
# map()
#
# A student may ask:
#
# "Everything sounds theoretical."
#
# "Where is the actual benefit?"
#
# Excellent question.
#
# Today's file is the first major
# real-world example where threading
# produces an obvious improvement.

# ============================================================
# THE STORY
# ============================================================

# Imagine:
#
# You work at a company that wants
# to collect information from many
# websites.
#
# Example:
#
# Product prices
# News headlines
# Hotel availability
# Flight information
#
# This is a common use case known as:
#
# Web Scraping

# ============================================================
# ASK LEARNERS
# ============================================================

# Suppose:
#
# One website takes:
#
# 2 seconds
#
# to respond.
#
# Five websites exist.
#
# Prediction:
#
# How long will sequential execution take?

# ============================================================
# UNDERSTANDING THE WORKLOAD
# ============================================================

# Before writing code,
# we must classify the workload.
#
# Is it:
#
# CPU-bound?
#
# or
#
# I/O-bound?

# ============================================================
# THINK CAREFULLY
# ============================================================

# When downloading a webpage:
#
# What is the CPU doing?
#
# Huge calculations?
#
# Heavy mathematics?
#
# Complex image processing?

# ============================================================
# ANSWER
# ============================================================

# Usually:
#
# No.
#
# Most time is spent waiting.

# ============================================================
# WAITING FOR WHAT?
# ============================================================

# DNS lookup
# Network latency
# Server response
# Internet routing
# Data transfer
#
# The CPU spends a surprising
# amount of time doing nothing.

# ============================================================
# IMPORTANT REALIZATION
# ============================================================

# This is exactly what
# I/O-bound means.
#
# The bottleneck is waiting,
# not computation.

# ============================================================
# SIMULATED WEB REQUEST
# ============================================================

def download_page(url):

    print(
        f"Downloading {url}"
    )

    time.sleep(2)

    return f"HTML from {url}"

# ============================================================
# SAMPLE URLS
# ============================================================

urls = [
    "site-1.com",
    "site-2.com",
    "site-3.com",
    "site-4.com",
    "site-5.com"
]

# ============================================================
# SEQUENTIAL SCRAPER
# ============================================================

start = time.time()

results = []

for url in urls:

    html = download_page(url)

    results.append(html)

end = time.time()

print(
    "Sequential Time:",
    round(end - start, 2),
    "seconds"
)

# ============================================================
# ASK LEARNERS
# ============================================================

# Let's reason manually.
#
# Each request:
#
# 2 seconds
#
# Five requests:
#
# ?

# ============================================================
# ANSWER
# ============================================================

# Approximately:
#
# 10 seconds

# ============================================================
# TIMELINE VISUALIZATION
# ============================================================

# Time 0:
#
# Download Site 1
#
# Time 2:
#
# Download Site 2
#
# Time 4:
#
# Download Site 3
#
# Time 6:
#
# Download Site 4
#
# Time 8:
#
# Download Site 5
#
# Time 10:
#
# Finished

# ============================================================
# OBSERVATION
# ============================================================

# Notice something interesting.
#
# The CPU is not busy
# for ten seconds.
#
# It is mostly waiting.

# ============================================================
# THE BIG QUESTION
# ============================================================

# Can we overlap
# those waiting periods?

# ============================================================
# THREADPOOL SOLUTION
# ============================================================

start = time.time()

with ThreadPoolExecutor(
    max_workers=5
) as executor:

    results = list(

        executor.map(
            download_page,
            urls
        )

    )

end = time.time()

print(
    "ThreadPool Time:",
    round(end - start, 2),
    "seconds"
)

# ============================================================
# ASK LEARNERS
# ============================================================

# Did we change:
#
# download_page() ?
#
# Did we optimize:
#
# Network speed?
#
# Server speed?
#
# Internet speed?

# ============================================================
# ANSWER
# ============================================================

# No.
#
# The work remained identical.

# ============================================================
# WHAT CHANGED?
# ============================================================

# Only:
#
# Execution strategy

# ============================================================
# WORKER VISUALIZATION
# ============================================================

# Worker 1 -> site-1
# Worker 2 -> site-2
# Worker 3 -> site-3
# Worker 4 -> site-4
# Worker 5 -> site-5

# ============================================================
# TIMELINE VISUALIZATION
# ============================================================

# Time 0:
#
# All downloads begin.
#
# Time 2:
#
# Most downloads finish.

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# We did NOT make
# downloads faster.
#
# We made waiting overlap.

# ============================================================
# THIS IS THE ENTIRE TRICK
# ============================================================

# Sequential:
#
# Wait
# Wait
# Wait
# Wait
# Wait
#
# Total ≈ 10 seconds

# ============================================================

# ThreadPool:
#
# Wait
# Wait
# Wait
# Wait
# Wait
#
# Simultaneously
#
# Total ≈ 2 seconds

# ============================================================
# WHY THREADS HELP
# ============================================================

# Thread A waits.
#
# While A waits:
#
# Thread B runs.
#
# Thread C runs.
#
# Thread D runs.
#
# Thread E runs.

# ============================================================
# RELATION TO THE GIL
# ============================================================

# Students often ask:
#
# "Didn't we learn that
# the GIL blocks threads?"
#
# Excellent observation.

# ============================================================
# ANSWER
# ============================================================

# During many I/O operations:
#
# Python releases the GIL.
#
# Therefore:
#
# Other threads can continue.

# ============================================================
# THIS CONNECTS EVERYTHING
# ============================================================

# Lecture 8 taught:
#
# CPU-bound
# vs
# I/O-bound
#
# Today we finally see
# why that distinction matters.

# ============================================================
# THREADPOOL IS GREAT FOR
# ============================================================

# API calls
# Database calls
# Web scraping
# Network requests
# File operations

# ============================================================
# ASK LEARNERS
# ============================================================

# What about:
#
# Image compression?
# Video rendering?
# Huge calculations?
#
# Should we use
# ThreadPoolExecutor there?

# ============================================================
# ANSWER
# ============================================================

# Usually:
#
# No.
#
# Those are CPU-bound.

# ============================================================
# IMPORTANT WARNING
# ============================================================

# Many students reach the wrong
# conclusion after this demo.
#
# They think:
#
# "Threads are always faster."
#
# That is false.

# ============================================================
# THIS DEMO IS BIASED
# ============================================================

# We intentionally chose
# an I/O-bound workload.
#
# Naturally:
#
# ThreadPoolExecutor shines.

# ============================================================
# THE NEXT EXPERIMENT
# ============================================================

# What happens if we replace:
#
# Waiting
#
# with:
#
# Computation?

# ============================================================
# COMMON MISCONCEPTION #1
# ============================================================

# Wrong:
#
# Threads make work faster.
#
# Correct:
#
# Threads often make waiting overlap.

# ============================================================
# COMMON MISCONCEPTION #2
# ============================================================

# Wrong:
#
# GIL makes threading useless.
#
# Correct:
#
# Threading remains extremely useful
# for I/O-bound workloads.

# ============================================================
# COMMON MISCONCEPTION #3
# ============================================================

# Wrong:
#
# ThreadPoolExecutor is always best.
#
# Correct:
#
# Depends entirely on workload.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why does threading help
# web scraping?
#
# Answer:
#
# Most time is spent waiting.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# What is being overlapped?
#
# Answer:
#
# Waiting time.

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# Best executor for I/O-bound work?
#
# Answer:
#
# ThreadPoolExecutor

# ============================================================
# INTERVIEW QUESTION #4
# ============================================================

# Does the GIL make threading
# useless for I/O?
#
# Answer:
#
# No.

# ============================================================
# BRIDGE TO NEXT FILE
# ============================================================

# This demo looked amazing.
#
# ThreadPoolExecutor won.
#
# Students often conclude:
#
# "Use threads everywhere."
#
# The next file destroys
# that assumption.
#
# We will swap:
#
# I/O-bound work
#
# for
#
# CPU-bound work.
#
# Same idea.
#
# Completely different result.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Web scraping is I/O-bound.
#
# Most time is spent waiting.
#
# ThreadPoolExecutor overlaps
# waiting periods.
#
# Runtime can improve dramatically.
#
# GIL does not prevent useful
# I/O concurrency.
#
# Next:
#
# The Great Swap
#
# I/O-bound
# versus
# CPU-bound
