"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 06_flyweight_in_a_real_backend.py
============================================================

Topics Covered
--------------
1.  Where File 05 Left Us
2.  A Small Python Mystery
3.  Why 100 And 1000 Behave Differently
4.  Running This In A File vs The REPL
5.  Why "is" And Not "=="
6.  A CPython Detail, Not A Guarantee
7.  The Food Delivery Scenario
8.  The Shared Category
9.  The Factory And The Line Item
10. Pooling Reference Data
11. The Question To Always Ask
12. Key Takeaways
"""

# ============================================================
# WHERE FILE 05 LEFT US
# ============================================================

# We built BulletTypeFactory
# ourselves.
#
# A cache that hands back a
# shared object instead of
# building a new one.
#
# Now two places that same
# idea is already running.
#
# One inside Python itself.
#
# One inside code you have
# almost certainly written.

# ============================================================
# A SMALL PYTHON MYSTERY
# ============================================================

# In Python, if you write:
#
#     a = 100
#     b = 100
#
# and then check:
#
#     a is b
#
# it comes out True.
#
# But the same check with
# 1000 often comes out False.
#
# Any guesses why?
#
# Now that we know Flyweight.

# ============================================================
# THE ANSWER
# ============================================================

# Python caches and reuses
# small integer objects.
#
# Instead of creating a
# brand-new object every time
# your code uses one.
#
# The exact same idea as
# reusing BulletType.

# ============================================================
# WHAT CPYTHON ACTUALLY DOES
# ============================================================

# CPython — the standard
# Python implementation —
# pre-creates and caches small
# integers.
#
# Roughly the range -5 to 256.
#
# And hands back that same
# shared object every time
# your code uses one of those
# values.
#
# Instead of building a fresh
# one.
#
# Step outside that range,
# like 1000, and each one your
# code creates is typically
# its own separate object.

# ============================================================
# THE CODE
# ============================================================

print("Small Integer Caching")

a = 100
b = 100
print(a is b)   # True — same shared object

a = 1000
b = 1000
print(a is b)   # False, in most cases — two separate objects


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Notice we're using:
#
#     is
#
# Not:
#
#     ==
#
# Why does that matter for
# this specific check?

# ============================================================
# THE ANSWER
# ============================================================

# == checks if two values are
# equal.
#
# is checks if they're
# literally the same object in
# memory.
#
# We specifically want to know
# if a and b are pointing at
# one shared object.
#
# Which is exactly the
# question Flyweight is about.

# ============================================================
# A DETAIL, NOT A GUARANTEE
# ============================================================

# Worth flagging.
#
# This small-integer caching
# is a detail of CPython
# specifically.
#
# Not a guarantee the Python
# language makes.
#
# It's still a widely known,
# very real example of
# Flyweight running inside a
# language runtime.
#
# Same as short string
# literals often being
# "interned" — shared — the
# same way.
#
# For the same underlying
# reason.


# ============================================================
# KEY TAKEAWAYS
# ============================================================

# CPython pre-creates and
# caches small integers,
# roughly -5 to 256.
#
# That is Flyweight running
# inside a language runtime.
#
# Short string literals are
# often interned for the same
# reason.
#
# It is a CPython detail, not
# a language guarantee.
#
# is asks whether two names
# point at the same object.
#
# == only asks whether the
# values are equal.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Both patterns are now on the
# table.
#
# Decorator.
#
# Flyweight.
#
# Next we look at what happens
# when the two get combined —
#
# and one small, innocent
# looking field quietly breaks
# the sharing.
#
# Next:
#
# 07_ai_corner_and_wrapup.py
