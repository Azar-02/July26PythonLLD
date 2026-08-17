"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 02_decorator_implementation.py
============================================================

Topics Covered
--------------
1.  Where File 01 Left Us
2.  Step 1 : The Shared Interface
3.  Base Drinks Stand On Their Own
4.  Step 2 : The Base Drinks
5.  What An Add-On Needs To Hold
6.  Step 3 : The Shared Add-On Base Class
7.  The Add-Ons Themselves
8.  Placing An Order
9.  Tracing cost() By Hand
10. The Boolean Flags Alternative
11. Why Flags Don't Scale
12. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 01 LEFT US
# ============================================================

# A Beverage holding a list of
# Condiments ran out of room.
#
# Repeated add-ons.
#
# Add-ons that affect each
# other's price.
#
# We decided on the fix:
#
#     treat everything as the
#     same kind of thing —
#     a Beverage that can wrap
#     another Beverage
#     underneath it.
#
# Now we write it.

# ============================================================
# STEP 1 : THE SHARED INTERFACE
# ============================================================

# Every layer inherits from
# this.
#
# Base drink or add-on.
#
# No exceptions.


class Beverage(ABC):

    @abstractmethod
    def cost(self):
        ...

    @abstractmethod
    def get_description(self):
        ...


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# A base drink has to be able
# to stand on its own.
#
# You can't build an order
# with zero base drink.
#
# What does that tell us about
# how Espresso should be
# coded?
#
# Compared to an add-on like
# Mocha.

# ============================================================
# THE ANSWER
# ============================================================

# The base drink doesn't wrap
# anything.
#
# It just implements Beverage
# directly.
#
# With a fixed cost and a
# fixed description.
#
# An add-on, on the other
# hand, always has to wrap
# SOMETHING.

# ============================================================
# STEP 2 : THE BASE DRINKS
# ============================================================

# These don't wrap anything.
#
# They ARE the starting point.


class Espresso(Beverage):

    def cost(self):
        return 80.0

    def get_description(self):
        return "Espresso"


class DarkRoast(Beverage):

    def cost(self):
        return 70.0

    def get_description(self):
        return "Dark Roast"


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now think about an add-on
# like Mocha.
#
# It needs to hold the
# Beverage it's wrapping.
#
# And add its own cost and
# description on top.
#
# What would that class look
# like?

# ============================================================
# THE ANSWER
# ============================================================

# A class that implements
# Beverage.
#
# Stores a Beverage inside it.
#
# Whatever it's wrapping.
#
# And whose cost() method
# calls the wrapped object's
# cost() FIRST.
#
# Then adds its own price on
# top.
#
# Read that order again.
#
# Wrapped first.
#
# Own price second.

# ============================================================
# STEP 3 : A SHARED BASE CLASS FOR ADD-ONS
# ============================================================

# This stays abstract too.
#
# It inherits from Beverage
# but never implements cost()
# or get_description() itself.
#
# So it exists only to give
# Mocha, Whip, etc. a shared
# "store what I'm wrapping"
# step.
#
# Instead of repeating that in
# every add-on class.


class CondimentDecorator(Beverage):

    def __init__(self, wrapped_beverage):
        self.wrapped_beverage = wrapped_beverage


# ============================================================
# THE ADD-ONS
# ============================================================


class Mocha(CondimentDecorator):

    def cost(self):
        return self.wrapped_beverage.cost() + 20.0

    def get_description(self):
        return self.wrapped_beverage.get_description() + " + Mocha"


class Whip(CondimentDecorator):

    def cost(self):
        return self.wrapped_beverage.cost() + 15.0

    def get_description(self):
        return self.wrapped_beverage.get_description() + " + Whip"


# ============================================================
# PLACING AN ORDER
# ============================================================

# Espresso, then mocha, then
# whip.
#
# Each new line wraps the one
# before it.

print("Placing An Order")

