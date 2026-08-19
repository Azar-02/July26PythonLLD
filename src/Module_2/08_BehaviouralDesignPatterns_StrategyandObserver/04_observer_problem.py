"""
============================================================
DESIGN PATTERNS : BEHAVIOURAL FAMILY
FILE : 04_observer_problem.py
============================================================

Topics Covered
--------------
1.  Where File 03 Left Us
2.  Subscribing To A Channel
3.  Observer : The General Idea
4.  Back To Amazon's Order Flow
5.  What Facade Actually Solved
6.  Adding Loyalty Points
7.  The Fraud Team's Problem
8.  The Gap Facade Never Closed
9.  The Reframe
10. Strategy vs Observer, In Spirit
11. Key Takeaways
"""

# ============================================================
# WHERE FILE 03 LEFT US
# ============================================================

# Strategy answered:
#
#     "how does the caller pick
#      ONE way out of several?"
#
# Today's second pattern asks
# something that sounds
# similar.
#
# And isn't.

# ============================================================
# WARM UP : SUBSCRIBING
# ============================================================

# Think about subscribing to a
# YouTube channel.
#
# When the creator uploads a
# new video —
#
# do they personally message
# every single subscriber?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# The creator just uploads.
#
# YouTube handles notifying
# everyone who's subscribed.
#
# The creator doesn't even
# need to know who's
# subscribed.
#
# Or how many people there
# are.

# ============================================================
# THE EVERYDAY SHAPE
# ============================================================

# One publisher.
#
# Many subscribers.
#
# And the publisher never
# needs to know who's
# listening.

# ============================================================
# BOARD SUMMARY
# ============================================================

# OBSERVER (the general idea)
#
#     ONE publisher.
#     MANY subscribers.
#
#     The publisher lets people
#     subscribe or unsubscribe,
#     and just announces when
#     something happens.
#
#     It never needs to know
#     who's listening, how many
#     there are, or what each
#     one plans to do about it.

# ============================================================
# BACK TO AMAZON
# ============================================================

# Remember Amazon's
# order_place() from the
# Facade lecture.
#
# Invoicing.
#
# Warehouse update.
#
# Inventory update.
#
# And email.
#
# All fired from one place.
#
# What problem did Facade
# actually solve there?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# It moved all that unrelated
# coordination work out of
# order_place().
#
# And into one
# OrderPlacedFacade class.
#
# Fixing an SRP violation.

# ============================================================
# THE FACADE, AS IT STOOD
# ============================================================


class Wms:

    def update(self):
        print("  [wms] warehouse updated")


class Ims:

    def update(self):
        print("  [ims] inventory updated")


class Emails:

    def send_email(self):
        print("  [emails] confirmation sent")


class OrderPlacedFacade:

    def __init__(self, wms, ims, emails):
        self.wms = wms
        self.ims = ims
        self.emails = emails

    def invoice_generation(self):
        print("  [invoice] invoice generated")

    def on_order_place(self):
        self.invoice_generation()
        self.wms.update()
        self.ims.update()
        self.emails.send_email()


print("The Facade From Last Lecture")

facade = OrderPlacedFacade(Wms(), Ims(), Emails())
facade.on_order_place()

# Observation:
#
# Four reactions.
#
# One place.
#
# Named, one by one, in
# source code.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now say marketing wants a
# loyalty-points update added.
#
# Every time an order is
# placed.
#
# What do you have to do ?

# ============================================================
# THE ANSWER
# ============================================================

# Go back into
# on_order_place().
#
# And add one more line.
#
#     def on_order_place(self):
#         self.invoice_generation()
#         self.wms.update()
#         self.ims.update()
#         self.emails.send_email()
#         self.loyalty.update()     # <-- the edit
#
# It works.
#
# But notice what it cost.
#
# Existing, working code had
# to be reopened.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now say a separate
# fraud-detection team wants
# to add their own check.
#
# But they don't want to touch
# your OrderPlacedFacade class
# at all.
#
# Can the Facade support that?

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# Facade still means editing
# its own source code every
# time something new needs to
# happen.
#
# It cleaned up the
# coordination problem.
#
# But it never solved the
# "let other people plug in"
# problem.

# ============================================================
# THE REFRAME
# ============================================================

# So here's the reframe.
#
# Instead of Amazon calling
# every interested party by
# name —
#
# what if Amazon just
# announced
#
#     "an order was placed"
#
# and let anyone interested
# subscribe to that
# announcement?
#
# Without ever needing to know
# who's listening.

# ============================================================
# BOARD SUMMARY
# ============================================================

# FACADE fixed:
#
#     too much coordination
#     logic sitting in one
#     place
#
# FACADE did NOT fix:
#
#     adding a new reaction
#     still means editing
#     existing code — an
#     outside team still can't
#     plug in without touching
#     your class
#
# OBSERVER fixes exactly that
# gap.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Quick check against what we
# just learned.
#
# Strategy and Observer both
# involve one interface with
# multiple classes
# implementing it.
#
# What's actually different in
# SPIRIT between the two?

# ============================================================
# THE ANSWER
# ============================================================

# Strategy picks exactly ONE
# implementation.
#
# And uses just that one.
#
# Observer runs potentially
# MANY implementations.
#
# All at once.
#
# It's not "pick one".
#
# It's "notify everyone who's
# listening".
#
# Hold onto that thought.
#
# We'll come back to it
# properly later.

# ============================================================
# CHECKPOINT
# ============================================================

# Two things should be solid
# before we code this.
#
# One.
#
# One publisher, many
# subscribers, and the
# publisher knowing none of
# them.
#
# Two.
#
# Why Facade fixed the mess
# but not the plug-in problem.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# A YouTube creator uploads
# once, and everyone
# subscribed gets told.
#
# The creator never learns who
# they are.
#
# Facade solved a real problem
# — coordination logic piling
# up inside order_place().
#
# It did not solve who is
# allowed to add a new
# reaction.
#
# Every new reaction still
# means editing the Facade's
# own source.
#
# An outside team cannot plug
# in without touching your
# class.
#
# Observer closes exactly that
# gap, by announcing instead
# of calling by name.
#
# Strategy picks one
# implementation. Observer
# runs many.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We know what we want now.
#
# Amazon announces.
#
# Interested parties
# subscribe.
#
# Two questions remain open.
#
# What does every subscriber
# have to implement, so Amazon
# can treat them all the same
# way?
#
# And where does a subscriber
# actually sign up —
#
# without Amazon holding a
# hardcoded list of names?
#
# Next:
#
# 05_observer_implementation.py
