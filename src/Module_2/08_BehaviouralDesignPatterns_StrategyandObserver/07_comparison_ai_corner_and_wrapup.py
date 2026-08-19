"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 07_comparison_ai_corner_and_wrapup.py
============================================================

Topics Covered
--------------
1.  Recap Setup From Earlier Files
2.  Strategy vs Observer
3.  Quick Round : Which Is Which
4.  When Neither One Fits
5.  AI Corner : The Goal
6.  Step 1 — The Code With The Mistake
7.  Step 2 — Asking AI To Diagnose
8.  Step 3 — Choosing An Option, Writing The Fix
9.  Step 4 — What The AI Was Useful For
10. Wrap-Up : Strategy
11. Wrap-Up : Observer
12. Homework
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


class Path:

    def __init__(self):
        self.eta = 30

    def add_delay(self, minutes):
        self.eta += minutes

    def __repr__(self):
        return f"Path(eta={self.eta} min)"


def is_rush_hour():
    return True


class PathCalculator(ABC):

    @abstractmethod
    def find_path(self, source, destination):
        ...


class CarPathCalculator(PathCalculator):

    def find_path(self, source, destination):
        return Path()


class BikePathCalculator(PathCalculator):

    def find_path(self, source, destination):
        return Path()


class WalkPathCalculator(PathCalculator):

    def find_path(self, source, destination):
        return Path()


class PathCalculatorFactory:
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


class GoogleMaps:

    def find_path(self, source, destination, mode):
        pc = PathCalculatorFactory.get_pc(mode)
        return pc.find_path(source, destination)


# ============================================================
# TELLING THEM APART
# ============================================================

# Both patterns are built
# around one interface with
# multiple classes
# implementing it.
#
# If you had to explain the
# difference to a junior
# engineer in ONE sentence
# each —
#
# what would you say?
#
# Try it before reading on.

# ============================================================
# BOARD SUMMARY
# ============================================================

# STRATEGY
#
#     "Pick exactly ONE way to
#      do something, and the
#      caller decides which
#      one."
#
#     (car, bike, or walk —
#      you choose one)
#
# OBSERVER
#
#     "Announce that something
#      happened, and let
#      EVERYONE who's
#      interested react."
#
#     (order placed ->
#      invoicing, inventory,
#      email, fraud check —
#      ALL of them react, every
#      single time)

# ============================================================
# QUICK ROUND
# ============================================================

# Is model routing from the
# backend Strategy file closer
# to Strategy or Observer?
#
# What about token streaming
# from the backend Observer
# file?
#
# Answer:
#
# Model routing is Strategy.
#
# Exactly one model tier gets
# picked per query.
#
# Token streaming is Observer.
#
# Every observer reacts to
# every single token.

# ============================================================
# ONE MORE, RIGHT NOW
# ============================================================

# A payment system tries
# Razorpay first.
#
# And only falls back to
# Stripe if Razorpay fails.
#
# Is that Strategy or
# Observer?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# Neither one really fits.
#
# This is closer to a
# different pattern called
# Chain of Responsibility.
#
# Try one option, and only
# move to the next if it
# fails.
#
# It's not "pick one and stick
# with it" like Strategy.
#
# And it's not "notify
# everyone" like Observer.

# ============================================================
# A GOOD HABIT
# ============================================================

# Worth building for the rest
# of this course.
#
# Not everything you see will
# map perfectly onto a pattern
# you already know.
#
# Being able to say
#
#     "this is close to X, but
#      not quite"
#
# is more useful than forcing
# a label onto something that
# doesn't fit.

# ============================================================
# CHECKPOINT
# ============================================================

# Strategy vs Observer,
# locked in?
#
# Pick one.
#
# Versus tell everyone.

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
# STEP 1 OF 4 : THE CODE WITH THE MISTAKE
# ============================================================

# We're adding a feature by
# hand.
#
# No AI yet.
#
# We need a "traffic delay":
#
#     if the mode is car and
#     it's currently rush hour,
#     add 20 minutes to the
#     ETA.


class BuggyGoogleMaps:

    def find_path(self, source, destination, mode):
        pc = PathCalculatorFactory.get_pc(mode)
        path = pc.find_path(source, destination)

        if mode == "car" and is_rush_hour():
            path.add_delay(20)
        return path


print("Step 1 : The Traffic Delay")

buggy = BuggyGoogleMaps()
print(buggy.find_path("Jaipur", "Delhi", "car"))
print(buggy.find_path("Jaipur", "Delhi", "bike"))

