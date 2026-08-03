"""
PART 8 - ITERATORS

Topics Covered

1. Why iterators exist
2. Iterable vs Iterator
3. iter() and next()
4. StopIteration
5. Building a custom iterator
"""

# ============================================================
# MOTIVATION
# ============================================================

# We use for-loops every day.
#
# for number in numbers:
#     ...
#
# But have you ever wondered:
#
# How does the for-loop know where the next element is?
#
# The answer lies in Python's iterator protocol.

# ============================================================
# THEORY
# ============================================================

# Iterable:
# An object that can produce an iterator.
#
# Iterator:
# An object that remembers its current position and can
# produce one value at a time.
#
# Important methods:
#
# __iter__()
# __next__()

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# A list is NOT an iterator.
#
# A list is an iterable.
#
# Calling iter(list) creates an iterator.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# List
#  │
#  ▼
# iter()
#  │
#  ▼
# Iterator
#  │
#  ├── current position = 0
#  ├── current position = 1
#  └── current position = 2

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# If a for-loop keeps receiving one element at a time,
# which function is repeatedly called behind the scenes?
#
# Expected Answer:
#
# next()

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict the outputs before executing.
#
# What happens after the last element?

# ============================================================
# DEMO 1 - iter() AND next()
# ============================================================

numbers = [10, 20, 30]

iterator = iter(numbers)

print("Iterator Demo")
print(next(iterator))
print(next(iterator))
print(next(iterator))

try:
    print(next(iterator))
except StopIteration:
    print("StopIteration raised")

# Runtime Observation:
#
# next() advances the iterator.
#
# After the final element, StopIteration signals completion.

# ============================================================
# THEORY
# ============================================================

# A for-loop internally performs something similar to:
#
# iterator = iter(collection)
#
# while True:
#     try:
#         value = next(iterator)
#         ...
#     except StopIteration:
#         break

# ============================================================
# DEMO 2 - CUSTOM ITERATOR
# ============================================================

class Countdown:

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration

        value = self.current
        self.current -= 1
        return value

print("\nCustom Countdown")

for value in Countdown(5):
    print(value)

# Runtime Observation:
#
# __next__() is repeatedly called until StopIteration occurs.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

it = iter(["A", "B"])

print("\nExperiments")
print(type(it))
print(hasattr(it, "__next__"))
print(hasattr(it, "__iter__"))

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Difference:
#
# Iterable:
# Can produce an iterator.
#
# Iterator:
# Can produce successive values.
#
# Every iterator is iterable.
#
# Not every iterable is an iterator.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Iterable
#     │
# iter()
#     ▼
# Iterator
#     │
# next()
#     ▼
# Value
#
# StopIteration ends iteration.

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# Our Countdown stores all its state inside an object.
#
# Python provides a simpler way to create iterators:
#
# Generators.
#
# They use the yield keyword and automatically manage
# iterator state.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Lists are iterables, not iterators.
# ✓ iter() creates an iterator.
# ✓ next() retrieves one value at a time.
# ✓ StopIteration ends iteration.
# ✓ Custom iterators implement __iter__ and __next__.
