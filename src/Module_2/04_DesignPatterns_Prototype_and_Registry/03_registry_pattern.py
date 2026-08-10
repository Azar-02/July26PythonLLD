"""
============================================================
LLD-6 : DESIGN PATTERNS - PROTOTYPE & REGISTRY
FILE : 03_registry_pattern.py
============================================================

Topics Covered
--------------
1.  Recap: The Template Has Nowhere To Live
2.  Two Responsibilities, Not One
3.  The Simplest Possible Store
4.  Building VMImageRegistry
5.  Bootstrapping: fill_registry
6.  The Fill / Get / Clone Flow
7.  Forgetting To Clone
8.  The Missing Key Trap
9.  A Defensive get()
10. Thread Safety And The GIL
11. Check-Then-Act Races
12. Fixing It With A Lock
13. Registry vs Singleton
14. Interview Questions
15. Key Takeaways
"""

import threading
import time
from abc import ABC, abstractmethod

# ============================================================
# RECAP
# ============================================================

# Objects can now copy
# themselves.
#
# clone() works.
#
# Subclasses override it.
#
# But look at how the
# previous file ended.
#
#     golden_image = VMInstance()
#     golden_image.os = "Ubuntu 22.04"
#
# A local variable.
#
# In one script.
#
# Question:
#
# How does a different
# module get that template?

# ============================================================
# THE BAD ANSWERS
# ============================================================

# Option 1:
#
# Rebuild the template
# wherever it is needed.
#
# Now the "one validated
# template" exists in six
# places, slowly drifting
# apart.
#
# Option 2:
#
# Pass it as a parameter
# through every function
# that might eventually
# need it.
#
# Option 3:
#
# A module-level global,
# imported everywhere.
#
# None of these scale to
# ten template types.

# ============================================================
# THE MISSING PIECE
# ============================================================

# We need somewhere to KEEP
# pre-configured templates.
#
# Retrievable by name.
#
# From anywhere.
#
# Notice this is a completely
# different job from copying.
#
# Copying belongs to the
# object.
#
# Storage does not.


# ============================================================
# THE SIMPLEST STORE
# ============================================================

# Question:
#
# What data structure means
# "store something, retrieve
# it later by a key"?
#
# Answer:
#
# A dictionary.
#
# The pattern is genuinely
# that small.
#
# Its value is not
# cleverness.
#
# Its value is having ONE
# agreed place.

# ============================================================
# SETUP : THE PROTOTYPE CODE
# ============================================================


class Prototype(ABC):

    @abstractmethod
    def clone(self):
        ...


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
            f"host={self.hostname}, "
            f"ip={self.ip_address})"
        )


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


# ============================================================
# BUILDING THE REGISTRY
# ============================================================


class VMImageRegistry:

    def __init__(self):
        self._templates = {}

    def register(self, key, instance):
        self._templates[key] = instance

    def get(self, key):
        return self._templates.get(key)

    def keys(self):
        return list(self._templates.keys())


# Observation:
#
# Three lines of real logic.
#
# No inheritance.
#
# No abstract methods.
#
# The underscore on
# _templates is the same
# convention we discussed
# earlier.
#
# "Go through register()
# and get(), not around
# them."

# ============================================================
# BOOTSTRAPPING
# ============================================================

# Question:
#
# Who fills this registry?
#
# Answer:
#
# Startup code.
#
# Run once.
#
# Before anything asks
# for a template.


def fill_registry(registry):
    backend_image = VMInstance()
    backend_image.os = "Ubuntu 22.04"
    backend_image.runtime = "Python 3.11"
    backend_image.monitoring_agent = True
    backend_image.security_patches = True

    registry.register("backend-server-v3", backend_image)

    gpu_image = GpuVMInstance()
    gpu_image.os = "Ubuntu 22.04"
    gpu_image.runtime = "Python 3.11"
    gpu_image.monitoring_agent = True
    gpu_image.security_patches = True
    gpu_image.gpu_type = "NVIDIA A100"

    registry.register("gpu-training-v1", gpu_image)


# ============================================================
# THE FULL FLOW
# ============================================================

