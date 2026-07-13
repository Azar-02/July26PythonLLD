"""
============================================================
LLD-5 : OOP-4 (ABCs, PROTOCOLS AND MIXINS)
FILE : 05_payment_processing_lab.py
============================================================

CAPSTONE LAB

Topics Covered
--------------
1. Payment Gateway Design
2. ABCs
3. Protocols
4. Mixins
5. Razorpay Gateway
6. Stripe Gateway
7. Paytm Gateway
8. Third Party Integration
9. AuditMixin
10. RetryMixin
11. MRO Walkthrough
12. Production Style Design

This file combines everything
covered in Lecture 5.
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

# ============================================================
# MOTIVATION
# ============================================================

# We are building a payment system.
#
# Requirements:
#
# - Multiple gateways
# - Common contract
# - Auditing
# - Retry support
# - Third party integrations
#
# This is a perfect use case
# for:
#
# ABCs
# Protocols
# Mixins

# ============================================================
# ABC CONTRACT
# ============================================================


class PaymentGateway(ABC):

    @abstractmethod
    def charge(
        self,
        amount
    ):
        pass

    @abstractmethod
    def refund(
        self,
        transaction_id
    ):
        pass


# ============================================================
# RAZORPAY
# ============================================================


class RazorpayGateway(
    PaymentGateway
):

    def charge(
        self,
        amount
    ):

        print(
            f"Razorpay charging ₹{amount}"
        )

    def refund(
        self,
        transaction_id
    ):

        print(
            f"Razorpay refund "
            f"{transaction_id}"
        )


# ============================================================
# STRIPE
# ============================================================


class StripeGateway(
    PaymentGateway
):

    def charge(
        self,
        amount
    ):

        print(
            f"Stripe charging ₹{amount}"
        )

    def refund(
        self,
        transaction_id
    ):

        print(
            f"Stripe refund "
            f"{transaction_id}"
        )


# ============================================================
# PAYTM
# ============================================================


class PaytmGateway(
    PaymentGateway
):

    def charge(
        self,
        amount
    ):

        print(
            f"Paytm charging ₹{amount}"
        )

    def refund(
        self,
        transaction_id
    ):

        print(
            f"Paytm refund "
            f"{transaction_id}"
        )


# ============================================================
# POLYMORPHISM
# ============================================================

print("Gateway Polymorphism")

gateways = [
    RazorpayGateway(),
    StripeGateway(),
    PaytmGateway()
]

for gateway in gateways:

    gateway.charge(500)

# Same method.
#
# Different behaviour.

# ============================================================
# PROTOCOL
# ============================================================

# ABC requires inheritance.
#
# Protocol allows behaviour-based
# integration.


@runtime_checkable
class Chargeable(Protocol):

    def charge(
        self,
        amount
    ):
        ...


# ============================================================
# THIRD PARTY SDK
# ============================================================


class JuspayGateway:

    def charge(
        self,
        amount
    ):

        print(
            f"Juspay charging ₹{amount}"
        )


# ============================================================
# GENERIC PROCESSOR
# ============================================================


def process_payment(
    gateway: Chargeable,
    amount
):

    gateway.charge(amount)


print("\nProtocol Example")

process_payment(
    JuspayGateway(),
    700
)

# Juspay does not inherit
# our ABC.
#
# Yet it works.

# ============================================================
# AUDIT MIXIN
# ============================================================


class AuditMixin:

    def audit(
        self,
        message
    ):

        print(
            f"[AUDIT] {message}"
        )


# ============================================================
# RETRY MIXIN
# ============================================================


class RetryMixin:

    def retry(
        self,
        action_name
    ):

        print(
            f"Retrying "
            f"{action_name}"
        )


# ============================================================
# COMBINING MIXINS
# ============================================================


class ProductionGateway(
    AuditMixin,
    RetryMixin,
    RazorpayGateway
):

    pass


print("\nMixins Example")

gateway = ProductionGateway()

gateway.audit(
    "Payment Started"
)

gateway.retry(
    "Charge"
)

gateway.charge(1000)

# ============================================================
# MRO
# ============================================================

print("\nMRO")

print(
    [
        cls.__name__
        for cls
        in ProductionGateway.mro()
    ]
)

# MRO determines:
#
# Method lookup
# Attribute lookup
# super()

# ============================================================
# WHY THIS DESIGN?
# ============================================================

# PaymentGateway
#
# provides contract.
#
#
# Protocol
#
# enables external integrations.
#
#
# Mixins
#
# provide reusable features.
#
#
# Together:
#
# Flexible and safe design.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Which concept solves
# each problem?
#
# Contract?
#
# -> ABC
#
#
# Third-party integration?
#
# -> Protocol
#
#
# Reusable behaviour?
#
# -> Mixin

# ============================================================
# COMPLETE FLOW
# ============================================================

# RazorpayGateway
#
# implements ABC.
#
# ProductionGateway
#
# inherits:
#
# AuditMixin
# RetryMixin
# RazorpayGateway
#
# JuspayGateway
#
# participates using
# Protocol.
#
# All concepts work together.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ABC
#
# Contract.
#
# Protocol
#
# Behaviour-based contract.
#
# Mixin
#
# Reusable implementation.
#
# Production systems often
# combine all three.
#
# This lab demonstrates
# how they work together.
