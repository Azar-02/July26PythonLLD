"""
============================================================
LLD-5 : OOP-4 (ABCs, PROTOCOLS AND MIXINS)
FILE : 03_protocols_structural_subtyping.py
============================================================

Topics Covered
--------------
1. ABC Recap
2. Nominal Typing
3. Structural Typing
4. Membership Card Analogy
5. Protocols
6. runtime_checkable
7. Third Party Integrations
8. WhatsApp SDK Example
9. Protocol vs ABC
10. Key Takeaways

Based on Lecture 5 Notes.
"""

from typing import Protocol, runtime_checkable

# ============================================================
# MOTIVATION
# ============================================================

# Last file:
#
# ABC
#
# gives us contracts.
#
# Duck Typing
#
# gives us flexibility.
#
# Question:
#
# Can we get:
#
# - safety
# and
# - flexibility
#
# together?
#
# Protocols attempt to
# solve this problem.

# ============================================================
# NOMINAL TYPING
# ============================================================

# ABCs use:
#
# Nominal Typing
#
# Meaning:
#
# The relationship must be
# explicitly declared.
#
# Example:
#
# SMSChannel
# extends
# NotificationChannel
#
# Membership matters.

# ============================================================
# MEMBERSHIP CARD ANALOGY
# ============================================================

# Think about a gym.
#
# To enter:
#
# You need a membership card.
#
# Even if you are fit,
# you cannot enter without
# membership.
#
# ABCs behave similarly.
#
# Explicit membership is required.

# ============================================================
# STRUCTURAL TYPING
# ============================================================

# Structural Typing asks:
#
# Can you do the work?
#
# Not:
#
# Who are your parents?
#
# Behaviour matters.
#
# Structure matters.

# ============================================================
# PROTOCOL
# ============================================================


@runtime_checkable
class NotificationChannel(
    Protocol
):

    def send(
        self,
        message: str
    ) -> None:
        ...


# ============================================================
# SMS CHANNEL
# ============================================================


class SMSChannel:

    def send(
        self,
        message: str
    ):

        print(
            f"SMS -> {message}"
        )


# ============================================================
# EMAIL CHANNEL
# ============================================================


class EmailChannel:

    def send(
        self,
        message: str
    ):

        print(
            f"Email -> {message}"
        )


# ============================================================
# GENERIC FUNCTION
# ============================================================


def notify(
    channel: NotificationChannel,
    message: str
):

    channel.send(message)


print("Protocol Example")

notify(
    SMSChannel(),
    "Ride Accepted"
)

notify(
    EmailChannel(),
    "Ride Completed"
)

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# SMSChannel does NOT inherit:
#
# NotificationChannel
#
# Yet it works.
#
# Why?
#
# Because it has:
#
# send()

# ============================================================
# WHAT PROTOCOL CHECKS
# ============================================================

# Protocol asks:
#
# Does the object provide
# the required behaviour?
#
# If yes:
#
# It is accepted.

# ============================================================
# THIRD PARTY SDK EXAMPLE
# ============================================================

# Imagine:
#
# WhatsApp SDK
#
# comes from another company.
#
# We cannot modify it.

# ============================================================
# THIRD PARTY CLASS
# ============================================================


class WhatsAppSDK:

    def send(
        self,
        message: str
    ):

        print(
            f"WhatsApp -> "
            f"{message}"
        )


print("\nThird Party Integration")

notify(
    WhatsAppSDK(),
    "Driver Arrived"
)

# No inheritance.
#
# No ABC.
#
# Still works.

# ============================================================
# WHY PROTOCOLS EXIST
# ============================================================

# ABC:
#
# Requires inheritance.
#
# Third-party code may not
# inherit our classes.
#
# Protocol:
#
# Behaviour is enough.

# ============================================================
# RUNTIME CHECKABLE
# ============================================================

print("\nRuntime Checks")

print(
    isinstance(
        SMSChannel(),
        NotificationChannel
    )
)

print(
    isinstance(
        WhatsAppSDK(),
        NotificationChannel
    )
)

# Both return True.
#
# Because both implement:
#
# send()

# ============================================================
# WHAT IF SEND IS MISSING?
# ============================================================


class BrokenChannel:

    pass


print("\nBroken Channel")   

print(
    isinstance(
        BrokenChannel(),
        NotificationChannel
    )
)

# False

# Missing:
#
# send()

# ============================================================
# PROTOCOL VS DUCK TYPING
# ============================================================

# Duck Typing:
#
# "Try it and see."
#
# Protocol:
#
# "Define expected behaviour."
#
# Both focus on behaviour.
#
# Protocols provide more clarity.

# ============================================================
# PROTOCOL VS ABC
# ============================================================

# ABC
#
# Nominal Typing
#
# Requires inheritance.
#
#
# Protocol
#
# Structural Typing
#
# No inheritance required.
#
# Only behaviour matters.

# ============================================================
# DECISION FRAMEWORK
# ============================================================

# ABC:
#
# Strong contract.
#
# Protocol:
#
# Flexible contract.
#
# Duck Typing:
#
# No formal contract.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# What problem do Protocols solve?
#
# They allow:
#
# Static contracts
#
# without requiring
#
# inheritance.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Protocols support:
#
# Structural Typing.
#
# Behaviour matters more
# than inheritance.
#
# Third-party integrations
# become easier.
#
# runtime_checkable allows
# isinstance() checks.
#
# Protocol sits between:
#
# ABC
# and
# Duck Typing.
