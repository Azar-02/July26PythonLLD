"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 01_decorator_intro_and_coffee_problem.py
============================================================

Topics Covered
--------------
1.  Recap Of Adapter And Facade
2.  A Different Kind Of Problem
3.  Four Structural Patterns
4.  Today's Roadmap
5.  The Coffee Order
6.  The Same Question With Pizza
7.  What Is Common To Both
8.  Decorator : The General Idea
9.  The Coffee Shop Backend
10. The Common First Attempt
11. Where It Falls Apart
12. Everything Is A Beverage
13. Key Takeaways
"""

# ============================================================
# RECAP OF LAST CLASS
# ============================================================

# We covered Adapter and
# Facade.
#
# Both were about making
# things fit together nicely.
#
# Adapter
#
#     two things that don't
#     speak the same
#     "language"
#
#     we translate between
#     them
#
# Facade
#
#     one thing that's doing
#     too much
#
#     we hide all that mess
#     behind one simple entry
#     point

# ============================================================
# A DIFFERENT KIND OF PROBLEM
# ============================================================

# Today's two patterns are
# also Structural patterns.
#
# But they solve completely
# different problems.
#
# Here is the first one.
#
# What if you don't know
# ahead of time every possible
# combination of features a
# customer might want?
#
# Because they keep adding
# more, one at a time, while
# placing the order.
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# You can't create a separate
# class for every possible
# combination.
#
# There'd be too many.
#
# You need a way to add extra
# behaviour on top of an
# object.
#
# Without changing the
# object's original class.
#
# That is Decorator.

# ============================================================
# BOARD SUMMARY
# ============================================================

# ADAPTER
#
#     make two things that
#     don't fit, fit together
#
# FACADE
#
#     hide a messy system
#     behind one simple entry
#     point
#
# DECORATOR
#
#     add new behaviour to an
#     object while the program
#     is running, without
#     changing its class
#
# FLYWEIGHT
#
#     handle a huge number of
#     very similar objects
#     without running out of
#     memory
#
# Today:
#
#     Decorator
#
#     Flyweight



# ============================================================
# WARM UP : THE COFFEE ORDER
# ============================================================

# Think about the last time
# you ordered a coffee.
#
# At a place like Starbucks
# or CCD.
#
# You start with a plain
# espresso.
#
# Then what happens?
#
# Think before reading on.

# ============================================================
# WHAT HAPPENS
# ============================================================

# You add steamed milk.
#
# Maybe some mocha syrup.
#
# Maybe whipped cream on top.
#
# Each thing you add changes
# the price.
#
# And changes how you'd
# describe the drink.
#
# But underneath it all, it's
# still "a coffee."

# ============================================================
# THE SAME QUESTION WITH PIZZA
# ============================================================

# What's the equivalent there?
#
# You start with a plain base
# pizza.
#
# Then add cheese.
#
# Then olives.
#
# Then jalapeños.
#
# Each topping changes the
# price and the description.
#
# Nothing about the base
# pizza itself changes.

# ============================================================
# WHAT IS COMMON TO BOTH
# ============================================================

# You start with one base
# thing.
#
# And then you keep WRAPPING
# more on top of it.
#
# One layer at a time.
#
# Each new layer only changes
# two things.
#
# How much it costs.
#
# And how you'd describe it.
#
# The base thing underneath
# never changes.

# ============================================================
# WHY COFFEE, NOT PIZZA
# ============================================================

# We're going to build the
# coffee shop version in code
# today.
#
# It is the version you'll see
# most often in interviews.
#
# And in real codebases.

# ============================================================
# BOARD SUMMARY
# ============================================================

# DECORATOR (the general idea)
#
#     Start with a base object.
#
#     Wrap it with extra
#     behaviour, one layer at
#     a time, while the
#     program is running
#     (not decided ahead of
#     time).
#
#     Each layer changes the
#     result (cost,
#     description, behaviour)
#     without touching the
#     object underneath it.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the general idea?
#
# Now the real backend
# problem.

# ============================================================
# THE COFFEE SHOP BACKEND
# ============================================================

# Imagine you're building the
# backend for a coffee shop
# chain.
#
# A customer first picks a
# base drink.
#
#     Espresso
#
#     Dark Roast
#
#     House Blend
#
#     Decaf
#
# And then picks add-ons.
#
#     milk
#
#     mocha
#
#     whip
#
#     soy

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What two things does the
# system need to work out for
# any order?
#
# No matter what was picked.

# ============================================================
# THE TWO THINGS
# ============================================================

# The total cost.
#
# And a description of
# everything that's in the
# order.
#
# Every design we look at
# today has to answer exactly
# these two questions.

# ============================================================
# THE COMMON FIRST ATTEMPT
# ============================================================

# Make a Beverage class that
# holds a list of Condiment
# objects.
#
# A list of add-ons.
#
# With a separate cost()
# method on Beverage, and on
# each Condiment.


class Condiment:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def cost(self):
        return self.price


class Beverage:

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.condiments = []

    def add_condiment(self, condiment):
        self.condiments.append(condiment)

    def cost(self):
        total = self.price
        for condiment in self.condiments:
            total += condiment.cost()
        return total

    def get_description(self):
        description = self.name
        for condiment in self.condiments:
            description += " + " + condiment.name
        return description


# ============================================================
# RUNNING IT
# ============================================================

print("The Common First Attempt")

order = Beverage("Espresso", 80.0)
order.add_condiment(Condiment("Mocha", 20.0))
order.add_condiment(Condiment("Whip", 15.0))

print(order.get_description())
print(order.cost())

# Observation:
#
# For a simple order, this is
# fine.
#
# Two questions answered.
#
# Cost.
#
# Description.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Where does this fall apart?
#
# Think about two customers.
#
# One wants DOUBLE mocha.
#
# One wants a "large" size —
# which should increase the
# price of the base drink
# AND every add-on.
#
# Work through both before
# reading on.

# ============================================================
# WHERE IT FALLS APART
# ============================================================

# Once add-ons can repeat.
#
# Or affect each other's
# price.
#
# A simple fixed list attached
# to Beverage isn't enough
# anymore.
#
# We'd end up writing
# special-case code for every
# new combination that shows
# up.

# ============================================================
# BOARD SUMMARY
# ============================================================

# PROBLEM
#
# treating "Beverage" and
# "Condiment" as two separate
# things
#
#     Repeated add-ons, or
#     add-ons that affect
#     price, don't fit this
#     model
#
#     Every new combination
#     needs new, special-case
#     code
#
# FIX
# 
# treat everything as the same
# kind of thing: a "Beverage"
# that can wrap another
# Beverage underneath it.

# ============================================================
# THE FIX, SAID PLAINLY
# ============================================================

# Stop treating "drink" and
# "add-on" as two different
# kinds of things.
#
# Treat all of them —
#
#     Espresso
#
#     Mocha
#
#     Whip
#
# — as the exact same kind of
# thing.
#
# A beverage.
#
# Each one knows its own cost
# and its own description.
#
# And each one can WRAP
# another beverage underneath
# it.

# ============================================================
# WE HAVE MADE THIS MOVE BEFORE
# ============================================================

# Think back to the Adapter
# lecture.
#
# Every bank had to speak the
# same BankAPI interface.
#
# No matter which bank was
# underneath.
#
# What's the same move
# happening here?
#
# Think before reading on.

# ============================================================
# THE SAME MOVE
# ============================================================

# Define one shared interface.
#
#     Beverage
#
# With a cost() method.
#
# And a get_description()
# method.
#
# Every base drink and every
# add-on implements that same
# interface.
#
# An add-on also holds a
# reference to whatever
# Beverage it's wrapping.

# ============================================================
# CHECKPOINT
# ============================================================

# Two things should be solid
# before moving on.
#
# One.
#
# What wrapping means.
#
#     a base object,
#
#     layers on top,
#
#     the base never changing.
#
# Two.
#
# Why a Beverage holding a
# list of Condiments runs out
# of room.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Adapter made two things fit.
#
# Facade hid a messy system.
#
# Decorator adds new behaviour
# to an object while the
# program is running, without
# changing its class.
#
# You cannot write one class
# per possible combination of
# add-ons.
#
# There would be too many.
#
# A coffee order and a pizza
# order are the same shape:
#
#     one base thing,
#
#     layers wrapped on top,
#
#     each layer changing only
#     cost and description.
#
# Treating "drink" and
# "add-on" as two separate
# kinds of things is what
# breaks.
#
# Treating both as a Beverage
# that can wrap another
# Beverage is what fixes it.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We know what we want now.
#
# One shared interface.
#
# Base drinks that stand on
# their own.
#
# Add-ons that wrap something
# underneath.
#
# Two questions remain open:
#
# What does a base drink look
# like, compared to an add-on?
#
# And when we call cost() on a
# stack of three layers, which
# method actually runs first?
#
# Next:
#
# 02_decorator_implementation.py
