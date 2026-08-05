"""
============================================================
PART 01
DESIGN PATTERNS - INTRODUCTION
============================================================

Topics Covered
1. Why Design Patterns exist
2. SOLID vs Design Patterns
3. What is a Design Pattern?
4. Gang of Four (GoF)
5. Types of Design Patterns
6. Introduction to Singleton
7. Why do we need Singleton?
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lectures we learnt the SOLID principles.
#
# SOLID teaches us HOW to think while designing software.
#
# But imagine building ten different backend systems.
#
# Every few months you notice yourself solving the same
# design problem again and again.
#
# Eventually engineers stop inventing a fresh solution
# every time.
#
# Instead, they begin recognising recurring solutions.
#
# Those recurring solutions are called Design Patterns.
#
# This lecture intentionally begins from the problem before
# introducing the formal definition.

# ============================================================
# DISCUSSION
# ============================================================


# If SOLID already teaches good design,
# why did the software industry create Design Patterns?
#
#
# "Maybe SOLID is not enough?"
# "Patterns are reusable code?"
#
#
# SOLID provides principles.
# Design Patterns provide proven solution shapes for
# recurring design problems.

# ============================================================
# THEORY
# ============================================================

# Design Pattern
#
# A well-known, tested solution to a problem that keeps
# appearing across many software systems.
#
# A pattern is NOT code.
# A pattern is NOT a framework.
# A pattern is NOT copied implementation.
#
# It is a reusable design idea.

# Analogy
#
# A floor tile pattern repeats.
# A sine wave pattern repeats.
# Likewise, software design problems repeat.

# ============================================================
# GANG OF FOUR
# ============================================================

# In 1994 four authors documented 23 famous design patterns.
#
# They became popularly known as the Gang of Four (GoF).
#
# Their contribution was not inventing every pattern.
#
# They observed solutions repeatedly appearing in industry
# and documented them using common names.

# ============================================================
# WHY NAMES MATTER
# ============================================================

# Imagine a design review.
#
# Instead of explaining a complete architecture,
# one engineer simply says:
#
# "Let's use a Factory here."
#
# Every experienced engineer immediately understands the
# overall structure.
#
# Shared vocabulary is one of the biggest advantages of
# design patterns.

# ============================================================
# TYPES OF DESIGN PATTERNS
# ============================================================

# ASK LEARNERS
#
# If you had to group all design patterns,
# how would you categorise them?
#
# Expected Answer
#
# According to the kind of problem they solve.

CREATIONAL = [
    "Singleton",
    "Builder",
    "Prototype",
    "Factory"
]

STRUCTURAL = [
    "Adapter",
    "Decorator",
    "Facade"
]

BEHAVIOURAL = [
    "Strategy",
    "Observer"
]

print("Creational :", CREATIONAL)
print("Structural :", STRUCTURAL)
print("Behavioural:", BEHAVIOURAL)

# Expected Observation
#
# These are categories, not complete lists.

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Students often confuse a category with a pattern.
#
# Singleton is a pattern.
#
# Creational is merely the bucket that contains it.

# ============================================================
# INTRODUCTION TO SINGLETON
# ============================================================

#
# Just from the name "Singleton",
# what problem do you think it solves?
#
#
# Only one object should exist.

# Formal Idea
#
# A Singleton ensures:
#
# 1. Exactly one object exists.
# 2. Everyone accesses that same object.

# ============================================================
# WHY WOULD WE EVER WANT ONLY ONE OBJECT?
# ============================================================

# Reason 1
#
# Shared resource.
#
# Example:
#
# Database Connection
# Logger
# Cache

# Analogy
#
# Think about a shared office printer.
#
# Buying five printers for ten employees usually
# increases cost without solving a real problem.

# Reason 2
#
# Object creation is expensive.
#
# A database connection requires:
#
# - Network communication
# - Authentication
# - Resource allocation
#
# Repeating that work unnecessarily slows the application.

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict the output.

class DBConnection:
    pass

db1 = DBConnection()
db2 = DBConnection()

print()
print("db1 is db2 :", db1 is db2)
print("id(db1):", id(db1))
print("id(db2):", id(db2))

# Expected Output
#
# False
#
# Expected Observation
#
# Every constructor call creates a fresh object.

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Nothing currently prevents creating hundreds of
# DBConnection objects.
#
# This is exactly the problem Singleton attempts to solve.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Frequently Asked
#
# Difference between:
#
# SOLID
# vs
# Design Patterns
#
# Good answer:
#
# SOLID helps discover good designs.
# Design Patterns provide reusable solutions that
# repeatedly satisfy those principles.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Design Problems Repeat
#          ↓
# Engineers Reuse Good Solutions
#          ↓
# Those Solutions Become
# Design Patterns
#
# First Creational Pattern:
# Singleton

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# We now understand WHY Singleton exists.
#
# The next question naturally becomes:
#
# How can Python actually guarantee that only one object
# is ever created?
#
# That journey begins by writing the naive implementation
# first and gradually improving it.