# Observation:
#
# It works.
#
# Car gets the delay. Bike
# doesn't.
#
# This is the kind of thing
# any of us might type in five
# minutes without thinking
# twice.
#
# It's quick, it runs, and it
# passes the obvious test.
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

# Instead of guessing, do what
# we'd actually do at work.
#
# Paste it into an AI
# assistant and ask it to
# review it.
#
# The prompt used:
#
#     "Here's some code from
#      our ride ETA system. We
#      use the Strategy pattern
#      — a PathCalculator
#      interface with
#      CarPathCalculator,
#      BikePathCalculator,
#      WalkPathCalculator. Can
#      you review this method
#      and tell me if anything
#      is wrong with it, and
#      what the possible fixes
#      are? Don't rewrite it
#      yet — just diagnose
#      first."
#
# followed by the code from
# Step 1.

# ============================================================
# THE AI RESPONSE : DIAGNOSIS
# ============================================================

# Functionally this works —
# car rides during rush hour
# get delayed by 20 minutes,
# and nothing else changes.
# But there's a design issue:
# you're using the Strategy
# pattern specifically so
# GoogleMaps never has to know
# mode-specific details. This
# method now checks
# mode == "car" directly,
# which reintroduces the same
# coupling the pattern was
# meant to remove. If you add
# a bike-specific rule next,
# you'll likely add another
# condition here, and
# GoogleMaps slowly turns back
# into an if-elif chain.
#
# Possible fixes:
#
# 1. Move the rush-hour check
#    into
#    CarPathCalculator.find_path(),
#    so only the car strategy
#    knows rush hour exists.
#    GoogleMaps stays
#    untouched.
#
# 2. Introduce a decorator or
#    wrapper around
#    PathCalculator for
#    time-based adjustments, if
#    you expect many such rules
#    later.
#
# 3. If this really is a
#    one-off exception with no
#    plans to extend it, leave
#    it here and accept the
#    coupling — but that should
#    be a deliberate call, not
#    a default.
#
# Option 1 fits your existing
# pattern with the least
# change and no new
# abstractions, so it's the
# natural fit unless you
# expect several more
# time-based or
# condition-based rules soon.

# ============================================================
# ANIMATION
# ============================================================

# Strategy Pattern Regression
# in Code
#
# Link:
#
# https://acad-backend-vizs.vercel.app/instructor-notes-behavioural-design-patterns-strategy-and-observer/strategy-pattern-regression-in-code/
#
# What this animation shows:
#
# A split view: a code panel
# (left) showing "Before
# (Clean Strategy)" and "After
# (Regression)" side by side,
# and a dependency diagram
# (right) with boxes for
# GoogleMaps, StrategyFactory,
# PathCalculator, and
# CarPathCalculator.
#
# Step-through buttons advance
# the regression story: first,
# the clean
# factory.create(mode) line
# highlights green, and a
# green "delegates" arrow
# connects GoogleMaps to the
# Factory.
#
# Then the inline
# if mode == "car" block
# slides into the "After" code
# with a red highlight and
# pulsing red border — a
# dashed red "hard
# dependency!" arrow appears
# connecting GoogleMaps
# directly to
# CarPathCalculator.
#
# A red "bypassed" marker
# appears on the clean
# delegation arrow, showing
# the factory line is now
# skipped for car mode.
#
# The final summary step
# highlights both the
# regression lines (red) and
# the original clean line
# (green) simultaneously,
# making the contrast stark.
#
# What students learn from it:
#
# The visual before/after with
# the dependency arrows makes
# the regression tangible —
# you can literally see the
# hard coupling appear as a
# red dashed line.
#
# The pulsing red border on
# the inline check draws
# attention to exactly where
# the pattern breaks.
#
# Seeing the "bypassed" marker
# on the factory arrow cements
# that the Strategy Pattern is
# PARTIALLY broken — the
# factory still exists but is
# no longer always used.
#
# Step through to Step 3 where
# the red "hard dependency!"
# arrow appears, and pause —
# ask:
#
#     "If a second developer
#      adds a bike-specific
#      rule the same way, what
#      does the diagram look
#      like now?"

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
# Tied back to the reason we
# chose Strategy in the first
# place.
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
# Move the check into
# CarPathCalculator.
#
# We don't have a stated need
# for a decorator yet.
#
# Option 2 is over-engineering
# for now.
#
# And silently accepting the
# coupling — option 3 — undoes
# the whole point of the
# Google Maps section.
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


