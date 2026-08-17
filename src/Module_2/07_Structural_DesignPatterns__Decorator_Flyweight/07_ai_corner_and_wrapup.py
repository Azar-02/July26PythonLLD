"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 07_ai_corner_and_wrapup.py
============================================================

Topics Covered
--------------
1.  Recap Setup From Earlier Files
2.  AI Corner : The Goal
3.  Step 1 — The Code With The Mistake
4.  Watching The Bug Happen
5.  Step 2 — Asking AI To Diagnose
6.  Step 3 — Choosing An Option, Writing The Fix
7.  Step 4 — What The AI Was Useful For
8.  Wrap-Up : Decorator
9.  Wrap-Up : Flyweight
10. Homework
"""

from abc import ABC, abstractmethod

# ============================================================
# RECAP SETUP
# ============================================================

# Built in file 02.
#
# Repeated here only so this
# file runs on its own.
#
# Nothing below is new.


class Beverage(ABC):

    @abstractmethod
    def cost(self):
        ...

    @abstractmethod
    def get_description(self):
        ...


class CondimentDecorator(Beverage):

    def __init__(self, wrapped_beverage):
        self.wrapped_beverage = wrapped_beverage


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
# AI CORNER : THE GOAL
# ============================================================

# BRING YOUR BUGGY CODE,
# NOT JUST YOUR PROMPT
#
# So far we've used AI to
# GENERATE code.
#
# This time we flip it.
#
# The code gets written by
# hand.
#
# Badly, on purpose.
#
# Then pasted into an AI
# assistant with one question:
#
#     "What's wrong with this,
#      and how would you fix
#      it?"
#
# This mirrors real work.
#
# You often already have code,
# written by a human, that
# quietly broke a pattern.
#
# The AI's job here isn't to
# write from scratch.
#
# It's to diagnose and
# propose.
#
# The final fix still gets
# written by hand, after the
# discussion.

# ============================================================
# WHAT THE CODE INVOLVES
# ============================================================

# A Decorator.
#
#     Mocha and Whip wrapping
#     a Beverage.
#
# And a Flyweight.
#
#     BeanFlyweight
#
# that both Espresso and its
# decorators share, to look up
# bean cost and origin.
#
# The mistake is baked into
# how the Flyweight is USED.
#
# Not into the Decorator
# itself.

# ============================================================
# STEP 1 OF 4 : THE CODE WITH THE MISTAKE
# ============================================================

# We already have Espresso as
# our base Beverage.
#
# With Mocha and Whip as
# decorators.
#
# Every beverage looks up its
# bean details from a shared
# BeanFlyweight.
#
# One flyweight per bean
# origin, reused across every
# order of the day.
#
# So we're not creating a new
# object per cup, just to know
#
#     "Arabica costs 40,
#      roasted in
#      Chikmagalur."
#
# Now the shop wants a "hot"
# vs "iced" size adjustment on
# the bean cost.
#
# Added by hand.
#
# No AI yet.


class BuggyBeanFlyweight:

    def __init__(self, origin, base_cost):
        self.origin = origin
        self.base_cost = base_cost
        self.temperature = "hot"   # <-- added for the new feature

    def get_cost(self):
        cost = self.base_cost
        if self.temperature == "iced":
            cost += 10.0
        return cost


class BuggyBeanFlyweightFactory:
    _beans = {}

    @staticmethod
    def get_bean(origin, base_cost):
        if origin not in BuggyBeanFlyweightFactory._beans:
            BuggyBeanFlyweightFactory._beans[origin] = BuggyBeanFlyweight(origin, base_cost)
        return BuggyBeanFlyweightFactory._beans[origin]


class BuggyEspresso(Beverage):

    def __init__(self, temperature):
        self.bean = BuggyBeanFlyweightFactory.get_bean("Arabica", 40.0)
        self.bean.temperature = temperature   # mutate the shared flyweight

    def cost(self):
        return self.bean.get_cost()

    def get_description(self):
        return "Espresso"


print("Step 1 : One Iced Espresso")

iced = BuggyEspresso(temperature="iced")
print(iced.cost())

# Observation:
#
# This compiles.
#
# And if you order one iced
# espresso, it prints the
# right price.
#
# Leave it there for a second.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Just from reading it.
#
# Does anything feel off?
#
# Don't overthink it yet.

# ============================================================
# STEP 2 OF 4 : ASK AI TO DIAGNOSE, NOT REWRITE
# ============================================================

# Instead of guessing, paste
# it into an AI assistant and
# ask it to review.
#
# Not to fix.
#
# The prompt used:
#
#     "Here's a Flyweight
#      (BeanFlyweight /
#      BeanFlyweightFactory)
#      shared across Espresso
#      orders, and Espresso
#      itself, which is wrapped
#      by Decorator classes
#      like Mocha and Whip
#      elsewhere in the app. I
#      added a 'hot vs iced'
#      price adjustment. Can
#      you review this and tell
#      me if anything is wrong
#      with it, and what the
#      possible fixes are?
#      Don't rewrite it yet —
#      just diagnose first."
#
# followed by the code from
# Step 1.

# ============================================================
# THE AI RESPONSE : DIAGNOSIS
# ============================================================

# Functionally this works for
# one order at a time, but
# there's a real bug hiding
# here: temperature was added
# as a field on BeanFlyweight
# itself, and BeanFlyweight is
# shared and cached by origin
# in the factory. Every
# Espresso that orders
# "Arabica" gets back the
# exact same BeanFlyweight
# instance. If a hot Arabica
# order runs, then an iced
# Arabica order runs right
# after, the second one
# overwrites `temperature` on
# the shared object — and now
# the "hot" order's cost()
# would return the iced price
# too, if it's queried again.
# This is the classic
# Flyweight mistake: intrinsic
# state (origin, base_cost —
# same for every user of this
# object) got mixed with
# extrinsic state (temperature
# — different per order), and
# extrinsic state should never
# be stored on the flyweight.
#
# Separately, this also sits
# awkwardly next to your
# Decorator setup: Mocha and
# Whip already wrap Beverage
# to add cost without touching
# Espresso's fields, but this
# change went the opposite
# direction — it pushed new
# mutable state into a shared
# object instead of keeping
# per-order detail local to
# the object that represents
# that order.
#
# Possible fixes:
#
# 1. Keep BeanFlyweight fully
#    intrinsic (origin,
#    base_cost only) and pass
#    temperature as an
#    argument to
#    get_cost(temperature), the
#    way Flyweight is meant to
#    be used — extrinsic state
#    supplied by the caller,
#    not stored on the shared
#    object.
#
# 2. Store temperature on
#    Espresso itself
#    (per-instance, not shared)
#    and have Espresso.cost()
#    ask the flyweight for
#    base_cost, then apply the
#    temperature adjustment
#    locally.
#
# 3. If iced/hot pricing is
#    expected to grow more
#    complex over time, model
#    it as its own decorator
#    (e.g. IcedSurcharge) so it
#    composes the same way
#    Mocha and Whip do,
#    instead of living inside
#    Espresso or the flyweight
#    at all.

# ============================================================
# WATCHING THE BUG HAPPEN
# ============================================================

# The diagnosis describes two
# orders in a row.
#
# Here they are.

print("\nThe Bug, Live")

hot_order = BuggyEspresso(temperature="hot")
print(hot_order.cost())

iced_order = BuggyEspresso(temperature="iced")
print(iced_order.cost())

print(hot_order.cost())

# Observation:
#
# The hot order was 40.0.
#
# Then an iced order arrived.
#
# And the hot order became
# 50.0.
#
# Nobody touched it.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Notice what the AI did here.
#
# It didn't just say "this is
# wrong."
#
# What did it actually give
# us?

# ============================================================
# THE ANSWER
# ============================================================

# A diagnosis of WHY it's a
# problem.
#
# Mixing intrinsic and
# extrinsic state breaks
# sharing.
#
# And it doesn't fit how the
# Decorator layer already
# handles per-order
# differences.
#
# Plus more than one option.
#
# Not just one forced answer.

# ============================================================
# STEP 3 OF 4 : DISCUSS, THEN FIX BY HAND
# ============================================================

# Of the three options the AI
# gave, which one actually
# fits what we're doing?
#
# And why?
#
# Think before reading on.

# ============================================================
# THE CHOICE
# ============================================================

# Option 1.
#
# Pass temperature in as an
# argument, instead of storing
# it on the shared flyweight.
#
# It's the smallest change.
#
# It doesn't touch the
# Decorator classes at all.
#
# And it puts extrinsic state
# exactly where Flyweight says
# it belongs.
#
# With the caller.
#
# Not the shared object.
#
# Option 3 is worth
# remembering for later, if
# pricing rules keep growing.
#
# But it's more than we need
# today.
#
# Now that the class has
# decided, the fix gets
# written by hand.
#
# The AI didn't write this
# code.
#
# We did, after the
# discussion.

# ============================================================
# THE FIX
# ============================================================


class BeanFlyweight:
    # Only intrinsic state here — shared, unchanging, safe to reuse.

    def __init__(self, origin, base_cost):
        self.origin = origin
        self.base_cost = base_cost

    def get_cost(self, temperature):
        # temperature is extrinsic — supplied by the caller each time,
        # never stored on the shared object.
        cost = self.base_cost
        if temperature == "iced":
            cost += 10.0
        return cost


class BeanFlyweightFactory:
    _beans = {}

    @staticmethod
    def get_bean(origin, base_cost):
        if origin not in BeanFlyweightFactory._beans:
            BeanFlyweightFactory._beans[origin] = BeanFlyweight(origin, base_cost)
        return BeanFlyweightFactory._beans[origin]


class Espresso(Beverage):

    def __init__(self, temperature):
        self.bean = BeanFlyweightFactory.get_bean("Arabica", 40.0)
        self.temperature = temperature   # lives on the order, not the shared bean

    def cost(self):
        return self.bean.get_cost(self.temperature)

    def get_description(self):
        return "Espresso"


# ============================================================
# THE DECORATORS ARE UNTOUCHED
# ============================================================

# Mocha and Whip still wrap
# Espresso exactly as before.
#
# Nothing about this fix
# touched the decorator layer.

print("\nStep 3 : The Fix")

order = Espresso(temperature="iced")
order = Mocha(order)
order = Whip(order)

print(order.get_description())
print(order.cost())

# ============================================================
# AND THE BUG IS GONE
# ============================================================

print("\nTwo Orders Again")

hot_order = Espresso(temperature="hot")
print(hot_order.cost())

iced_order = Espresso(temperature="iced")
print(iced_order.cost())

print(hot_order.cost())

# Observation:
#
# The hot order stayed 40.0.
#
# Same shared bean.
#
# Different answers.

# ============================================================
# STEP 4 OF 4 : WHAT THE AI WAS USEFUL FOR
# ============================================================

# Think back over the whole
# exercise.
#
# What did the AI actually
# contribute?
#
# And what did it not do?

# ============================================================
# THE ANSWER
# ============================================================

# It didn't write any of the
# code we shipped.
#
# It reviewed code we wrote.
#
# It explained why storing
# per-order state on a shared
# flyweight silently corrupts
# other orders.
#
# And it laid out real options
# with a trade-off for each.
#
# Instead of silently "fixing"
# it its own way.
#
# The actual decision and the
# actual fix were still ours.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Used as a generator:
#
#     AI writes code, you hope
#     it kept the design.
#
# Used as a reviewer:
#
#     AI explains what's wrong
#     and why, gives you
#     options, YOU decide, YOU
#     write the fix.
#
# If a Flyweight has a field
# that changes per caller,
# it's not a Flyweight
# anymore — it's a shared
# object quietly leaking state
# between orders.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the difference
# between intrinsic state —
# safe to share —
#
# and extrinsic state — must
# be passed in, never stored
# on the flyweight?

# ============================================================
# WRAP-UP : DECORATOR
# ============================================================

# Adds behaviour to an object
# while the program is
# running, by wrapping it.
#
# The base class never changes
# when new wrappers are added.
#
# Built from:
#
#     a shared interface
#     + a base class
#     + one class per add-on
#
# Textbook example:
#
#     Beverage / Espresso /
#     Mocha (coffee shop)
#
# Real examples:
#
#     Python's io module
#     (FileIO -> BufferedReader
#     -> TextIOWrapper),
#
#     CSS layering,
#
#     Python's own @decorator
#     syntax,
#
#     and logging / retry /
#     rate-limit decorators
#     wrapped around a service

# ============================================================
# WRAP-UP : FLYWEIGHT
# ============================================================

# Handles huge numbers of
# near-identical objects
# cheaply.
#
# Split into:
#
#     INTRINSIC
#     (shared, reused)
#
#     EXTRINSIC
#     (unique per object)
#
# A factory/cache hands back
# shared intrinsic objects
# instead of rebuilding them.
#
# Real examples:
#
#     CPython's small-integer
#     caching and string
#     interning,
#
#     shared read-only
#     reference data (like
#     Category) behind a
#     factory cache

# ============================================================
# THE TWO QUESTIONS
# ============================================================

# You've probably already used
# both patterns without
# knowing their names.
#
# Every time you've opened a
# file, or written
# @staticmethod, you've
# touched Decorator.
#
# Decorator answers:
#
#     "How do I keep adding
#      behaviour without
#      editing the original
#      class?"
#
# Flyweight answers:
#
#     "How do I stop paying
#      memory for the same data
#      over and over?"

# ============================================================
# HOMEWORK
# ============================================================

# 1. Add a "Soy" decorator to
#    the coffee shop example,
#    and build an order with
#    all four layers:
#    Espresso + Mocha + Whip +
#    Soy. Print the final
#    description and cost.
#
# 2. Add a
#    CachingNotificationDecorator
#    to the example in file 04
#    — it should skip calling
#    wrapped.send() if the
#    exact same message was
#    already sent to that
#    user_id in the last
#    minute.
#
# 3. Extend BulletTypeFactory
#    (file 05) so it prints a
#    log line only the FIRST
#    time a new gun's
#    BulletType is created —
#    prove to yourself that
#    firing 1,000 bullets from
#    the same gun only logs
#    once.
#
# 4. Find one real Decorator
#    and one real Flyweight in
#    any codebase or library
#    you've used (check
#    Python's io module, a
#    caching layer, or a
#    connection pool). Write
#    two lines identifying
#    what's being wrapped, or
#    what's intrinsic vs
#    extrinsic.
#
# 5. Push all your code to
#    GitHub, on a branch named:
#
#        decorator-flyweight-lecture-complete

# ============================================================
# BRIDGE TO THE NEXT CLASS
# ============================================================

# Today's problem was either:
#
#     "keep adding behaviour
#      without touching the
#      base"
#
#     (Decorator)
#
# or:
#
#     "stop repeating the same
#      heavy data across
#      thousands of objects"
#
#     (Flyweight)
#
# Next class, we move to
# Behavioral patterns.
#
# How objects actually talk to
# and coordinate with each
# other.
#
# Starting with Strategy and
# Observer.
