"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 06_adapter_vs_facade_and_ai_corner.py
============================================================

Topics Covered
--------------
1.  Recap Setup From Earlier Files
2.  Both Patterns Wrap Something
3.  Ask Why The Wrapper Exists
4.  Compatibility vs Complexity
5.  The Logging Services Test Case
6.  AI Corner : The Goal
7.  Step 1 — The Code With The Mistake
8.  Step 2 — Asking AI To Diagnose
9.  Counting The Couplings
10. Step 3 — Choosing An Option, Writing The Fix
11. Step 4 — What The AI Was Useful For
12. Wrap-Up : The Whole Picture
13. Homework
"""

from abc import ABC, abstractmethod

# ============================================================
# RECAP SETUP
# ============================================================

# Everything in this block was
# built in files 01 to 05.
#
# It is repeated here only so
# this file runs on its own.
#
# Nothing below is new.


class Bank:

    def __init__(self, account_number, account_holder_name):
        self.account_number = account_number
        self.account_holder_name = account_holder_name


class BankAPI(ABC):

    @abstractmethod
    def add_bank_account(self, bank):
        ...

    @abstractmethod
    def pay(self, amount, account):
        ...

    @abstractmethod
    def check_balance(self):
        ...

    @abstractmethod
    def transfer_funds(self, source, destination, amount):
        ...


class YesBank:

    def open_account(self, acc_number, holder_name):
        print(f"  [YesBank] open_account({acc_number}, {holder_name})")

    def do_payment(self, account, amt):
        # returns a status CODE, not a boolean — 0 means success
        print(f"  [YesBank] do_payment({account}, {amt})")
        return 0

    def get_acc_balance(self, account):
        return 5000.0

    def do_fund_transfer(self, from_acc, to_acc, amt):
        print(f"  [YesBank] do_fund_transfer({from_acc}, {to_acc}, {amt})")


class YesBankAdapter(BankAPI):

    def __init__(self, yes_bank):
        self.yes_bank = yes_bank

    def add_bank_account(self, bank):
        self.yes_bank.open_account(
            bank.account_number,
            bank.account_holder_name
        )

    def pay(self, amount, account):
        status = self.yes_bank.do_payment(account, amount)
        return status == 0

    def check_balance(self):
        return self.yes_bank.get_acc_balance(None)

    def transfer_funds(self, source, destination, amount):
        self.yes_bank.do_fund_transfer(source, destination, amount)


class HDFCBank:

    def create_account(self, acc_number, holder_name):
        print(f"  [HDFC] create_account({acc_number}, {holder_name})")

    def make_payment(self, account, amount):
        print(f"  [HDFC] make_payment({account}, {amount})")
        return True

    def balance_enquiry(self, account):
        return 7200.0

    def move_money(self, from_acc, to_acc, amount):
        print(f"  [HDFC] move_money({from_acc}, {to_acc}, {amount})")


class HDFCBankAdapter(BankAPI):

    def __init__(self, hdfc_bank):
        self.hdfc_bank = hdfc_bank

    def add_bank_account(self, bank):
        self.hdfc_bank.create_account(
            bank.account_number,
            bank.account_holder_name
        )

    def pay(self, amount, account):
        return self.hdfc_bank.make_payment(account, amount)

    def check_balance(self):
        return self.hdfc_bank.balance_enquiry(None)

    def transfer_funds(self, source, destination, amount):
        self.hdfc_bank.move_money(source, destination, amount)


class PhonePe:

    def __init__(self, bank_api):
        self.bank_api = bank_api

    def perform_bank_operations(self):
        bank = Bank("1234567890", "John Doe")
        self.bank_api.add_bank_account(bank)

        paid = self.bank_api.pay(100.0, "1234567890")
        if paid:
            self.bank_api.transfer_funds(
                "1234567890",
                "9876543210",
                50.0
            )


# ============================================================
# BOTH PATTERNS WRAP SOMETHING
# ============================================================

# Adapter wraps something.
#
# Facade wraps something.
#
# Both give the client a
# cleaner surface to talk to.
#
# So here is the real
# question.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# In a design review, how
# would you tell whether a new
# wrapper class is an Adapter
# or a Facade?
#
# Take your time on this one.
#
# Work it through before you
# read the answer.

# ============================================================
# THE TEST
# ============================================================

# Ask WHY the wrapper exists.
#
# Two interfaces do not fit
# together and need
# translating
#
#     -> Adapter
#
# One thing is doing too much
# and needs to be simplified
# or hidden
#
#     -> Facade
#
# Not what it looks like.
#
# Why it exists.

# ============================================================
# BOARD SUMMARY
# ============================================================

# ADAPTER
#
#     "These two things don't
#      fit — translate."
#
#     Usually ONE adaptee
#     being wrapped
#
#     The problem is
#     COMPATIBILITY
#
# FACADE
#
#     "This is too complicated
#      — simplify."
#
#     Usually MULTIPLE
#     subsystems being
#     coordinated
#
#     The problem is
#     COMPLEXITY,
#     not compatibility
#
# They often show up TOGETHER
# — a Facade can use several
# Adapters inside it, to talk
# to different third-party
# systems.

# ============================================================
# TEST CASE
# ============================================================

# You have a class that talks
# to three different logging
# services.
#
# Each with a different API.
#
# It combines their output
# into one log stream.
#
# Is this an Adapter, a
# Facade, or both?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# Both.
#
# One Adapter per logging
# service, to normalise each
# one's different API.
#
# All three Adapters sit
# inside one Facade, which
# exposes a single, simple
# log() method.

# ============================================================
# IMPORTANT
# ============================================================

# Real systems almost never
# use just one pattern in
# isolation.
#
# If a pattern answer feels
# too quick or too confident,
# push back with:
#
#     "could this actually be
#      two patterns working
#      together?"

# 
# ============================================================
# AI CORNER : THE GOAL
# ============================================================

# BRING YOUR BUGGY CODE,
# NOT JUST YOUR PROMPT
#
# So far we have used AI to
# GENERATE code.
#
# This time we flip it.
#
# The code gets written by
# hand.
#
# Badly, on purpose.
#
# Then it is pasted into an AI
# assistant with one question:
#
#     "What's wrong with this,
#      and how would you fix
#      it?"
#
# This mirrors real work.
#
# You often already have code,
# written by a human, that
# quietly broke a pattern.
#
# The AI's job here is not to
# write from scratch.
#
# It is to diagnose and
# propose.
#
# The final fix still gets
# written by hand, after the
# discussion.

# ============================================================
# WHAT THE CODE INVOLVES
# ============================================================

# An Adapter.
#
#     HDFCBankAdapter
#
# And a Facade.
#
#     PhonePeFacade
#
# sitting in front of
# PhonePe's banking logic.
#
# The mistake is baked into
# how the Facade is USED.
#
# Not into the Adapter itself.
#
# Keep that in mind while
# reading.

# ============================================================
# STEP 1 OF 4 : THE CODE WITH THE MISTAKE
# ============================================================

# We already have PhonePe
# working with a YesBankAdapter
# through the BankAPI
# interface.
#
# Now we are adding a
# PhonePeFacade to simplify
# the checkout flow for the
# app team.
#
# Hide the bank-selection
# details behind one simple
# method.
#
# HDFC support and the facade
# get added by hand.
#
# No AI yet.


class BadPhonePeFacade:

    def __init__(self, phone_pe):
        self.phone_pe = phone_pe

    def checkout(self, amount, account, bank_name):
        if bank_name == "YesBank":
            self.phone_pe.bank_api = YesBankAdapter(YesBank())
        elif bank_name == "HDFCBank":
            self.phone_pe.bank_api = HDFCBankAdapter(HDFCBank())

        return self.phone_pe.bank_api.pay(amount, account)


print("Step 1 : The Flawed Facade")

bad_facade = BadPhonePeFacade(PhonePe(YesBankAdapter(YesBank())))
print(bad_facade.checkout(500, "12345", "YesBank"))
print(bad_facade.checkout(500, "12345", "HDFCBank"))

# Observation:
#
# This compiles.
#
# Checkout works for both
# banks.
#
# And it looks like exactly
# what a Facade is supposed to
# do — give callers one simple
# method.
#
# Leave it there for a second.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Just from reading it.
#
# Does anything feel off?
#
# Do not overthink it yet.

# ============================================================
# STEP 2 OF 4 : ASK AI TO DIAGNOSE, NOT REWRITE
# ============================================================

# Instead of guessing, paste
# it into an AI assistant and
# ask it to review.
#
# Not to fix.
#
# The prompt used:
#
#     "Here's a Facade we added
#      in front of PhonePe.
#      PhonePe already uses
#      Adapter classes
#      (YesBankAdapter,
#      HDFCBankAdapter) that
#      implement a common
#      BankAPI interface, so
#      PhonePe itself never has
#      to know which bank it's
#      talking to. Can you
#      review this Facade and
#      tell me if anything is
#      wrong with it, and what
#      the possible fixes are?
#      Don't rewrite it yet —
#      just diagnose first."
#
# followed by the
# PhonePeFacade code from
# Step 1.

# ============================================================
# THE AI RESPONSE : DIAGNOSIS
# ============================================================

# Functionally this works —
# checkout succeeds for both
# banks. But there's a design
# issue: the whole point of the
# Adapter setup was that
# PhonePe never needs an
# if/elif to pick a bank. This
# Facade just moved that same
# if/elif one layer up, into
# itself. It didn't remove the
# coupling — it relocated it,
# and gave it a friendlier
# name.
#
# This matters because a
# Facade's job is to simplify a
# set of existing,
# already-decoupled calls for
# the caller. It isn't supposed
# to become a new place that
# knows every adapter's name
# and construction details. As
# written, adding a third bank
# means editing PhonePeFacade —
# the exact "editing existing
# code to add a bank" problem
# the Adapter was built to
# avoid in the first place.
#
# Possible fixes:
#
# 1. Keep bank selection
#    outside the Facade
#    entirely — the caller
#    builds the right adapter
#    and hands it to PhonePe
#    (or to the Facade) already
#    assembled. The Facade's
#    checkout() just calls
#    pay(), nothing more.
#
# 2. Add a small lookup (e.g. a
#    dict of bank_name ->
#    adapter class, or a
#    registry) so PhonePeFacade
#    doesn't hardcode each bank
#    by name, and a new bank
#    means registering a class,
#    not editing an if/elif.
#
# 3. If PhonePe is only ever
#    going to support exactly
#    these two banks with no
#    plans to add more, leave it
#    as is — but that should be
#    a deliberate call, not a
#    default.
#
# Option 1 fits your existing
# pattern with the least new
# machinery — the Facade should
# be simplifying calls, not
# deciding which adapter to
# build. Option 2 is worth it
# only if bank selection needs
# to stay inside the Facade for
# some other reason.


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Notice what the AI did here.
#
# It did not just say "this is
# wrong."
#
# What did it actually give
# us?

# ============================================================
# THE ANSWER
# ============================================================

# A diagnosis of WHY it is a
# problem.
#
# Tied back to what the
# Adapter was for.
#
# And to what a Facade is
# actually supposed to do.
#
# Plus more than one option.
#
# Not just one forced answer.

# ============================================================
# STEP 3 OF 4 : DISCUSS, THEN FIX BY HAND
# ============================================================

# Of the three options the AI
# gave, which one actually
# fits what we are doing?
#
# And why?
#
# Think before reading on.

# ============================================================
# THE CHOICE
# ============================================================

# Option 1.
#
# Keep bank selection out of
# the Facade.
#
# We do not have a stated need
# for a registry yet.
#
# Option 2 is over-engineering
# for now.
#
# And quietly accepting the
# if/elif — option 3 — undoes
# the whole point of using
# Adapter in the first place.
#
# Now that the class has
# decided, the fix gets
# written by hand.
#
# The AI did not write this
# code.
#
# We did, after the
# discussion.


class PhonePeFacade:

    def __init__(self, phone_pe):
        self.phone_pe = phone_pe

    def checkout(self, amount, account):
        # PhonePe already holds whichever BankAPI adapter it was given —
        # the Facade just simplifies the call, it doesn't choose the bank.
        return self.phone_pe.bank_api.pay(amount, account)


print("\nStep 3 : The Fix")

# Caller assembles the adapter and hands it in — same as before,
# neither PhonePe nor PhonePeFacade need to change for a new bank.
bank_api = HDFCBankAdapter(HDFCBank())
phone_pe = PhonePe(bank_api)
facade = PhonePeFacade(phone_pe)
print(facade.checkout(amount=500, account="12345"))

# Observation:
#
# checkout() lost a parameter.
#
# bank_name is gone.
#
# The Facade no longer knows
# any bank by name.

# ============================================================
# STEP 4 OF 4 : WHAT THE AI WAS USEFUL FOR
# ============================================================

# Think back over the whole
# exercise.
#
# What did the AI actually
# contribute?
#
# And what did it not do?

# ============================================================
# THE ANSWER
# ============================================================

# It did not write any of the
# code we shipped.
#
# It reviewed code we wrote.
#
# It explained why the Facade
# had quietly re-introduced
# the coupling the Adapter was
# meant to remove.
#
# And it laid out real options
# with a trade-off for each.
#
# Instead of silently "fixing"
# it its own way.
#
# The actual decision and the
# actual fix were still ours.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Used as a generator:
#
#     AI writes code, you hope
#     it kept the design.
#
# Used as a reviewer:
#
#     AI explains what's wrong
#     and why, gives you
#     options, YOU decide, YOU
#     write the fix.
#
# A Facade that hardcodes
# if/elif on adapter names
# hasn't simplified anything —
# it's just moved the coupling
# one layer up.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the difference
# between a Facade that
# simplifies existing
# decoupled calls
#
# versus one that quietly
# becomes a new if/elif chain?

# ============================================================
# WRAP-UP
# ============================================================

# ADAPTER
#
#     Makes two incompatible
#     interfaces work together
#
#     Doesn't touch either
#     side
#
#     Built from:
#     Target Interface +
#     Adaptee + Adapter
#
#     One adaptee, wrapped
#
# FACADE
#
#     Hides several complex
#     subsystems behind one
#     simple entry point
#
#     Multiple subsystems,
#     coordinated
#
# THE TEST
#
#     Ask WHY the wrapper
#     exists
#
#     Incompatibility
#         -> Adapter
#
#     Complexity
#         -> Facade
#
#     Often both, together, in
#     the same real system

# ============================================================
# YOU HAVE ALREADY HIT THESE
# ============================================================

# You have likely already hit
# both of today's problems
# without naming them.
#
# Swapping a database driver,
# an LLM SDK, or a payment
# gateway
#
#     -> Adapter
#
# A checkout() or run() method
# that quietly coordinates
# five things behind it
#
#     -> Facade

# ============================================================
# HOMEWORK
# ============================================================

# 1. Extend YesBankAdapter
#    with an HDFCBankAdapter,
#    where HDFC's real methods
#    return an int status code
#    instead of a boolean.
#    Write down, yourself,
#    exactly which int values
#    mean success — before
#    writing the translation.
#
# 2. Build the AgentFacade
#    sketch from file 05 into
#    real, even stubbed, code —
#    retriever, planner,
#    tool_executor, memory as
#    separate classes,
#    coordinated by one Facade.
#
# 3. Find one real Adapter and
#    one real Facade in any
#    library or SDK you've
#    used. Write two lines
#    identifying the Target
#    Interface / Adaptee /
#    Adapter, or the subsystems
#    a Facade is coordinating.
#
# 4. Push all your code to
#    GitHub, on a branch named:
#
#        adapter-facade-lecture-complete

# ============================================================
# BRIDGE TO THE NEXT CLASS
# ============================================================

# Today's problem was:
#
#     "how do we make things
#      fit together"
#
# Either by translating an
# incompatible interface.
#
# Or by hiding coordination
# complexity behind a simple
# entry point.
#
# Next class:
#
# Decorator and Flyweight.
#
# Adding behaviour to an
# object at runtime without
# touching its class.
#
# And handling far too many
# nearly-identical objects
# eating memory.
