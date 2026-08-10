"""
============================================================
LLD-6 : DESIGN PATTERNS - PROTOTYPE & REGISTRY
FILE : 04_shallow_vs_deep_copy.py
============================================================

Topics Covered
--------------
1.  Recap: Why Independence Held Until Now
2.  Adding One Mutable Field
3.  The AI Corner: A Vague Prompt
4.  Reading The Generated Code
5.  Proving The Bug With id()
6.  The Shared Box Picture
7.  The One Line Fix
8.  Where The Fix Stops Working
9.  Nested Mutable State
10. The copy Module
11. copy.copy vs copy.deepcopy
12. When deepcopy Is Wrong
13. Sharing On Purpose
14. A Better Prompt
15. Interview Questions
16. Key Takeaways
"""

import copy
from abc import ABC, abstractmethod

# ============================================================
# RECAP
# ============================================================

# Three files in.
#
# Objects clone themselves.
#
# Templates live in a
# registry.
#
# Clients customize only
# what varies.
#
# And every single field
# we used was a string,
# a bool, or None.
#
# That was not an accident.

# ============================================================
# WHY IT WORKED
# ============================================================

# Consider:
#
#     self.os = source.os
#
# Two names now point at
# the same string.
#
# Question:
#
# Is that a bug?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# Strings are immutable.
#
# Nobody can change the
# string in place.
#
# Assigning a new OS:
#
#     copy.os = "Debian 12"
#
# rebinds the NAME.
#
# It does not modify the
# original string.
#
# So sharing is invisible.
#
# And harmless.

# ============================================================
# THE MOMENT THAT ENDS
# ============================================================

# Now a real requirement.
#
# Platform team asks:
#
# "Track which packages are
# installed on each VM."
#
# One new field.
#
#     installed_packages
#
# A list.
#
# Mutable.

# ============================================================
# THE AI CORNER
# ============================================================

# This is where most
# engineers reach for an
# AI assistant.
#
# Reasonably.
#
# It is a small mechanical
# change.
#
# The prompt used was:
#
#     "Add an installed_packages
#      list field to this
#      VMInstance class and
#      update __init__ and
#      clone() accordingly."
#
# Here is what came back.

# ============================================================
# THE GENERATED CODE
# ============================================================


class Prototype(ABC):

    @abstractmethod
    def clone(self):
        ...


class BuggyVMInstance(Prototype):

    def __init__(self, source=None):
        if source is None:
            self.os = None
            self.runtime = None
            self.hostname = None
            self.installed_packages = []
        else:
            self.os = source.os
            self.runtime = source.runtime
            self.hostname = source.hostname
            self.installed_packages = source.installed_packages

    def clone(self):
        return BuggyVMInstance(self)

    def __repr__(self):
        return (
            f"BuggyVMInstance("
            f"host={self.hostname}, "
            f"pkgs={self.installed_packages})"
        )


# ============================================================
# READ IT BEFORE JUDGING IT
# ============================================================

# The field was added.
#
# __init__ handles both
# branches.
#
# The blank branch creates
# an empty list.
#
# clone() is unchanged and
# still correct.
#
# Nothing is missing.
#
# Nothing is misspelled.
#
# The code runs.
#
# The shape is right.

# ============================================================
# THE LINE TO WATCH
# ============================================================

#     self.installed_packages = source.installed_packages
#
# Question:
#
# Does this line create a
# NEW list?
#
# Or does it point at the
# list that already exists?

# ============================================================
# PROVING IT
# ============================================================

original = BuggyVMInstance()

original.os = "Ubuntu 22.04"
original.hostname = "web-01"
original.installed_packages = ["nginx"]

duplicate = original.clone()

print("Same Object?")
print(original is duplicate)

print("\nSame List?")
print(original.installed_packages is duplicate.installed_packages)

# Observation:
#
# The objects differ.
#
# The lists do not.
#
# clone() produced a new
# VMInstance wrapping the
# SAME list.

# ============================================================
# THE ADDRESSES
# ============================================================

print("\nOriginal List Address")
print(id(original.installed_packages))

print("\nCopy List Address")
print(id(duplicate.installed_packages))

# Observation:
#
# Identical.
#
# One list.
#
# Two owners.

# ============================================================
# THE CONSEQUENCE
# ============================================================

duplicate.hostname = "web-02"
duplicate.installed_packages.append("redis")

print("\nAfter Modifying Only The Copy")

print("Copy")
print(duplicate)

print("Original")
print(original)

# Observation:
#
# We touched the copy.
#
# The original changed too.
#
# hostname stayed separate.
#
# packages did not.

