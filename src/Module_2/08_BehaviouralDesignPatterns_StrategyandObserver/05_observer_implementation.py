"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 05_observer_implementation.py
============================================================

Topics Covered
--------------
1.  Where File 04 Left Us
2.  What Every Subscriber Must Implement
3.  The Subscriber Interface
4.  The Publisher And Its List
5.  Where A Subscriber Registers Itself
6.  The First Two Subscribers
7.  Running It
8.  The Real Test : An Outside Team
9.  FraudCheck Plugs In
10. Leaving The List
11. Quiz : Facade vs Observer
12. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 04 LEFT US
# ============================================================

# Facade fixed the mess.
#
# It did not fix who is
# allowed to add a new
# reaction.
#
# The reframe:
#
#     Amazon announces.
#
#     Interested parties
#     subscribe.
#
# Now we write it.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What does every subscriber
# need to implement,
#
# so Amazon can treat all of
# them the same way?

# ============================================================
# THE ANSWER
# ============================================================

# One common interface.
#
# With one method.
#
# Something like:
#
#     on_order_placed()

# ============================================================
# THE SUBSCRIBER INTERFACE
# ============================================================


class OrderPlacedSubscriber(ABC):

    @abstractmethod
    def on_order_placed(self, order):
        ...


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Amazon needs a list of
# subscribers.
#
# Plus a way for people to
# join or leave that list.
#
# What would that look like?

# ============================================================
# THE PUBLISHER
# ============================================================


class Amazon:

    def __init__(self):
        self.subscribers = []

    def register_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def unregister_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def order_placed(self, order):
        for subscriber in self.subscribers:
            subscriber.on_order_placed(order)


# ============================================================
# NOTICE WHAT IS MISSING
# ============================================================

# No invoice.
#
# No warehouse.
#
# No email.
#
# Amazon names nobody.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Here's a question worth
# pausing on.
#
# Where should each subscriber
# actually register itself?
#
# Should Amazon keep a
# hardcoded list of every
# subscriber by name, inside
# its own code?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# Each subscriber should
# register ITSELF.
#
# Usually right when it's
# created.
#
# That way, Amazon never needs
# to know the full list of
# subscribers ahead of time.

# ============================================================
# THE FIRST TWO SUBSCRIBERS
# ============================================================


class InvoiceGenerator(OrderPlacedSubscriber):

    def __init__(self, amazon):
        amazon.register_subscriber(self)

    def on_order_placed(self, order):
        print(f"  [invoice] generated for {order}")


class WarehouseInventory(OrderPlacedSubscriber):

    def __init__(self, amazon):
        amazon.register_subscriber(self)

    def on_order_placed(self, order):
        print(f"  [warehouse] inventory updated for {order}")


# ============================================================
# RUNNING IT
# ============================================================

print("Two Subscribers")

amazon = Amazon()

InvoiceGenerator(amazon)
WarehouseInventory(amazon)

amazon.order_placed("ORDER-42")

# Observation:
#
# Amazon announced once.
#
# Two things reacted.
#
# Amazon called neither by
# name.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now the real test.
#
# Can that fraud-detection
# team add their own reaction,
#
# without touching a single
# line inside Amazon?

# ============================================================
# THE ANSWER
# ============================================================

# Yes.
#
# They just write FraudCheck,
# inheriting from
# OrderPlacedSubscriber.
#
# Register it in their own
# constructor.
#
# And that's it.
#
# Amazon never needs to
# change.


class FraudCheck(OrderPlacedSubscriber):

    def __init__(self, amazon):
        amazon.register_subscriber(self)

    def on_order_placed(self, order):
        print(f"  [fraud] checks run on {order}")


# ============================================================
# RUNNING IT AGAIN
# ============================================================

print("\nThe Fraud Team Plugs In")

fraud = FraudCheck(amazon)

amazon.order_placed("ORDER-43")

# Observation:
#
# Three reactions now.
#
# Scroll up and read the
# Amazon class again.
#
# Not one line of it changed.

# ============================================================
# LEAVING THE LIST
# ============================================================

# Subscribing is only half of
# it.
#
# People can leave too.

print("\nAfter Unregistering Fraud")

amazon.unregister_subscriber(fraud)

amazon.order_placed("ORDER-44")

# Observation:
#
# Back to two.
#
# Again, without editing
# Amazon.


# ============================================================
# QUIZ
# ============================================================

# What's the real difference
# between how Facade and
# Observer let you add a new
# reaction to an event?
#
# A) There's no real
#    difference
#
# B) Facade needs you to edit
#    its own source code;
#    Observer lets a new
#    reaction register itself
#    without touching any
#    existing code
#
# C) Observer needs editing
#    existing code; Facade
#    doesn't
#
# D) Both need the same amount
#    of editing
#
# Answer:
#
# B)

# ============================================================
# CHECKPOINT
# ============================================================

# Solid on the shape?
#
# A subscriber interface.
#
# A publisher holding a list.
#
# Subscribers signing
# themselves up.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Every subscriber implements
# one interface with one
# method, so the publisher can
# treat them identically.
#
# Amazon holds a list, offers
# register and unregister, and
# loops over it.
#
# It names no subscriber
# anywhere.
#
# Each subscriber registers
# itself, usually in its own
# constructor.
#
# So the publisher never needs
# the full list ahead of time.
#
# A new team adds a reaction
# by writing one class — no
# edit to Amazon at all.
#
# That is the exact gap Facade
# left open.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We built this for orders.
#
# Next, the same structure
# somewhere you have watched
# it happen, character by
# character, without naming
# it.
#
# An LLM streaming a response.
#
# Next:
#
# 06_observer_in_a_real_backend.py
