"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 02_strategy_implementation.py
============================================================

Topics Covered
--------------
1.  Where File 01 Left Us
2.  The Shared Interface
3.  One Class Per Mode
4.  Who Picks The Calculator
5.  GoogleMaps After The Fix
6.  Rebuild Or Reuse
7.  The Factory
8.  Running It
9.  An Unknown Mode
10. Spotting The Singleton
11. Spotting The Factory
12. Three Patterns, Stacked
13. Quiz
14. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 01 LEFT US
# ============================================================

# One find_path() method with
# an if-elif per mode broke
# two principles at once.
#
# Open-Closed.
#
# Single Responsibility.
#
# We decided on the fix:
#
#     one shared interface,
#
#     one class per mode.
#
# Now we write it.

# ============================================================
# A SMALL PLACEHOLDER
# ============================================================

# Every calculator returns a
# Path.
#
# What's inside it doesn't
# matter for today.


class Path:

    def __repr__(self):
        return "Path()"


# ============================================================
# THE SHARED INTERFACE
# ============================================================

# Every mode-specific way of
# finding a path implements
# this.


class PathCalculator(ABC):

    @abstractmethod
    def find_path(self, source, destination):
        ...


# ============================================================
# ONE CLASS PER MODE
# ============================================================

# Notice mode is never passed
# in.
#
# Each class simply IS one
# specific way of finding a
# path.


class CarPathCalculator(PathCalculator):

    def find_path(self, source, destination):
        print("  car-specific logic")
        return Path()


class BikePathCalculator(PathCalculator):

    def find_path(self, source, destination):
        print("  bike-specific logic")
        return Path()


class WalkPathCalculator(PathCalculator):

    def find_path(self, source, destination):
        print("  walk-specific logic")
        return Path()


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# GoogleMaps.find_path() still
# takes a mode parameter.
#
# The caller still has to say
# which one they want.
#
# So how does GoogleMaps
# figure out WHICH
# PathCalculator to use —
#
# without bringing back the
# if-elif we just got rid of?

# ============================================================
# THE ANSWER
# ============================================================

# We need something whose only
# job is:
#
#     "give me the right
#      PathCalculator for this
#      mode."
#
# That's a Factory.

# ============================================================
# GOOGLEMAPS AFTER THE FIX
# ============================================================


class GoogleMaps:

    def find_path(self, source, destination, mode):
        pc = PathCalculatorFactory.get_pc(mode)
        return pc.find_path(source, destination)


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now think about how
# PathCalculatorFactory should
# be built.
#
# Does it need to create a
# fresh CarPathCalculator
# every single time someone
# asks for one?
#
# Or can it just reuse the
# same one?

# ============================================================
# THE ANSWER
# ============================================================

# It can reuse the same one.
#
# None of these classes hold
# any state that changes
# between calls.
#
# So there's no real reason to
# keep rebuilding them.

# ============================================================
# THE FACTORY
# ============================================================


class PathCalculatorFactory:
    # This dict is built exactly ONCE — the moment this class is
    # first defined — the same "build it once, reuse it forever"
    # idea we saw with a Java static block, just expressed as a
    # plain class-level dictionary here.
    _calculators = {
        "car": CarPathCalculator(),
        "bike": BikePathCalculator(),
        "walk": WalkPathCalculator(),
    }

    @staticmethod
    def get_pc(mode):
        calculator = PathCalculatorFactory._calculators.get(mode)
        if calculator is None:
            raise ValueError(f"Unknown mode: {mode}")
        return calculator


# ============================================================
# RUNNING IT
# ============================================================

print("Three Modes, One GoogleMaps")

maps = GoogleMaps()

for mode in ["car", "bike", "walk"]:
    print(maps.find_path("Jaipur", "Delhi", mode))

# Observation:
#
# GoogleMaps has no branches
# left in it.
#
# It asks. It delegates. It
# returns.

# ============================================================
# AN UNKNOWN MODE
# ============================================================

print("\nAn Unknown Mode")

try:
    maps.find_path("Jaipur", "Delhi", "transit")
except ValueError as error:
    print(error)

# Observation:
#
# The failure happens in one
# place.
#
# The factory.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Look closely at that
# _calculators dict.
#
# Each value is created
# exactly once and reused
# forever.
#
# Where have we seen this idea
# before in this course?

# ============================================================
# THE ANSWER
# ============================================================

# That's a Singleton.
#
# Each strategy is basically
# being used as a single,
# shared instance.

print("\nSame Object Every Time")

first = PathCalculatorFactory.get_pc("car")
second = PathCalculatorFactory.get_pc("car")
print(first is second)

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# And what about get_pc(mode)
# itself?
#
# A method whose whole job is
# deciding which object to
# hand back, based on some
# input?

# ============================================================
# THE ANSWER
# ============================================================

# That's a Factory.
#
# The same simple factory idea
# we already used earlier in
# the course.

# ============================================================
# THREE PATTERNS, STACKED
# ============================================================

# So here's something worth
# sitting with.
#
# What we call "the Strategy
# pattern" is really three
# smaller patterns, stacked
# together.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Strategy, fully assembled,
# is really THREE ideas
# working together:
#
# 1. STRATEGY
#
#        each way of doing the
#        task gets its own
#        class, all behind one
#        shared interface
#
# 2. SINGLETON
#
#        each of those classes
#        is reused, not rebuilt
#
# 3. FACTORY
#
#        one place decides which
#        one to hand back
#
# This is a good reminder that
# a "named pattern" is often
# just a few smaller, familiar
# ideas, used together.


# ============================================================
# QUIZ
# ============================================================

# A team builds Strategy
# correctly, but writes
# PathCalculatorFactory.get_pc()
# so that it creates a
# brand-new CarPathCalculator
# every single time it's
# called —
#
# even though CarPathCalculator
# has no changing state.
#
# What's the actual cost of
# doing this?
#
# A) No cost — this is
#    required for correctness
#
# B) It creates unnecessary
#    objects for something that
#    could easily be shared —
#    exactly the kind of waste
#    Singleton exists to avoid
#
# C) It breaks the Strategy
#    pattern completely
#
# D) It violates the Liskov
#    Substitution Principle
#
# Answer:
#
# B)

# ============================================================
# CHECKPOINT
# ============================================================

# Solid on the shape?
#
# An interface.
#
# One class per way of doing
# the task.
#
# A factory handing out shared
# instances.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Each mode gets its own class
# behind one shared
# PathCalculator interface.
#
# The mode parameter never
# reaches the calculator — the
# class already IS that mode.
#
# GoogleMaps asks a factory
# for the right calculator and
# delegates.
#
# No branches remain inside
# it.
#
# The strategies hold no
# changing state, so the
# factory builds each one once
# and reuses it forever.
#
# What we call "Strategy" is
# really Strategy plus
# Singleton plus Factory,
# working together.
#
# A named pattern is often
# just a few smaller, familiar
# ideas used at once.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We built this for routes.
#
# Next, the same structure on
# a problem that decides where
# your money goes.
#
# Thousands of AI queries a
# minute.
#
# Some trivial.
#
# Some genuinely hard.
#
# And one decision to make for
# every single one of them.
#
# Next:
#
# 03_strategy_in_a_real_backend.py
