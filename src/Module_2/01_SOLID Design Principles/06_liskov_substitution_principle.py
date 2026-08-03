"""
============================================================
PART 06
LISKOV SUBSTITUTION PRINCIPLE (LSP)
============================================================

Topics Covered
1. Revisiting the Penguin Problem
2. What is substitutability?
3. Discovering LSP naturally
4. Capability-based design
5. Flyable and Danceable
6. Multiple inheritance
7. Square vs Rectangle
8. Interview observations
9. Board summary
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lesson we split birds into FlyingBird and
# NonFlyingBird to avoid fake fly() methods.
#
# That solved one problem.
#
# But another question appears.
#
# Is the real issue that Penguin cannot fly?
#
# Or is there something even deeper?

# ============================================================
# STOP AND THINK
# ============================================================

# Imagine the following function.

def make_bird_fly(bird):
    bird.fly()

# Ask yourself:
#
# Should this function care whether it receives
# Sparrow, Eagle or Parrot?
#
# Ideally...
#
# No.
#
# If every flying bird behaves according to the
# expected contract, the caller should not require
# any special handling.

# ============================================================
# BACKEND DEVELOPER ANALOGY
# ============================================================

# Consider a company hiring Backend Developers.
#
# Management assumes every Backend Developer can:
#
# • Design APIs
# • Debug services
# • Write business logic
#
# Now imagine one employee is hired as a
# Backend Developer but cannot perform any backend work.
#
# Every manager now has to write:
#
# if employee.name == "X":
#     don't assign API work
#
# This is a design smell.
#
# The role "Backend Developer" promised
# a capability that one object cannot honour.

# ============================================================
# THE SAME IDEA APPLIES TO BIRDS
# ============================================================

class Bird:
    def eat(self):
        print("Bird is eating.")

class Sparrow(Bird):
    def fly(self):
        print("Sparrow flies.")

class Penguin(Bird):
    pass

# ============================================================
# DISCUSSION
# ============================================================

# A Penguin is definitely a Bird.
#
# But should every place that works with Bird
# now ask:
#
# if isinstance(bird, Penguin):
#     ...
#
# The moment callers begin writing special cases,
# substitutability starts breaking down.

# ============================================================
# DISCOVERING LSP
# ============================================================

# Think about inheritance.
#
# Why do we create child classes?
#
# One important reason is:
#
# We want to use the child anywhere the parent
# is expected.
#
# If replacing Parent with Child changes the
# correctness of the program,
# then the inheritance hierarchy communicates
# the wrong relationship.

# ============================================================
# FORMAL IDEA
# ============================================================

# Liskov Substitution Principle
#
# Objects of a subclass should be replaceable
# wherever objects of the superclass are expected,
# without breaking program correctness.

# ============================================================
# BAD DESIGN EXAMPLE
# ============================================================

class FlyingBird(Bird, ABC):

    @abstractmethod
    def fly(self):
        pass

class Eagle(FlyingBird):
    def fly(self):
        print("Eagle soars.")

birds = [Eagle()]

for b in birds:
    b.fly()

# ============================================================
# OBSERVATION
# ============================================================

# Every object inside birds supports fly().
#
# Therefore the caller never needs:
#
# if isinstance(...)
#
# or
#
# try:
#     fly()
# except:
#     ...
#
# This is a strong indicator that the abstraction
# communicates the correct capability.

# ============================================================
# CAPABILITY-BASED DESIGN
# ============================================================

class Flyable(ABC):

    @abstractmethod
    def fly(self):
        pass


class Danceable(ABC):

    @abstractmethod
    def dance(self):
        pass


class BirdBase:
    def eat(self):
        print("Eating...")


class Sparrow(BirdBase, Flyable, Danceable):

    def fly(self):
        print("Fluttering flight.")

    def dance(self):
        print("Sparrow courtship dance.")


class Penguin(BirdBase, Danceable):

    def dance(self):
        print("Penguin dance.")

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Notice something interesting.
#
# Penguin never lies.
#
# It never pretends to fly.
#
# Sparrow advertises Flyable.
#
# Penguin does not.
#
# The inheritance hierarchy now reflects reality.

s = Sparrow()
p = Penguin()

s.eat()
s.fly()
s.dance()

p.eat()
p.dance()

# ============================================================
# WHY MULTIPLE INHERITANCE?
# ============================================================

# We are no longer modelling categories.
#
# We are modelling independent capabilities.
#
# A bird may:
#
# • Fly
# • Dance
# • Swim
#
# These capabilities evolve independently.

# ============================================================
# SAFE COLLECTIONS
# ============================================================

flyers = [Sparrow()]

for bird in flyers:
    bird.fly()

# Observation:
#
# The loop is completely safe because every
# object satisfies the Flyable contract.

# ============================================================
# CLASS EXPLOSION AVOIDED
# ============================================================

# Earlier we discussed:
#
# FlyingBird
# NonFlyingBird
# FlyingSwimmingBird
# ...
#
# Instead,
#
# capabilities are composed as required.

# ============================================================
# CLASSIC INTERVIEW QUESTION
# ============================================================

class Rectangle:

    def __init__(self):
        self.width = 0
        self.height = 0

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def area(self):
        return self.width * self.height


class Square(Rectangle):

    def set_width(self, w):
        self.width = w
        self.height = w

    def set_height(self, h):
        self.width = h
        self.height = h

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

def use_rectangle(rect):
    rect.set_width(5)
    rect.set_height(10)
    print("Expected Area =", 50)
    print("Actual Area   =", rect.area())

print("Rectangle")
use_rectangle(Rectangle())

print("\nSquare")
use_rectangle(Square())

# ============================================================
# DISCUSSION
# ============================================================

# Why did Square fail?
#
# Because callers expected Rectangle behaviour.
#
# Replacing Rectangle with Square changed
# the observable behaviour.
#
# Therefore Square is NOT a behavioural substitute
# for Rectangle.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# LSP is NOT:
#
# "Always use inheritance."
#
# LSP is NOT:
#
# "Every child must override methods."
#
# LSP IS:
#
# Child objects should preserve the behavioural
# expectations established by the parent.

# ============================================================
# INTERVIEW OBSERVATIONS
# ============================================================

# Questions often asked:
#
# 1. Explain LSP without using the definition.
# 2. Why is Square-Rectangle famous?
# 3. How do isinstance() checks indicate
#    possible design issues?
# 4. Why is capability-based design often
#    preferred over deep inheritance?

# ============================================================
# BOARD SUMMARY
# ============================================================

# Parent promises behaviour
#           ↓
# Child must honour that promise
#           ↓
# Caller should never require
# special handling for one child
#
# Think in terms of capabilities,
# not forced inheritance.

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# We have separated behaviour using capabilities.
#
# But another question remains.
#
# Should every class be forced to implement
# methods it never uses?
#
# That naturally leads us to the
# Interface Segregation Principle.
