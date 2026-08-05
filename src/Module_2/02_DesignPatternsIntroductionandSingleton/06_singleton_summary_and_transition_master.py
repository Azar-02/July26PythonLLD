"""
============================================================
PART 07
SINGLETON RECAP, COMPARISON & DECISION GUIDE
============================================================

Topics Covered

1. Revisiting the Singleton journey
2. Comparing every implementation
3. Choosing the right implementation
4. Production decision making
5. Common mistakes
6. Interview discussions
7. Final board summary
"""

# ============================================================
# MOTIVATION
# ============================================================

# Before moving to the Builder Pattern, we should answer one
# important question.
#
# Imagine you join a company tomorrow.
#
# You already know five different Singleton implementations.
#
# Which one should you actually choose?
#
# Memorising implementations is easy.
#
# Engineering is choosing the right implementation for the
# right situation.

# ============================================================
# ASK LEARNERS
# ============================================================

# Which Singleton implementation would you pick for:
#
# • Logger
# • Configuration
# • Cache Client
# • Framework Settings
#
# Student Thinking
#
# Most students immediately answer:
#
# "Metaclass."
#
# Pause...
#
# Is the most advanced solution always the best solution?

# ============================================================
# REVISITING THE JOURNEY
# ============================================================

# We did not start by writing code.
#
# We started with a problem.
#
# Expensive objects.
#
# Shared resources.
#
# Repeated object creation.
#
# Every implementation we studied attempts to solve exactly
# the same problem.

# ============================================================
# COMPARISON TABLE
# ============================================================

comparison = [
    ("Module Level", "★★★★★", "Most Pythonic"),
    ("__new__", "★★★★☆", "Learning / Explicit"),
    ("Decorator", "★★★★☆", "Reusable"),
    ("Metaclass", "★★★★★", "Reusable + Powerful"),
]

print("=" * 70)
print(f'{"Approach":20} {"Difficulty":12} Recommendation')
print("-" * 70)
for row in comparison:
    print(f"{row[0]:20} {row[1]:12} {row[2]}")

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Notice something interesting.
#
# None of the approaches changed the goal.
#
# They only changed HOW we reached that goal.

# ============================================================
# DECISION TREE
# ============================================================

# ASK LEARNERS
#
# Do you actually need a class?
#
# If No
#      ↓
# Module-level object
#
# If Yes
#      ↓
# Do many classes need Singleton?
#
# If No
#      ↓
# __new__
#
# If Yes
#      ↓
# Decorator or Metaclass

# ============================================================
# COMMON MISTAKES
# ============================================================

# Mistake 1
#
# Choosing Singleton because it sounds advanced.
#
# Mistake 2
#
# Turning every service into a Singleton.
#
# Mistake 3
#
# Forgetting thread safety.
#
# Mistake 4
#
# Ignoring testing difficulties.

# ============================================================
# SMALL DISCUSSION
# ============================================================

# ASK LEARNERS
#
# Can Singleton violate SOLID?
#
# Student Thinking
#
# "No. It's a design pattern."
#
# Reveal
#
# Any pattern can be misused.
#
# If Singleton introduces unnecessary coupling or hidden
# dependencies, it can hurt maintainability.

# ============================================================
# INTERVIEW SIMULATION
# ============================================================

# Interviewer:
#
# Why didn't you choose a metaclass?
#
# Strong Candidate:
#
# "Because only one class required Singleton behaviour.
# A module-level object solved the problem with far less
# complexity."
#
# Interviewer:
#
# Excellent.
#
# Notice the candidate justified the decision using the
# problem—not the popularity of a pattern.

# ============================================================
# MASTER TAKEAWAYS
# ============================================================

# Pattern mastery means:
#
# 1. Recognising the recurring problem.
# 2. Understanding the trade-offs.
# 3. Selecting the simplest correct solution.
# 4. Explaining WHY that solution fits.

# ============================================================
# FINAL BOARD SUMMARY
# ============================================================

# Shared Resource
#        │
#        ▼
# Need One Object
#        │
#        ▼
# Singleton
#        │
#        ├── Module
#        ├── __new__
#        ├── Decorator
#        └── Metaclass
#
# Simplest Correct Solution
#          >
# Most Complicated Solution

# ============================================================
# BRIDGE TO BUILDER PATTERN
# ============================================================

# Singleton answered:
#
# "How do we ensure only one object exists?"
#
# The next creational pattern asks a completely different
# question.
#
# What if creating an object itself becomes difficult because
# it has too many fields, optional values and construction
# steps?
#
# That naturally begins our journey into the Builder Pattern.
