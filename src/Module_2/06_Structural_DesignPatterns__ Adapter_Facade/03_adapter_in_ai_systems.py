"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 03_adapter_in_ai_systems.py
============================================================

Topics Covered
--------------
1. Where File 02 Left Us
2. One App, Many LLM Providers
3. Naming The Pattern
4. The Three Pieces, Again
5. The Common Interface
6. One Adapter Per Provider
7. Swapping Providers At Runtime
8. How Real Multi-Model Tools Are Built
9. Why The Business Cares
10. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 02 LEFT US
# ============================================================

# We built the Adapter for
# banks.
#
# Target Interface.
#
# Adaptee.
#
# Adapter.
#
# Nothing about that structure
# was banking specific.
#
# Now here is one close to what
# many of you actually build.

# ============================================================
# THE SETUP
# ============================================================

# Your app needs to talk to
# an LLM.
#
# You want it to work with
# OpenAI.
#
# And Anthropic.
#
# And Gemini.
#
# Now the trouble.

# ============================================================
# WHAT IS DIFFERENT BETWEEN THEM
# ============================================================

# Each SDK has a different
# request shape.
#
# Different parameter names.
#
# Different streaming format.
#
# None of them agreed on
# anything with each other.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What pattern is this?
#
# It is the one we just spent
# two files building.
#
# Say the name before you
# read on.

# ============================================================
# THE ANSWER
# ============================================================

# Adapter.
#
# One common interface our
# app codes against.
#
# One adapter per provider.
#
# Each translating our
# interface into that
# provider's real SDK calls.

# ============================================================
# THE THREE PIECES, AGAIN
# ============================================================

# Exactly the same structure
# as the bank problem.
#
# Only the names changed.
#
# Target Interface
#
#     BankAPI
#         becomes
#     ChatModel
#
# Adaptee
#
#     YesBank
#         becomes
#     the vendor's SDK client
#
# Adapter
#
#     YesBankAdapter
#         becomes
#     OpenAIAdapter
#
# If you can see that mapping,
# you have the pattern.

# ============================================================
# THE COMMON INTERFACE
# ============================================================


class ChatModel(ABC):

    @abstractmethod
    def generate(self, prompt, params):
        ...


# ============================================================
# THE VENDOR CLIENTS
# ============================================================

# Stand-ins for the real SDKs.
#
# Notice they disagree on
# everything.
#
# Method name.
#
# Parameter names.
#
# The shape of the input.


class OpenAIClient:

    def complete(self, messages, temperature):
        return f"[openai] {messages[0]['content']}"


class AnthropicClient:

    def message(self, user_text, temp):
        return f"[anthropic] {user_text}"


# ============================================================
# ONE ADAPTER PER PROVIDER
# ============================================================


class OpenAIAdapter(ChatModel):

    def __init__(self, client):
        self.client = client

    def generate(self, prompt, params):
        # translate into OpenAI's chat.completions.create(...) shape
        return self.client.complete(
            messages=[{"role": "user", "content": prompt}],
            temperature=params["temperature"]
        )


class AnthropicAdapter(ChatModel):

    def __init__(self, client):
        self.client = client

    def generate(self, prompt, params):
        # translate into Anthropic's messages.create(...) shape
        return self.client.message(
            user_text=prompt,
            temp=params["temperature"]
        )


# ============================================================
# RUNNING IT
# ============================================================

print("One Interface, Many Vendors")

models = [
    OpenAIAdapter(OpenAIClient()),
    AnthropicAdapter(AnthropicClient())
]

for model in models:
    print(model.generate("Explain hashing", {"temperature": 0.2}))

# Observation:
#
# The loop calls generate().
#
# Once.
#
# The same way both times.
#
# It never learns which vendor
# it is talking to.

# ============================================================
# THE SAME MOVE AS BEFORE
# ============================================================

# Your app talks to one
# interface.
#
# Swapping GPT for Claude for
# Gemini becomes a one line
# change.
#
# Same as swapping
# YesBankAdapter for
# HDFCBankAdapter.

# ============================================================
# HOW REAL TOOLS ARE BUILT
# ============================================================

# This is exactly how real
# multi-model AI tools are
# built.
#
# Libraries that let you swap
# between GPT, Claude, and
# Gemini with one line of
# config
#
# are basically one big
# Adapter layer
#
# over many different LLM
# SDKs.
#
# You have used one.
#
# Now you know what is inside
# it.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Why does this matter for
# the business?
#
# Not just for clean code.
#
# Name a few reasons.

# ============================================================
# WHY THE BUSINESS CARES
# ============================================================

# Prices change.
#
# A model gets deprecated.
#
# You want to A/B test quality
# across providers.
#
# A new, better or cheaper
# model shows up.
#
# None of that should mean
# rewriting the whole app.

# ============================================================
# CHECKPOINT
# ============================================================

# Is Adapter fully landed?
#
# Two very different domains.
#
# Banks.
#
# LLM providers.
#
# One identical structure
# underneath.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# The Adapter pattern is not
# about banks.
#
# It is about two sides that
# do not fit.
#
# Different SDK shapes,
# parameter names, and
# streaming formats are the
# same problem as different
# bank method names.
#
# One common interface the app
# codes against.
#
# One adapter per provider.
#
# The client loop never learns
# which vendor is underneath.
#
# The payoff is commercial,
# not just aesthetic:
#
#     prices, deprecations,
#     A/B tests, and cheaper
#     models
#
# should never mean rewriting
# the app.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Adapter is done.
#
# It solved one kind of
# problem:
#
#     two things that do not
#     fit together.
#
# The second structural
# pattern today solves a
# different one.
#
# Not incompatibility.
#
# Too much complexity in one
# place.
#
# Next:
#
# 04_facade_problem_and_implementation.py
