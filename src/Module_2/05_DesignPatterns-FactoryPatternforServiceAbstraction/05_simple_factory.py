"""
============================================================
DESIGN PATTERNS : CREATIONAL FAMILY
FILE : 05_simple_factory.py
============================================================

Topics Covered
--------------
1. Did The Decision Disappear
2. Practical / Simple Factory
3. What The Win Actually Is
4. What To Watch For
5. Where This Runs In Production
6. When A Factory Is Unnecessary
7. Module Summary
8. Interview Questions
9. Key Takeaways
10. Homework
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# Look again at
#
#     AIServiceClientProvider
#         .get_client()
#
# THINK BEFORE READING ON
#
# Has the match/case actually
# disappeared?
#
# Or has it just moved
# somewhere else?

# ============================================================
# THE HONEST ANSWER
# ============================================================

# It moved.
#
# But it moved to exactly
# ONE dedicated, well known
# place.
#
# Every caller across the
# codebase goes through this
# same method,
#
# instead of writing its own
# branch.


class AIServiceClient(ABC):

    @abstractmethod
    def complete(self, prompt):
        ...


class OpenAIClient(AIServiceClient):

    def complete(self, prompt):
        return "response from OpenAI"


class AnthropicClient(AIServiceClient):

    def complete(self, prompt):
        return "response from Anthropic"


class GeminiClient(AIServiceClient):

    def complete(self, prompt):
        return "response from Gemini"


class AIServiceClientProvider:

    @staticmethod
    def get_client(provider):
        match provider:
            case "openai":
                return OpenAIClient()
            case "anthropic":
                return AnthropicClient()
            case "gemini":
                return GeminiClient()
            case _:
                raise ValueError(
                    f"Unknown provider: {provider}"
                )


print("One Decision, One Place")

for name in ["openai", "anthropic", "gemini"]:
    client = AIServiceClientProvider.get_client(name)
    print(f"{name} -> {client.complete('ping')}")

# ============================================================
# PRACTICAL FACTORY
# ============================================================

# Also called Simple Factory.
#
# Core Rule:
#
# The decision does not fully
# disappear.
#
# Someone, somewhere, always
# has to decide which
# concrete class to build.
#
# The win is centralizing
# that decision to ONE place,
#
# so the rest of the codebase
# never repeats it.

# ============================================================
# BEING HONEST ABOUT THIS
# ============================================================

# This is worth being honest
# about.
#
# Students often expect
# "Factory" to mean zero
# conditionals anywhere.
#
# It does not.
#
# It means exactly ONE
# conditional,
#
# in exactly ONE well known
# location,
#
# instead of the same
# decision copy pasted across
# the whole codebase.


# ============================================================
# WHERE THIS RUNS IN PRODUCTION
# ============================================================

# THINK BEFORE READING ON
#
# Does this exact shape —
#
# interface
#
# plus concrete
# implementations
#
# plus a factory deciding
# which one to build
#
# — sound like something you
# have already used, under a
# different name, somewhere
# else in backend work?

# LLM provider abstraction
#
# Swap OpenAI, Anthropic, and
# Gemini behind one
# AIServiceClient interface.
#
# Failover, A/B testing, and
# per user model choice all
# become small additions,
# not rewrites.
#
#
# Payment gateways
#
# One checkout flow
# supporting Razorpay,
# Stripe, PayPal, and UPI
# behind a
# PaymentGatewayFactory.
#
# Add a new gateway without
# touching checkout logic
# anywhere.
#
#
# Cloud storage SDKs
#
# A StorageFactory returning
# an S3 backed client, a GCS
# backed client, or an Azure
# backed client depending on
# config.
#
# How most multi cloud
# backend systems are
# actually structured.
#
#
# Database connections
#
# From the SOLID class.
#
# SQLAlchemy's
# create_engine(url) reads
# the prefix of the URL and
# internally factory selects
# the correct database
# driver.
#
# Same pattern, already
# familiar.
#
#
# Logging
#
# Also from the SOLID class.
#
# logging.getLogger(__name__)
# is a factory method you have
# likely called many times,
#
# without naming it, until
# today.


# ============================================================
# WHEN A FACTORY IS UNNECESSARY
# ============================================================

# Factory is not magic
# either.
#
# If your app will only ever
# call ONE AI provider,
# forever,
#
# a factory is unnecessary
# structure.
#
# Just like Builder was
# overkill for a tiny Point
# class.
#
# And Prototype was overkill
# for a cheap to construct
# object.
#
# It earns its place the
# moment "which concrete
# implementation" becomes a
# decision that VARIES.
#
# By config.
#
# By user.
#
# By vendor outage.
#
# Or by time.

# ============================================================
# MODULE SUMMARY
# ============================================================

# FACTORY METHOD
#
# One method whose job is to
# create and return an object
# of another, usually
# related, class.
#
#
# ABSTRACT FACTORY
#
# A group of related factory
# methods behind ONE
# interface,
#
# guaranteeing a consistent,
# compatible FAMILY of
# objects.
#
# Worth it only when objects
# genuinely need to stay
# matched.
#
# For example a provider's
# chat client and embeddings
# client together.
#
#
# PRACTICAL / SIMPLE FACTORY
#
# A dedicated class that
# centralizes the "which
# concrete class do I build"
# decision to exactly one
# place.
#
#
# THE HONEST TRUTH
#
# A decision has to happen
# SOMEWHERE.
#
# Factory patterns do not
# eliminate that decision.
#
# They contain it, so it
# happens once, in one
# predictable place,
#
# instead of being copy
# pasted across your entire
# codebase.
#
# Ideally that place is
# registrable, not hardcoded.

# ============================================================
# QUIZ
# ============================================================

# After introducing a
# factory, how many places in
# the codebase decide which
# concrete class to build?
#
# A) Zero
# B) Exactly one
# C) One per caller
# D) One per concrete class
#
# Answer:
#
# B) Exactly one

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Does the Factory pattern
# eliminate conditionals?
#
# No.
#
# It centralizes them.
#
# One conditional, in one
# well known location.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Name two factories you have
# already used without
# calling them factories.
#
# SQLAlchemy's
# create_engine(), which
# selects a driver from the
# URL prefix.
#
# And logging.getLogger().

# ============================================================
# COMMON MISTAKE
# ============================================================

# Assuming a factory means no
# branching anywhere.
#
# It means the branching
# stops being duplicated.

# ============================================================
# BEST PRACTICE
# ============================================================

# Keep the decision in one
# well known place.
#
# And prefer a place that can
# be registered into,
#
# over one that must be
# edited for every new type.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# The decision does not
# disappear. It relocates.
#
# A simple factory
# centralizes it to exactly
# one place.
#
# Watch for factories that
# look extensible but still
# need editing for every new
# type.
#
# This exact shape already
# runs in payment gateways,
# storage SDKs,
# create_engine(), and
# getLogger().
#
# A factory earns its place
# only when the choice of
# implementation genuinely
# varies.

# ============================================================
# HOMEWORK
# ============================================================

# 1. Build a registry backed
#    AIServiceClientFactory.
#
#    Add a fourth provider
#    WITHOUT editing the
#    factory class itself.
#
# 2. Extend ChatService's
#    failover loop to log
#    which provider actually
#    served each request.
#
#    Useful for cost and
#    reliability tracking in
#    a real system.
#
# 3. Ask an AI assistant to
#    design a "payment gateway
#    factory" for Stripe,
#    Razorpay, and PayPal.
#
#    Push it on the same
#    question we asked live:
#
#        "how do I add a new
#         gateway without
#         editing this
#         factory?"
#
#    Fix the design if it
#    cannot answer cleanly.
#
# 4. Push all your code to
#    GitHub, on a branch
#    named:
#
#    factory-service-
#    abstraction-lecture-
#    complete

# ============================================================
# BRIDGE TO THE NEXT MODULE
# ============================================================

# That closes out Creational
# Patterns for this module.
#
# Today's problem was:
#
#     "the right class to
#      construct is not known
#      until runtime, so
#      contain that decision
#      in one place"
#
# Next class we move into
# Structural Patterns.
#
# The question shifts from:
#
#     "how do I create this
#      object"
#
# to:
#
#     "how do I make two
#      things that were not
#      built to work together,
#      work together anyway"
