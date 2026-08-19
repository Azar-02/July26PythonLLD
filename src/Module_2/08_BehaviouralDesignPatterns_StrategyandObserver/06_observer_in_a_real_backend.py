"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 06_observer_in_a_real_backend.py
============================================================

Topics Covered
--------------
1. Where File 05 Left Us
2. A Response Arriving Token By Token
3. Who Should The Core Code Call
4. The Token Observer Interface
5. Three Observers
6. Watching The Fan-Out
7. How Streaming Actually Works In SDKs
8. Multi-Agent Telemetry
9. You May Know It As A Webhook
10. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 05 LEFT US
# ============================================================

# A subscriber interface.
#
# A publisher holding a list.
#
# Subscribers signing
# themselves up.
#
# That was orders.
#
# Now somewhere you have
# watched this happen without
# naming it.

# ============================================================
# THE SCENE
# ============================================================

# When an LLM streams a
# response, text shows up
# token by token.
#
# Now imagine you also need a
# logger tracking usage.
#
# And a moderation system
# scanning every token as it
# comes in.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Should the core
# token-generating code
# directly call the UI, the
# logger, and the moderation
# system?
#
# One by one?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# That ties the core logic
# tightly to a bunch of
# unrelated concerns.
#
# Each of those things should
# just subscribe to a
#
#     "new token arrived"
#
# event instead.

# ============================================================
# THE OBSERVER INTERFACE
# ============================================================


class TokenObserver(ABC):

    @abstractmethod
    def on_token(self, token):
        ...


# ============================================================
# THREE OBSERVERS
# ============================================================


class UIUpdater(TokenObserver):

    def on_token(self, token):
        print(f"  [ui] appended {token!r} to chat")


class UsageLogger(TokenObserver):

    def on_token(self, token):
        print(f"  [usage] token counted: {token!r}")


class ModerationChecker(TokenObserver):

    def on_token(self, token):
        print(f"  [moderation] scanned {token!r}")


# ============================================================
# WATCHING THE FAN-OUT
# ============================================================

# Three unrelated concerns.
#
# One event.

print("Streaming Three Tokens")

observers = [UIUpdater(), UsageLogger(), ModerationChecker()]

for token in ["Design", " patterns", " help."]:
    for observer in observers:
        observer.on_token(token)

# Observation:
#
# Every observer saw every
# token.
#
# None of them knows the
# others exist.

# ============================================================
# HOW STREAMING ACTUALLY WORKS
# ============================================================

# This is genuinely how
# streaming works in most LLM
# SDKs.
#
# Something like:
#
#     on_token
#
# or:
#
#     on_chunk
#
# is Observer, just wearing a
# different name.
#
# Anywhere you see a callback
# registered for streamed
# data, or an on_message
# handler —
#
# that's an Observer being
# registered.

# ============================================================
# MULTI-AGENT TELEMETRY
# ============================================================

# Multi-agent systems use the
# same idea for telemetry.
#
# Every tool call and every
# reasoning step can notify a
# set of observers.
#
#     logging
#
#     cost tracking
#
#     dashboards
#
# Without the agent's core
# logic needing to know any of
# them exist.

# ============================================================
# YOU MAY KNOW IT AS A WEBHOOK
# ============================================================

# You've probably also heard
# this called a "webhook".
#
# A payment gateway fires a
#
#     "payment succeeded"
#
# event to whichever URLs
# registered for it.
#
# Without knowing or caring
# who they belong to.
#
# Same pattern.
#
# Across a network instead of
# inside one process.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What would go wrong if the
# agent's core reasoning loop
# directly called a
# dashboard-logging function
# itself?
#
# Inline.

# ============================================================
# THE ANSWER
# ============================================================

# Every time someone wants a
# new kind of observability,
#
# they'd have to go back and
# edit the core reasoning
# loop.
#
# Exactly the problem we've
# been trying to avoid this
# whole lecture.

# ============================================================
# CHECKPOINT
# ============================================================

# Two domains now.
#
# An order being placed.
#
# A token arriving.
#
# Same structure underneath.
#
# One announcement, many
# reactions.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# UI updates, usage logging
# and moderation are three
# unrelated concerns reacting
# to one event.
#
# The core token-generating
# code should call none of
# them by name.
#
# on_token and on_chunk
# callbacks in LLM SDKs are
# Observer under a different
# name.
#
# So is any on_message
# handler.
#
# Agent frameworks use the
# same idea for logging, cost
# tracking and dashboards.
#
# A webhook is this pattern
# stretched across a network.
#
# Calling observability code
# inline means editing the
# core loop every time
# somebody wants more of it.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Both patterns are now on the
# table.
#
# Strategy.
#
# Observer.
#
# Both built on one interface
# with many implementations.
#
# Next we separate them for
# good.
#
# And then watch a working
# Strategy quietly turn back
# into an if-elif, one
# innocent line at a time.
#
# Next:
#
# 07_comparison_ai_corner_and_wrapup.py
