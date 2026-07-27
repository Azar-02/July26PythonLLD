"""
PART 9 - GENERATORS

Topics Covered

1. Why generators exist
2. yield keyword
3. Pause and resume execution
4. Generator expressions
5. Lazy evaluation
6. Memory-efficient processing
"""

# ============================================================
# MOTIVATION
# ============================================================

# Our Countdown iterator worked well, but we had to write
# __iter__() and __next__() ourselves.
#
# Python gives us a much simpler mechanism:
#
# Generators.
#
# They automatically implement the iterator protocol.

# ============================================================
# THEORY
# ============================================================

# A generator is a special function that uses the keyword:
#
# yield
#
# Unlike return, yield pauses the function.
#
# The next call resumes exactly where execution stopped.

# ============================================================
# ANALOGY
# ============================================================

# Imagine reading a book.
#
# A bookmark remembers exactly where you stopped.
#
# When you reopen the book, you continue from that page.
#
# yield works like that bookmark.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# yield does NOT terminate the function forever.
#
# It temporarily pauses execution.
#
# Later, next() resumes from the same point.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# generator()
#      │
#      ▼
# Generator Object
#      │
#      ▼
# next()
#      │
#      ▼
# yield 1  (paused)
#      │
# next()
#      ▼
# yield 2  (paused)
#      │
# next()
#      ▼
# StopIteration

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# Which print statement executes first?
#
# Does the entire function execute immediately?

# ============================================================
# DEMO 1 - BASIC GENERATOR
# ============================================================

def countdown(start):
    while start > 0:
        print(f"Preparing {start}")
        yield start
        start -= 1

gen = countdown(3)

print("Generator created")
print(next(gen))
print(next(gen))
print(next(gen))

try:
    print(next(gen))
except StopIteration:
    print("Generator exhausted")

# Runtime Observation:
#
# The function pauses after every yield.
# It resumes exactly where it stopped.

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# Why didn't all "Preparing..." messages appear immediately?
#
# Expected Answer:
#
# The generator executes only when next() requests a value.

# ============================================================
# DEMO 2 - FOR LOOP
# ============================================================

print("\nGenerator in a for-loop")

for number in countdown(5):
    print("Received:", number)

# Runtime Observation:
#
# The for-loop repeatedly calls next() internally.

# ============================================================
# THEORY - GENERATOR EXPRESSIONS
# ============================================================

# Similar to list comprehensions, Python also supports
# generator expressions.
#
# They produce values lazily.

# ============================================================
# DEMO 3 - GENERATOR EXPRESSION
# ============================================================

squares = (x * x for x in range(5))

print("\nGenerator Expression")

for value in squares:
    print(value)

# ============================================================
# THEORY - LAZY EVALUATION
# ============================================================

# Lists compute every value immediately.
#
# Generators compute values only when requested.
#
# This makes them ideal for processing very large datasets.

# ============================================================
# DEMO 4 - LARGE STREAM
# ============================================================

def numbers(limit):
    for value in range(limit):
        yield value

stream = numbers(1000000)

print("\nLazy Stream")
print(next(stream))
print(next(stream))
print(next(stream))

# Runtime Observation:
#
# One million values are NOT stored in memory at once.
#
# Values are produced one by one.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

print("\nExperiments")
print(type(stream))
print(hasattr(stream, "__next__"))
print(hasattr(stream, "__iter__"))

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Difference:
#
# return
# -> Ends the function.
#
# yield
# -> Pauses the function.
#
# Generators are useful when:
#
# - Working with large files
# - Infinite sequences
# - Streaming data
# - Memory optimisation

# ============================================================
# BOARD SUMMARY
# ============================================================

# yield
#   │
# pause
#   │
# next()
#   │
# resume
#   │
# yield again
#   │
# StopIteration

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# Python's standard library provides many ready-made iterator
# and generator utilities.
#
# Next we will explore itertools and build practical utilities
# such as timer and retry decorators in the lab.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ yield pauses instead of terminating.
# ✓ next() resumes execution.
# ✓ Generators are automatically iterators.
# ✓ Generator expressions are lazy.
# ✓ Generators are memory efficient.
