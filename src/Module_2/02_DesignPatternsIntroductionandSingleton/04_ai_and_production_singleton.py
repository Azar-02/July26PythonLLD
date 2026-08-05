"""
============================================================
PART 04
AI CORNER AND SINGLETON IN PRODUCTION
============================================================

Topics Covered

1. AI-generated Singleton
2. Discovering the missing thread-safety
3. Thinking like a code reviewer
4. Singleton in production systems
5. Logging
6. Configuration
7. Connection Pools
8. Cache clients
9. Board summary
"""

import threading

# ============================================================
# MOTIVATION
# ============================================================

# We now know how to build a correct thread-safe Singleton.
#
# But in real projects, engineers rarely type every line from
# memory.
#
# They often ask ChatGPT, Copilot or Claude to generate the
# first draft.
#
# Does that mean the generated code is always production ready?
#
# Today's objective is not to criticise AI.
#
# Instead, we will learn how experienced engineers review
# AI-generated code.

# ============================================================
# ASK LEARNERS
# ============================================================

# Suppose you ask an AI:
#
# "Write a Singleton class in Python."
#
# What do you think the AI will generate?
#
# Student Thinking
#
# - A class with __new__
# - A class variable called _instance
# - Return the existing object
#
# All of these are reasonable expectations.

# ============================================================
# A TYPICAL FIRST DRAFT
# ============================================================

class AISingleton:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# ============================================================
# THINK BEFORE REVIEWING
# ============================================================

# ASK LEARNERS
#
# Before saying "Looks good",
# review the code like a senior engineer.
#
# Question:
#
# What important production concern is missing?

# ============================================================
# REVEAL
# ============================================================

# Thread safety.
#
# There is no Lock.
#
# Two concurrent threads may still create
# multiple objects.

print("=" * 60)
print("AI Singleton")
print(AISingleton() is AISingleton())

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The runtime behaviour appears correct in simple tests.
#
# This is exactly why race conditions are dangerous.
#
# Local testing rarely reveals them.

# ============================================================
# DISCUSSION
# ============================================================

# AI is extremely useful for producing
# the INITIAL SHAPE of the pattern.
#
# Your responsibility begins afterwards.
#
# Ask yourself:
#
# • Is it thread-safe?
# • Is it scalable?
# • What happens under load?
# • What would a code reviewer question?

# ============================================================
# COMMON REVIEW QUESTIONS
# ============================================================

# Imagine you are reviewing a pull request.
#
# Review comments could include:
#
# "Where is the Lock?"
#
# "Will this survive concurrent requests?"
#
# "Does __init__ execute repeatedly?"
#
# "Can this object ever be recreated?"

# ============================================================
# WHERE HAVE YOU ALREADY USED SINGLETON?
# ============================================================

# Many developers use Singleton without even
# realising it.

# ============================================================
# LOGGING
# ============================================================

class Logger:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

logger1 = Logger()
logger2 = Logger()

print("=" * 60)
print("Logger Example")
print(logger1 is logger2)

# Runtime Observation
#
# A single logger usually writes to the same
# destination.
#
# Creating dozens of logger objects
# rarely provides additional value.

# ============================================================
# CONFIGURATION OBJECTS
# ============================================================

class AppConfig:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.environment = "production"

        return cls._instance

config = AppConfig()

print("=" * 60)
print("Environment:", config.environment)

# Discussion
#
# Configuration is usually loaded once.
#
# Every service reads the same values.

# ============================================================
# CONNECTION POOL MANAGER
# ============================================================

# Important observation:
#
# Modern frameworks often do NOT keep
# one database connection.
#
# Instead they keep one CONNECTION POOL.
#
# The pool manager itself behaves like
# a Singleton.
#
# The pool internally manages many
# database connections.

# ============================================================
# CACHE CLIENT
# ============================================================

class CacheClient:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance

cache1 = CacheClient()
cache2 = CacheClient()

cache1.cache["user"] = "Alice"

print("=" * 60)
print("Shared Cache")
print(cache2.cache)

# Runtime Observation
#
# Both references observe the same cache
# because both refer to the same object.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Singleton does NOT mean:
#
# "Only one database connection."
#
# It may instead mean:
#
# One manager.
# One logger.
# One configuration object.
# One cache client.
#
# That object itself may internally manage
# many resources.

# ============================================================
# INTERVIEW OBSERVATIONS
# ============================================================

# Frequently Asked
#
# Give practical uses of Singleton.
#
# Why is Logger often implemented
# as a Singleton?
#
# Why is a Connection Pool Manager
# a better example than a raw
# database connection?

# ============================================================
# BOARD SUMMARY
# ============================================================

# AI
#   ↓
# Generates First Draft
#   ↓
# Engineer Reviews
#   ↓
# Thread Safety
# Scalability
# Production Readiness
#
# Common Singleton Examples
#
# Logger
# Config
# Cache Client
# Connection Pool Manager

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# We have implemented Singleton ourselves.
#
# But Python provides more Pythonic ways
# to achieve the same behaviour.
#
# In the next lesson we will explore
# module-level Singletons,
# decorators,
# and metaclasses.
