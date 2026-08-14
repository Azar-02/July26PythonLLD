"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 01_structural_intro_and_adapter_problem.py
============================================================

Topics Covered
--------------
1.  Recap Of The Creational Family
2.  A New Bucket Of Patterns
3.  Creational vs Structural
4.  Today's Roadmap
5.  A Real Physical Adapter
6.  The Dongle In The Middle
7.  Adapter : The General Idea
8.  PhonePe Talks To Yes Bank
9.  What Breaks Tomorrow
10. Why Direct Coupling Hurts
11. The Move We Have Made Before
12. Key Takeaways
"""

# ============================================================
# RECAP OF LAST CLASS
# ============================================================

# We finished Creational
# Patterns.
#
# Singleton.
#
# Builder.
#
# Prototype / Registry.
#
# Factory.
#
# Four patterns.
#
# All four answered exactly
# one question:
#
#     "How and when should an
#      object get CREATED?"

# ============================================================
# A NEW BUCKET
# ============================================================

# Today we start a new bucket.
#
# Structural Patterns.
#
# Question before reading on:
#
#     Just going by that name,
#     what kind of question do
#     you think these patterns
#     answer instead?
#
# Think about it.
#
# Then read the next block.

# ============================================================
# THE ANSWER
# ============================================================

# How classes and objects are
# organised.
#
# How they are connected to
# each other.
#
# Not how they are created.
#
# Structural patterns are about
# how the pieces of a system
# fit together.

# ============================================================
# BOARD SUMMARY
# ============================================================

# CREATIONAL PATTERNS
#
#     HOW and WHEN objects
#     get created
#
# STRUCTURAL PATTERNS
#
#     HOW objects are organised
#     and connected
#
# Today:
#
#     Adapter
#
#     Facade

# ============================================================
# ONE IMPORTANT NOTE
# ============================================================

# Both patterns today are about
# fitting things together.
#
# But for different reasons.
#
# We will nail down that
# difference by the end of
# this class.
#
# Keep the question open until
# then.

# ============================================================
# WARM UP : NAME A REAL ADAPTER
# ============================================================

# Before any code.
#
# Think of a real, physical
# adapter you have used.
#
# Name one.
#
# Some answers:
#
# A phone charger.
#
# A USB-C to HDMI dongle.
#
# A plug adapter when
# travelling.

# ============================================================
# THE DONGLE
# ============================================================

# Take the USB-C to HDMI
# dongle.
#
# Your laptop only has USB-C.
#
# The projector only wants
# HDMI.
#
# Neither side changed.
#
# So what is the dongle
# actually doing?
#
# Think before reading on.

# ============================================================
# WHAT THE DONGLE IS DOING
# ============================================================

# It sits in between.
#
# It translates the signal
# from one format to another.
#
# Neither the laptop nor the
# projector had to change.
#
# That is the whole idea
# behind this pattern too.

# ============================================================
# BOARD SUMMARY
# ============================================================

# ADAPTER (general idea)
#
#     A middle layer that
#     connects two things that
#     do not fit together
#
#     WITHOUT changing
#     either side.

# ============================================================
# REMEMBER THIS PHRASE
# ============================================================

# "without changing
#  either side"
#
# It is the key to this
# whole pattern.
#
# Every decision we make from
# here traces back to it.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the general idea?
#
# Now the real backend
# problem.

# ============================================================
# THE PROBLEM : PHONEPE
# ============================================================

# Say you are building
# PhonePe.
#
# Today it talks to Yes Bank's
# API.
#
# Yes Bank has its own method
# names.
#
# Maybe:
#
#     do_payment()
#
#     get_acc_balance()
#
# Those names were chosen by
# Yes Bank.
#
# Not by us.

# ============================================================
# THE THIRD PARTY
# ============================================================

# This is Yes Bank's code.
#
# We do not own it.
#
# We are only calling it.


class YesBank:

    def do_payment(self, account, amt):
        print(f"  [YesBank] do_payment({account}, {amt})")
        return 0

    def get_acc_balance(self, account):
        print(f"  [YesBank] get_acc_balance({account})")
        return 5000.0


# ============================================================
# CALLING IT DIRECTLY
# ============================================================

# Now the version we are
# warning about.
#
# The entire PhonePe codebase
# calls Yes Bank's methods
# directly.
#
# Everywhere.


class PhonePe:

    def __init__(self):
        self.yes_bank = YesBank()

    def pay(self, amount, account):
        status = self.yes_bank.do_payment(account, amount)
        return status == 0

    def show_balance(self, account):
        return self.yes_bank.get_acc_balance(account)


print("PhonePe Tied To Yes Bank")

phone_pe = PhonePe()
print(phone_pe.pay(100.0, "1234567890"))
print(phone_pe.show_balance("1234567890"))

# Observation:
#
# It works.
#
# Nothing is broken today.
#
# That is exactly why this
# design survives long enough
# to become a problem.

# ============================================================
# COUNT THE TOUCH POINTS
# ============================================================

# In this tiny file, Yes Bank
# is named in:
#
#     __init__
#
#     pay
#
#     show_balance
#
# Three places.
#
# In a real PhonePe codebase,
# it is everywhere.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# The business now also wants
# to support HDFC Bank.
#
# What happens?
#
# Do not read the next block
# until you have an answer.

# ============================================================
# WHAT HAPPENS
# ============================================================

# You would have to rewrite
# a lot of code.
#
# HDFC's method names would
# be different.
#
# Its parameters would be
# different.
#
# Everything would be
# different.
#
# And every one of those
# touch points has to be
# found and edited.

# ============================================================
# BOARD SUMMARY
# ============================================================

# PROBLEM
#
# PhonePe is directly tied to
# Yes Bank's API.
#
#     Adding HDFC
#         -> almost a full
#            rewrite of the
#            payment code
#
#     Yes Bank API changes
#         -> same pain again
#
#     Yes Bank shuts down
#         -> same pain again

# ============================================================
# NOTICE THE SHAPE
# ============================================================

# Three different events.
#
# Adding a bank.
#
# A bank changing its API.
#
# A bank disappearing.
#
# One single cause behind
# all three.
#
# PhonePe knows a specific
# bank by name.

# ============================================================
# WE HAVE SOLVED THIS BEFORE
# ============================================================

# Think back to the Factory
# lecture.
#
# ChatService never cared
# which AI vendor was
# underneath.
#
# Why not?
#
# Because it only talked to
# one interface.
#
# Question:
#
#     What is the same move
#     here?
#
# Think before reading on.

# ============================================================
# THE SAME MOVE
# ============================================================

# Step 1
#
# Make our own interface.
#
# What PhonePe actually needs
# from ANY bank.
#
# Step 2
#
# Write something that
# translates our interface's
# calls into Yes Bank's real
# calls.
#
# Notice what Step 2 is.
#
# It is the dongle.

# ============================================================
# CHECKPOINT
# ============================================================

# Two things should be solid
# before moving on.
#
# One.
#
# What a middle layer does,
# and what it must not do.
#
#     It must not change
#     either side.
#
# Two.
#
# Why calling Yes Bank
# directly hurts, in three
# separate future events,
# not just one.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Creational patterns asked
# how and when objects get
# created.
#
# Structural patterns ask how
# objects are organised and
# connected.
#
# An Adapter is a middle layer
# connecting two things that
# do not fit, without changing
# either side.
#
# PhonePe calling Yes Bank
# directly works today, and
# breaks on the next business
# request.
#
# The fix has the same shape
# as the Factory lecture:
#
#     our own interface,
#
#     plus something that
#     translates.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We now know what we want.
#
# Our own interface.
#
# Plus a translator.
#
# Two questions remain open:
#
# What exactly does that
# interface look like?
#
# And who is allowed to write
# the translator, given that
# Yes Bank's code is not ours
# to edit?
#
# Next:
#
# 02_adapter_implementation.py
