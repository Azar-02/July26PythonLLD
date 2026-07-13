"""
============================================================
LLD-5 : OOP-4 (ABCs, PROTOCOLS AND MIXINS)
FILE : 02_abc_vs_duck_typing.py
============================================================

Topics Covered
--------------
1. ABC Recap
2. Notification System
3. SMS Channel
4. Email Channel
5. Push Channel
6. ABC Approach
7. Duck Typing Approach
8. Safety vs Flexibility
9. Trade-offs
10. Decision Framework

Based on Lecture 5 Notes.
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# Last class:
#
# ABCs gave us contracts.
#
# Question:
#
# Does every system need
# strict contracts?
#
# Or can we be more flexible?
#
# This leads us to:
#
# ABC vs Duck Typing.

# ============================================================
# NOTIFICATION SYSTEM
# ============================================================

# Consider:
#
# SMS
# Email
# Push Notification
#
# Every channel should support:
#
# send()

# ============================================================
# ABC APPROACH
# ============================================================


class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message):
        pass


class SMSChannel(NotificationChannel):

    def send(self, message):

        print(
            f"SMS -> {message}"
        )


class EmailChannel(NotificationChannel):

    def send(self, message):

        print(
            f"Email -> {message}"
        )


class PushChannel(NotificationChannel):

    def send(self, message):

        print(
            f"Push -> {message}"
        )


# ============================================================
# GENERIC SENDER
# ============================================================


def notify(
    channel,
    message
):

    channel.send(message)


print("ABC Example")

notify(
    SMSChannel(),
    "Ride accepted"
)

notify(
    EmailChannel(),
    "Ride completed"
)

notify(
    PushChannel(),
    "Driver arrived"
)

# ============================================================
# BENEFIT OF ABC
# ============================================================

# Every channel MUST
# implement send().
#
# Missing implementation
# causes failure during
# object creation.

# ============================================================
# FORGOTTEN IMPLEMENTATION
# ============================================================


class WhatsAppChannel(
    NotificationChannel
):

    pass


print("\nABC Protection")

try:

    channel = WhatsAppChannel()

except TypeError as ex:

    print(ex)

# ABC catches the mistake
# immediately.

# ============================================================
# DUCK TYPING APPROACH
# ============================================================

# Question:
#
# What if we remove ABC?
#
# Python often focuses on:
#
# behaviour
#
# instead of:
#
# inheritance.

# ============================================================
# SIMPLE FUNCTION
# ============================================================


def notify_v2(
    channel,
    message
):

    channel.send(message)


class SlackChannel:

    def send(self, message):

        print(
            f"Slack -> {message}"
        )


print("\nDuck Typing")

notify_v2(
    SlackChannel(),
    "Deployment successful"
)

# SlackChannel does not
# inherit NotificationChannel.
#
# Still works.

# ============================================================
# WHY?
# ============================================================

# Python asks:
#
# Does the object have:
#
# send()
#
# If yes:
#
# proceed.
#
# This is Duck Typing.

# ============================================================
# FAMOUS QUOTE
# ============================================================

# If it walks like a duck,
# quacks like a duck,
# it is a duck.

# ============================================================
# THIRD PARTY SDK EXAMPLE
# ============================================================


class ThirdPartySMSProvider:

    def send(self, message):

        print(
            f"Third Party SMS -> "
            f"{message}"
        )


notify_v2(
    ThirdPartySMSProvider(),
    "OTP Sent"
)

# No inheritance.
#
# No ABC.
#
# Still works.

# ============================================================
# THE RISK
# ============================================================

# Duck Typing provides
# flexibility.
#
# But flexibility has risks.

# ============================================================
# WRONG OBJECT
# ============================================================


class MaintenanceTicket:

    def send(self, message):

        print(
            f"Ticket Updated: "
            f"{message}"
        )


print("\nUnexpected Success")

notify_v2(
    MaintenanceTicket(),
    "Hello"
)

# Observation:
#
# No error.
#
# Python saw send()
# and executed it.
#
# But:
#
# MaintenanceTicket is not
# really a notification channel.

# ============================================================
# ABC VS DUCK TYPING
# ============================================================

# ABC
#
# Pros:
# - Explicit contract
# - Early validation
# - Safer teams
#
# Cons:
# - Less flexible
#
#
# Duck Typing
#
# Pros:
# - Flexible
# - Easy integration
# - No inheritance needed
#
# Cons:
# - Wrong objects may work
# - Bugs can be subtle

# ============================================================
# WHEN TO USE ABC
# ============================================================

# Use ABC when:
#
# - You own the hierarchy.
# - Contract is important.
# - Early bug detection matters.
# - Large team environment.

# ============================================================
# WHEN TO USE DUCK TYPING
# ============================================================

# Use Duck Typing when:
#
# - Integrating external code.
# - Plugins.
# - SDKs.
# - Flexible architecture.
# - Rapid experimentation.

# ============================================================
# DECISION FRAMEWORK
# ============================================================

# Question:
#
# Do I need a strict contract?
#
# YES
#  -> ABC
#
# NO
#  -> Duck Typing

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Can Duck Typing replace ABC?
#
# Sometimes.
#
# But ABC provides stronger
# guarantees.
#
# The choice depends on
# safety vs flexibility.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ABC:
#
# Contract-first design.
#
# Duck Typing:
#
# Behaviour-first design.
#
# ABC prioritizes safety.
#
# Duck Typing prioritizes
# flexibility.
#
# Python supports both.
