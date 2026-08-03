"""
PART 7 - SINGLETON DECORATOR

Topics Covered

1. Why Singleton exists
2. Traditional Singleton idea
3. Singleton using a decorator
4. Closure storing instances
5. Practical demonstration
"""

# ============================================================
# MOTIVATION
# ============================================================

# Some classes should have only ONE object.
#
# Examples:
# - Database Connection
# - Configuration Manager
# - Logger
# - Cache
#
# Creating multiple objects may waste resources or cause
# inconsistent state.
#
# Singleton ensures only one instance exists.

# ============================================================
# DISCUSSION
# ============================================================

# ASK LEARNERS
#
# If two parts of the application each create a configuration
# object, should they receive different configurations?
#
# Ideally, no.
#
# Everyone should share the same object.

# ============================================================
# THEORY
# ============================================================

# A Singleton guarantees:
#
# 1. Only one object is created.
# 2. Every future request returns the same object.

# ============================================================
# COMMON MISCONCEPTION
# ============================================================

# Singleton does NOT stop you from calling the class.
#
# Instead, it intercepts object creation and returns the
# previously created instance.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

# App A --------┐
#               │
# App B --------┼------> Configuration Object
#               │
# App C --------┘

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# If we create Database() three times,
# how many actual objects will exist?

# ============================================================
# DEMO 1 - SINGLETON DECORATOR
# ============================================================

from functools import wraps

def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            print(f"Creating first instance of {cls.__name__}")
            instances[cls] = cls(*args, **kwargs)
        else:
            print(f"Reusing existing instance of {cls.__name__}")
        return instances[cls]

    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Connecting to database...")

db1 = Database()
db2 = Database()
db3 = Database()

print("\nIdentity Checks")
print(db1 is db2)
print(db2 is db3)
print(id(db1))
print(id(db2))
print(id(db3))

# Runtime Observation:
#
# __init__ executed only once.
#
# Every later call returned the same object.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

print("\nType Information")
print(type(db1))
print(callable(Database))

# ============================================================
# THEORY - HOW IT WORKS
# ============================================================

# The closure contains:
#
# instances = {}
#
# Since the closure survives after singleton() finishes,
# the dictionary remains available for every future call.
#
# The dictionary remembers whether an object has already
# been created.

# ============================================================
# EXECUTION FLOW
# ============================================================

# @singleton
# class Database:
#     ...
#
# becomes
#
# Database = singleton(Database)
#
# Later:
#
# Database()
#      │
#      ▼
# get_instance()
#      │
#      ├── already exists? -> return existing object
#      └── otherwise create and store it

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Why is a closure useful here?
#
# Because it remembers the instances dictionary without
# making it global.
#
# Why use a decorator?
#
# It separates Singleton logic from business logic.

# ============================================================
# BOARD SUMMARY
# ============================================================

# singleton(cls)
#        │
#        ▼
# instances {}
#        │
#        ▼
# get_instance()
#        │
#        ├── create once
#        └── reuse forever

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# Decorators showed us how functions can wrap behaviour.
#
# Next we move to another powerful Python protocol:
#
# Iterators.
#
# We will discover how for-loops really work internally.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ Singleton ensures only one object exists.
# ✓ Closures remember the instances dictionary.
# ✓ Decorators cleanly separate creation logic.
# ✓ Future calls reuse the same object.
