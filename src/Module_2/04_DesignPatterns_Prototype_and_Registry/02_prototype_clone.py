"""
============================================================
LLD-6 : DESIGN PATTERNS - PROTOTYPE & REGISTRY
FILE : 02_prototype_clone.py
============================================================

Topics Covered
--------------
1.  Recap: Why The Object Must Copy Itself
2.  Forcing A Method To Exist
3.  The Prototype Abstract Base Class
4.  Abstract Enforcement In Action
5.  Return Type Hints In A Dynamic Language
6.  Python Allows Only One __init__
7.  The Optional Source Parameter
8.  Implementing VMInstance
9.  Implementing clone()
10. Verifying Independence
11. Subclasses: GpuVMInstance
12. The Critical Rule Of Prototype
13. Watching A Subclass Fail Silently
14. An Advanced Alternative: type(self)
15. Interview Questions
16. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# RECAP
# ============================================================

# In the previous file we
# copied an object by hand.
#
# It worked.
#
# And it broke three things:
#
# Coupling.
#
# Encapsulation.
#
# Open/Closed.
#
# We ended with one answer:
#
# The object itself must
# know how to copy itself.
#
# Now we build that.

# ============================================================
# THE FIRST DESIGN DECISION
# ============================================================

# If every copyable class
# copies itself, the client
# needs a promise.
#
# A guaranteed method.
#
# With a fixed name.
#
# On every copyable type.
#
# Question:
#
# What forces a class to
# provide a specific method?

# ============================================================
# THE ANSWER
# ============================================================

# An abstract base class.
#
# With an abstract method.
#
# ABC.
#
# abstractmethod.


class Prototype(ABC):

    @abstractmethod
    def clone(self):
        ...


# Observation:
#
# The body is literally
# three dots.
#
# There is nothing to
# implement here.
#
# The base class is not
# providing behaviour.
#
# It is providing an
# obligation.

# ============================================================
# ABSTRACT ENFORCEMENT IN ACTION
# ============================================================

# Does Python actually
# enforce this?
#
# Let us try to break it.


class IncompleteVM(Prototype):
    """
    Inherits the obligation.
    Never fulfils it.
    """

    def __init__(self):
        self.os = None


print("Abstract Enforcement")

try:
    broken = IncompleteVM()
    print(broken)
except TypeError as error:
    print(error)

# Observation:
#
# TypeError.
#
# At INSTANTIATION time.
#
# Not at call time.
#
# The object is never
# allowed to exist.
#
# This is the same shape
# of protection we saw
# with __eq__ and __hash__.
#
# Python refuses to create
# something it knows is
# incomplete.

# ============================================================
# IMPORTANT DISCUSSION
# ============================================================

# Notice WHEN the error
# arrives.
#
# Early.
#
# Loud.
#
# At the exact place the
# mistake was made.
#
# Remember this.
#
# Later in this file we
# will meet a mistake that
# does the opposite.


# ============================================================
# THE SECOND DESIGN DECISION
# ============================================================

# Now the constructor.
#
# We need two behaviours:
#
# Create a blank object.
#
# Create an object copied
# from an existing one.
#
# In some languages that is
# two constructors.
#
# Recall from the Builder
# class:
#
# Can Python do that?

# ============================================================
# SMALL EXPERIMENT
# ============================================================


class TwoConstructors:

    def __init__(self):
        self.mode = "blank"

    def __init__(self, source):
        self.mode = "copied"


print("\nTwo __init__ Methods")

try:
    obj = TwoConstructors()
    print(obj.mode)
except TypeError as error:
    print(error)

# Observation:
#
# The blank call fails.
#
# The first __init__ is gone.
#
# Not merged.
#
# Not overloaded.
#
# Simply replaced.
#
# A class body is executed
# top to bottom, and the
# second assignment to the
# name __init__ wins.

# ============================================================
# THE PYTHONIC SOLUTION
# ============================================================

# One __init__.
#
# One optional parameter.
#
# Defaulting to None.
#
#     def __init__(self, source=None):
#
# If source is None:
# start blank.
#
# Otherwise:
# copy from source.

# ============================================================
# IMPLEMENTING VMInstance
# ============================================================


class VMInstance(Prototype):

    def __init__(self, source=None):
        if source is None:
            self.os = None
            self.runtime = None
            self.monitoring_agent = None
            self.security_patches = None
            self.hostname = None
            self.ip_address = None
        else:
            self.os = source.os
            self.runtime = source.runtime
            self.monitoring_agent = source.monitoring_agent
            self.security_patches = source.security_patches
            self.hostname = source.hostname
            self.ip_address = source.ip_address

    def clone(self):
        return VMInstance(self)

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"os={self.os}, "
            f"runtime={self.runtime}, "
            f"host={self.hostname}, "
            f"ip={self.ip_address})"
        )


# ============================================================
# THE KEY OBSERVATION
# ============================================================

# Look at the else branch.
#
# It reads source.os,
# source.runtime, and the
# rest.
#
# Identical lines to the
# manual copying we rejected
# in the previous file.
#
# Same lines.
#
# Different location.
#
# That location is the
# entire pattern.

# ============================================================
# WHY LOCATION CHANGES
# EVERYTHING
# ============================================================

# Inside the class:
#
# Full legitimate access
# to every field, including
# private ones.
#
# One place to update when
# a field is added.
#
# The class owns its own
# shape.
#
# Outside the class:
#
# Guessing.
#
# Duplication.
#
# Silent staleness.

# ============================================================
# USING IT
# ============================================================

golden_image = VMInstance()

golden_image.os = "Ubuntu 22.04"
golden_image.runtime = "Python 3.11"
golden_image.monitoring_agent = True
golden_image.security_patches = True

print("\nGolden Image")
print(golden_image)

server = golden_image.clone()

server.hostname = "web-01"
server.ip_address = "10.0.0.14"

print("\nCloned Server")
print(server)

# Observation:
#
# Two lines of client code.
#
# One clone call.
#
# One field set.
#
# The client never named
# os or runtime.

# ============================================================
# VERIFYING INDEPENDENCE
# ============================================================

# A copy must be a separate
# object.
#
# Not another name for the
# same object.

print("\nIdentity Check")
print(golden_image is server)

print("\nDistinct Addresses")
print(id(golden_image) != id(server))

print("\nTemplate Hostname")
print(golden_image.hostname)

# Observation:
#
# The template is untouched.
#
# Setting hostname on the
# clone did nothing to the
# original.
#
# For these simple fields,
# independence holds.
#
# Remember that phrase.
#
# For THESE fields.

# ============================================================
# A DELIBERATE GAP
# ============================================================

# Every field here is a
# string, a bool, or None.
#
# Immutable, or replaced
# whole.
#
# We have not yet added a
# list.
#
# Or a dict.
#
# Or another object.
#
# When we do, this exact
# clone() will develop a
# very quiet bug.
#

# ============================================================
# SUBCLASSES
# ============================================================

# Machine learning teams
# need GPU machines.
#
# One extra field.
#
# gpu_type.
#
# Question:
#
# What must its clone()
# do that the parent's
# cannot?


class GpuVMInstance(VMInstance):

    def __init__(self, source=None):
        super().__init__(source)

        if source is None:
            self.gpu_type = None
        else:
            self.gpu_type = source.gpu_type

    def clone(self):
        return GpuVMInstance(self)

    def __repr__(self):
        return (
            f"GpuVMInstance("
            f"os={self.os}, "
            f"gpu={self.gpu_type}, "
            f"host={self.hostname})"
        )


# Observation:
#
# Two responsibilities,
# split cleanly.
#
# super().__init__(source)
# handles every parent field.
#
# The subclass handles only
# what it added.
#
# No field is named twice.

# ============================================================
# USING THE SUBCLASS
# ============================================================

gpu_image = GpuVMInstance()

gpu_image.os = "Ubuntu 22.04"
gpu_image.runtime = "Python 3.11"
gpu_image.gpu_type = "NVIDIA A100"

trainer = gpu_image.clone()

trainer.hostname = "train-01"

print("\nGPU Clone")
print(trainer)

print("\nClone Type")
print(type(trainer).__name__)

print("\nGPU Preserved")
print(trainer.gpu_type)

# ============================================================
# THE CRITICAL RULE
# ============================================================

# Core Rule:
#
# EVERY subclass MUST
# override clone().
#
# Not "should".
#
# Not "usually".
#
# Must.
#
# Now we find out why.

# ============================================================
# WATCHING IT FAIL
# ============================================================

# Below is a subclass that
# does everything right,
# except one thing.
#
# Its __init__ is correct.
#
# It copies gpu_type.
#
# It simply forgets to
# override clone().


class ForgetfulGpuVM(VMInstance):

    def __init__(self, source=None):
        super().__init__(source)

        if source is None:
            self.gpu_type = None
        else:
            self.gpu_type = source.gpu_type

    # clone() is NOT overridden.
    # It is inherited from VMInstance.


forgetful_image = ForgetfulGpuVM()

forgetful_image.os = "Ubuntu 22.04"
forgetful_image.gpu_type = "NVIDIA A100"

print("\nSource Type")
print(type(forgetful_image).__name__)

print("\nSource GPU")
print(forgetful_image.gpu_type)

bad_copy = forgetful_image.clone()

print("\nCopy Type")
print(type(bad_copy).__name__)

# Observation:
#
# A GPU machine went in.
#
# A plain machine came out.
#
# Because the inherited
# clone() body says:
#
#     return VMInstance(self)
#
# It hardcodes the parent
# class name.
#
# It has no idea a subclass
# ever existed.

# ============================================================
# WHERE THE ERROR SURFACES
# ============================================================

print("\nReading gpu_type On Copy")

try:
    print(bad_copy.gpu_type)
except AttributeError as error:
    print(error)

# Observation:
#
# AttributeError.
#
# But notice WHERE.
#
# Not at the clone call.
#
# Not at class definition.
#
# Here.
#
# Wherever someone finally
# reads the field.
#
# Possibly a different file.
#
# Possibly a different team.
#
# Possibly production.

# ============================================================
# COMPARE THE TWO FAILURES
# ============================================================

# Earlier in this file:
#
# IncompleteVM failed at
# instantiation.
#
# Immediately.
#
# Precisely.
#
# ForgetfulGpuVM failed
# far away from the mistake.
#
# The abstract method
# protected us.
#
# Nothing protects us from
# a forgotten override.
#
# Python cannot know that
# clone() was supposed to
# be rewritten.

# ============================================================
# THE PRODUCTION VERSION
# ============================================================

# Now imagine this at scale.
#
# Ten GPU servers requested.
#
# Ten launched.
#
# Every one of them a plain
# machine.
#
# No error anywhere.
#
# The bug is noticed when
# training jobs start
# failing for "no reason".
#
# Hours later.
#
# By a different team.

# ============================================================
# BOARD NOTE
# ============================================================

# Critical rule of Prototype:
#
# EVERY subclass MUST
# override clone().
#
# A forgotten override runs
# the PARENT's clone logic,
# dropping every field the
# child added.
#
# No error.
#
# No crash.
#
# Just silently wrong data.

# ============================================================
# AN ADVANCED ALTERNATIVE
# ============================================================

# A reasonable question:
#
# Why hardcode the class
# name at all?
#
# Python knows the real
# type at runtime.
#
#     type(self)
#
# So why not write clone()
# once, generically?


class SmartPrototype(ABC):

    def clone(self):
        return type(self)(self)


class SmartVM(SmartPrototype):

    def __init__(self, source=None):
        if source is None:
            self.os = None
            self.hostname = None
        else:
            self.os = source.os
            self.hostname = source.hostname

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"os={self.os}, "
            f"host={self.hostname})"
        )


class SmartGpuVM(SmartVM):

    def __init__(self, source=None):
        super().__init__(source)

        if source is None:
            self.gpu_type = None
        else:
            self.gpu_type = source.gpu_type

    def __repr__(self):
        return (
            f"SmartGpuVM("
            f"os={self.os}, "
            f"gpu={self.gpu_type})"
        )


smart_image = SmartGpuVM()

smart_image.os = "Ubuntu 22.04"
smart_image.gpu_type = "NVIDIA A100"

smart_copy = smart_image.clone()

print("\nSmart Clone Type")
print(type(smart_copy).__name__)

print("\nSmart Clone GPU")
print(smart_copy.gpu_type)

# Observation:
#
# The subclass never wrote
# clone().
#
# And it still worked.

# ============================================================
# IMPORTANT DISCUSSION
# ============================================================

# So did we just delete
# the rule?
#
# No.
#
# We MOVED it.
#
# type(self)(self) is only
# correct if every subclass
# __init__ accepts a source
# and copies its own fields.
#
# The obligation did not
# disappear.
#
# It relocated from clone()
# to __init__.
#
# Forget it there, and the
# field vanishes exactly
# the same way.

# ============================================================
# WHICH ONE TO TEACH
# ============================================================

# We write clone() explicitly
# in this course.
#
# Two reasons.
#
# One: it makes the
# obligation visible in
# every subclass, where a
# reviewer can see it.
#
# Two: it is the form you
# will meet in Java, C#,
# and in most design pattern
# literature.
#
# In real Python code,
# type(self)(self) is a
# perfectly good choice,
# provided the team knows
# where the rule now lives.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception 1:
#
# "The ABC guarantees my
# subclasses clone correctly."
#
# It guarantees the method
# EXISTS.
#
# Not that it is right.
#
# ForgetfulGpuVM inherited
# a working clone().
#
# Python was satisfied.

# Misconception 2:
#
# "super().__init__(source)
# copies everything, so the
# subclass is done."
#
# It copies everything the
# PARENT knows about.
#
# The parent has never
# heard of gpu_type.

# Misconception 3:
#
# "clone() returns a new
# object, so it is fully
# independent."
#
# True today.
#
# Only because every field
# is immutable.
#
# File 04 removes that
# comfort.

# ============================================================
# QUIZ
# ============================================================

# GpuVMInstance inherits from
# VMInstance but forgets to
# override clone(). What
# happens on .clone()?
#
# A) Python raises an error
#    immediately
# B) VMInstance's clone()
#    runs, silently dropping
#    gpu_type
# C) The program crashes
#    at runtime
# D) It works correctly
#
# Answer:
#
# B) Silently dropping
#    gpu_type.

# ============================================================
# QUIZ 2
# ============================================================

# When does Python raise an
# error for a subclass that
# never implements an
# abstractmethod?
#
# A) At class definition
# B) At instantiation
# C) At the first method call
# D) Never
#
# Answer:
#
# B) At instantiation.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why can Python not have
# two constructors, and what
# is used instead?
#
# A class body is executed
# sequentially, so a second
# __init__ replaces the
# first.
#
# One __init__ with an
# optional parameter is
# used instead.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# An abstract clone() method
# forces every subclass to
# have the method. Why is
# that still not enough?
#
# Because a subclass can
# inherit the parent's
# implementation and satisfy
# the abstract requirement
# while returning the wrong
# type.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Writing __init__ correctly
# in a subclass and assuming
# clone() follows.
#
# They are two separate
# obligations.
#
# ForgetfulGpuVM got the
# first one right and still
# produced wrong objects.

# ============================================================
# BEST PRACTICE
# ============================================================

# In code review, whenever
# a subclass appears, ask
# one question:
#
# "Does this subclass add
# a field, and if so, did
# clone() change too?"
#
# Adding a field and
# updating clone() should
# be one commit, never two.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Prototype in code:
#
# 1. Prototype(ABC) with
#    abstract clone()
#
# 2. One __init__ with
#    source=None
#
# 3. clone() returns
#    ClassName(self)
#
# 4. Subclass calls
#    super().__init__(source)
#    then copies its own
#    fields
#
# 5. Subclass MUST override
#    clone()
#
# The abstract method is
# checked by Python.
#
# The override rule is
# checked by you.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# The copying lines did not
# change from file 01.
#
# Their location did, and
# that is the whole pattern.
#
# ABC guarantees a method
# exists, not that it is
# correct.
#
# Python allows exactly one
# __init__ per class.
#
# An optional source
# parameter serves both
# blank and copy creation.
#
# A forgotten clone()
# override fails silently,
# far from the mistake.
#
# type(self)(self) removes
# the override rule from
# clone() and moves it
# into __init__.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Objects can now copy
# themselves.
#
# But notice something in
# this file.
#
# golden_image was created
# by hand, in this script,
# as a local variable.
#
# In a real system, other
# modules need that template.
#
# By name.
#
# Without importing this
# file.
#
# That is a second, separate
# problem.
#
# Next:
#
# 03_registry_pattern.py
