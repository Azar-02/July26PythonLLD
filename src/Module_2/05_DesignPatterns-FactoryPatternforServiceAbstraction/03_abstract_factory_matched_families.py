"""
============================================================
DESIGN PATTERNS : CREATIONAL FAMILY
FILE : 03_abstract_factory_matched_families.py
============================================================

Topics Covered
--------------
1. A Provider Is Not One Object
2. Why One Flat Factory Is Not Enough
3. Naming The Pattern
4. Building The Abstract Factory
5. The Matched Family Guarantee
6. What Mixing Vendors Costs
7. When A Plain Factory Method Is Enough
8. Interview Questions
9. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# A NAMING WARNING FIRST
# ============================================================

# The previous file was about
# abstract methods and ABC.
#
# This file is about a
# pattern called "Abstract
# Factory".
#
# Same word.
#
# Unrelated meaning.
#
# Here "abstract" is the
# pattern's name, not the
# "shared state" idea we just
# covered.

# ============================================================
# MOTIVATION
# ============================================================

# Here is something specific
# to real AI SDKs.
#
# A provider usually is not
# just "one client object".
#
# OpenAI's SDK, for example,
# gives you:
#
# a chat client
#
# an embeddings client
#
# and a moderation client
#
# Three separate objects.

# ============================================================
# THE REQUIREMENT
# ============================================================

# Say your app needs all
# three,
#
# and they must always come
# from the SAME vendor.
#
# You never want a chat
# client from OpenAI paired
# with an embeddings client
# from Anthropic.
#
# THINK BEFORE READING ON
#
# Is one flat
#
#     get_client(provider)
#
# factory method enough for
# that?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# You would need several
# related factory methods,
#
# one per object type,
#
# all guaranteed to come from
# the same vendor.

# ============================================================
# NAMING IT
# ============================================================

# ABSTRACT FACTORY
#
# A GROUP of related factory
# methods behind ONE
# interface,
#
# guaranteeing a consistent,
# compatible FAMILY of
# related objects.

# ============================================================
# THE THREE COMPONENT TYPES
# ============================================================


class ChatClient(ABC):

    @abstractmethod
    def complete(self, prompt):
        ...


class EmbeddingsClient(ABC):

    @abstractmethod
    def embed(self, text):
        ...


class ModerationClient(ABC):

    @abstractmethod
    def check(self, text):
        ...


# ============================================================
# THE THREE VENDOR FAMILIES
# ============================================================


class OpenAIChatClient(ChatClient):

    def complete(self, prompt):
        return "chat response from OpenAI"


class OpenAIEmbeddingsClient(EmbeddingsClient):

    def embed(self, text):
        return "embedding from OpenAI"


class OpenAIModerationClient(ModerationClient):

    def check(self, text):
        return "moderation verdict from OpenAI"


class AnthropicChatClient(ChatClient):

    def complete(self, prompt):
        return "chat response from Anthropic"


class AnthropicEmbeddingsClient(EmbeddingsClient):

    def embed(self, text):
        return "embedding from Anthropic"


class AnthropicModerationClient(ModerationClient):

    def check(self, text):
        return "moderation verdict from Anthropic"


class GeminiChatClient(ChatClient):

    def complete(self, prompt):
        return "chat response from Gemini"


class GeminiEmbeddingsClient(EmbeddingsClient):

    def embed(self, text):
        return "embedding from Gemini"


class GeminiModerationClient(ModerationClient):

    def check(self, text):
        return "moderation verdict from Gemini"


# ============================================================
# THE ABSTRACT FACTORY
# ============================================================

# AIProviderFactory
#
#     create_chat_client()
#         -> ChatClient
#
#     create_embeddings_client()
#         -> EmbeddingsClient
#
#     create_moderation_client()
#         -> ModerationClient


class AIProviderFactory(ABC):

    @abstractmethod
    def create_chat_client(self):
        ...

    @abstractmethod
    def create_embeddings_client(self):
        ...

    @abstractmethod
    def create_moderation_client(self):
        ...


class OpenAIProviderFactory(AIProviderFactory):

    def create_chat_client(self):
        return OpenAIChatClient()

    def create_embeddings_client(self):
        return OpenAIEmbeddingsClient()

    def create_moderation_client(self):
        return OpenAIModerationClient()


class AnthropicProviderFactory(AIProviderFactory):

    def create_chat_client(self):
        return AnthropicChatClient()

    def create_embeddings_client(self):
        return AnthropicEmbeddingsClient()

    def create_moderation_client(self):
        return AnthropicModerationClient()


class GeminiProviderFactory(AIProviderFactory):

    def create_chat_client(self):
        return GeminiChatClient()

    def create_embeddings_client(self):
        return GeminiEmbeddingsClient()

    def create_moderation_client(self):
        return GeminiModerationClient()


# ============================================================
# THE MATCHED FAMILY
# ============================================================

# Notice what the caller
# never does.
#
# It never names a concrete
# class.


def build_family(factory):
    return [
        type(factory.create_chat_client()).__name__,
        type(factory.create_embeddings_client()).__name__,
        type(factory.create_moderation_client()).__name__
    ]


print("Each Factory Returns Its Own Matched Set")

for provider_factory in [
    OpenAIProviderFactory(),
    AnthropicProviderFactory(),
    GeminiProviderFactory()
]:
    print(type(provider_factory).__name__)
    print("   ", build_family(provider_factory))

# Observation:
#
# Three vendors.
#
# Three complete families.
#
# Each factory only ever
# returns its OWN matched
# set.

# ============================================================
# WHY THIS MATTERS
# ============================================================

# THINK BEFORE READING ON
#
# Why does it matter that
# ChatClient,
# EmbeddingsClient, and
# ModerationClient all come
# from the SAME factory,
#
# instead of being picked
# independently by whoever
# needs them?

# So you cannot accidentally
# end up with a mismatched
# combination.
#
# For example an OpenAI chat
# client paired with a Gemini
# moderation client.

print("\nA Mismatched Combination")

mismatched = [
    type(OpenAIProviderFactory().create_chat_client()).__name__,
    type(OpenAIProviderFactory().create_embeddings_client()).__name__,
    type(GeminiProviderFactory().create_moderation_client()).__name__
]

print(mismatched)

# Observation:
#
# Two vendors in one
# pipeline.
#
# Which might use:
#
# different auth
#
# different response formats
#
# different rate limits
#
# The factory guarantees a
# matched, compatible family.
#
# Core Rule:
#
# Guards against mixing
# vendors.
#
# Each factory only ever
# returns its OWN matched
# set.

# ============================================================
# QUIZ
# ============================================================

# What is the core difference
# between a Factory Method
# and an Abstract Factory?
#
# A) Factory Method builds
#    objects directly,
#    Abstract Factory does not
#    build anything at all
# B) A Factory Method creates
#    one object. An Abstract
#    Factory groups several
#    related factory methods
#    behind one interface, to
#    build a consistent family
#    of related objects
# C) Abstract Factory only
#    works with AI providers
# D) There is no real
#    difference
#
# Answer:
#
# B)

# ============================================================
# WHEN A PLAIN FACTORY METHOD IS ENOUGH
# ============================================================

# THINK BEFORE READING ON
#
# For a lot of apps though —
# one that only ever needs a
# single chat client per
# provider, nothing else —
#
# is a full Abstract Factory
# worth the extra structure?
#
# Or is a plain Factory
# Method enough?

# A plain Factory Method is
# enough.
#
# Abstract Factory earns its
# complexity only when there
# is a genuine FAMILY of
# related objects that must
# stay matched together.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What does an Abstract
# Factory guarantee that
# three separate factory
# methods do not?
#
# That the objects you get
# back belong to one matched,
# compatible family.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# When is Abstract Factory
# the wrong choice?
#
# When there is only one
# product type per provider.
#
# Then it is a Factory Method
# wearing extra structure.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Letting each part of the
# app pick its own client
# independently,
#
# and assuming everyone will
# remember to use the same
# vendor.

# ============================================================
# BEST PRACTICE
# ============================================================

# Let the caller hold a
# factory.
#
# Not a provider string.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# One vendor often means a
# FAMILY of objects, not one.
#
# Picking components
# independently allows
# mismatched combinations.
#
# Mismatched vendors may
# differ in auth, response
# formats, and rate limits.
#
# An Abstract Factory groups
# related factory methods
# behind one interface.
#
# Each concrete factory
# returns only its own
# matched set.
#
# Use it only when a genuine
# family must stay matched.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We now have:
#
# a factory method for one
# object
#
# and an abstract factory for
# a matched family
#
# Next we walk the whole idea
# end to end.
#
# First the naive
# ChatService, fully broken.
#
# Then fixed properly with a
# factory.
#
# And then the reason teams
# building on LLMs actually
# need this in production.
#
# Next:
#
# 04_ai_client_failover.py
