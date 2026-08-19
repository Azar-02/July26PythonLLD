"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 03_strategy_in_a_real_backend.py
============================================================

Topics Covered
--------------
1.  Where File 02 Left Us
2.  The Stage : A Cost-Effective AI Backend
3.  Two Users, Two Very Different Questions
4.  What A Model Router Does
5.  The Trap Of if-elif Routing
6.  Why It Breaks Down
7.  The Dict-Based Router Factory
8.  Model Routing And RAG In Practice
9.  Factory vs Strategy
10. Adapter vs Strategy
11. The Restaurant Analogy
12. Rapid-Fire Scenarios
13. Key Takeaways
"""

from abc import ABC, abstractmethod
from enum import Enum

# ============================================================
# WHERE FILE 02 LEFT US
# ============================================================

# An interface.
#
# One class per way of doing
# the task.
#
# A factory handing out shared
# instances.
#
# That was routes on a map.
#
# Now the same structure, on a
# problem that decides where
# your money goes.

# ============================================================
# THE STAGE
# ============================================================

# Imagine you are scaling an
# AI-powered customer support
# platform.
#
# Thousands of users are
# sending queries every
# minute.

# ============================================================
# TWO USERS
# ============================================================

# User A asks:
#
#     "How do I reset my
#      password?"
#
# Simple. Repetitive.
#
# User B asks:
#
#     "Can you analyze this
#      multi-threaded deadlock
#      stack trace and refactor
#      the synchronization
#      logic?"
#
# Complex. Requires deep
# reasoning.

# ============================================================
# WHY ONE MODEL FOR EVERYTHING FAILS
# ============================================================

# Sending every single request
# to a massive,
# state-of-the-art LLM will
# bankrupt your startup.
#
# Through high API costs.
#
# And slow response times for
# easy questions.
#
# Conversely, sending complex
# logic to a cheap,
# lightweight model results in
# broken code.
#
# Both directions cost you
# something.

# ============================================================
# WHAT WE NEED
# ============================================================

# A Model Router.
#
# A component that classifies
# the incoming query first.
#
# And routes it to the most
# cost-effective model tier.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# A lot of real AI products
# decide, for every incoming
# question, which model to
# send it to.
#
# A cheap and fast model for
# simple questions.
#
# A bigger and more expensive
# model for hard ones.
#
# If someone wrote this as one
# big method with if-elif
# checks on "how complex is
# this query" —
#
# what problem are we straight
# back into?

# ============================================================
# THE ANSWER
# ============================================================

# The exact same problem from
# the Google Maps section.
#
# Every new routing rule means
# going back and editing that
# same method again.
#
# Violating the Open/Closed
# Principle.

# ============================================================
# THE PIECES
# ============================================================


class ModelChoice(Enum):
    FAST_CHEAP_MODEL = "fast_cheap"
    LARGE_CAPABLE_MODEL = "large_capable"


class QueryComplexity(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"


class RoutingStrategy(ABC):

    @abstractmethod
    def select_model(self, query):
        ...


class SimpleQueryStrategy(RoutingStrategy):

    def select_model(self, query):
        return ModelChoice.FAST_CHEAP_MODEL


class ComplexReasoningStrategy(RoutingStrategy):

    def select_model(self, query):
        return ModelChoice.LARGE_CAPABLE_MODEL


# ============================================================
# THE TRAP OF if-elif ROUTING
# ============================================================

# In an initial
# implementation, a developer
# might write a factory to
# hand off the strategy using
# a traditional conditional
# check.


class IfElifRouterFactory:
    _simple = SimpleQueryStrategy()
    _complex = ComplexReasoningStrategy()

    @staticmethod
    def get_strategy(complexity):
        if complexity == QueryComplexity.SIMPLE:
            return IfElifRouterFactory._simple
        return IfElifRouterFactory._complex  # What happens when we add 'MEDIUM', 'VISION', or 'CODE'?


print("The if-elif Router")

simple_query = "How do I reset my password?"
complex_query = "Analyze this deadlock stack trace."

for complexity, query in [(QueryComplexity.SIMPLE, simple_query),
                          (QueryComplexity.COMPLEX, complex_query)]:
    strategy = IfElifRouterFactory.get_strategy(complexity)
    print(strategy.select_model(query))

# ============================================================
# WHY THIS BREAKS DOWN
# ============================================================

# This drops you right back
# into the Open/Closed
# Principle violation.
#
# Every time product
# management introduces a new
# model tier —
#
# a mid-tier model for
# intermediate questions,
#
# or a specialized model for
# code-generation —
#
# you have to reopen this
# class, add another elif
# branch, and risk breaking
# existing routing paths.

# ============================================================
# THE SOLUTION
# ============================================================

# Using a dict-based approach,
# we can completely eliminate
# the if-elif chain.
#
# The RouterFactory no longer
# needs to make decisions.
#
# It simply acts as a clean
# registry lookup.


class RouterFactory:
    # Dict lookups happen instantly, with no conditional logic at all
    _strategies = {
        QueryComplexity.SIMPLE: SimpleQueryStrategy(),
        QueryComplexity.COMPLEX: ComplexReasoningStrategy(),
    }

    @staticmethod
    def get_strategy(complexity):
        strategy = RouterFactory._strategies.get(complexity)
        if strategy is None:
            raise ValueError(f"Unknown query complexity: {complexity}")
        return strategy


print("\nThe Dict-Based Router")

for complexity, query in [(QueryComplexity.SIMPLE, simple_query),
                          (QueryComplexity.COMPLEX, complex_query)]:
    strategy = RouterFactory.get_strategy(complexity)
    print(strategy.select_model(query))

# Observation:
#
# Same two answers.
#
# The difference isn't what it
# returns today.
#
# It's what adding a third
# tier costs tomorrow.

# ============================================================
# MODEL ROUTING IN PRACTICE
# ============================================================

# This is genuinely how
# model-routing systems get
# built in practice.
#
# A question gets classified
# first.
#
# And then a strategy decides
# which model tier handles it.
#
# This keeps costs down on the
# easy questions.
#
# While dynamically scaling
# intelligence for the hard
# ones.

# ============================================================
# RAG SYSTEMS
# ============================================================

# The exact same pattern
# appears in
# Retrieval-Augmented
# Generation pipelines.
#
# For choosing a retrieval
# method.
#
# Instead of if-elif buried
# inside the retrieval code,
#
# you'd have a
# RetrievalStrategy interface
# with one class per approach.
#
#     Keyword Search
#
#     Vector Search
#
#     Hybrid Search
#
# Your factory handles handing
# out the right strategy based
# on the context.

# ============================================================
# CHECKPOINT
# ============================================================

# Is Strategy solid?
#
# Before we move on, one thing
# needs clearing up.

# ============================================================
# CLEARING THE CONFUSION
# ============================================================

# We just built a Strategy.
#
# But to make it work, we had
# to use a Factory.
#
# And back in the Google Maps
# section, someone might have
# noticed this shape looks an
# awful lot like the Adapter
# pattern we learned earlier
# in the course.
#
# They all rely on interfaces
# and multiple classes
# implementing them.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# If you had to explain the
# difference in their actual
# JOBS to a junior developer,
# what would you say?
#
# Start with Factory vs
# Strategy.

# ============================================================
# THE ANSWER
# ============================================================

# Factory is about CREATING
# the object.
#
# Strategy is about what the
# object DOES once you have
# it.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now, what about Adapter?
#
# How is Adapter different
# from Strategy?

# ============================================================
# THE ANSWER
# ============================================================

# Strategy is about choosing
# different algorithms or
# behaviours for the same
# task.
#
# Adapter is just a
# translator.
#
# It takes an existing class
# that has the wrong interface
# and forces it to fit yours.
#
# Without changing its core
# behaviour.

# ============================================================
# THE RESTAURANT
# ============================================================

# Let's lock this in with a
# non-software analogy, so you
# never mix them up in an
# interview.
#
# Think about running a busy,
# modern restaurant.
#
# THE FACTORY
#
#     is the Kitchen Expediter
#     (Manager).
#
#     An order comes in for
#     "Sushi", and their only
#     job is to route that
#     ticket to the Sushi
#     Station.
#
#     They don't cook the food.
#
#     Their job is just to
#     provide the right worker.
#
# THE STRATEGY
#
#     is the Station Chef
#     themselves.
#
#     The Sushi Chef prepares
#     food one way.
#
#     The Grill Chef prepares
#     food a totally different
#     way.
#
#     They represent different
#     behaviours for the exact
#     same overarching task —
#     cooking a meal.
#
# THE ADAPTER
#
#     is the Host handling the
#     food delivery tablets.
#
#     Your kitchen only
#     understands standard,
#     printed paper tickets.
#
#     But a third-party app
#     like UberEats sends
#     orders digitally to a
#     proprietary tablet.
#
#     You don't force your busy
#     chefs to learn a new
#     digital system.
#
#     Instead, the Host acts as
#     the adapter. They read
#     the tablet and punch it
#     into the cash register so
#     it prints a standard
#     paper ticket for the
#     kitchen.
#
#     They don't cook the food
#     — they just bridge the
#     gap between two
#     incompatible interfaces.

# ============================================================
# BOARD SUMMARY
# ============================================================

# THE "INTERFACE" PATTERNS —
# WHO DOES WHAT?
#
# FACTORY
#
#     CREATES.
#
#     "Here is the object you
#      asked for."
#
#     (Returns a new or cached
#      instance)
#
# STRATEGY
#
#     BEHAVES.
#
#     "Here is my specific way
#      of doing the task."
#
#     (Executes the algorithm)
#
# ADAPTER
#
#     TRANSLATES.
#
#     "I don't do the work, I
#      just translate your call
#      so this third-party
#      library understands it."
#
#     (Bridges incompatible
#      interfaces)


# ============================================================
# RAPID-FIRE : SCENARIO 1
# ============================================================

# Your backend needs to upload
# a file.
#
# Sometimes you upload it to
# AWS S3, and sometimes to
# Google Cloud Storage.
#
# The caller decides which one
# to use.
#
# Answer:
#
# Strategy.
#
# Two different ways to do the
# exact same task.

# ============================================================
# RAPID-FIRE : SCENARIO 2
# ============================================================

# You just installed a new
# third-party analytics
# library.
#
# But its method is called
# track_event(xml_data),
#
# and your entire app only
# knows how to use an
# interface that calls
# log(json_data).
#
# Answer:
#
# Adapter.
#
# Bridging the gap between
# your interface and their
# incompatible library.

# ============================================================
# RAPID-FIRE : SCENARIO 3
# ============================================================

# You have a
# NotificationService.
#
# Based on whether the user is
# on the free tier or premium
# tier, you need to
# instantiate and return
# either a BasicEmailSender or
# a PrioritySMSGateway.
#
# Answer:
#
# Factory.
#
# Its job is purely to decide
# which object to build and
# return.

# ============================================================
# CHECKPOINT
# ============================================================

# Are the borders between
# these three completely
# clear?
#
# Creates.
#
# Behaves.
#
# Translates.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Sending every query to the
# most capable model is a cost
# problem, not just an
# engineering one.
#
# A model router classifies
# first, then picks a tier.
#
# An if-elif inside the
# factory puts you back into
# the Open/Closed violation
# the pattern was meant to
# fix.
#
# A dict lookup removes the
# conditional entirely, and a
# new tier becomes a new
# registry entry.
#
# The same structure chooses
# retrieval methods in RAG
# pipelines.
#
# Factory creates. Strategy
# behaves. Adapter translates.
#
# Same shape, three different
# jobs.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Strategy is done.
#
# It answered:
#
#     "how does the caller pick
#      ONE way out of several?"
#
# The second pattern today
# asks something that sounds
# similar and isn't.
#
# What if the answer isn't
# "pick one" —
#
# but "tell everyone who
# cares"?
#
# Next:
#
# 04_observer_problem.py