vm_registry = VMImageRegistry()

fill_registry(vm_registry)

print("Registered Templates")
print(vm_registry.keys())

server = vm_registry.get("backend-server-v3").clone()

server.hostname = "web-01"
server.ip_address = "10.0.0.14"

print("\nLaunched Server")
print(server)

trainer = vm_registry.get("gpu-training-v1").clone()

trainer.hostname = "train-01"
trainer.ip_address = "10.0.0.22"

print("\nLaunched Trainer")
print(trainer)

# ============================================================
# THREE STEPS
# ============================================================

# FILL
#
# Populate templates once,
# at startup.
#
# GET
#
# Retrieve the right stored
# template by key.
#
# CLONE
#
# Produce an independent
# copy to customize.
#
# Read the launch lines
# again.
#
# Every one of them is
# get, then clone, then
# set only what varies.

# ============================================================
# VERIFYING THE TEMPLATE
# ============================================================

# We set hostname on two
# clones.
#
# Did the stored template
# notice?

stored = vm_registry.get("backend-server-v3")

print("\nTemplate After Two Launches")
print(stored)

# Observation:
#
# hostname is still None.
#
# The template is untouched.
#
# Clone protected it.

# ============================================================
# NOW REMOVE THE CLONE
# ============================================================

# What if someone forgets
# that middle step?
#
# get() alone returns the
# stored object itself.
#
# Not a copy.
#
# The registry hands out
# a reference.

careless = vm_registry.get("backend-server-v3")

careless.hostname = "web-99"
careless.ip_address = "10.0.0.99"

print("\nTemplate After Careless Use")
print(vm_registry.get("backend-server-v3"))

# Observation:
#
# The template is now
# a specific server.
#
# Permanently.
#
# For every future caller.

# ============================================================
# IMPORTANT
# ============================================================

# Watch what happens to
# the NEXT machine launched
# from this template.

next_server = vm_registry.get("backend-server-v3").clone()

print("\nNext Server Before Setup")
print(next_server)

# Observation:
#
# It was born with someone
# else's hostname.
#
# And someone else's IP.
#
# One forgotten .clone()
# poisoned the shared
# template.
#
# This is the single most
# common Registry bug.

# ============================================================
# RESTORING THE TEMPLATE
# ============================================================

repaired = VMInstance()
repaired.os = "Ubuntu 22.04"
repaired.runtime = "Python 3.11"
repaired.monitoring_agent = True
repaired.security_patches = True

vm_registry.register("backend-server-v3", repaired)

print("\nTemplate Repaired")
print(vm_registry.get("backend-server-v3"))

# ============================================================
# DESIGN DISCUSSION
# ============================================================

# Could the registry protect
# us here?
#
# It could.
#
# get() could clone before
# returning.
#
# Then callers can never
# reach the template.
#
# But then the registry is
# doing two jobs again.
#
# Storage AND copying.
#
# Both designs exist in
# real code.
#
# We keep them separate so
# the two patterns stay
# visible and separately
# teachable.

# ============================================================
# THE MISSING KEY TRAP
# ============================================================

# A different failure.
#
# Someone types:
#
#     "backendserver-v3"
#
# One missing hyphen.
#
# What does get() return?

typo_result = vm_registry.get("backendserver-v3")

print("\nTypo Lookup")
print(typo_result)

# Observation:
#
# None.
#
# No error.
#
# dict.get() considers a
# missing key a normal
# outcome.

# ============================================================
# WHERE IT ACTUALLY BREAKS
# ============================================================

print("\nCloning The Typo Result")

try:
    ghost = vm_registry.get("backendserver-v3").clone()
    print(ghost)
except AttributeError as error:
    print(error)

# Observation:
#
# AttributeError on None.
#
# The message mentions
# clone.
#
# It does not mention the
# key.
#
# It does not mention the
# typo.
#
# The error names the
# victim, not the cause.

# ============================================================
# THE FAMILIAR SHAPE
# ============================================================

