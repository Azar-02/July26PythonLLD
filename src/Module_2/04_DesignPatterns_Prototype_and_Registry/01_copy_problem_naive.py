"""
============================================================
LLD-6 : DESIGN PATTERNS - PROTOTYPE & REGISTRY
FILE : 01_copy_problem_naive.py
============================================================

Topics Covered
--------------
1.  Recap: What Builder Solved
2.  A Fully Configured Object
3.  Manual Field By Field Copying
4.  Problem 1: Tight Coupling
5.  What Happens When A Field Is Added
6.  Problem 2: Encapsulation Violation
7.  Name Mangling In Python
8.  Problem 3: isinstance() Chains
9.  The Open/Closed Principle Again
10. Where The Responsibility Belongs
11. The Cloud VM Image Intuition
12. Fixed Fields vs Varying Fields
13. Build From Scratch vs Clone
14. Naming The Pattern
15. Interview Questions
16. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# Last file we studied Builder.
#
# Builder answered:
#
#     "How do I safely construct
#      ONE complicated object,
#      gradually, with validation?"
#
# Today the problem flips.
#
# Suppose the object already
# exists.
#
# Fully configured.
#
# Already validated.
#
# You need a second one,
# almost identical.
#
# Only two fields differ.
#
# Question:
#
# Do you build it again
# from scratch?

# ============================================================
# THE RUNNING EXAMPLE
# ============================================================

# We will model a cloud
# virtual machine.
#
# Fields:
#
#     os
#     runtime
#     monitoring_agent
#     security_patches
#     hostname
#     ip_address
#
# The first four are decided
# by the platform team.
#
# The last two are assigned
# when the machine boots.


class VMInstance:

    def __init__(self):
        self.os = None
        self.runtime = None
        self.monitoring_agent = None
        self.security_patches = None
        self.hostname = None
        self.ip_address = None

    def __repr__(self):
        return (
            f"VMInstance("
            f"os={self.os}, "
            f"runtime={self.runtime}, "
            f"agent={self.monitoring_agent}, "
            f"patches={self.security_patches}, "
            f"host={self.hostname}, "
            f"ip={self.ip_address})"
        )


# ============================================================
# THE ORIGINAL OBJECT
# ============================================================

original = VMInstance()

original.os = "Ubuntu 22.04"
original.runtime = "Python 3.11"
original.monitoring_agent = True
original.security_patches = True
original.hostname = "web-01"
original.ip_address = "10.0.0.14"

print("Original VM")
print(original)

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# We need a SECOND machine.
#
# Same OS.
#
# Same runtime.
#
# Same monitoring.
#
# Same patches.
#
# Different hostname.
#
# Different IP.
#
# Using only what we know
# so far, how would we
# create it?

# ============================================================
# ATTEMPT 1 : MANUAL FIELD BY FIELD COPY
# ============================================================

copy = VMInstance()

copy.os = original.os
copy.runtime = original.runtime
copy.monitoring_agent = original.monitoring_agent
copy.security_patches = original.security_patches

copy.hostname = "web-02"
copy.ip_address = "10.0.0.15"

print("\nManual Copy")
print(copy)

# Observation:
#
# It works.
#
# The output is correct.
#
# This is exactly why the
# problem is dangerous.
#
# Correct output hides
# structural damage.

# ============================================================
# FIRST QUESTION
# ============================================================

# As the person writing
# the copying code:
#
# What did you have to KNOW
# about VMInstance?
#
# Answer:
#
# Every single field name.
#
# Including fields you never
# actually cared about.

# ============================================================
# PROBLEM 1 : TIGHT COUPLING
# ============================================================

# The copying code lives
# OUTSIDE the class.
#
# But it depends on the
# INSIDE of the class.
#
# That dependency is invisible.
#
# No import breaks.
#
# No signature changes.
#
# Nothing warns you.

# ============================================================
# SMALL EXPERIMENT
# ============================================================

# Let the platform team add
# ONE new field.
#
# region.
#
# A perfectly reasonable
# business request.


class VMInstanceV2:

    def __init__(self):
        self.os = None
        self.runtime = None
        self.monitoring_agent = None
        self.security_patches = None
        self.hostname = None
        self.ip_address = None
        self.region = None

    def __repr__(self):
        return (
            f"VMInstanceV2("
            f"os={self.os}, "
            f"region={self.region}, "
            f"host={self.hostname})"
        )


def copy_backend_vm(source):
    """
    Written BEFORE region existed.
    Nobody remembered to update it.
    """
    result = VMInstanceV2()

    result.os = source.os
    result.runtime = source.runtime
    result.monitoring_agent = source.monitoring_agent
    result.security_patches = source.security_patches
    result.hostname = source.hostname
    result.ip_address = source.ip_address

    return result


production_vm = VMInstanceV2()

production_vm.os = "Ubuntu 22.04"
production_vm.runtime = "Python 3.11"
production_vm.monitoring_agent = True
production_vm.security_patches = True
production_vm.hostname = "web-01"
production_vm.ip_address = "10.0.0.14"
production_vm.region = "ap-south-1"

stale_copy = copy_backend_vm(production_vm)

print("\nSource region")
print(production_vm.region)

print("\nCopy region")
print(stale_copy.region)

# Observation:
#
# The copy lost its region.
#
# No error.
#
# No warning.
#
# No crash.
#
# A machine silently
# deployed to nowhere.

# ============================================================
# IMPORTANT
# ============================================================

# The class changed.
#
# The copying code did not.
#
# And Python had no way
# to connect the two.
#
# Now multiply this.
#
# Ten copy sites across
# the codebase.
#
# All of them stale.

# ============================================================
# BOARD NOTE
# ============================================================

# Problem 1: Tight coupling
#
# The client must know every
# field of VMInstance just
# to copy it.
#
# If the fields change,
# every manual copy site
# breaks silently.

# ============================================================
# PROBLEM 2 : ENCAPSULATION
# ============================================================

# Now a harder question.
#
# What if some fields are
# deliberately internal?
#
# Not part of the public
# surface of the class.


class SecureVM:

    def __init__(self):
        self.os = None
        self.hostname = None
        self.__security_key = "AKIA-SECRET-9931"

    def rotate_key(self, new_key):
        self.__security_key = new_key

    def key_fingerprint(self):
        return self.__security_key[:4] + "****"

    def __repr__(self):
        return (
            f"SecureVM("
            f"os={self.os}, "
            f"host={self.hostname}, "
            f"key={self.key_fingerprint()})"
        )


secure_original = SecureVM()

secure_original.os = "Ubuntu 22.04"
secure_original.hostname = "vault-01"

print("\nSecure VM")
print(secure_original)

# ============================================================
# TRYING TO COPY THE PRIVATE FIELD
# ============================================================

print("\nDirect Access Attempt")

try:
    print(secure_original.__security_key)
except AttributeError as error:
    print(error)

# Observation:
#
# The class deliberately
# does not expose it.
#
# There is no setter.
#
# There is no getter.
#
# Only a fingerprint.

# ============================================================
# NAME MANGLING
# ============================================================

# Python does not have
# true private fields.
#
# A name like:
#
#     __security_key
#
# is renamed internally to:
#
#     _SecureVM__security_key
#
# This is called
# name mangling.
#
# It is a social signal.
#
# Not a lock.

print("\nMangled Access")
print(secure_original._SecureVM__security_key)

# Observation:
#
# We CAN reach it.
#
# The question is whether
# we SHOULD.

# ============================================================
# THE REAL POINT
# ============================================================

# External copying code
# reaching into a mangled
# name is not a clever trick.
#
# It is a design smell.
#
# The class said:
#
# "This is mine."
#
# The copying code replied:
#
# "Not anymore."
#
# Where Python ALLOWS it,
# the responsibility is
# still in the wrong place.

# ============================================================
# BOARD NOTE
# ============================================================

# Problem 2: Encapsulation
# gets violated
#
# Manual field-by-field
# copying reaches into
# details the class wanted
# to keep internal.

# ============================================================
# PROBLEM 3 : SUBCLASSES
# ============================================================

# Reality arrives
#
# Machine learning teams
# need GPU machines.
#
# One extra field.
#
# gpu_type.


class GpuVMInstance(VMInstanceV2):

    def __init__(self):
        super().__init__()
        self.gpu_type = None

    def __repr__(self):
        return (
            f"GpuVMInstance("
            f"os={self.os}, "
            f"gpu={self.gpu_type}, "
            f"host={self.hostname})"
        )


# ============================================================
# THE COPY FUNCTION MUST NOW BRANCH
# ============================================================


def copy_any_vm_wrong(source):
    """
    Branch order matters.
    This version gets it wrong.
    """
    if isinstance(source, VMInstanceV2):
        result = VMInstanceV2()
    elif isinstance(source, GpuVMInstance):
        result = GpuVMInstance()
    else:
        raise TypeError("Unknown VM type")

    result.os = source.os
    result.hostname = source.hostname

    return result


gpu_vm = GpuVMInstance()

gpu_vm.os = "Ubuntu 22.04"
gpu_vm.hostname = "train-01"
gpu_vm.gpu_type = "NVIDIA A100"

print("\nSource Type")
print(type(gpu_vm).__name__)

wrong_copy = copy_any_vm_wrong(gpu_vm)

print("\nCopy Type")
print(type(wrong_copy).__name__)

# Observation:
#
# A GPU machine went in.
#
# A plain machine came out.
#
# Because a subclass IS
# an instance of its parent.
#
# The first branch matched.
#
# The GPU branch was
# unreachable.

# ============================================================
# THE FIX IS FRAGILE
# ============================================================


def copy_any_vm_ordered(source):
    """
    Most specific type first.
    Correct today.
    Fragile forever.
    """
    if isinstance(source, GpuVMInstance):
        result = GpuVMInstance()
        result.gpu_type = source.gpu_type
    elif isinstance(source, VMInstanceV2):
        result = VMInstanceV2()
    else:
        raise TypeError("Unknown VM type")

    result.os = source.os
    result.hostname = source.hostname

    return result


ordered_copy = copy_any_vm_ordered(gpu_vm)

print("\nOrdered Copy Type")
print(type(ordered_copy).__name__)

print("\nOrdered Copy GPU")
print(ordered_copy.gpu_type)

# Observation:
#
# It works.
#
# But correctness now depends
# on the ORDER of branches.
#
# That is not a design.
#
# That is a landmine.

# ============================================================
# THE OPEN / CLOSED PRINCIPLE
# ============================================================

# Recall the principle:
#
# Software should be
# OPEN for extension.
#
# CLOSED for modification.
#
# Now count.
#
# Every new VM type means
# one more elif.
#
# Inside code that was
# already working.
#
# Already tested.
#
# Already in production.

# ============================================================
# BOARD NOTE
# ============================================================

# Problem 3: isinstance()
# chains break OCP
#
# Every new subtype forces
# an edit to code that
# already worked.

# ============================================================
# STEPPING BACK
# ============================================================

# Three problems.
#
# One root cause.
#
# The copying logic lives
# OUTSIDE the object.
#
# So ask:
#
# Who actually knows all
# the fields of VMInstance?
#
# Who has legitimate access
# to its private state?
#
# Who knows what a GPU
# machine needs that a
# plain machine does not?

# ============================================================
# THE ANSWER
# ============================================================

# The object itself.
#
# The client should not
# BUILD the copy.
#
# The client should ASK
# for one.
#
# All three problems
# dissolve at once:
#
# No coupling.
#
# No encapsulation break.
#
# No isinstance chain.

# ============================================================
# STEPPING OUTSIDE CODE
# ============================================================

# Before we write anything,
# look at how cloud providers
# already solved this.
#
# AWS.
#
# Azure.
#
# GCP.
#
# You click "launch instance".
#
# A server is live in
# under a minute.
#
# Nobody installed an OS
# in that minute.

# ============================================================
# NAMING THE PATTERN
# ============================================================

# Now the name earns itself.
#
# Prototype Design Pattern:
#
# Instead of building an
# object from scratch,
# create it by COPYING an
# existing template object,
# then changing only what
# is different.
#
# The saved image is
# the prototype.
#
# Every launched VM is
# a copy of it.

# ============================================================
# WHAT WE HAVE NOT DONE YET
# ============================================================

# Notice what is missing.
#
# We named the idea.
#
# We wrote zero clone code.
#
# That is deliberate.
#
# The next file gives the
# object the one method
# this entire file was
# asking for.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception 1:
#
# "Manual copying is fine
# for small classes."
#
# Small classes grow.
#
# The copy sites do not
# grow with them.

# Misconception 2:
#
# "Python has no private
# fields, so encapsulation
# does not apply."
#
# The convention exists
# precisely so the design
# intent stays readable.

# Misconception 3:
#
# "isinstance() is the
# normal way to handle
# subtypes."
#
# It is the normal way
# to reintroduce a bug
# with every new subtype.

# ============================================================
# QUIZ
# ============================================================

# A copy function was written
# when VMInstance had six
# fields. A seventh field is
# added later. What happens
# to the copies?
#
# A) TypeError at runtime
# B) The new field is copied
#    automatically
# C) The new field is silently
#    missing from every copy
# D) Python warns at import
#
# Answer:
#
# C) Silently missing.

# ============================================================
# QUIZ 2
# ============================================================

# In an isinstance() chain,
# why must the most specific
# subclass be checked first?
#
# A) It runs faster
# B) A subclass instance also
#    matches its parent check
# C) Python requires it
# D) It does not matter
#
# Answer:
#
# B) The parent branch would
#    match first and win.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why is field-by-field
# copying from outside a
# class considered a
# design problem, even
# when it produces correct
# output today?
#
# Because correctness
# depends on knowledge
# that lives in another
# class and can change
# without notice.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Which SOLID principle do
# isinstance() copy chains
# violate, and how?
#
# Open/Closed.
#
# Every new subtype forces
# modification of existing,
# working code.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Treating a copy bug as
# a data bug.
#
# The missing region field
# looks like bad input.
#
# It is bad structure.

# ============================================================
# BEST PRACTICE
# ============================================================

# Ask one question of any
# copying code:
#
# "If this class gains a
# field tomorrow, who has
# to remember to update
# this line?"
#
# If the answer is
# "a human", the design
# is wrong.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Naive copying breaks
# three things:
#
# 1. Coupling
#    Client knows every field
#
# 2. Encapsulation
#    Client touches internals
#
# 3. OCP
#    Every subtype edits
#    working code
#
# One fix for all three:
#
# Move the responsibility
# INTO the object.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Copying an object from
# outside couples the caller
# to its internal shape.
#
# Silent field loss is the
# signature failure of
# manual copying.
#
# Name mangling is a signal,
# not a lock.
#
# isinstance() chains grow
# forever and depend on
# branch order.
#
# The object itself is the
# only place that knows how
# to copy the object.
#
# Prototype means: keep a
# validated template, copy
# it, customize only the
# difference.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We now know WHY the
# object must copy itself.
#
# Next we make it do so.
#
# An abstract base class.
#
# A single __init__ that
# handles two jobs.
#
# And one rule every
# subclass must obey.
#
# Next:
#
# 02_prototype_clone.py
