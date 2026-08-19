"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 01_strategy_intro_and_maps_problem.py
============================================================

Topics Covered
--------------
1.  Recap Of Decorator And Flyweight
2.  A New Bucket : Behavioural
3.  Four Patterns, Four Questions
4.  Today's Roadmap
5.  Paying At A Shop
6.  Getting To The Airport
7.  Strategy : The General Idea
8.  Google Maps And Three Modes
9.  How Most People First Write It
10. The Two Principles It Breaks
11. One Class Per Mode
12. Where The mode Parameter Goes
13. Key Takeaways
"""

# ============================================================
# RECAP OF LAST CLASS
# ============================================================

# We covered Decorator and
# Flyweight.
#
# Both were Structural
# patterns.
#
# Decorator
#
#     add new behaviour to an
#     object while the program
#     is running, without
#     touching its class
#
# Flyweight
#
#     handle a huge number of
#     near-identical objects
#     cheaply, by sharing the
#     heavy, unchanging part

# ============================================================
# A NEW BUCKET
# ============================================================

# Today we're moving into a
# new bucket of patterns.
#
# Behavioural.
#
# Just going by the name —
#
# what kind of problem do you
# think a Behavioural pattern
# solves?
#
# Compared to something like
#
#     "how do I build this
#      object"
#
# or
#
#     "how do two things fit
#      together"
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# How objects behave and
# interact at runtime.
#
# How they make decisions.
#
# How they talk to each other.
#
# Or how they share the work
# of getting something done.

# ============================================================
# A LIVE EXAMPLE
# ============================================================

# Google Maps shows a
# different route depending on
# whether you're driving,
# walking, or cycling.
#
# If one single method had to
# handle all three modes,
#
# what do you think goes
# wrong?
#
# Think before reading on.

# ============================================================
# WHAT GOES WRONG
# ============================================================

# That method turns into a
# giant if-elif block.
#
# And every time a new mode
# gets added,
#
# you're stuck editing code
# that already works fine.
#
# That's exactly the problem
# Strategy fixes.
#
# Our first pattern today.

# ============================================================
# BOARD SUMMARY
# ============================================================

# DECORATOR
#
#     add new behaviour to an
#     object while it's
#     running, without
#     touching its class
#
# FLYWEIGHT
#
#     handle a huge number of
#     near-identical objects
#     without wasting memory
#
# STRATEGY
#
#     pick ONE way of doing
#     something, out of several
#     options
#
# OBSERVER
#
#     notify MANY interested
#     parties automatically
#     when something happens
#
# Today:
#
#     Strategy
#
#     Observer


# ============================================================
# WARM UP : PAYING AT A SHOP
# ============================================================

# Think about paying at a
# shop.
#
# Card.
#
# UPI.
#
# Or cash.
#
# Does "paying" actually work
# the same way underneath, no
# matter which one you pick?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# Card talks to a card
# network.
#
# UPI talks to a totally
# different provider.
#
# Cash needs no network call
# at all.
#
# The word "paid" is the same.
#
# But what actually happens is
# completely different,
# depending on which method
# you chose.

# ============================================================
# GETTING TO THE AIRPORT
# ============================================================

# One more example.
#
# Nothing to do with software.
#
# You're going from home to
# the airport.
#
# You could take an auto.
#
# A cab.
#
# Or the metro.
#
# Is "getting to the airport"
# the same set of steps for
# all three ?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# Each one has its own booking
# step.
#
# Its own route.
#
# Its own way of tracking
# where you are.
#
# But all three are just
# different answers to the
# same question:
#
#     "how do I get to the
#      airport?"

# ============================================================
# THE SHAPE WE CARE ABOUT
# ============================================================

# One task.
#
# Several genuinely different
# ways to do it.
#
# And at any given moment, you
# pick exactly one of them.

# ============================================================
# WHY GOOGLE MAPS
# ============================================================

# We're going to build this
# out properly using Google
# Maps.
#
# It's the version you'll
# actually see in interviews.
#
# And in real code.

# ============================================================
# BOARD SUMMARY
# ============================================================

# STRATEGY (the general idea)
#
#     One task. Several
#     different ways to do it.
#
#     At any point, exactly ONE
#     way gets picked and used —
#
#     and it's the caller who
#     decides which one, not
#     the code itself.
#
#     Adding a new way
#     shouldn't mean editing
#     the old ways.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the general idea?
#
# Now the real problem.

# ============================================================
# THE PROBLEM : GOOGLE MAPS
# ============================================================

# Picture Google Maps.
#
# You search a route from A to
# B.
#
# And switch between driving,
# walking, and cycling.
#
# Do you get the same path
# every time?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# Walking can cut through a
# park, or use a footpath a
# car simply can't take.
#
# Driving has to respect
# one-way streets.
#
# Cycling prefers routes with
# bike lanes.
#
# Each mode genuinely needs
# its own logic to figure out
# the best path.

# ============================================================
# HOW MOST PEOPLE FIRST WRITE IT
# ============================================================

# find_path(source,
#           destination,
#           mode)
#
# What do you think that looks
# like?


class GoogleMaps:

    def find_path(self, source, destination, mode):
        if mode == "car":
            print("  car-specific pathfinding")
        elif mode == "bike":
            print("  bike-specific pathfinding")
        elif mode == "walk":
            print("  walk-specific pathfinding")
        return None


print("One Method, Three Modes")

maps = GoogleMaps()

for mode in ["car", "bike", "walk"]:
    maps.find_path("Jaipur", "Delhi", mode)

# Observation:
#
# Three modes.
#
# One method.
#
# All three branches living in
# the same place.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# We've run into this exact
# shape before in this course.
#
# Which TWO design principles
# does this break?
#
# Name both before reading on.

# ============================================================
# THE TWO PRINCIPLES
# ============================================================

# Open-Closed Principle
#
#     If Google adds a new mode
#     tomorrow, like public
#     transit, someone has to
#     go back and edit this
#     method again.
#
# Single Responsibility
# Principle
#
#     This one method is now
#     responsible for every
#     mode's entire
#     path-finding logic.
#
#     All crammed into the same
#     place.

# ============================================================
# THE FIX
# ============================================================

# Stop treating "find a path"
# as one method with a bunch
# of branches inside it.
#
# Instead, give each mode its
# own class.
#
# And make all of them follow
# the same shared interface.

# ============================================================
# BOARD SUMMARY
# ============================================================

# PROBLEM
#
# one method, if-elif per mode
#
#     Adding a new mode means
#     editing code that already
#     works
#
#     One method carries the
#     entire logic for every
#     mode at once
#
# FIX
#
# one shared interface, one
# class per mode
#
#     Each class only knows its
#     own way of finding a
#     path.

# ============================================================
# WE HAVE MADE THIS MOVE BEFORE
# ============================================================

# Every bank spoke the same
# interface in the Adapter
# lecture.
#
# Every add-on implemented the
# same Beverage interface in
# the Decorator lecture.
#
# What's happening here that's
# similar?
#
# Think before reading on.

# ============================================================
# THE SAME MOVE
# ============================================================

# We define one shared
# interface with a find_path()
# method.
#
# Every mode gets its own
# class implementing that
# interface.
#
# And notice —
#
# mode disappears as a
# parameter.
#
# Because a CarPathCalculator
# already IS the car way of
# doing things.
#
# It doesn't need to be told
# what mode it is.

# ============================================================
# CHECKPOINT
# ============================================================

# Two things should be solid
# before moving on.
#
# One.
#
# What Strategy is for.
#
#     one task,
#
#     several ways,
#
#     exactly one picked,
#
#     by the caller.
#
# Two.
#
# Why one method with an
# if-elif per mode breaks both
# Open-Closed and Single
# Responsibility.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Behavioural patterns are
# about how objects behave and
# interact at runtime.
#
# Not how they're built, or
# how they fit together.
#
# Paying by card, UPI or cash
# is one task with genuinely
# different implementations.
#
# So is getting to the airport
# by auto, cab or metro.
#
# Strategy means exactly one
# of those ways gets picked,
# and the caller decides which.
#
# One find_path() with an
# if-elif per mode breaks
# Open-Closed and Single
# Responsibility at once.
#
# The fix is one shared
# interface and one class per
# mode.
#
# A class that IS the car way
# never needs to be told it's
# the car way.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We know what we want now.
#
# One interface.
#
# One class per mode.
#
# But one question is still
# open.
#
# The caller still has to say
# which mode they want.
#
# So who turns "car" into a
# CarPathCalculator —
#
# without bringing back the
# if-elif we just removed?
#
# Next:
#
# 02_strategy_implementation.py
