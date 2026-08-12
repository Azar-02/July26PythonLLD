"""
============================================================
DESIGN PATTERNS : CREATIONAL FAMILY
FILE : 01_factory_problem_and_method.py
============================================================

Topics Covered
--------------
1.  The Hardcoded Decision
2.  Breaking The Open/Closed Principle
3.  Duplicated Decision Logic
4.  The Same Shape With AI Providers
5.  Where Should The Decision Live
6.  Factory Method Defined
7.  The AIServiceClient Contract
8.  Building The Provider Factory
9.  Adding A Fourth Provider
10. Passing Call Specific Data
11. The Single Responsibility Risk
12. Interview Questions
13. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# So far, "which object to
# build" was always obvious.
#
# We knew the exact class we
# wanted.
#
# Prototype let an object
# copy itself.
#
# Registry gave us one place
# to store and fetch
# templates by name.
#
# THINK BEFORE READING ON
#
# But what if we do not know
# the class until runtime?
#
# Based on a config value.
#
# A user's plan.
#
# Or which vendor's API we
# are calling this week.

# ============================================================
# THE STARTING POINT
# ============================================================

# Say you are building a
# NotificationService.
#
# It needs to send a message
# by SMS, Email, or Push,
#
# depending on what the
# caller asks for.
#
# Using only what you already
# know, what is the simplest
# way to write this?


class SmsSender:

    def send(self, message):
        return f"SMS sent: {message}"


class EmailSender:

    def send(self, message):
        return f"Email sent: {message}"


class PushSender:

    def send(self, message):
        return f"Push sent: {message}"


class NotificationService:

    def send(self, type_, message):
        if type_ == "SMS":
            sender = SmsSender()
            return sender.send(message)
        elif type_ == "EMAIL":
            sender = EmailSender()
            return sender.send(message)
        elif type_ == "PUSH":
            sender = PushSender()
            return sender.send(message)


service = NotificationService()

print("Naive Notification Service")
print(service.send("SMS", "Order shipped"))
print(service.send("EMAIL", "Order shipped"))
print(service.send("PUSH", "Order shipped"))

# Observation:
#
# This works fine.
#
# Today.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Six months from now,
# product asks for a fourth
# channel.
#
# WhatsApp.
#
# What has to change?
#
# And where?

# ============================================================
# PROBLEM 1 : OPEN/CLOSED PRINCIPLE
# ============================================================

# You have to go back into
#
#     NotificationService
#         .send()
#
# and add one more elif.
#
# Inside a method that
# already worked.
#
# And was already tested.


class WhatsAppSender:

    def send(self, message):
        return f"WhatsApp sent: {message}"


class NotificationServiceV2:

    def send(self, type_, message):
        if type_ == "SMS":
            return SmsSender().send(message)
        elif type_ == "EMAIL":
            return EmailSender().send(message)
        elif type_ == "PUSH":
            return PushSender().send(message)
        elif type_ == "WHATSAPP":
            return WhatsAppSender().send(message)


print("\nAfter Editing Working Code")
print(NotificationServiceV2().send("WHATSAPP", "Order shipped"))

# Core Rule:
#
# Every new channel means
# editing code that already
# worked,
#
# instead of just adding new
# code next to it.
#
# Open/Closed Principle
# broken.

# ============================================================
# PROBLEM 2 : DUPLICATED DECISION LOGIC
# ============================================================

# Now say NotificationService
# is not the only class that
# needs to send a
# notification.
#
# Three other services also
# need to pick SMS vs Email
# vs Push.
#
# THINK BEFORE READING ON
#
# What happens to this same
# if/elif block?


class OrderService:

    def notify(self, type_, message):
        if type_ == "SMS":
            return SmsSender().send(message)
        elif type_ == "EMAIL":
            return EmailSender().send(message)


class AlertService:

    def raise_alert(self, type_, message):
        if type_ == "SMS":
            return SmsSender().send(message)
        elif type_ == "EMAIL":
            return EmailSender().send(message)


print("\nSame Decision, Copy Pasted")
print(OrderService().notify("SMS", "Payment failed"))
print(AlertService().raise_alert("EMAIL", "Server down"))

# Observation:
#
# It gets copy pasted into
# every place that needs the
# same decision.
#
# So a new provider now means
# hunting down and editing
# that same if/elif in four
# or five different files.
#
# Core Rule:
#
# The decision
#
#     "which class do I build"
#
# is copy pasted everywhere
# it is needed,
#
# instead of living in one
# place.

# ============================================================
# THE SAME SHAPE, WITH AI PROVIDERS
# ============================================================

# One more, and this is the
# one that matters most in
# 2026.
#
# The same shape shows up
# when the "provider" is not
# SMS, Email, or Push,
#
# but an AI model provider.
#
# Your app calls an LLM, and
# today it is hardcoded to
# OpenAI.


class OpenAISdk:

    def complete(self, prompt):
        return "response from OpenAI"


class NaiveChatService:

    def get_response(self, prompt):
        client = OpenAISdk()
        return client.complete(prompt)


print("\nHardcoded Chat Service")
print(NaiveChatService().get_response("ping"))

# THINK BEFORE READING ON
#
# If leadership decides next
# quarter you also need
# Anthropic and Gemini,
#
# so users can pick a model,
#
# or you can fail over
# automatically if one vendor
# is down,
#
# what is fundamentally
# broken about ChatService as
# written?

# ============================================================
# THE DIAGNOSIS
# ============================================================

# ChatService is tightly
# coupled to one vendor's SDK.
#
# Adding a second provider
# means rewriting ChatService
# itself,
#
# instead of just adding new
# code beside it.

# BEFORE
#
# ChatService depends
# directly on OpenAIClient.
#
# New vendor?
#
# Must edit ChatService
# itself.
#
# Open/Closed broken.
#
# Same logic duplicated
# across many callers.

# ============================================================
# THE KEY QUESTION
# ============================================================

# So if hardcoding one
# vendor's class inside the
# calling service causes all
# of this,
#
# where should the
# responsibility for
#
#     "give me the right AI
#      client"
#
# actually live?

# Somewhere else.
#
# A dedicated place whose
# only job is deciding and
# building the correct
# client,
#
# so ChatService only ever
# depends on a generic
# interface.
#
# ChatService should not know
# how to BUILD a specific
# vendor's client.
#
# It should just ASK for one
# that matches an interface
# it already understands.
#
# This fixes both problems at
# once.

# ============================================================
# NAMING IT
# ============================================================

# FACTORY METHOD
#
# A method whose only job is
# to CREATE and RETURN an
# object of another, usually
# related, class.
#
# Nothing more.
#
# It is not always called out
# by name in every codebase.
#
# But it is probably the
# single most common
# creational pattern in real
# code,
#
# simply because it is this
# simple.

# ============================================================
# STEP 1 : DEFINE THE CONTRACT
# ============================================================

# One abstract base class
# every provider must
# implement.


class AIServiceClient(ABC):

    @abstractmethod
    def complete(self, prompt):
        ...


# ============================================================
# STEP 2 : IMPLEMENT EACH VENDOR
# ============================================================


class OpenAIClient(AIServiceClient):

    def complete(self, prompt):
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
# STEP 3 : THE FACTORY METHOD
# ============================================================

# Something still has to
# decide which concrete class
# to build.
#
# Let that something be a
# single method whose only
# job is
#
#     "return the correct
#      AIServiceClient"


class AIServiceClientProvider:

    @staticmethod
    def get_client(provider):
        if provider == "openai":
            return OpenAIClient()
        if provider == "anthropic":
            return AnthropicClient()
        if provider == "gemini":
            return GeminiClient()
        raise ValueError(f"Unknown provider: {provider}")


print("\nFactory Method In Action")

for name in ["openai", "anthropic", "gemini"]:
    built = AIServiceClientProvider.get_client(name)
    print(f"{name} -> {type(built).__name__}")

# Observation:
#
# A string went in.
#
# A different concrete class
# came back out each time.

# ============================================================
# STEP 4 : THE CALLER
# ============================================================


class ChatService:

    def __init__(self, provider):
        self.client = AIServiceClientProvider.get_client(provider)

    def get_response(self, prompt):
        return self.client.complete(prompt)


print("\nSame Service, Different Config")

for configured_provider in ["openai", "anthropic", "gemini"]:
    chat = ChatService(configured_provider)
    print(chat.get_response("ping"))

# ============================================================
# THE PAYOFF
# ============================================================

# THINK BEFORE READING ON
#
# What is the actual payoff?
#
# What happens to ChatService
# the day a fourth provider
# gets added?

# ChatService does not change
# at all.
#
# It only depends on the
# AIServiceClient interface.
#
# get_client() is the only
# place that needs to know
# about the new vendor's
# class.

# AFTER
#
# ChatService depends only on
# the AIServiceClient
# interface,
#
# implemented by OpenAIClient,
# AnthropicClient, and
# GeminiClient,
#
# all built by
# AIServiceClientProvider.
#
# New vendor?
#
# Add one new class only.
#
# ChatService is never
# touched.

# ============================================================
# EXTRA BEAT : PASSING CALL SPECIFIC DATA
# ============================================================

# So far get_client(provider)
# only needs one piece of
# information.
#
# Which type to build.
#
# THINK BEFORE READING ON
#
# What if building the object
# also needs data that is
# specific to THIS particular
# call,
#
# not just the type?
#
# Like a per user API key.
#
# Or a recipient's phone
# number, for the
# NotificationService
# example.
#
# Where should that extra
# data go?

# The factory method's
# signature just grows.
#
# It takes whatever extra
# parameters it needs to hand
# off to the constructor of
# the concrete class it is
# building.


class ConfiguredOpenAIClient(AIServiceClient):

    def __init__(self, api_key):
        self.api_key = api_key

    def complete(self, prompt):
        return f"response from OpenAI ({self.api_key})"


class ConfiguredAnthropicClient(AIServiceClient):

    def __init__(self, api_key):
        self.api_key = api_key

    def complete(self, prompt):
        return f"response from Anthropic ({self.api_key})"


class ConfiguredGeminiClient(AIServiceClient):

    def __init__(self, api_key):
        self.api_key = api_key

    def complete(self, prompt):
        return f"response from Gemini ({self.api_key})"


class ConfiguredClientProvider:

    @staticmethod
    def get_client(provider, api_key):
        if provider == "openai":
            return ConfiguredOpenAIClient(api_key)
        if provider == "anthropic":
            return ConfiguredAnthropicClient(api_key)
        if provider == "gemini":
            return ConfiguredGeminiClient(api_key)
        raise ValueError(f"Unknown provider: {provider}")


print("\nFactory Carrying Per Call Data")

client = ConfiguredClientProvider.get_client(
    "anthropic",
    "sk-user-123"
)

print(client.complete("summarise this"))

# ============================================================
# SAME IDEA, NOTIFICATION EXAMPLE
# ============================================================


class SmsChannel:

    def __init__(self, recipient):
        self.recipient = recipient

    def send(self, message):
        return f"SMS to {self.recipient}: {message}"


class EmailChannel:

    def __init__(self, recipient):
        self.recipient = recipient

    def send(self, message):
        return f"Email to {self.recipient}: {message}"


class PushChannel:

    def __init__(self, recipient):
        self.recipient = recipient

    def send(self, message):
        return f"Push to {self.recipient}: {message}"


class NotificationFactory:

    @staticmethod
    def get_sender(type_, recipient):
        if type_ == "SMS":
            return SmsChannel(recipient)
        if type_ == "EMAIL":
            return EmailChannel(recipient)
        if type_ == "PUSH":
            return PushChannel(recipient)
        raise ValueError(f"Unknown type: {type_}")


print("\nNotification Factory With Data")
print(NotificationFactory.get_sender("SMS", "+91-90000-00000").send("Hi"))
print(NotificationFactory.get_sender("EMAIL", "ops@example.com").send("Hi"))

# ============================================================
# IMPORTANT DISCUSSION
# ============================================================

# Does adding api_key or
# recipient change what kind
# of pattern this is?
#
# No.
#
# It is still a Factory
# Method.
#
# The job is still
#
#     decide which class,
#     then build and return it
#
# The method just now also
# forwards along whatever per
# call data that specific
# instance needs to be
# constructed correctly.

# Core Rule:
#
# get_client(provider)
#
# decides WHICH class to
# build.
#
# get_client(provider, api_key)
#
# also carries the DATA that
# instance needs.
#
# The decision logic and the
# data plumbing are different
# concerns,
#
# but the factory method is
# free to carry both at once.

# ============================================================
# THE SINGLE RESPONSIBILITY RISK
# ============================================================

# THINK BEFORE READING ON
#
# Now imagine this factory
# class starts picking up
# more jobs over time.
#
# get_client() for AI
# providers.
#
# Plus get_payment_gateway().
#
# Plus get_storage_client().
#
# All bundled into one giant
# ServiceProvider class,
#
# along with some unrelated
# app configuration logic.
#
# What is starting to go
# wrong?


class GodServiceProvider:
    """Deliberately bad. Do not copy this."""

    @staticmethod
    def get_client(provider):
        ...

    @staticmethod
    def get_payment_gateway(name):
        ...

    @staticmethod
    def get_storage_client(name):
        ...

    @staticmethod
    def load_app_config(path):
        ...


# Observation:
#
# That class now has
# multiple, unrelated jobs
# bundled together.
#
# A Single Responsibility
# violation.
#
# The same shape we have seen
# with earlier patterns.

# Core Rule:
#
# A single factory method is
# great for ONE family of
# things.
#
# Once a class starts hosting
# factory methods for many
# UNRELATED families of
# objects, it is doing too
# many jobs.
#
# Single Responsibility
# Principle broken.

# ============================================================
# QUIZ
# ============================================================

# What is the defining job of
# a factory method?
#
# A) Store reusable templates
# B) Copy an existing object
# C) Create and return an
#    object of another,
#    usually related, class
# D) Guarantee a single
#    instance
#
# Answer:
#
# C)

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Which principle does a
# hardcoded if/elif over
# concrete classes break?
#
# Open/Closed.
#
# Every new type forces an
# edit to code that already
# worked.

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# What does ChatService
# depend on once a factory is
# introduced?
#
# Only the AIServiceClient
# interface.
#
# Never a concrete vendor
# class.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Bundling factory methods
# for unrelated families of
# objects into one class.
#
# One factory class, one
# family.

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

# Hardcoding which class to
# build breaks Open/Closed,
#
# and duplicates the decision
# across every caller.
#
# A factory method creates
# and returns an object of
# another, usually related,
# class.
#
# Callers depend on an
# interface, never on a
# concrete vendor.
#
# The factory may also carry
# per call data into the
# constructor.
#
# One factory class should
# serve ONE family of
# objects.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Our AIServiceClient was
# just a contract.
#
# No stored data.
#
# No shared logic.
#
# Every method fully written
# out separately in each
# subclass.
#
# What if every client also
# needs to REMEMBER something
# in common?
#
# Like its own provider_name.
#
# Or a timeout_ms setting.
#
# And what if one method
# should be written ONCE and
# inherited by everyone,
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
#
# Next:
#
# 02_abc_pure_contract_vs_shared_state.py