# ============================================================
# WHY THE DIFFERENCE
# ============================================================

# Two operations.
#
# Two very different things.
#
#     duplicate.hostname = "web-02"
#
# Rebinding a name.
#
# Affects one object.
#
#     duplicate.installed_packages.append("redis")
#
# Mutating a shared object
# in place.
#
# Affects everyone pointing
# at it.
#
# The dot on the left of an
# assignment is safe.
#
# A method that changes the
# object is not.

# ============================================================
# THE SHARED BOX PICTURE
# ============================================================

# Same picture as the
# phone_numbers bug from
# the Builder class.
#
#   original ──┐
#              ├──► ["nginx", "redis"]
#   duplicate ─┘
#
# Two names.
#
# One box.
#
# One arrow each.
#
# Nothing was ever copied.
#
# Only the arrow was.

# ============================================================
# WHAT WAS PROMISED
# ============================================================

# The entire promise of
# clone() was independence.
#
# "Here is your own object.
# Do what you like to it."
#
# A shallow copy breaks
# that promise silently.
#
# Imagine ten "clean"
# servers launched from
# one template.
#
# Every one of them ends up
# with redis installed,
# because one clone
# appended to a list nobody
# realised was shared.

# ============================================================
# THE FIX
# ============================================================

# One line.
#
#     list(source.installed_packages)
#
# Builds a NEW list.
#
# Same contents.
#
# Different box.


class FixedVMInstance(Prototype):

    def __init__(self, source=None):
        if source is None:
            self.os = None
            self.runtime = None
            self.hostname = None
            self.installed_packages = []
        else:
            self.os = source.os
            self.runtime = source.runtime
            self.hostname = source.hostname
            self.installed_packages = list(source.installed_packages)

    def clone(self):
        return FixedVMInstance(self)

    def __repr__(self):
        return (
            f"FixedVMInstance("
            f"host={self.hostname}, "
            f"pkgs={self.installed_packages})"
        )


# ============================================================
# VERIFYING THE FIX
# ============================================================

fixed_original = FixedVMInstance()

fixed_original.os = "Ubuntu 22.04"
fixed_original.hostname = "web-01"
fixed_original.installed_packages = ["nginx"]

fixed_copy = fixed_original.clone()

print("\nSame List Now?")
print(fixed_original.installed_packages is fixed_copy.installed_packages)

fixed_copy.installed_packages.append("redis")

print("\nAfter Modifying Only The Copy")

print("Copy")
print(fixed_copy)

print("Original")
print(fixed_original)

# Observation:
#
# The original is untouched.
#
# Contents were copied.
#
# Not the reference to the
# container holding them.

# ============================================================
# THE HABIT
# ============================================================

# For every field in any
# clone() method, ask:
#
# "Is this mutable?"
#
# If no: assignment is fine.
#
# If yes: did I copy the
# CONTENTS, or just the
# arrow?

# ============================================================
# WHERE THE FIX STOPS WORKING
# ============================================================

# Now a harder case.
#
# Firewall rules.
#
# A list of dictionaries.
#
# Mutable objects INSIDE
# a mutable container.


class NestedVMInstance(Prototype):

    def __init__(self, source=None):
        if source is None:
            self.hostname = None
            self.firewall_rules = []
        else:
            self.hostname = source.hostname
            self.firewall_rules = list(source.firewall_rules)

    def clone(self):
        return NestedVMInstance(self)

    def __repr__(self):
        return (
            f"NestedVMInstance("
            f"host={self.hostname}, "
            f"rules={self.firewall_rules})"
        )


nested_original = NestedVMInstance()

nested_original.hostname = "web-01"
nested_original.firewall_rules = [
    {"port": 22, "allow": "admin-subnet"},
    {"port": 443, "allow": "public"}
]

nested_copy = nested_original.clone()

print("\nOuter Lists Same?")
print(nested_original.firewall_rules is nested_copy.firewall_rules)

print("\nInner Dicts Same?")
print(nested_original.firewall_rules[0] is nested_copy.firewall_rules[0])

# Observation:
#
# The outer list was copied.
#
# The dictionaries inside
# it were not.
#
# list() copies one level.
#
# Exactly one.

# ============================================================
# THE LEAK
# ============================================================

nested_copy.firewall_rules[0]["allow"] = "0.0.0.0/0"

print("\nCopy Rules")
print(nested_copy.firewall_rules[0])

print("\nOriginal Rules")
print(nested_original.firewall_rules[0])

