"""
PART 05 - THE PENGUIN PROBLEM, CAPABILITY SPLITTING
AND THE CLASS EXPLOSION

Topics Covered
1. The Penguin problem
2. Why the current abstraction breaks
3. FlyingBird vs NonFlyingBird
4. Is the design really solved?
5. The class explosion problem
6. Why another principle is needed
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lesson we built an abstract Bird class.
#
# Every concrete bird was forced to implement fly().
#
# It looked like a beautiful design.
#
# But software design is rarely finished.
#
# New requirements keep arriving.
#
# Today a product manager says:
#
#     "Please support Penguins."

# ============================================================
# STOP AND THINK
# ============================================================

# Before reading further, answer honestly.
#
# Is a Penguin a Bird?
#
# Yes.
#
# Can a Penguin fly?
#
# No.
#
# Now ask yourself:
#
# What happens if Bird forces EVERY subclass
# to implement fly()?

# ============================================================
# THE CURRENT DESIGN
# ============================================================

class Bird(ABC):

    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")

    @abstractmethod
    def fly(self):
        pass

# ============================================================
# FIRST ATTEMPT
# ============================================================

# Most beginners write something similar to this.

class Penguin(Bird):

    def fly(self):
        raise NotImplementedError("Penguins cannot fly!")

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Does this design feel correct?
#
# Question:
#
# Does Penguin REALLY know how to fly?
#
# Or are we only satisfying the compiler/interpreter?

try:
    Penguin("Pingu").fly()
except NotImplementedError as ex:
    print("Runtime:", ex)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The program compiles.
#
# The object exists.
#
# But the design is dishonest.
#
# We created a fly() method
# on an object that should never
# have had one.

# ============================================================
# WHY "pass" IS NOT BETTER
# ============================================================

# Some developers replace the exception with:
#
# def fly(self):
#     pass
#
# Is that better?
#
# No.
#
# Now callers think flying succeeded,
# even though nothing actually happened.
#
# Silent failures are often worse than
# explicit failures.

# ============================================================
# A BETTER IDEA
# ============================================================

# Instead of asking:
#
# "Which birds exist?"
#
# Ask:
#
# "Which birds can fly?"

class BirdV2(ABC):

    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")


class FlyingBird(BirdV2, ABC):

    @abstractmethod
    def fly(self):
        pass


class NonFlyingBird(BirdV2):
    """No fly() exists here."""
    pass


class Sparrow(FlyingBird):

    def fly(self):
        print("Fluttering flight.")


class PenguinV2(NonFlyingBird):
    pass

# ============================================================
# SMALL EXPERIMENT
# ============================================================

sparrow = Sparrow("Jack")
sparrow.fly()

penguin = PenguinV2("Pingu")

print("Penguin has fly():", hasattr(penguin, "fly"))

# ============================================================
# DISCUSSION
# ============================================================

# Compare both designs.
#
# OLD DESIGN
#
# Penguin had a fake fly().
#
# NEW DESIGN
#
# Penguin simply has no fly().
#
# That is much closer to reality.

# ============================================================
# STOP AND THINK
# ============================================================

# Have we completely solved the problem?
#
# Imagine a new requirement:
#
# Some birds can dance.
#
# Some cannot.

# ============================================================
# THINK BEFORE READING
# ============================================================

# If we continue using the same idea,
# what classes might appear?

# ============================================================
# DISCUSSION
# ============================================================

# FlyingDancingBird
# FlyingNonDancingBird
# NonFlyingDancingBird
# NonFlyingNonDancingBird
#
# Already four classes.

# Add swimming.
#
# The number doubles again.

# ============================================================
# THE CLASS EXPLOSION
# ============================================================

# Behaviours      Classes
# ------------------------
# 1                    2
# 2                    4
# 3                    8
# 4                   16
# n                  2^n
#
# Every new capability
# doubles the number of classes.

# ============================================================
# WHY THIS IS A PROBLEM
# ============================================================

# At first,
# the hierarchy looks organised.
#
# But every new behaviour forces
# another split.
#
# Eventually maintaining the hierarchy
# becomes harder than maintaining
# the original code.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Splitting classes is good.
#
# Splitting forever is not.
#
# A better abstraction is still waiting
# to be discovered.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Interviewers often ask:
#
# "Why is FlyingBird / NonFlyingBird
# still not an ideal design?"
#
# Good answer:
#
# Because every additional capability
# doubles the inheritance hierarchy,
# leading to class explosion.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

#                 Bird
#               /      \
#      FlyingBird    NonFlyingBird
#          |              |
#      Sparrow        Penguin
#
# Add dancing...
#
#             4 classes
#
# Add swimming...
#
#             8 classes

# ============================================================
# BOARD SUMMARY
# ============================================================

# Fake behaviour
#      ↓
# Bad design
#
# Split by capability
#      ↓
# Better
#
# Too many capabilities
#      ↓
# Class Explosion

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# We now know that:
#
# One giant Bird class is bad.
#
# Splitting only by FlyingBird and
# NonFlyingBird is still not enough.
#
# The next question becomes:
#
# Instead of grouping birds,
# can we group independent capabilities?
#
# That idea leads us directly to the
# Liskov Substitution Principle and
# capability-based design.