order = Espresso()
print(order.get_description())   # Espresso
print(order.cost())              # 80.0

order = Mocha(order)
print(order.get_description())   # Espresso + Mocha
print(order.cost())              # 80.0 + 20.0 = 100.0

order = Whip(order)
print(order.get_description())   # Espresso + Mocha + Whip
print(order.cost())              # 100.0 + 15.0 = 115.0

# Observation:
#
# The variable name never
# changed.
#
# Each line wrapped whatever
# "order" was at that moment.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Trace order.cost() by hand.
#
# Step by step.
#
# When we call it, which
# method actually runs first?
#
# And what does it do?
#
# Work it out before reading
# the next block.

# ============================================================
# THE TRACE : GOING DOWN
# ============================================================

# order.cost() is really
# Whip.cost().
#
# But before it adds its own
# 15.0, it first calls cost()
# on whatever it's wrapping.
#
#     Mocha
#
# Mocha.cost() does the same
# thing.
#
# Before it adds its own 20.0,
# it calls cost() on what
# IT's wrapping.
#
#     Espresso
#
# Espresso.cost() isn't
# wrapping anything.
#
# So it just returns 80.0
# right away.

# ============================================================
# THE TRACE : COMING BACK UP
# ============================================================

# Now the answers travel back
# up.
#
# 80.0
#
# Mocha adds 20.0
#
# 100.0
#
# Whip adds 15.0
#
# 115.0
#
# Nothing computed the total
# in one place.
#
# Every layer added exactly
# its own piece.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now compare this to a
# different design.
#
# One giant Espresso class.
#
# With boolean flags like
# has_mocha, has_whip,
# has_soy.
#
# And one big cost() method
# with an if check for each
# flag.
#
# What's wrong with that?

# ============================================================
# THE FLAG VERSION
# ============================================================


class FlagEspresso:

    def __init__(self, has_mocha, has_whip, has_soy):
        self.has_mocha = has_mocha
        self.has_whip = has_whip
        self.has_soy = has_soy

    def cost(self):
        total = 80.0
        if self.has_mocha:
            total += 20.0
        if self.has_whip:
            total += 15.0
        if self.has_soy:
            total += 10.0
        return total


print("\nThe Flag Version")

flag_order = FlagEspresso(has_mocha=True, has_whip=True, has_soy=False)
print(flag_order.cost())

# Observation:
#
# Same answer.
#
# 115.0.
#
# Getting the right number was
# never the hard part.

# ============================================================
# WHY FLAGS DON'T SCALE
# ============================================================

# Every new add-on means going
# back and editing that same
# class.
#
# Adding a new flag.
#
# And a new if check inside
# cost().
#
# This doesn't scale.
#
# And unlike our wrapping
# approach, the combination
# isn't really decided while
# the program runs.
#
# It's all hardcoded into one
# method ahead of time.

# ============================================================
# CHECKPOINT
# ============================================================

# Solid on the shape?
#
# One shared interface.
#
# Base drinks that implement
# it directly.
#
# Add-ons that implement it
# AND hold one of it.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Every layer — base drink or
# add-on — implements the same
# Beverage interface.
#
# A base drink wraps nothing
# and returns a fixed cost and
# description.
#
# An add-on always wraps
# something.
#
# CondimentDecorator exists
# only to hold the wrapped
# beverage, so each add-on
# doesn't repeat that step.
#
# An add-on's cost() calls the
# wrapped cost() first, then
# adds its own price.
#
# The call travels down to the
# base, and the answers travel
# back up.
#
# Boolean flags get the same
# number, but every new add-on
# means editing the class, and
# nothing is decided at
# runtime.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We built this for coffee.
#
# Now the surprising part.
#
# You have already used this
# exact structure.
#
# Every single time you have
# opened a file in Python.
#
# And every time you have
# typed an @ above a function
# definition.
#
# Next:
#
# 03_decorator_in_real_tools.py
