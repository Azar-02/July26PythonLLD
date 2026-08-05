"""
============================================================
PART 02
BUILDING THE SINGLETON – DISCOVERING THE SOLUTION
============================================================

Topics Covered

1. Revisiting the DBConnection problem
2. Why the naive implementation fails
3. Discovering where object creation happens
4. __new__ vs __init__
5. Building the first Singleton
6. Why __init__ still executes
7. Important observations
8. Interview notes
9. Board summary
"""

# ============================================================
# MOTIVATION
# ============================================================

# Last class we answered WHY Singleton exists.
# 
# We discovered two major reasons:
#
# 1. A class manages a shared resource.
# 2. Creating the object is expensive.
#
# We deliberately stopped before writing the implementation.
#
# Today we will build the implementation naturally.
#
# We will NOT jump directly to the final Singleton.
#
# Instead we will first write the code that every beginner
# would naturally write.
#
# Then we will discover why it fails.

# ============================================================
# ============================================================

# Imagine we have a DBConnection class.
#
# Should Python automatically stop us from creating two
# database connections?
#
#
# "Maybe yes."
# "Maybe Python already remembers the first object."
#
# Reveal--
#
# No.
#
# Every constructor call creates a fresh object unless we
# explicitly change that behaviour.

# ============================================================
# VERSION 1 – THE NAIVE IMPLEMENTATION
# ============================================================

class DBConnectionV1:

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# db1 is db2 ?
#
# Same object?
# Different object?
#
# Why?

db1 = DBConnectionV1("db.prod", "admin", "secret")
db2 = DBConnectionV1("db.prod", "admin", "secret")

print("=" * 60)
print("V1")
print("db1 is db2 :", db1 is db2)
print("id(db1)    :", id(db1))
print("id(db2)    :", id(db2))

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Python never checked whether another DBConnection already
# existed.
#
# Every call to DBConnectionV1(...)
#
#          Constructor
#               │
#               ▼
#        New Object Created
#
# Therefore nothing prevents:
#
# db1
# db2
# db3
# db1000

# ============================================================
# WHY IS THIS A PROBLEM?
# ============================================================

# ASK LEARNERS
#
# Imagine every service creates its own connection.
#
# UserService
# OrderService
# PaymentService
#
# What is being wasted?
#
# ---
#
# Repeated connection setup.
#
# Multiple expensive objects.
#
# Multiple resources doing identical work.

# ============================================================
# COMMON WRONG IDEA
# ============================================================

# Students often suggest:
#
# "Let's stop object creation inside __init__."
#
# Excellent instinct.
#
# But first we need to answer one question.

# ============================================================
# DISCOVERY
# ============================================================

#
# Which method actually CREATES an object?
#
# __init__ ?
#
# __new__ ?
#
#
# Most beginners answer:
#
# __init__

# ============================================================
# REVEAL
# ============================================================

# Python object creation actually happens in two phases.
#
#             Constructor Call
#                    │
#                    ▼
#              __new__(...)
#                    │
#          Raw object gets created
#                    │
#                    ▼
#              __init__(...)
#                    │
#      Object fields are initialised
#
# Therefore:
#
# __new__ creates.
#
# __init__ initialises.

# ============================================================
# SMALL EXPERIMENT
# ============================================================

class Demo:

    def __new__(cls):
        print("__new__ called")
        return super().__new__(cls)

    def __init__(self):
        print("__init__ called")

print("=" * 60)
print("Object Creation Order")
Demo()

# Runtime Observation
#
# __new__ always executes before __init__.

# ============================================================
# ============================================================

# If we want to refuse creation of a second object...
#
# Which method should contain the check?

# Reveal
#
# __new__
#
# Because no object exists before __new__ finishes.

# ============================================================
# VERSION 2 – FIRST SINGLETON
# ============================================================

class DBConnectionV2:

    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            print("Creating first object...")
            cls._instance = super().__new__(cls)

        else:
            print("Returning existing object...")

        return cls._instance

    def __init__(self, url, username, password):
        print("__init__ executing")
        self.url = url
        self.username = username
        self.password = password

print("=" * 60)
print("Singleton V1")

a = DBConnectionV2("db.prod", "admin", "secret")
b = DBConnectionV2("db.prod", "admin", "secret")

print("a is b :", a is b)
print(id(a))
print(id(b))

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Did you notice something surprising?
#
# We created only ONE object.
#
# Yet "__init__ executing" appeared twice.
#
# Why?

# ============================================================
# EXPLANATION
# ============================================================

# Returning an existing object from __new__
# DOES NOT skip __init__.
#
# Python still calls __init__
# on whatever object __new__ returns.
#
# Therefore:
#
# Constructor Call
#        │
#        ▼
# __new__ returns old object
#        │
#        ▼
# __init__ runs again
#
# This is harmless here because we pass the same values.
#
# In production, expensive work inside __init__
# often needs additional guarding.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

#          a --------┐
#                    │
#                    ▼
#             DBConnection Object
#                    ▲
#                    │
#          b --------┘

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception 1
#
# __init__ creates objects.
#
# Incorrect.
#
# __new__ creates.
# __init__ initialises.
#
# Misconception 2
#
# __init__ executes only once.
#
# Incorrect.
#
# It executes after every constructor call.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Very common questions:
#
# Why can't Singleton logic be placed inside __init__?
#
# Explain the difference between
# __new__ and __init__.
#
# Why does __init__ execute twice
# in a Singleton implementation ?

# ============================================================
# BOARD SUMMARY
# ============================================================

# Constructor
#      │
#      ▼
#   __new__
#      │
# Creates Object
#      │
#      ▼
#   __init__
#      │
# Initialises Object
#
# Singleton intercepts creation inside __new__.

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# Our Singleton now works perfectly...
#
# ...as long as only ONE thread calls it.
#
# What if two threads call DBConnection()
# at exactly the same time?
#
# That question leads us directly into
# thread safety and race conditions.