# Observation:
#
# The template's SSH rule
# is now open to the entire
# internet.
#
# Nobody edited the template.
#
# Nobody edited the registry.
#
# One clone changed one
# dictionary.

# ============================================================
# IMPORTANT
# ============================================================

# The one-line fix was not
# wrong.
#
# It was incomplete.
#
# "Copy the contents" has
# a depth.
#
# list() goes one level.
#
# The bug goes as deep as
# the data does.

# ============================================================
# THE copy MODULE
# ============================================================

# Python ships the answer.
#
#     copy.copy()
#
# Shallow. One level.
#
#     copy.deepcopy()
#
# Recursive. All levels.

shallow_rules = copy.copy(nested_original.firewall_rules)
deep_rules = copy.deepcopy(nested_original.firewall_rules)

print("\nShallow Inner Same?")
print(shallow_rules[0] is nested_original.firewall_rules[0])

print("\nDeep Inner Same?")
print(deep_rules[0] is nested_original.firewall_rules[0])

# Observation:
#
# copy.copy behaves exactly
# like list().
#
# copy.deepcopy rebuilt
# every level.

# ============================================================
# DEEPCOPY ON THE OBJECT
# ============================================================


class DeepVMInstance(Prototype):

    def __init__(self, source=None):
        if source is None:
            self.hostname = None
            self.firewall_rules = []
        else:
            self.hostname = source.hostname
            self.firewall_rules = copy.deepcopy(source.firewall_rules)

    def clone(self):
        return DeepVMInstance(self)

    def __repr__(self):
        return (
            f"DeepVMInstance("
            f"host={self.hostname}, "
            f"rules={self.firewall_rules})"
        )


deep_original = DeepVMInstance()

deep_original.hostname = "web-01"
deep_original.firewall_rules = [
    {"port": 22, "allow": "admin-subnet"}
]

deep_copy = deep_original.clone()

deep_copy.firewall_rules[0]["allow"] = "0.0.0.0/0"

print("\nDeep Copy Rules")
print(deep_copy.firewall_rules[0])

print("\nDeep Original Rules")
print(deep_original.firewall_rules[0])

# Observation:
#
# The template survived.
#
# At every level.

# ============================================================
# THE OBVIOUS QUESTION
# ============================================================

# If deepcopy solves this
# completely, why write
# clone() by hand at all?
#
#     def clone(self):
#         return copy.deepcopy(self)
#
# One line.
#
# Every field.
#
# Every depth.
#
# Every subclass, correctly
# typed.
#
# Why not always?

# ============================================================
# WHEN DEEPCOPY IS WRONG
# ============================================================

# Because sometimes sharing
# is the POINT.
#
# Consider a VM template
# holding a database
# connection pool.
#
# Or a logger.
#
# Or a metrics client.
#
# These are expensive.
#
# They are meant to be
# shared.
#
# Duplicating them is not
# safety.
#
# It is a resource leak.


class ConnectionPool:

    def __init__(self, size):
        self.size = size
        self.pool_id = "pool-9931"

    def __repr__(self):
        return f"ConnectionPool(id={self.pool_id})"


class ServiceVM(Prototype):

    def __init__(self, source=None):
        if source is None:
            self.hostname = None
            self.installed_packages = []
            self.db_pool = None
        else:
            self.hostname = source.hostname

            # Duplicated on purpose.
            self.installed_packages = list(source.installed_packages)

            # Shared on purpose.
            self.db_pool = source.db_pool

    def clone(self):
        return ServiceVM(self)


service_template = ServiceVM()

service_template.hostname = "orders-01"
service_template.installed_packages = ["nginx"]
service_template.db_pool = ConnectionPool(size=20)

service_copy = service_template.clone()

print("\nPackages Same?")
print(service_template.installed_packages is service_copy.installed_packages)

print("\nPool Same?")
print(service_template.db_pool is service_copy.db_pool)

# ============================================================
# COMPARE WITH DEEPCOPY
# ============================================================

blind_copy = copy.deepcopy(service_template)

print("\nDeepcopy Pool Same?")
print(service_template.db_pool is blind_copy.db_pool)

# Observation:
#
# deepcopy duplicated the
# connection pool.
#
# Two pools now exist where
# the design intended one.
#
# Clone a hundred VMs and
# the database sees a
# hundred pools.

# ============================================================
# THE REAL RULE
# ============================================================

# deepcopy is not "the safe
# option".
#
# It is "the maximum option".
#
# A hand-written clone()
# lets you state, field by
# field, what is duplicated
# and what is shared.
#
# Use deepcopy when a plain,
# total copy is genuinely
# what you want.
#
# Write clone() when the
# answer differs per field.

