"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 09_summary_and_homework.py
============================================================

Lecture Summary
---------------
1. Dunders As Protocols
2. Representation Methods
3. Comparison And Hashing
4. Context Managers
5. Callable Objects
6. Container Protocols
7. Homework
8. Interview Revision
"""

# ============================================================
# MOTIVATION
# ============================================================

# This file serves as a revision
# of the entire lecture.
#
# The objective is not to introduce
# new concepts.
#
# The objective is to connect all
# the ideas we have studied so far.
#
# By the end of the lecture we should
# be able to explain:
#
# Why len() works.
#
# Why == works.
#
# Why with works.
#
# Why () works.
#
# Why custom collections behave like
# native Python collections.

# ============================================================
# BIG IDEA OF THE ENTIRE LECTURE
# ============================================================

# Earlier lectures focused on:
#
# Classes
# Objects
# Inheritance
# Abstract Base Classes
# Protocols
# Mixins
#
# This lecture focused on a different
# question:
#
# How does an object become a
# first-class citizen of Python?
#
# The answer:
#
# Dunder Methods.
#
# More specifically:
#
# Protocols.

# ============================================================
# DUNDERS AS PROTOCOLS
# ============================================================

# The biggest mental model from
# this lecture:
#
# You do not call dunder methods.
#
# Python calls them for you.
#
# Ordinary syntax triggers them.

# ============================================================
# COMMON TRANSLATIONS
# ============================================================

# len(x)
# -> x.__len__()
#
# x + y
# -> x.__add__(y)
#
# x == y
# -> x.__eq__(y)
#
# x < y
# -> x.__lt__(y)
#
# x[0]
# -> x.__getitem__(0)
#
# x[0] = value
# -> x.__setitem__(0, value)
#
# print(x)
# -> str(x)
# -> x.__str__()
#
# x()
# -> x.__call__()
#
# with x:
# -> x.__enter__()
# -> x.__exit__()

# ============================================================
# REPRESENTATION METHODS
# ============================================================

# Representation controls how
# objects appear when printed.

# ============================================================
# __str__
# ============================================================

# Human-friendly representation.
#
# Used by:
#
# print(obj)
#
# str(obj)

# ============================================================
# __repr__
# ============================================================

# Developer-friendly representation.
#
# Commonly used by:
#
# REPL
# Containers
# Debugging tools

# ============================================================
# __format__
# ============================================================

# Supports:
#
# f"{obj:spec}"
#
# Custom formatting behaviour.

# ============================================================
# COMPARISON AND HASHING
# ============================================================

# This was the most important
# section of the lecture.

# ============================================================
# THE ZONE MYSTERY
# ============================================================

# We added:
#
# __eq__
#
# Equality worked.
#
# Then:
#
# set()
#
# stopped working.

# ============================================================
# THE ANSWER
# ============================================================

# Python protects the
# equality/hash contract.

# ============================================================
# THE CONTRACT
# ============================================================

# If:
#
# a == b
#
# Then:
#
# hash(a) == hash(b)
#
# Must be True.

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# Reverse is not required.
#
# Different objects may still
# share the same hash.
#
# This is called a collision.

# ============================================================
# WHY PYTHON DISABLES HASHING
# ============================================================

# If __eq__ exists but __hash__
# does not,
#
# Python cannot guarantee
# the contract.
#
# Therefore:
#
# __hash__ becomes None.
#
# The object becomes unhashable.

# ============================================================
# IMMUTABILITY RULE
# ============================================================

# Objects used inside:
#
# set
# dict
#
# should generally be immutable.
#
# Fields participating in:
#
# __eq__
# __hash__
#
# should not change.

# ============================================================
# CONTEXT MANAGERS
# ============================================================

# Context Managers solve
# resource-management problems.

# ============================================================
# RESOURCE LIFECYCLE
# ============================================================

# Acquire Resource
#
# Use Resource
#
# Release Resource

# ============================================================
# THE PROTOCOL
# ============================================================

# __enter__
#
# Acquire / setup.
#
#
# __exit__
#
# Cleanup / teardown.

# ============================================================
# IMPORTANT BEHAVIOUR
# ============================================================

# Cleanup happens even if
# exceptions occur.

# ============================================================
# EXCEPTION SUPPRESSION
# ============================================================

# Returning True from __exit__
# suppresses the exception.
#
# Use carefully.

# ============================================================
# CALLABLE OBJECTS
# ============================================================

# Objects can behave like
# functions.

# ============================================================
# THE PROTOCOL
# ============================================================

# __call__

# ============================================================
# TRANSLATION
# ============================================================

# obj()
#
# becomes:
#
# obj.__call__()

# ============================================================
# WHY USE CALLABLE OBJECTS?
# ============================================================

# They combine:
#
# Behaviour
# State
#
# inside one object.

# ============================================================
# CONTAINER PROTOCOLS
# ============================================================

# The Deck lab demonstrated
# how custom objects can
# behave like collections.

# ============================================================
# __len__
# ============================================================

# Enables:
#
# len(deck)

# ============================================================
# __getitem__
# ============================================================

# Enables:
#
# deck[index]

# ============================================================
# __setitem__
# ============================================================

# Enables:
#
# deck[index] = value

# ============================================================
# __contains__
# ============================================================

# Enables:
#
# value in deck

# ============================================================
# __iter__
# ============================================================

# Enables:
#
# for item in deck

# ============================================================
# SHUFFLING PAYOFF
# ============================================================

# random.shuffle()
#
# never learned what a Deck is.
#
# It works because the Deck
# speaks the mutable sequence
# protocol.

# ============================================================
# THE LARGER LESSON
# ============================================================

# Python APIs rarely care about
# concrete classes.
#
# They care about protocols.
#
# If an object speaks the protocol,
# the API works.

# ============================================================
# INTERVIEW REVISION #1
# ============================================================

# What is a dunder method?
#
# A special method surrounded
# by double underscores that
# Python calls automatically.

# ============================================================
# INTERVIEW REVISION #2
# ============================================================

# Why can defining __eq__
# make an object unhashable?
#
# Python protects the
# equality/hash contract.

# ============================================================
# INTERVIEW REVISION #3
# ============================================================

# What makes an object callable?
#
# __call__

# ============================================================
# INTERVIEW REVISION #4
# ============================================================

# Which methods are required
# for the with statement?
#
# __enter__
# __exit__

# ============================================================
# INTERVIEW REVISION #5
# ============================================================

# Which methods allow a custom
# object to behave like a sequence?
#
# __len__
# __getitem__
# __setitem__

# ============================================================
# HOMEWORK 1
# ============================================================

# Deck.__add__
#
# Combine two decks.
#
# Reuse ideas from:
#
# Fare.__add__

# ============================================================
# HOMEWORK 2
# ============================================================

# Create a Hand class.
#
# A Hand contains cards
# drawn from a deck.

# ============================================================
# HOMEWORK 3
# ============================================================

# Hashability Audit
#
# Choose two previously built
# classes.
#
# Examples:
#
# Driver
# Zone
# PaymentGateway
#
# Determine:
#
# Should it be hashable?
#
# Why or why not?

# ============================================================
# HOMEWORK 4
# ============================================================

# DispatchSession Context Manager
#
# __enter__
#
# Start a timer.
#
# __exit__
#
# Print how many trips
# were matched.

# ============================================================
# HOMEWORK 5
# ============================================================

# Push solutions to GitHub.
#
# Branch:
#
# lecture-6-complete

# ============================================================
# FINAL RECAP
# ============================================================

# Dunders As Protocols
#
# Representation
#
# Comparison
#
# Hashing
#
# Context Managers
#
# Callable Objects
#
# Container Protocols

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Python is heavily protocol driven.
#
# Dunder methods allow custom
# objects to participate in
# native Python syntax.
#
# The Python Data Model is a
# collection of these protocols.
#
# If an object implements the
# expected protocol, Python APIs
# work automatically.
#
# This idea appears throughout
# professional Python codebases.

# ============================================================
# BRIDGE TO THE NEXT CLASS
# ============================================================

# Next Class:
#
# OOP Lab Session
#
# No major new theory.
#
# Instead we combine concepts
# from OOP-1 through OOP-5 into
# larger design exercises.
