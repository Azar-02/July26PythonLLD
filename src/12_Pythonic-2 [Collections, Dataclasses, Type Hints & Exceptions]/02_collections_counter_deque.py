
"""
===============================================================================
PART 02 - COLLECTIONS
Counter & deque
===============================================================================

Topics Covered
--------------
1. Counter - effortless frequency counting
2. deque - efficient double-ended queue
3. deque(maxlen)
4. list vs deque
5. queue.Queue callback

The comments are the classroom lecture.
The executable code demonstrates runtime behaviour.
"""

from collections import Counter, deque

# =============================================================================
# MOTIVATION
# =============================================================================
#
# In the previous class we saw that Python provides specialised containers
# whenever developers repeatedly write the same boilerplate.
#
# Today we continue that journey with two more containers.
#
# Counter answers:
#
#     "How many times does each item occur?"
#
# deque answers:
#
#     "How can I efficiently add/remove items from both ends?"
#
# One tool.
# One recurring problem.


# =============================================================================
# THEORY - Counter
# =============================================================================
#
# Suppose we want to count word frequencies.
#
# Most beginners naturally write:
#
# if word in counts:
#     counts[word] += 1
# else:
#     counts[word] = 1
#
# There is nothing wrong with this solution.
#
# The question is:
#
# Why write this logic every single time?
#
# Counter already knows how to count.


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# Imagine analysing a book.
#
# Which word appears most frequently?
#
# How many votes did each candidate receive?
#
# How many times did each error occur?
#
# These are all frequency-counting problems.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Predict:
#
# Which word appears most often?
#

text = "the cat sat on the mat the end the"

counts = Counter(text.split())

print("Counter :", counts)
print("'the'   :", counts["the"])
print("Top 2   :", counts.most_common(2))

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Counter automatically performs the counting loop.
#
# Even better,
#
# .most_common()
#
# is already implemented for us.
#
# The focus shifts from
#
# "How do I count?"
#
# to
#
# "What information do I want?"


# =============================================================================
# SMALL EXPERIMENTS
# =============================================================================

letters = Counter("banana")
print("\nLetter frequencies:", letters)
print("Most common letter :", letters.most_common(1))

# =============================================================================
# COMMON MISCONCEPTIONS
# =============================================================================
#
# Counter is NOT limited to strings.
#
# It counts any iterable.
#
# Lists
# Tuples
# Characters
# Words
# Numbers
# Anything hashable.
#


# =============================================================================
# INTERVIEW OBSERVATION
# =============================================================================
#
# Counter is one of the most frequently used standard-library classes in
# coding interviews involving:
#
# - Frequency counting
# - Top-K elements
# - Character statistics
# - Vote counting
#


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# Counter(iterable)
#
#        ↓
#
# Counts everything automatically.
#
# most_common(n)
#
#        ↓
#
# Returns the n highest frequencies.
#


# =============================================================================
# TRANSITION
# =============================================================================
#
# Counter removed boilerplate for counting.
#
# Now let's remove inefficiency from queues.
#


# =============================================================================
# THEORY - deque
# =============================================================================
#
# A normal Python list performs very well at the END.
#
# append()
# pop()
#
# But removing from the FRONT requires shifting every remaining element.
#
# Think of people standing in a queue.
#
# If the first person leaves,
# everybody behind steps forward.
#
# That shifting is the hidden cost of list.pop(0).
#
# deque ("deck")
#
# is built differently.
#
# It efficiently supports both ends.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Predict the output after each operation.
#

d = deque([1, 2, 3])

d.append(4)
d.appendleft(0)

print("\nDeque after additions :", d)

front = d.popleft()
print("Removed from front    :", front)
print("Current deque         :", d)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Unlike a list,
# deque removes the front element without shifting every remaining item.
#
# This makes it ideal for queue-like behaviour.
#


# =============================================================================
# SMALL EXPERIMENT
# =============================================================================

recent = deque(maxlen=3)

for i in range(6):
    recent.append(i)

print("\nRolling window:", recent)

# Runtime Observation
#
# deque(maxlen=3)
#
# automatically discards the oldest item.
#
# No manual cleanup code is required.


# =============================================================================
# CALLBACK TO CONCURRENCY
# =============================================================================
#
# Remember queue.Queue from the concurrency lecture.
#
# queue.Queue
#
#      ↓
#
# Thread-safe
#
# Internal locking
#
#
# deque
#
#      ↓
#
# Lightweight
#
# Single-thread
#
# Faster when locking is unnecessary.
#


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# If you need communication between multiple threads,
# should you choose deque?
#
# Expected Answer:
#
# No.
#
# queue.Queue exists specifically for thread-safe producer-consumer workflows.
#


# =============================================================================
# INTERVIEW OBSERVATION
# =============================================================================
#
# Use deque when:
#
# - BFS
# - Sliding window
# - Recent history
# - Queue simulation
#
# Use queue.Queue when threads are involved.
#


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# Counter
#
# Frequency counting
#
# ↓
#
# Counter(iterable)
#
#
# deque
#
# Fast front
# Fast back
#
# append()
# appendleft()
# pop()
# popleft()
#
# deque(maxlen)
#
# Rolling window
#


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ Counter removes manual counting loops.
# ✓ most_common() is built in.
# ✓ deque supports efficient operations at both ends.
# ✓ deque(maxlen) automatically maintains recent history.
# ✓ queue.Queue is the threaded counterpart of deque.
#
# Choose the container that matches the problem.
#
#
# =============================================================================
# BRIDGE TO THE NEXT TOPIC
# =============================================================================
#
# So far we've improved containers.
#
# Next we'll improve how we represent data itself.
#
# Instead of writing repetitive classes,
# Python can generate much of that code automatically using @dataclass.