# We have seen this before.
#
# Silently missing region
# in file 01.
#
# Silently dropped gpu_type
# in file 02.
#
# Now a silently missing
# template.
#
# Same shape every time:
#
# The mistake happens here.
#
# The error appears there.

# ============================================================
# A DEFENSIVE REGISTRY
# ============================================================


class StrictVMImageRegistry:

    def __init__(self):
        self._templates = {}

    def register(self, key, instance):
        self._templates[key] = instance

    def get(self, key):
        if key not in self._templates:
            available = ", ".join(sorted(self._templates))
            raise KeyError(
                f"No template registered under {key!r}. "
                f"Available: {available}"
            )

        return self._templates[key]


strict_registry = StrictVMImageRegistry()
fill_registry(strict_registry)

print("\nStrict Lookup")

try:
    strict_registry.get("backendserver-v3")
except KeyError as error:
    print(error)

# Observation:
#
# The error arrives at the
# lookup.
#
# It names the bad key.
#
# It lists the valid ones.
#
# The typo is visible in
# the message itself.

# ============================================================
# THREAD SAFETY
# ============================================================

# A registry is shared state.
#
# Multiple threads will
# read it.
#
# Some may write it.
#
# Question, from the
# Concurrency module:
#
# If two threads call
# register() at the exact
# same moment, can the
# dictionary be corrupted?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# A single assignment:
#
#     self._templates[key] = value
#
# is atomic under the GIL.
#
# The dictionary cannot end
# up in a broken internal
# state.
#
# One of the two writes wins.
#
# Both are complete.

# ============================================================
# BUT
# ============================================================

# That safety covers ONE
# operation.
#
# The moment code does:
#
# "check if a key exists,
# and only then write it"
#
# there are TWO operations.
#
# And a gap between them.

# ============================================================
# A CHECK-THEN-ACT REGISTRY
# ============================================================


class UnsafeRegistry:

    def __init__(self):
        self._templates = {}

    def register_if_absent(self, key, instance):
        if key not in self._templates:
            # Simulating any real work:
            # validation, a disk read,
            # a network call.
            time.sleep(0.05)

            self._templates[key] = instance
            return True

        return False


# ============================================================
# TWO THREADS, ONE KEY
# ============================================================

unsafe = UnsafeRegistry()

claims = []


def claim_template(owner):
    template = VMInstance()
    template.os = owner

    won = unsafe.register_if_absent("shared-image", template)

    claims.append((owner, won))


thread_a = threading.Thread(target=claim_template, args=("team-a",))
thread_b = threading.Thread(target=claim_template, args=("team-b",))

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()

print("\nUnsafe Registration")
print(claims)

print("\nWinner Stored")
print(unsafe._templates["shared-image"].os)

# Observation:
#
# Both threads were told
# they won.
#
# Both got True.
#
# Only one template
# survived.
#
# The other team is now
# holding a false belief
# about production.

# ============================================================
# WHY
# ============================================================

# Thread A checked.
#
# Key absent.
#
# Thread A paused.
#
# Thread B checked.
#
# Key still absent.
#
# Both proceeded to write.
#
# The dictionary was never
# corrupted.
#
# The LOGIC was.

# ============================================================
# FIXING IT WITH A LOCK
# ============================================================


class SafeRegistry:

    def __init__(self):
        self._templates = {}
        self._lock = threading.Lock()

    def register_if_absent(self, key, instance):
        with self._lock:
            if key not in self._templates:
                time.sleep(0.05)

                self._templates[key] = instance
                return True

            return False


safe = SafeRegistry()

safe_claims = []


def claim_safely(owner):
    template = VMInstance()
    template.os = owner

    won = safe.register_if_absent("shared-image", template)

    safe_claims.append((owner, won))


thread_c = threading.Thread(target=claim_safely, args=("team-a",))
thread_d = threading.Thread(target=claim_safely, args=("team-b",))

thread_c.start()
thread_d.start()

thread_c.join()
thread_d.join()

print("\nSafe Registration")
print(safe_claims)

# Observation:
#
# Exactly one True.
#
# Exactly one False.
#
# The check and the write
# became one indivisible
# step.

