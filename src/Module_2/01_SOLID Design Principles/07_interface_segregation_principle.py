"""
============================================================
PART 07
INTERFACE SEGREGATION PRINCIPLE (ISP)
============================================================

Topics Covered
1. Why LSP is still not the complete answer
2. Fat interfaces
3. Interface Segregation Principle
4. Bird capability example
5. Real-world examples
6. Common mistakes
7. Interview discussion
8. Bridge to DIP
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lesson we introduced capabilities like
# Flyable and Danceable.
#
# That solved an important LSP problem.
#
# But imagine we design one giant interface.

class BirdActions(ABC):

    @abstractmethod
    def fly(self):
        pass

    @abstractmethod
    def dance(self):
        pass

    @abstractmethod
    def swim(self):
        pass

    @abstractmethod
    def hunt(self):
        pass

# ============================================================
# STOP AND THINK
# ============================================================

# Should every bird be forced to implement
# all four methods?
#
# Think of:
#
# • Sparrow
# • Penguin
# • Eagle
# • Ostrich
#
# Do they all support every capability?

# ============================================================
# FIRST ATTEMPT
# ============================================================

class Sparrow(BirdActions):

    def fly(self):
        print("Sparrow flies.")

    def dance(self):
        print("Sparrow dances.")

    def swim(self):
        raise NotImplementedError("Sparrow is not a swimming bird.")

    def hunt(self):
        raise NotImplementedError("Sparrow does not hunt like an eagle.")

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The compiler/interpreter is satisfied.
#
# But our design is not.
#
# Sparrow is now forced to contain
# methods that make no sense.

# ============================================================
# DISCUSSION
# ============================================================

# This is a common design smell.
#
# If a class repeatedly writes:
#
# raise NotImplementedError(...)
#
# pass
#
# or empty implementations,
#
# ask yourself:
#
# "Am I forcing this class to implement
# something it doesn't need?"

# ============================================================
# DISCOVERING ISP
# ============================================================

# Before giving the definition,
# think about the following question.
#
# Which is better?
#
# One interface with 20 methods?
#
# OR
#
# Four interfaces with 5 focused methods each?

# ============================================================
# FORMAL IDEA
# ============================================================

# Interface Segregation Principle
#
# Clients should not be forced
# to depend on methods they do not use.
#
# In simple words:
#
# Prefer many small focused interfaces
# over one large interface.

# ============================================================
# BETTER DESIGN
# ============================================================

class Flyable(ABC):

    @abstractmethod
    def fly(self):
        pass


class Danceable(ABC):

    @abstractmethod
    def dance(self):
        pass


class Swimmable(ABC):

    @abstractmethod
    def swim(self):
        pass


class Huntable(ABC):

    @abstractmethod
    def hunt(self):
        pass


class Bird:
    def eat(self):
        print("Eating...")

# ============================================================
# CAPABILITY COMPOSITION
# ============================================================

class Sparrow(Bird, Flyable, Danceable):

    def fly(self):
        print("Fluttering flight.")

    def dance(self):
        print("Sparrow courtship dance.")


class Penguin(Bird, Swimmable):

    def swim(self):
        print("Penguin swims beautifully.")


class Eagle(Bird, Flyable, Huntable):

    def fly(self):
        print("Eagle soars high.")

    def hunt(self):
        print("Eagle hunts prey.")

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

sparrow = Sparrow()
penguin = Penguin()
eagle = Eagle()

sparrow.fly()
sparrow.dance()

penguin.swim()

eagle.fly()
eagle.hunt()

# ============================================================
# OBSERVATION
# ============================================================

# Every class now advertises only
# the capabilities it truly supports.
#
# No fake methods.
# No meaningless overrides.
# No empty implementations.

# ============================================================
# REAL WORLD ANALOGY
# ============================================================

# Imagine a university portal.
#
# Student Portal
# Faculty Portal
# Admin Portal
#
# Instead of one gigantic interface:
#
# login()
# grade_students()
# approve_budget()
# submit_assignment()
# conduct_exam()
#
# each role receives only the operations
# it actually needs.

# ============================================================
# COMMON DESIGN SMELLS
# ============================================================

# 1. Large interfaces with unrelated methods.
#
# 2. Classes throwing
#    NotImplementedError frequently.
#
# 3. Empty method bodies.
#
# 4. Interfaces whose implementations
#    use only a small subset of methods.

# ============================================================
# SMALL EXPERIMENT
# ============================================================

flyers = [Sparrow(), Eagle()]

for bird in flyers:
    bird.fly()

# Observation:
#
# Because every object satisfies Flyable,
# the caller remains simple.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# ISP does NOT mean:
#
# Every interface should contain
# exactly one method.
#
# A focused interface may contain
# multiple related methods.
#
# The keyword is:
#
# Related.

# ============================================================
# INTERVIEW CORNER
# ============================================================

# Question:
#
# How do you identify an ISP violation?
#
# Good answer:
#
# If several implementations contain
# empty methods,
# pass,
# or NotImplementedError,
# the interface is probably too large.

# ============================================================
# SELF CHECK
# ============================================================

# Which is better?
#
# PaymentService
#
# with:
# card()
# upi()
# crypto()
# cheque()
# cash()
#
# OR
#
# Separate focused payment interfaces?
#
# Think before answering.

# ============================================================
# ANSWER
# ============================================================

# Prefer focused abstractions
# whenever clients use different subsets
# of functionality.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Large Interface
#        ↓
# Forced methods
#        ↓
# Fake implementations
#        ↓
# Poor design
#
# Focused interfaces
#        ↓
# Honest capabilities
#        ↓
# Better maintainability

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# We now have small interfaces.
#
# But another question appears.
#
# Who should depend on whom?
#
# Should high-level business logic
# depend on concrete classes?
#
# Or should both depend on abstractions?
#
# That question introduces the
# Dependency Inversion Principle.
