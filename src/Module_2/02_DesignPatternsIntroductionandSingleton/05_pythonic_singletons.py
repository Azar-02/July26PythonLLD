"""
============================================================
PART 05
PYTHONIC WAYS TO BUILD A SINGLETON
============================================================

Topics Covered

1. Revisiting our __new__ implementation
2. Why Python offers multiple approaches
3. Module-level Singleton
4. Decorator-based Singleton
5. Metaclass-based Singleton
6. Comparing all approaches
7. Interview observations
8. Board summary
"""

from threading import Lock

# ============================================================
# MOTIVATION
# ============================================================

# So far we manually controlled object creation by overriding
# __new__.
#
# That works well and teaches the core idea behind Singleton.
#
# However, experienced Python developers often solve the same
# problem using more idiomatic approaches.
#
# Today's goal is NOT to replace our earlier implementation.
#
# Instead, we will discover several Pythonic alternatives,
# understand their trade-offs, and learn when each one is
# appropriate.

# ============================================================
# ASK LEARNERS
# ============================================================

# Suppose I ask you to build a Singleton in Python.
#
# Is overriding __new__ the ONLY possible solution?
#
# Student Thinking
#
# "Probably yes."
#
# Reveal
#
# No.
#
# Python's module system, decorators and metaclasses can
# also help us implement the same guarantee.

# ============================================================
# APPROACH 1 - MODULE LEVEL SINGLETON
# ============================================================

# Theory
#
# Python imports a module only once.
#
# After the first import, Python caches the module object.
#
# Every later import receives the SAME module object.

class Configuration:
    def __init__(self):
        self.environment = "production"

config = Configuration()

# Imagine this object lives at module level.
#
# Every file importing this module would access the same
# 'config' object.
# from src.Module_2.02_DesignPatternsIntroductionandSingleton import config

#Python returns the same module object from its import cache. That means:
#       the module is loaded only once
#       config is created only once
#       every importer sees the same config object

print("=" * 60)
print("Module Level Singleton")
print(config.environment)

# Runtime Observation
#
# This is the most Pythonic approach for many applications.
#
# We don't even need to override __new__.

# ============================================================
# ============================================================

# What did Python do for us here?
#
# Expected Answer
#
# Python's import system guarantees the module is loaded only
# once, making module-level objects naturally shared.

# ============================================================
# APPROACH 2 - DECORATOR
# ============================================================

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Logger:

    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)

logger1 = Logger()
logger2 = Logger()

logger1.log("Application Started")

print("=" * 60)
print("Decorator Singleton")
print(logger1 is logger2)
print(logger2.messages)

# Runtime Observation
#
# The decorator stores one object for each decorated class.
#
# Every constructor call returns that stored object.

# ============================================================
# DISCUSSION
# ============================================================

#
# What advantage does the decorator provide over writing
# __new__ inside every class?
#
# Expected Answer
#
# Reusable logic.
#
# We write the Singleton implementation once and apply it to
# multiple classes.

# ============================================================
# APPROACH 3 - METACLASS 
# ============================================================

class SingletonMeta(type):

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:

            with cls._lock:

                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class CacheManager(metaclass=SingletonMeta):

    def __init__(self):
        self.cache = {}


cache1 = CacheManager()
cache2 = CacheManager()

cache1.cache["language"] = "Python"

print("=" * 60)
print("Metaclass Singleton")
print(cache1 is cache2)
print(cache2.cache)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The metaclass intercepts constructor calls.
#
# Instead of each class implementing Singleton separately,
# the metaclass centralises the behaviour.

# A metaclass can change the behavior of class instantiation 
# itself. In this example, the metaclass ensures that every 
# time a class using it is “constructed”, the system returns 
# one shared instance instead of building a new object.


# ============================================================
# COMPARISON
# ============================================================

# Module Level
#
# + Simplest
# + Most Pythonic
# + No extra machinery
#
# Decorator
#
# + Reusable
# + Easy to apply
#
# Metaclass
#
# + Centralised
# + Powerful
# + Excellent when many classes require identical behaviour

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# There is no universally "best" Singleton implementation.
#
# Choose the simplest solution that satisfies the problem.
#
# Many real projects never need a metaclass.

# ============================================================
# INTERVIEW OBSERVATIONS
# ============================================================

# Frequently Asked
#
# Which Singleton approach would you use in Python?
#
# Why is the module-level approach considered Pythonic?
#
# When would a metaclass be justified?
#
# Difference between a decorator and a metaclass?

# ============================================================
# BOARD SUMMARY
# ============================================================

# Module
#    ↓
# Decorator
#    ↓
# __new__
#    ↓
# Metaclass
#
# Same Goal
#
# Exactly One Shared Object

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# We have now explored multiple implementations of the
# Singleton pattern.
#
# Before leaving Singleton completely, one final discussion
# remains:
#
# What are its drawbacks?
#
# How does pickling affect a Singleton?
#
# Can Enum help us?
#
# Those advanced topics complete our Singleton journey.