# ============================================================
# THE PRACTICAL RULE
# ============================================================

# Plain register() and get()
# need no lock.
#
# Single atomic operations.
#
# Anything shaped like
# "look, then decide, then
# write" needs a lock.
#
# Same rule as the shared
# counters in the
# Concurrency classes.
#
# Nothing new here.
#
# Only a new place for it
# to appear.

# ============================================================
# REGISTRY VS SINGLETON
# ============================================================

# A fair question:
#
# Is this just a Singleton?
#
# No.
#
# Singleton controls how
# many instances of a class
# exist.
#
# Registry controls where
# named objects are found.
#
# They often meet, because
# an application usually
# wants one registry.
#
# But the problems are
# different.
#
# One is about creation.
#
# One is about lookup.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# Misconception 1:
#
# "get() gives me a copy."
#
# It gives a reference.
#
# The clone is your job.

# Misconception 2:
#
# "A dict is too simple to
# be a design pattern."
#
# The pattern is the
# DISCIPLINE of one named
# place, not the data
# structure.

# Misconception 3:
#
# "The GIL makes my registry
# thread safe."
#
# It makes single operations
# safe.
#
# Not sequences of them.

# ============================================================
# QUIZ
# ============================================================

# registry.get("gpu-training-v1")
# is called, but only
# "backend-server-v3" was
# registered. What happens?
#
# A) An error is raised
#    immediately inside get()
# B) get() returns None; the
#    crash happens later
#    wherever None is used
# C) get() creates an empty
#    template
# D) Python ignores it
#
# Answer:
#
# B) Silent until later.

# ============================================================
# QUIZ 2
# ============================================================

# A developer writes:
#
#     vm = registry.get("backend-server-v3")
#     vm.hostname = "web-07"
#
# What is the consequence?
#
# A) Nothing, vm is a copy
# B) The stored template is
#    permanently modified
# C) A TypeError is raised
# D) The registry
#    auto-restores it
#
# Answer:
#
# B) The template itself
#    was modified.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Why keep the Registry
# separate from the
# Prototype?
#
# They change for different
# reasons.
#
# Copying logic changes when
# a class gains fields.
#
# Lookup logic changes when
# storage or naming rules
# change.
#
# Single Responsibility.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Dictionary writes are
# atomic under the GIL,
# so why would a registry
# ever need a lock?
#
# Because atomicity covers
# one operation.
#
# A check-then-act sequence
# is two, and threads can
# interleave between them.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Treating the registry as
# a cache of usable objects
# rather than a shelf of
# read-only templates.
#
# Templates are for copying.
#
# Never for using directly.

# ============================================================
# BEST PRACTICE
# ============================================================

# Two habits.
#
# One:
#
# Make get() raise on a
# missing key.
#
# Two:
#
# Treat get() and clone()
# as a single expression.
#
#     registry.get(key).clone()
#
# Never store the result of
# a bare get() in a variable
# you intend to modify.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Prototype:
#
# "Ask the OBJECT for a
# copy of itself."
#
# Fixes coupling,
# encapsulation, OCP.
#
# Registry:
#
# "Keep named templates in
# ONE retrievable place."
#
# Fixes templates being
# rebuilt or scattered.
#
# Used together.
#
# Solving separate problems.
#
# Flow: fill, get, clone.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# A Registry is a dictionary
# plus a discipline.
#
# Fill once at startup, then
# get and clone repeatedly.
#
# get() returns the template
# itself, so a forgotten
# clone() corrupts it for
# everyone.
#
# A missing key returns None
# and fails far away, so
# raise instead.
#
# Single dict writes are
# atomic; check-then-act
# needs a lock.
#
# Registry answers "where do
# I find it", Singleton
# answers "how many exist".

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We now have the full
# machinery.
#
# Templates stored.
#
# Objects cloning themselves.
#
# Clients customizing only
# what varies.
#
# And every field we have
# used so far has been a
# string, a bool, or None.
#
# Add one list to VMInstance.
#
# The clone() we trust will
# quietly stop producing
# independent objects.
#
# Next:
#
# 04_shallow_vs_deep_copy.py
