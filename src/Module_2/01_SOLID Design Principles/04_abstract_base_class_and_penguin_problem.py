"""
PART 04 - REBUILDING BIRD USING ABSTRACT BASE CLASSES
(Preparing for the Penguin Problem)

Topics Covered
1. Why OCP is still incomplete
2. What belongs in Bird?
3. Shared vs specific behaviour
4. Abstract Base Classes (ABC)
5. @abstractmethod
6. Why Bird objects should not be created directly
7. First look at the Penguin problem
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lesson we achieved something important.
#
# We separated different birds into different classes.
#
# Pigeon owns its flying behaviour.
# Sparrow owns its flying behaviour.
# Eagle owns its flying behaviour.
#
# Excellent.
#
# But pause for a moment.
#
# Are all birds completely different?
#
# Or do they also share some common characteristics?

# ============================================================
# STOP AND THINK
# ============================================================

# Imagine you are creating classes for:
#
#     Pigeon
#     Sparrow
#     Eagle
#
# Question:
#
# Should every class independently store:
#
# • name
# • age
# • color
#
# Or is there a better place for this common data?

# ============================================================
# DISCUSSION
# ============================================================

# These attributes belong to EVERY bird.
#
# Copying them into every class creates duplication.
#
# Whenever several classes share common state or behaviour,
# inheritance becomes a natural candidate.

# ============================================================
# FIRST REFACTOR
# ============================================================

class Bird(ABC):

    def __init__(self, name: str, age: int, color: str):
        self.name = name
        self.age = age
        self.color = color

    def eat(self):
        print(f"{self.name} is eating.")

# ============================================================
# SELF CHECK
# ============================================================

# Which methods belong in Bird?
#
# Generic behaviour?
# or
# Bird-specific behaviour?
#
# Think before continuing.

# ============================================================
# DISCUSSION
# ============================================================

# eat() is generic.
#
# Every bird eats.
#
# Therefore Bird can provide one implementation.
#
# But what about fly()?

# ============================================================
# STOP AND THINK
# ============================================================

# Should Bird implement fly()?
#
# Consider:
#
# Does every bird fly in exactly the same way?

# ============================================================
# DISCUSSION
# ============================================================

# No.
#
# Pigeon flies differently.
# Sparrow flies differently.
# Eagle flies differently.
#
# Therefore Bird cannot provide one correct implementation.

# ============================================================
# ABSTRACT METHOD
# ============================================================

class BirdV2(ABC):

    def __init__(self, name, age, color):
        self.name = name
        self.age = age
        self.color = color

    def eat(self):
        print(f"{self.name} is eating.")

    @abstractmethod
    def fly(self):
        """
        Every concrete bird must provide
        its own flying behaviour.
        """
        pass

# ============================================================
# WHY ABSTRACT?
# ============================================================

# Think about what would happen if BirdV2
# contained a fake fly() implementation.
#
# Subclasses might forget to override it.
#
# The system would silently use incorrect behaviour.
#
# By making fly() abstract,
# Python forces every concrete subclass
# to provide an implementation.

# ============================================================
# DEMO
# ============================================================

class Pigeon(BirdV2):

    def fly(self):
        print("Pigeon: short bursts near the ground.")

class Sparrow(BirdV2):

    def fly(self):
        print("Sparrow: quick fluttering flight.")

class Eagle(BirdV2):

    def fly(self):
        print("Eagle: long soaring glides.")

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# Can BirdV2 be instantiated directly?

p = Pigeon("Oliver",2,"Grey")
s = Sparrow("Max",1,"Brown")
e = Eagle("Sky",5,"Black")

p.eat()
p.fly()
s.fly()
e.fly()

# Uncomment to observe Python's behaviour.
#
# BirdV2("Bird",1,"Grey")

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Pigeon, Sparrow and Eagle work correctly.
#
# But BirdV2 itself cannot be instantiated.
#
# Python protects us from creating an
# incomplete object.
#
# Every concrete bird MUST honour the contract
# established by BirdV2.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

#               BirdV2 (Abstract)
#             /        |        \
#            /         |         \
#      Pigeon      Sparrow      Eagle
#
# Shared:
#   name
#   age
#   color
#   eat()
#
# Specific:
#   fly()

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Abstract classes are NOT created because
# they save lines of code.
#
# They exist to model incomplete ideas.
#
# A generic Bird is a concept.
#
# Real objects are:
#
# • Pigeon
# • Sparrow
# • Eagle

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Interview Question:
#
# Why use an abstract class instead of
# a normal parent class?
#
# Good answer:
#
# Because the parent represents an incomplete
# concept and should never be instantiated.
# It defines the common contract that every
# subclass must follow.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Shared behaviour
#      ↓
#    Bird (ABC)
#
# Specific behaviour
#      ↓
# Concrete subclasses
#
# Abstract methods define contracts.

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# Everything looks perfect...
#
# Until a new requirement arrives.
#
# "Support Penguin."
#
# Penguins are birds.
#
# But Penguins cannot fly.
#
# Our current design now faces
# its biggest challenge.
