"""
============================================================
DESIGN PATTERNS : CREATIONAL FAMILY
FILE : 04_ai_client_failover.py
============================================================

Topics Covered
--------------
1.  The Naive ChatService
2.  Where The Decision Should Live
3.  match/case As A Tidier Chain
4.  Fixing It With A Factory Method
5.  Switching Providers By Config
6.  What An Outage Costs
7.  The Failover Loop
8.  Why This Change Was Safe
9.  What Else This Unlocks
10. Interview Questions
11. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# We now walk the whole idea
# end to end.
#
# In two steps.
#
# First get the naive version
# fully broken.
#
# Then fix it properly.

# ============================================================
# STEP 1 OF 2 : THE INTERFACE
# ============================================================

# What is the minimum an
# AIServiceClient interface
# needs,
#
# if all we care about right
# now is:
#
#     send a prompt,
#     get text back


class AIServiceClient(ABC):

    @abstractmethod
    def complete(self, prompt):
        ...


# A stand in for a real
# outage, so this file can
# demonstrate failover later.

OPENAI_DOWN = False


class OpenAIClient(AIServiceClient):

    def complete(self, prompt):
        if OPENAI_DOWN:
            raise RuntimeError("openai unavailable")
        # calls OpenAI's SDK underneath
        return "response from OpenAI"


class AnthropicClient(AIServiceClient):

    def complete(self, prompt):
        # calls Anthropic's SDK underneath
        return "response from Anthropic"


class GeminiClient(AIServiceClient):

    def complete(self, prompt):
        # calls Google's SDK underneath
        return "response from Gemini"


# ============================================================
# THE NAIVE APPROACH
# ============================================================

# Without a factory, how
# would ChatService decide
# which one to use,
#
# based on a config value
# like:
#
#     AI_PROVIDER=anthropic


class NaiveChatService:

    def __init__(self, provider):
        if provider == "openai":
            self.client = OpenAIClient()
        elif provider == "anthropic":
            self.client = AnthropicClient()
        elif provider == "gemini":
            self.client = GeminiClient()

    def get_response(self, prompt):
        return self.client.complete(prompt)


print("Naive Chat Service")
print(NaiveChatService("anthropic").get_response("ping"))

# Observation:
#
# It needed its own if/elif
# reading the config value.
#
# Exactly the problem this
# module opened with,
#
# just moved into ChatService
# directly.

# ============================================================
# STEP 2 OF 2 : WHERE IT BELONGS
# ============================================================

# That if/elif belongs in a
# dedicated factory class.
#
# Not inside ChatService.

# ============================================================
# A TIDIER SPELLING
# ============================================================

# Python gives us a slightly
# tidier way to write a long
# chain of
#
#     "check this value
#      against several
#      options"
#
# One that reads a bit more
# like a table of cases.
#
# match / case
#
# Structural pattern matching.


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


print("\nFactory With match/case")

for name in ["openai", "anthropic", "gemini"]:
    built = AIServiceClientProvider.get_client(name)
    print(f"{name} -> {type(built).__name__}")

# ============================================================
# THE CALLER
# ============================================================


class ChatService:

    def __init__(self, provider):
        self.client = AIServiceClientProvider.get_client(provider)

    def get_response(self, prompt):
        return self.client.complete(prompt)


# ============================================================
# THE CONFIG SWAP
# ============================================================

# THINK BEFORE READING ON
#
# Walk through what happens
# if AI_PROVIDER changes from
#
#     "openai"
#
# to
#
#     "anthropic"
#
# with zero code changes
# anywhere else.

print("\nSwitching Providers By Config")

for env in [
    {"AI_PROVIDER": "openai"},
    {"AI_PROVIDER": "anthropic"}
]:
    chat = ChatService(env["AI_PROVIDER"])
    print(chat.get_response("ping"))

# Observation:
#
# ChatService is built with a
# different string.
#
# get_client() returns a
# different concrete class.
#
# get_response() runs exactly
# the same code.
#
# It never notices the switch,
# because it only ever talks
# to the AIServiceClient
# interface.

# Core Rule:
#
# Client only knows the
# interface.
#
# The factory knows the
# vendor.

# ============================================================
# THE SECOND MOTIVATION
# ============================================================

# We have solved:
#
#     "pick a provider once,
#      at startup"
#
# Now the reason teams
# building on LLMs actually
# need this structure.
#
# Not tidiness.
#
# A real production need.
#
# Failover.

# ============================================================
# WHAT AN OUTAGE COSTS
# ============================================================

# THINK BEFORE READING ON
#
# Say OpenAI's API is having
# an outage.
#
# If ChatService is hardcoded
# to one client, what happens
# to your app?

OPENAI_DOWN = True

print("\nSingle Provider During An Outage")

try:
    ChatService("openai").get_response("ping")
except RuntimeError as error:
    print("RuntimeError:", error)

# Observation:
#
# The whole app's AI feature
# goes down with it.
#
# There is no way to fall
# back to a different
# provider without
# redeploying code.

# ============================================================
# THE SMALLEST POSSIBLE CHANGE
# ============================================================

# What does ChatService
# actually need?
#
# A LIST of provider names.
#
# It asks the factory for
# each one until one
# succeeds.
#
# Nothing about
# AIServiceClient,
# OpenAIClient, or the
# factory itself needs to
# change.


class FailoverChatService:

    def __init__(self, provider_priority):
        self.provider_priority = provider_priority

    def get_response(self, prompt):
        for provider in self.provider_priority:
            try:
                client = AIServiceClientProvider.get_client(provider)
                return client.complete(prompt)
            except Exception:
                pass  # log and try the next provider
        raise RuntimeError("All AI providers failed")


print("\nFailover : openai down")

service = FailoverChatService(
    ["openai", "anthropic", "gemini"]
)

print(service.get_response("ping"))

# Observation:
#
# openai raised.
#
# The loop moved on.
#
# anthropic answered.
#
# gemini was never asked.

OPENAI_DOWN = False

# ============================================================
# WHY THIS WAS A SAFE CHANGE
# ============================================================

# THINK BEFORE READING ON
#
# Why was this a small, safe
# change instead of a risky
# one?

# Because the abstraction was
# already in place.
#
# ChatService never depended
# on a specific vendor's
# class to begin with.
#
# So adding failover did not
# require touching:
#
# OpenAIClient
#
# AnthropicClient
#
# or the factory's internals
#
# at all.

# ============================================================
# WHAT ELSE THIS UNLOCKS
# ============================================================

# This is the real payoff of
# using Factory for service
# abstraction.
#
# It is not just cleaner code.
#
# It directly enables:
#
# failover
#
# A/B testing between models
#
# per user model choice
#
# cost based routing
#
# All as small additions
# instead of rewrites.

# ============================================================
# QUIZ
# ============================================================

# AI_PROVIDER changes from
# "openai" to "anthropic".
#
# What has to change inside
# ChatService?
#
# A) Its __init__
# B) Its get_response()
# C) Nothing
# D) The AIServiceClient
#    interface
#
# Answer:
#
# C) Nothing

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# What does ChatService
# depend on once the factory
# is introduced?
#
# Only the AIServiceClient
# interface.
#
# Never a concrete vendor
# class.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Why was adding failover a
# small change?
#
# Because the caller already
# depended on an interface.
#
# The pattern was not added
# for failover.
#
# Failover became cheap
# because the pattern was
# already there.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Letting a caller import a
# vendor class directly,
# bypassing the factory.
#
# The moment that happens,
# swapping providers means
# rewriting that caller
# again.

# ============================================================
# BEST PRACTICE
# ============================================================

# Callers depend on the
# interface only.
#
# The factory is the single
# place that names concrete
# vendor classes.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Without a factory, the
# caller grows its own
# if/elif over vendors.
#
# match/case is a tidier
# spelling of the same
# decision.
#
# A config change swaps
# providers with zero code
# changes.
#
# Failover is a list of
# providers plus a loop.
#
# The change was small only
# because the abstraction
# already existed.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# One question remains.
#
# Look at
#
#     get_client()
#
# again.
#
# Has the match/case actually
# disappeared?
#
# Or has it just moved
# somewhere else?
#
# Next:
#
# 05_simple_factory_and_registry.py