class RushHourAwareCarPathCalculator(PathCalculator):

    def find_path(self, source, destination):
        path = self._compute_car_path(source, destination)
        if is_rush_hour():
            path.add_delay(20)
        return path

    def _compute_car_path(self, source, destination):
        return Path()


# only the strategy registered for "car" changes.
# GoogleMaps and the factory itself are untouched.
PathCalculatorFactory._calculators["car"] = RushHourAwareCarPathCalculator()

print("\nStep 3 : The Fix")

maps = GoogleMaps()
print(maps.find_path("Jaipur", "Delhi", "car"))
print(maps.find_path("Jaipur", "Delhi", "bike"))

# ============================================================
# GOOGLEMAPS NEVER CHANGED
# ============================================================

# Same ETAs as the buggy
# version.
#
# But scroll up and read
# GoogleMaps again.
#
#     def find_path(self, source,
#                   destination, mode):
#         pc = PathCalculatorFactory.get_pc(mode)
#         return pc.find_path(source, destination)
#
# No mode check.
#
# Nothing about cars.
#
# Nothing about rush hour.

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
# It explained WHY it was a
# problem, by connecting it
# back to a design decision.
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
# The second habit catches
# problems the first one
# hides.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the difference
# between asking AI to write
# code,
#
# versus asking AI to review
# code you already wrote?

# ============================================================
# WRAP-UP : STRATEGY
# ============================================================

# Picks exactly ONE way, out
# of several options, to do a
# task.
#
# Built from:
#
#     an interface
#
#     + one class per way of
#       doing it
#
#     + a Singleton-style
#       Factory to hand out the
#       right one
#
# Textbook example:
#
#     PathCalculator / Car /
#     Bike / Walk (Google Maps)
#
# Real example:
#
#     routing an AI query to a
#     cheap vs. expensive model

# ============================================================
# WRAP-UP : OBSERVER
# ============================================================

# Notifies MANY interested
# parties automatically when
# something happens.
#
# Built from:
#
#     a subscriber interface
#
#     + a register/unregister
#       list
#
#     + a loop that notifies
#       everyone
#
# Textbook example:
#
#     OrderPlacedSubscriber /
#     InvoiceGenerator /
#     WarehouseInventory /
#     FraudCheck
#
# Real example:
#
#     token-streaming callbacks
#     and webhook-style events

# ============================================================
# THE TWO QUESTIONS
# ============================================================

# You've likely already used
# both patterns without
# knowing their names.
#
# Every time an SDK gave you
# an on_message callback, that
# was Observer.
#
# Every time you passed in
# "which mode/tier/strategy to
# use", that was Strategy.
#
# Strategy answers:
#
#     "How do I let the caller
#      pick from several ways
#      of doing something,
#      without a wall of
#      if-elif?"
#
# Observer answers:
#
#     "How do I let many
#      unrelated things react to
#      one event, without
#      hardcoding all of them
#      into the same place?"

# ============================================================
# HOMEWORK
# ============================================================

# 1. Implement RainWaterTrapping
#    as a Strategy: brute force
#    O(n^2) time / O(1) space,
#    an optimal O(n) time /
#    O(n) space version, and a
#    most-optimal O(n) time /
#    O(1) space version — each
#    in its own class, picked
#    by a factory based on
#    requested complexity.
#
#        class RainWaterStrategy(ABC):
#            @abstractmethod
#            def solve(self, height):
#                ...
#
#        class RainWaterTrappingFactory:
#            @staticmethod
#            def get(time_complexity, space_complexity):
#                ...
#
# 2. Build the token-streaming
#    Observer example from file
#    06. Add one new observer
#    type without touching the
#    token-generating code at
#    all.
#
# 3. Spend 10 minutes
#    researching Chain of
#    Responsibility. Write two
#    lines on how it's
#    different from both
#    Strategy and Observer.
#
# 4. Find one real Strategy and
#    one real Observer in a
#    codebase or library you've
#    used before. (Passing a
#    custom key function into
#    sorted()/min()/max() is a
#    Strategy — you're handing
#    in "my own way of comparing
#    things" instead of writing
#    if-elif. Any SDK with an
#    on_message-style callback
#    is an Observer.)
#
# 5. Push your code to GitHub,
#    on a branch named:
#
#        behavioural-patterns-lecture-complete

# ============================================================
# BRIDGE TO THE NEXT CLASS
# ============================================================

# Next class:
#
# UML Diagrams.
#
# The standard notation for
# communicating any of these
# designs to another engineer.
#
# Without writing a single
# line of code.