# ============================================================
# BACK TO THE AI CORNER
# ============================================================

# Look at what the assistant
# actually got right.
#
# The field.
#
# The constructor branches.
#
# The clone method.
#
# The naming.
#
# The SHAPE was correct.
#
# What it missed was the
# one property nobody
# stated out loud:
#
# independence.

# ============================================================
# WHY IT MISSED IT
# ============================================================

# The prompt said:
#
#     "update __init__ and
#      clone() accordingly"
#
# Accordingly to WHAT?
#
# The prompt described the
# EDIT.
#
# It never described the
# GUARANTEE.
#
# A shallow assignment
# satisfies the edit
# perfectly.

# ============================================================
# A BETTER PROMPT
# ============================================================

# Name the property, not
# the edit.
#
#     "Add an installed_packages
#      list field. Update clone()
#      so the copy has its own
#      independent list —
#      mutating the copy's list
#      must NOT affect the
#      original's list."
#
# The second prompt is
# testable.
#
# The first one was not.

# ============================================================
# THE TRANSFERABLE LESSON
# ============================================================

# AI is reliably good at
# the shape of a pattern.
#
# It is not reliably good
# at the invariant the
# pattern exists to protect.
#
# Same lesson as Builder's
# AI Corner.
#
# New pattern.
#
# Identical failure.
#
# Review generated code for
# the PROMISE, not the
# structure.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception 1:
#
# "A new object means a
# new copy."
#
# The wrapper is new.
#
# Its contents may not be.

# Misconception 2:
#
# "list() makes it safe."
#
# One level deep.
#
# Nested dicts stay shared.

# Misconception 3:
#
# "deepcopy is always
# safest."
#
# It duplicates things that
# were meant to be shared.

# Misconception 4:
#
# "The code ran, so the
# copy worked."
#
# Every bug in this file
# ran without error.

# ============================================================
# QUIZ
# ============================================================

# self.tags = source.tags
# where tags is a list.
# What does clone() produce?
#
# A) A new object with a
#    new list
# B) A new object sharing
#    the original's list
# C) A TypeError
# D) The same object
#
# Answer:
#
# B) New object.
#    Shared list.

# ============================================================
# QUIZ 2
# ============================================================

# firewall_rules is a list
# of dicts, copied with
# list(). A clone edits
# rules[0]["port"]. What
# happens to the original?
#
# A) Unaffected
# B) Its rules[0] changes too
# C) TypeError
# D) The list length changes
#
# Answer:
#
# B) The inner dict is
#    shared.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why does copying a string
# field by assignment cause
# no bug, while copying a
# list field the same way
# does?
#
# Strings are immutable, so
# sharing cannot be observed.
#
# Lists can be mutated in
# place, so sharing becomes
# visible to every holder.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# When is copy.deepcopy the
# wrong choice for clone()?
#
# When some fields are meant
# to be shared, such as
# connection pools, loggers,
# or caches.
#
# deepcopy duplicates them
# and multiplies expensive
# resources.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Testing a clone by reading
# it.
#
# Reading proves the values
# arrived.
#
# Only MUTATING the copy and
# re-reading the original
# proves independence.

# ============================================================
# BEST PRACTICE
# ============================================================

# Write the independence
# test first.
#
#     copy = original.clone()
#     copy.some_list.append("x")
#     assert "x" not in original.some_list
#
# Three lines.
#
# They would have caught
# every bug in this file.

# ============================================================
# BOARD SUMMARY
# ============================================================

# self.pkgs = source.pkgs
#     shallow, same list
#
# self.pkgs = list(source.pkgs)
#     one level deep
#
# copy.deepcopy(source.pkgs)
#     all levels deep
#
# Immutable fields:
#     assignment is fine
#
# Mutable fields:
#     copy the contents
#
# Shared-by-design fields:
#     assignment on purpose,
#     with a comment saying so

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Independence held for three
# files only because every
# field was immutable.
#
# Assignment copies the
# arrow, never the box.
#
# list() and copy.copy()
# copy exactly one level.
#
# copy.deepcopy() copies all
# levels, including things
# meant to be shared.
#
# Hand-written clone() exists
# to decide per field.
#
# Generated code gets the
# shape right and the
# invariant wrong; state the
# guarantee in the prompt.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# The pattern is complete.
#
# Prototype.
#
# Registry.
#
# Correct copying at depth.
#
# What remains is judgement.
#
# Where does this belong in
# real systems, and where
# is it needless overhead?
#
# Next:
#
# 05_prototype_in_production.py
