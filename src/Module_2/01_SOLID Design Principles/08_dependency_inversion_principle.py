"""
============================================================
PART 08
DEPENDENCY INVERSION PRINCIPLE (DIP)
============================================================

Topics Covered
1. Understanding coupling
2. Tight coupling vs Loose coupling
3. Discovering the Dependency Inversion Principle
4. Refactoring using abstractions
5. Bird flying behaviour example
6. Runtime flexibility
7. Interview discussion
8. Bridge to Dependency Injection
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# So far we have learned:
#
# SRP  -> One responsibility
# OCP  -> Extend without modifying
# LSP  -> Child should honour parent contract
# ISP  -> Small focused interfaces
#
# One question still remains.
#
# Who should depend on whom?
#
# Imagine changing one low-level implementation
# forces changes throughout your application.
#
# Is that a healthy design?

# ============================================================
# STORY
# ============================================================

# Suppose a NotificationService always sends emails.

class EmailService:
    def send(self, message):
        print(f"Email: {message}")

class NotificationServiceV1:

    def __init__(self):
        self.email = EmailService()

    def notify(self, message):
        self.email.send(message)

print("=== Tight Coupling ===")
NotificationServiceV1().notify("Welcome!")

# ============================================================
# DISCUSSION
# ============================================================

# NotificationService directly creates EmailService.
#
# Ask yourself:
#
# Tomorrow the business says:
#
# "Use SMS instead."
#
# Which class changes?
#
# Answer:
# NotificationService.
#
# The high-level business logic is tightly
# coupled to one concrete implementation.

# ============================================================
# STOP AND THINK
# ============================================================

# Which part of the system changes more often?
#
# Business rules?
#
# or
#
# Delivery mechanisms?
#
# Usually delivery mechanisms evolve faster.

# ============================================================
# DISCOVERING THE PROBLEM
# ============================================================

# High-level modules contain business decisions.
#
# Low-level modules perform technical work.
#
# Ideally, changing technical details should not
# force business logic to change.

# ============================================================
# DEPENDENCY INVERSION PRINCIPLE
# ============================================================

# High-level modules should not depend on
# low-level modules.
#
# Both should depend upon abstractions.
#
# Abstractions should not depend upon details.
#
# Details should depend upon abstractions.

# ============================================================
# REFACTORING
# ============================================================

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message):
        pass


class EmailChannel(NotificationChannel):

    def send(self, message):
        print(f"Email: {message}")


class SMSChannel(NotificationChannel):

    def send(self, message):
        print(f"SMS: {message}")


class WhatsAppChannel(NotificationChannel):

    def send(self, message):
        print(f"WhatsApp: {message}")

# ============================================================
# HIGH LEVEL MODULE
# ============================================================

class NotificationService:

    def __init__(self, channel: NotificationChannel):
        self.channel = channel

    def notify(self, message):
        print("Business Logic:")
        self.channel.send(message)

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

email_service = NotificationService(EmailChannel())
sms_service = NotificationService(SMSChannel())
wa_service = NotificationService(WhatsAppChannel())

email_service.notify("Order Confirmed")
sms_service.notify("OTP: 654321")
wa_service.notify("Package Delivered")

# ============================================================
# OBSERVATION
# ============================================================

# Did NotificationService change?
#
# No.
#
# Only the supplied implementation changed.
#
# The business logic remained untouched.

# ============================================================
# SAME IDEA USING BIRDS
# ============================================================

class FlyingBehaviour(ABC):

    @abstractmethod
    def fly(self):
        pass


class FlutterFlight(FlyingBehaviour):

    def fly(self):
        print("Fluttering flight")


class GlideFlight(FlyingBehaviour):

    def fly(self):
        print("Long gliding flight")


class Bird:

    def __init__(self, name, behaviour: FlyingBehaviour):
        self.name = name
        self.behaviour = behaviour

    def perform_flight(self):
        print(self.name, "starts flying...")
        self.behaviour.fly()

print("\n=== Bird Example ===")

Bird("Sparrow", FlutterFlight()).perform_flight()
Bird("Eagle", GlideFlight()).perform_flight()

# ============================================================
# WHY IS THIS BETTER?
# ============================================================

# Bird no longer depends upon
# FlutterFlight
# or
# GlideFlight.
#
# It depends only on the abstraction:
#
# FlyingBehaviour

# ============================================================
# SMALL EXPERIMENT
# ============================================================

class NoFlight(FlyingBehaviour):

    def fly(self):
        print("Cannot fly.")

print("\n=== Runtime Behaviour Change ===")
penguin = Bird("Penguin", NoFlight())
penguin.perform_flight()

# ============================================================
# DISCUSSION
# ============================================================

# Without changing Bird,
# we changed its behaviour.
#
# This is a powerful consequence
# of depending on abstractions.

# ============================================================
# COMMON DESIGN SMELLS
# ============================================================

# 1. Creating concrete objects using new/class()
#    deep inside business logic.
#
# 2. Frequent modifications whenever
#    implementations change.
#
# 3. High-level modules importing
#    numerous concrete classes.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# DIP does NOT mean:
#
# "Everything must be abstract."
#
# Use abstractions where flexibility
# and independent evolution matter.

# ============================================================
# INTERVIEW CORNER
# ============================================================

# Q. Why is DIP important?
#
# A.
# It isolates business rules from
# implementation details.
#
# Q. Which SOLID principle usually enables
# Dependency Injection?
#
# A.
# Dependency Inversion Principle.

# ============================================================
# BOARD SUMMARY
# ============================================================

# High Level
#      |
#      v
# Abstraction
#      ^
#      |
# Low Level
#
# Everyone depends upon the abstraction.

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# One question still remains.
#
# We have removed tight coupling.
#
# But who should create EmailChannel(),
# SMSChannel(),
# or FlutterFlight()?
#
# Should Bird create them?
#
# Or should someone else provide them?
#
# That leads us to
# Dependency Injection.
