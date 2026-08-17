"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 04_decorator_in_a_real_backend.py
============================================================

Topics Covered
--------------
1.  Where File 03 Left Us
2.  The Notification Service
3.  What The Business Keeps Asking For
4.  The Decorator-Shaped Fix
5.  The Interface And The Real Sender
6.  The Shared Decorator Base
7.  Logging, Retry, Rate Limiting
8.  Wiring The Chain
9.  Adding A Fourth Concern
10. Cross-Cutting Concerns
11. Middleware By Another Name
12. Key Takeaways
"""

import time
from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 03 LEFT US
# ============================================================

# Coffee.
#
# Files.
#
# The @ symbol.
#
# All three were the same
# shape.
#
# Now the version you will
# actually build one day.

# ============================================================
# THE SCENARIO
# ============================================================

# Say you have a
# NotificationService that
# sends a message to a user.
#
#     send(user_id, message)
#
# That is the whole job.
#
# At first.

# ============================================================
# WHAT THE BUSINESS KEEPS ASKING FOR
# ============================================================

# Over time, the business
# keeps asking for more.
#
#     "log every notification
#      we send"
#
#     "retry if it fails"
#
#     "don't send more than 5
#      messages per user per
#      minute"
#
# Each one arrives separately.
#
# Weeks apart.

# ============================================================
# IF WE CODE IT ALL INSIDE
# ============================================================

# If we code each of these
# directly inside
# NotificationService,
#
# that one class turns into a
# mess.
#
# Logging.
#
# Retries.
#
# Rate limiting.
#
# And the actual sending.
#
# All tangled together in one
# place.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# We've seen this exact shape
# of problem twice already
# today.
#
# Once with Beverage almost
# growing boolean flags.
#
# And once with Amazon's
# order_place() in the Facade
# lecture.
#
# What's the Decorator-shaped
# fix here ?

# ============================================================
# THE FIX
# ============================================================

# Keep NotificationService as
# a simple interface.
#
# With just one method.
#
#     send()
#
# Then wrap it.
#
# One decorator for logging.
#
# One for retries.
#
# One for rate limiting.
#
# And stack them.
#
# Instead of writing all that
# logic inside the base
# sender.

# ============================================================
# THE INTERFACE
# ============================================================


class NotificationService(ABC):

    @abstractmethod
    def send(self, user_id, message):
        ...


# ============================================================
# THE REAL, BASE IMPLEMENTATION
# ============================================================

# Its only job is to actually
# send.
#
# Nothing else.


class SmsNotificationService(NotificationService):

    def send(self, user_id, message):
        # calls the real SMS gateway / provider API
        print(f"Sending SMS to {user_id}: {message}")


# ============================================================
# THE SHARED DECORATOR BASE
# ============================================================

# Same idea as
# CondimentDecorator.
#
# It exists only to hold what
# it is wrapping.


class NotificationDecorator(NotificationService):

    def __init__(self, wrapped):
        self.wrapped = wrapped


# ============================================================
# CONCERN 1 : LOGGING
# ============================================================


class LoggingNotificationDecorator(NotificationDecorator):

    def send(self, user_id, message):
        print(f"[LOG] Sending to {user_id} at {time.time()}")
        self.wrapped.send(user_id, message)
        print(f"[LOG] Send completed for {user_id}")


# ============================================================
# CONCERN 2 : RETRY
# ============================================================


class RetryNotificationDecorator(NotificationDecorator):

    def __init__(self, wrapped, max_attempts):
        super().__init__(wrapped)
        self.max_attempts = max_attempts

    def send(self, user_id, message):
        attempts = 0
        while attempts < self.max_attempts:
            try:
                self.wrapped.send(user_id, message)
                return
            except Exception:
                attempts += 1
                if attempts == self.max_attempts:
                    raise


# ============================================================
# CONCERN 3 : RATE LIMITING
# ============================================================


class RateLimitedNotificationDecorator(NotificationDecorator):

    def __init__(self, wrapped, max_per_minute):
        super().__init__(wrapped)
        self.max_per_minute = max_per_minute
        self.count_this_minute = {}

    def send(self, user_id, message):
        count = self.count_this_minute.get(user_id, 0)
        if count >= self.max_per_minute:
            print(f"[RATE LIMIT] Blocked notification for {user_id}")
            return
        self.count_this_minute[user_id] = count + 1
        self.wrapped.send(user_id, message)


# ============================================================
# WIRING IT ALL TOGETHER
# ============================================================

# Read bottom-up.
#
# Just like the coffee order.

print("The Notification Chain")

service = SmsNotificationService()
service = RetryNotificationDecorator(service, 3)
service = RateLimitedNotificationDecorator(service, 5)
service = LoggingNotificationDecorator(service)

service.send("user_123", "Your order has shipped!")

# Observation:
#
# One call.
#
# Four classes involved.
#
# Only one of them actually
# sent anything.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What's the exact same
# benefit we saw with Amazon
# and PhonePe in the Facade
# lecture?
#
# What happens the day the
# business asks for a FOURTH
# concern?
#
# Say:
#
#     "also send a copy to our
#      audit system"

# ============================================================
# THE ANSWER
# ============================================================

# We write one new
# AuditNotificationDecorator.
#
# And add it to the chain of
# wrapping.
#
# SmsNotificationService and
# every existing decorator
# stay completely untouched.

# ============================================================
# CROSS-CUTTING CONCERNS
# ============================================================

# This is exactly how real
# backend systems handle
# cross-cutting concerns.
#
# Logging.
#
# Retries.
#
# Caching.
#
# Rate limiting.
#
# Authentication.
#
# Metrics.
#
# Without polluting the core
# business logic.

# ============================================================
# MIDDLEWARE BY ANOTHER NAME
# ============================================================

# You'll see this same shape
# called "middleware" in web
# frameworks.
#
# Retry and circuit-breaker
# libraries use this exact
# idea.
#
# To build wrappers around a
# plain function or client
# call.
#
# Different names.
#
# Same pattern.

# ============================================================
# THE CORE LESSON
# ============================================================

# The moment you catch
# yourself about to add
#
#     "just one more concern"
#
# directly into a class that
# already does the real work —
#
# that's your cue to reach for
# a decorator instead.

# ============================================================
# CHECKPOINT
# ============================================================

# Is the production version
# clear?
#
# A base that does the real
# work.
#
# One wrapper per concern.
#
# Stacked, not merged.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# A service that does the real
# work should keep doing only
# that.
#
# Logging, retries and rate
# limiting are separate
# concerns, and each becomes
# its own wrapper.
#
# NotificationDecorator plays
# the same role
# CondimentDecorator did —
# holding the wrapped object.
#
# The chain is read
# bottom-up, exactly like the
# coffee order.
#
# A fourth concern means one
# new decorator class, and
# nothing else changes.
#
# Cross-cutting concerns are
# what this pattern is for.
#
# In web frameworks the same
# shape is called middleware.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Decorator is done.
#
# It answered one question:
#
#     "how do I keep adding
#      behaviour without
#      editing the original
#      class?"
#
# The second pattern today
# answers a completely
# different one.
#
# What happens when you have
# far too many objects, and
# almost all of them are
# carrying the same data?
#
# Next:
#
# 05_flyweight_problem_and_implementation.py
