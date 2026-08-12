"""
============================================================
DESIGN PATTERNS : CREATIONAL FAMILY
FILE : 02_abc_pure_contract_vs_shared_state.py
============================================================

Topics Covered
--------------
1. Where We Left Off
2. The New Requirement
3. What ABC Can Actually Hold
4. Building A Partial Implementation
5. The Inherited Method
6. Comparing The Two Designs
7. What Stays Abstract, And Why
8. Choosing Between Them
9. Interview Questions
10. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# So far our AIServiceClient
# was just a contract.
#
# No stored data.
#
# No shared logic.
#
# Every method fully written
# out separately in each
# subclass.


class AIServiceClient(ABC):

    @abstractmethod
    def complete(self, prompt):
        ...


class PlainOpenAIClient(AIServiceClient):

    def complete(self, prompt):
        return "response from OpenAI"


print("Pure Contract")
print(PlainOpenAIClient().complete("ping"))

# ============================================================
# THE NEW REQUIREMENT
# ============================================================

# THINK BEFORE READING ON
#
# What if every client also
# needs to REMEMBER something
# in common?
#
# Like its own provider_name.
#
# Or a timeout_ms setting.
#
# And one method should be
# written ONCE and inherited
# by everyone,
#
# instead of being copy
# pasted into every subclass?
#
# Does our current
# AIServiceClient already
# support this,
#
# or does something need to
# change?

# ============================================================
# THE ANSWER
# ============================================================

# It can actually already
# support this.
#
# An ABC is not limited to
# being a pure, empty
# contract.
#
# It can hold real fields,
# set up in __init__,
#
# and fully written, concrete
# methods,
#
# sitting right alongside
# methods that stay abstract
# and must be filled in by
# each subclass.

# Core Rule:
#
# There is no separate
# "interface" construct here.
#
# Everything is built from
# the same ABC.
#
# The difference between
# "pure contract" and
# "partial implementation
# with shared state" is not a
# different tool.
#
# It is just a different way
# of using the same one.

# ============================================================
# BUILDING A PARTIAL IMPLEMENTATION
# ============================================================


class BaseAIServiceClient(ABC):

    def __init__(self, provider_name, timeout_ms):
        self.provider_name = provider_name
        self.timeout_ms = timeout_ms

    # written ONCE here
    # inherited by every subclass
    # never reimplemented
    def supports_provider(self, name):
        return self.provider_name.lower() == name.lower()

    # still forces each vendor
    # to supply its own logic
    @abstractmethod
    def complete(self, prompt):
        ...


class OpenAIClient(BaseAIServiceClient):

    def __init__(self):
        super().__init__("openai", timeout_ms=5000)

    def complete(self, prompt):
        # calls OpenAI's SDK / HTTP API underneath
        return "response from OpenAI"


class AnthropicClient(BaseAIServiceClient):

    def __init__(self):
        super().__init__("anthropic", timeout_ms=5000)

    def complete(self, prompt):
        return "response from Anthropic"


class GeminiClient(BaseAIServiceClient):

    def __init__(self):
        super().__init__("gemini", timeout_ms=5000)

    def complete(self, prompt):
        return "response from Gemini"


print("\nShared State Version")

clients = [
    OpenAIClient(),
    AnthropicClient(),
    GeminiClient()
]

for client in clients:
    print(client.provider_name, client.timeout_ms)

# ============================================================
# THE INHERITED METHOD
# ============================================================

# supports_provider() was
# written once, in the base
# class.
#
# Every subclass gets it for
# free.

print("\nSupports Provider, Written Once")

for client in clients:
    print(
        client.provider_name,
        client.supports_provider("ANTHROPIC")
    )

# Observation:
#
# Three classes.
#
# One implementation.

# ============================================================
# COMPARING THE TWO DESIGNS
# ============================================================

# THINK BEFORE READING ON
#
# What is the actual
# difference between the
# plain AIServiceClient from
# earlier,
#
# and this
# BaseAIServiceClient?

# Both are built from ABC.
#
# Nothing different at the
# language level.
#
# The difference is how much
# each one actually holds.
#
# AIServiceClient was a pure
# contract.
#
# Nothing shared.
#
# BaseAIServiceClient carries
# real state
#
#     provider_name
#     timeout_ms
#
# plus one already written
# method
#
#     supports_provider()
#
# that every subclass gets
# for free,
#
# while complete() stays
# abstract, still forcing
# each vendor to write its
# own version.

# ============================================================
# BOARD SUMMARY
# ============================================================

# PURE CONTRACT
#
# Only abstract methods.
#
# Every subclass writes
# everything from scratch.
#
#
# PARTIAL IMPLEMENTATION
#
# Fields, concrete methods,
# and abstract methods.
#
# Shared logic written ONCE,
# inherited by every
# subclass.
#
#
# Both built the SAME way in
# Python, using ABC.
#
# The difference is a DESIGN
# CHOICE about how much lives
# in the base class,
#
# not a different language
# feature.

# ============================================================
# WHAT STAYS ABSTRACT, AND WHY
# ============================================================

# Important:
#
# Going "shared state" does
# not mean everything becomes
# concrete.
#
# complete() stayed abstract.
#
# Because that variation is
# genuinely irreducible.
#
# Service specific request
# building and response
# parsing can never be
# meaningfully shared.
#
# Even a shared state design
# keeps those parts abstract.

# ============================================================
# CHOOSING BETWEEN THEM
# ============================================================

# Use PURE CONTRACT when:
#
# there is no shared state or
# logic between
# implementations
#
#
# Use SHARED STATE when:
#
# subclasses genuinely share
# real data or logic
#
# for example provider_name,
# timeout_ms, or a
# supports_provider() check
# written once

# ============================================================
# QUIZ
# ============================================================

# In Python, what is the
# difference between an
# "interface" and an
# "abstract class"?
#
# A) Different keywords
# B) Interfaces cannot hold
#    fields, abstract classes
#    can
# C) No language level
#    difference — both are
#    ABC, it is a design
#    choice
# D) Interfaces are faster
#
# Answer:
#
# C)

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Can an ABC hold real fields
# and fully written methods?
#
# Yes.
#
# Alongside abstract methods
# that subclasses must still
# implement.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# In a shared state base
# class, which methods should
# stay abstract?
#
# The ones whose variation is
# genuine.
#
# Vendor specific request
# building and response
# parsing cannot be
# meaningfully shared.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Assuming an ABC must be
# empty,
#
# and copy pasting the same
# helper into every subclass
# because of it.

# ============================================================
# BEST PRACTICE
# ============================================================

# Put something in the base
# class when implementations
# genuinely share it.
#
# Leave it abstract when the
# only honest answer is
# "each subclass decides".

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Python has one tool here.
#
# ABC.
#
# A pure contract and a
# partial implementation are
# two ways of using it.
#
# Shared state means fields
# and concrete methods live
# in the base class.
#
# Abstract methods still
# force each subclass to
# supply its own logic.
#
# Which to use is a design
# choice, not a language
# feature.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# So far one provider has
# meant one client object.
#
# But a provider usually is
# not just "one client
# object".
#
# OpenAI's SDK, for example,
# gives you a chat client, an
# embeddings client, and a
# moderation client.
#
# Three separate objects.
#
# What if your app needs all
# three,
#
# and they must always come
# from the SAME vendor?
#
# A warning before you read
# on.
#
# The next file covers
# "Abstract Factory".
#
# Same word "abstract".
#
# Unrelated meaning.
#
# Do not confuse it with the
# abstract methods we just
# covered.
#
# Next:
#
# 03_abstract_factory_matched_families.py
