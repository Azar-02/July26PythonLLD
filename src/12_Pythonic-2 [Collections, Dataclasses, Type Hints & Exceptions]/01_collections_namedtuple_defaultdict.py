
"""
===============================================================================
PART 01 - COLLECTIONS
namedtuple & defaultdict
===============================================================================

Topics Covered

1. Why specialised containers exist
2. namedtuple
3. defaultdict
4. When to use each
5. Common interview discussions

This is a classroom teaching script.

The comments are the lecture.
The executable code is only for demonstration.
"""

from collections import namedtuple, defaultdict


# =============================================================================
# MOTIVATION
# =============================================================================
#
# Until now we have mainly used:
#
#     list
#     tuple
#     dict
#     set
#
# These four containers solve most programming problems.
#
# So naturally students ask:
#
#     "Why do we even need collections?"
#
# Excellent question.
#
# The answer is that Python noticed developers repeatedly solving the SAME
# problems with ordinary containers.
#
# Instead of writing the same boilerplate every day, Python provides specialised
# containers.
#
# Today's philosophy:
#
#     Don't memorise containers.
#
#     Identify the problem first.
#
#     Then choose the container designed for that problem.
#
# Throughout this lecture remember one sentence:
#
#     One problem.
#     One specialised container.
#
# This entire collections module is built around that philosophy.
#


# =============================================================================
# THEORY
# =============================================================================
#
# We begin with tuples.
#
# -------------------------------------------------------------------------
# Pain Point
# -------------------------------------------------------------------------
#
# Imagine someone gives you:
#
#     point = (3, 5)
#
# Several months later you read:
#
#     point[0]
#
# Question:
#
# What exactly is position zero?
#
# x?
# y?
# latitude?
# longitude?
#
# Position numbers contain no meaning.
#
# Humans understand names much better than numbers.
#
# Python therefore introduced namedtuple.
#
# A namedtuple is STILL a tuple.
#
# It is NOT replacing tuples.
#
# It is simply giving names to tuple positions.
#


# =============================================================================
# DISCUSSION
# =============================================================================
#
# ASK LEARNERS
#
# Which is easier to understand?
#
# point[0]
#
# OR
#
# point.x
#
# Student Thinking
#
# The second version immediately tells us what the value represents.
#
# Expected Answer
#
# point.x
#
# because names carry meaning whereas indexes only carry position.
#


# =============================================================================
# MEMORY DIAGRAM
# =============================================================================
#
#                 Point Object
#
#          +-----------------------+
#          |  x = 3                |
#          |  y = 5                |
#          +-----------------------+
#
#           ▲                 ▲
#           │                 │
#
#        p.x               p[0]
#
# Both refer to the same stored value.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Predict the answers.
#
# 1. Can we still access indexes?
#
# 2. Is namedtuple mutable?
#
# 3. Is it actually a tuple?
#


# =============================================================================
# DEMO
# =============================================================================

Point = namedtuple("Point", ["x", "y"])

p = Point(3, 5)

print("Object :", p)
print("x      :", p.x)
print("y      :", p.y)
print("Index0 :", p[0])
print("Index1 :", p[1])


# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Notice something interesting.
#
# We never lost tuple behaviour.
#
# Index access still works.
#
# namedtuple simply ADDS readable names.
#


# =============================================================================
# SMALL EXPERIMENTS
# =============================================================================

print(type(p))
print(isinstance(p, tuple))

try:
    p.x = 100
except AttributeError as e:
    print(type(e).__name__, "->", e)


# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Many beginners assume namedtuple behaves like a normal class.
#
# It doesn't.
#
# It remains immutable exactly like a tuple.
#


# =============================================================================
# COMMON MISCONCEPTIONS
# =============================================================================
#
# Misconception 1
#
# namedtuple replaces classes.
#
# Incorrect.
#
# It is intended for lightweight immutable data.
#
# Later in today's lecture we will discover @dataclass,
# which is the natural evolution beyond namedtuple.
#


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# tuple
#
#     ↓
#
# namedtuple
#
# Same tuple
#
# + readable field names
#
# Immutable
#
# Lightweight
#


# =============================================================================
# TRANSITION
# =============================================================================
#
# Tuples became easier to read.
#
# Let's now solve another everyday annoyance.
#
# Dictionaries.
#


# =============================================================================
# MOTIVATION - defaultdict
# =============================================================================
#
# Imagine grouping words by first character.
#
# With a normal dictionary we repeatedly write:
#
# if key not in dictionary:
#       dictionary[key] = []
#
# This check appears again...
#
# and again...
#
# and again.
#
# Python recognised this repetitive pattern and automated it.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Compare the next two solutions.
#
# Which lines disappear?
#


words = ["apple", "avocado", "banana"]

groups = {}

for word in words:
    first = word[0]
    if first not in groups:
        groups[first] = []
    groups[first].append(word)

print("\nNormal dict:", groups)


# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Every iteration potentially asks:
#
# "Does this key already exist?"
#
# That repeated check is the boilerplate.
#


groups = defaultdict(list)

for word in words:
    groups[word[0]].append(word)

print("defaultdict:", dict(groups))


# =============================================================================
# DISCUSSION
# =============================================================================
#
# ASK LEARNERS
#
# Which code feels easier to maintain?
#
# Expected Answer
#
# defaultdict
#
# because our code now focuses on the actual problem
# (grouping)
# instead of dictionary bookkeeping.
#


# =============================================================================
# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# defaultdict(list)
#
# Missing key
#
#      ↓
#
# automatically creates []
#
#
# defaultdict(int)
#
# Missing key
#
#      ↓
#
# automatically creates 0
#


# =============================================================================
# INTERVIEW OBSERVATION
# =============================================================================
#
# Q:
# Why not always use defaultdict?
#
# A:
#
# Use it only when automatic creation makes sense.
#
# If creating a missing key should be considered a bug,
# a normal dictionary is the better choice.
#


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# namedtuple
# ----------
#
# tuple
# +
# readable field names
#
#
# defaultdict
# -----------
#
# Missing key
#
#      ↓
#
# default value
#
# list  -> grouping
#
# int   -> counting
#


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ collections solves recurring programming problems.
#
# ✓ Choose the right container instead of forcing list/dict everywhere.
#
# ✓ namedtuple improves readability without losing tuple behaviour.
#
# ✓ namedtuple is immutable.
#
# ✓ defaultdict removes repeated existence checks.
#
# ✓ defaultdict(list) is ideal for grouping.
#
# ✓ defaultdict(int) is ideal for counting.
#


# =============================================================================
# BRIDGE TO THE NEXT TOPIC
# =============================================================================
#
# We have now seen two specialised containers.
#
# The collections module contains two more that are extremely popular:
#
# Counter
#
# and
#
# deque.
#
# Counter eliminates manual frequency counting.
#
# deque provides fast operations at both ends of a sequence.
#
# Those are the next step in becoming more Pythonic.
