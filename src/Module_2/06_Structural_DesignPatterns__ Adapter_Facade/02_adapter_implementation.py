"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 02_adapter_implementation.py
============================================================

Topics Covered
--------------
1.  Where File 01 Left Us
2.  The Target Interface
3.  Who Makes Yes Bank Fit
4.  Why We Never Edit Third Party Code
5.  The Three Pieces Of The Pattern
6.  Why This Helps Long Term
7.  The Adaptee
8.  The Adapter
9.  Method Call Translation
10. The Client
11. The Complete Runtime Flow
12. Adding HDFC Tomorrow
13. Open / Closed In Action
14. Key Takeaways
"""

from abc import ABC, abstractmethod

# ============================================================
# WHERE FILE 01 LEFT US
# ============================================================

# PhonePe was calling Yes
# Bank's methods directly.
#
# It worked.
#
# It also meant that adding
# HDFC, or Yes Bank changing
# its API, or Yes Bank shutting
# down, all caused the same
# pain.
#
# We decided on the move:
#
# Step 1
#
# Make our own interface.
#
# Step 2
#
# Write something that
# translates our calls into
# Yes Bank's real calls.
#
# This file does both.

# ============================================================
# STEP 1 : WRITE THE INTERFACE FIRST
# ============================================================

# What does PhonePe need,
# regardless of which bank is
# behind it?
#
# Not what Yes Bank offers.
#
# What WE need.


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


# ============================================================
# NOTICE
# ============================================================

# These names are ours.
#
# pay.
#
# check_balance.
#
# transfer_funds.
#
# No bank chose them.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# PhonePe will now only talk
# to BankAPI.
#
# But Yes Bank never agreed to
# implement our interface.
#
# It is a third party.
#
# We do not control their
# code.
#
# So who makes Yes Bank's
# shape match BankAPI's shape?

# ============================================================
# THE ANSWER
# ============================================================

# We write our own class.
#
# It inherits from BankAPI.
#
# And inside it, it calls Yes
# Bank's real methods.

# ============================================================
# QUICK CHECK
# ============================================================

# Could we just edit Yes
# Bank's own source code
# instead?
#
# So that it matches BankAPI
# directly?
#
# Think before reading on.

# ============================================================
# NO, USUALLY NOT
# ============================================================

# It is third party code.
#
# We do not own it.
#
# And even if we could edit
# it, every update from Yes
# Bank would wipe out our
# changes.
#
# So we never touch the third
# party's code.
#
# We write our own small
# wrapper class instead.
#
# That wrapper is the Adapter.

# ============================================================
# BOARD SUMMARY
# ============================================================

# 3 PIECES OF THE
# ADAPTER PATTERN
#
# 1. Target Interface
#
#        what the CLIENT
#        expects
#
#        BankAPI
#
# 2. Adaptee
#
#        the existing,
#        incompatible class
#
#        YesBank
#
# 3. Adapter
#
#        implements Target,
#        wraps an Adaptee,
#        translates calls
#        between the two

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Besides just "it works
# today":
#
# Why does writing this
# Adapter actually help us
# long term?
#
# Try to name more than one
# reason.

# ============================================================
# THE REASONS
# ============================================================

# PhonePe stays free of any
# one bank's API.
#
# If Yes Bank changes or shuts
# down, only the adapter
# changes.
#
# PhonePe itself stays
# untouched.
#
# The same trick also works
# for old, legacy banking
# systems.
#
# Not just modern ones.
#
# Adding a new bank means
# adding a new adapter class.
#
# Not editing PhonePe's
# existing code.
#
# That is Open/Closed in
# action.
#
# Open to adding new banks.
#
# Closed to changing what
# already works.

# ============================================================
# BOARD SUMMARY
# ============================================================

# WHY THIS ACTUALLY MATTERS
#
#     Decoupling
#
#         PhonePe never depends
#         on one bank's API
#
#     Versioning
#
#         Bank changes its API?
#         Only the adapter
#         changes
#
#     Legacy systems
#
#         same trick works for
#         old systems too
#
#     Open/Closed
#
#         new bank = new adapter
#         class, not edited
#         PhonePe code

# ============================================================
# CHECKPOINT
# ============================================================

# Solid on the three pieces
# before we write the code?
#
# Target Interface.
#
# Adaptee.
#
# Adapter.

# ============================================================
# A SMALL DATA HOLDER
# ============================================================


class Bank:

    def __init__(self, account_number, account_holder_name):
        self.account_number = account_number
        self.account_holder_name = account_holder_name


# ============================================================
# THE ADAPTEE
# ============================================================

# Yes Bank's own real methods.
#
# Named however Yes Bank
# designed them.
#
# Completely different shape
# from our BankAPI interface.


class YesBank:

    def open_account(self, acc_number, holder_name):
        # Yes Bank's own account-creation logic
        print(f"  [YesBank] open_account({acc_number}, {holder_name})")

    def do_payment(self, account, amt):
        # Yes Bank's own payment logic
        # returns a status CODE, not a boolean — 0 means success
        print(f"  [YesBank] do_payment({account}, {amt})")
        return 0

    def get_acc_balance(self, account):
        # Yes Bank's own balance-check logic
        print(f"  [YesBank] get_acc_balance({account})")
        return 5000.0

    def do_fund_transfer(self, from_acc, to_acc, amt):
        # Yes Bank's own transfer logic
        print(f"  [YesBank] do_fund_transfer({from_acc}, {to_acc}, {amt})")


# ============================================================
# THE ADAPTER
# ============================================================


class YesBankAdapter(BankAPI):

    def __init__(self, yes_bank):
        self.yes_bank = yes_bank

    def add_bank_account(self, bank):
        # translate our method call into Yes Bank's real method call
        self.yes_bank.open_account(
            bank.account_number,
            bank.account_holder_name
        )

    def pay(self, amount, account):
        # Yes Bank returns an int status code, not a boolean —
        # this is the exact translation the Adapter exists for
        status = self.yes_bank.do_payment(account, amount)
        return status == 0

    def check_balance(self):
        # here the shape already matches, so the call passes straight through
        return self.yes_bank.get_acc_balance(None)

    def transfer_funds(self, source, destination, amount):
        # just renaming the call — Yes Bank calls it do_fund_transfer
        self.yes_bank.do_fund_transfer(source, destination, amount)


# ============================================================
# THE CLIENT
# ============================================================


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
# RUNNING IT
# ============================================================

print("Adapter Wiring")

yes_bank = YesBank()
bank_api = YesBankAdapter(yes_bank)
phone_pe = PhonePe(bank_api)

phone_pe.perform_bank_operations()

# Observation:
#
# Read PhonePe again.
#
# The words "Yes Bank" do not
# appear inside it.
#
# Not once.


# ============================================================
# THINK BEFORE READING ON
# ============================================================

# HDFC Bank support gets added
# tomorrow.
#
# What has to change inside
# PhonePe?

# ============================================================
# THE ANSWER
# ============================================================

# Nothing.
#
# Write a new HDFCBankAdapter,
# inheriting from BankAPI.
#
# Hand that in instead.
#
# PhonePe never changes.


# ============================================================
# CHECKPOINT
# ============================================================

# Solid on Adapter's shape?
#
# One interface we own.
#
# One third party class we
# do not own.
#
# One small wrapper joining
# them.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# The interface is written from
# the CLIENT's needs, not from
# what the vendor happens to
# offer.
#
# We never edit third party
# code.
#
# Even if we could, the next
# vendor update would wipe the
# edit out.
#
# The pattern has exactly three
# pieces:
#
#     Target Interface
#
#     Adaptee
#
#     Adapter
#
# The adapter's real work is
# translation — renaming a
# method, reordering arguments,
# converting a return type.
#
# Adding a bank means adding an
# adapter class, never editing
# PhonePe.
#
# That is Open/Closed.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We built this for banks.
#
# But nothing about the pattern
# was banking specific.
#
# Next we point the exact same
# structure at a problem many
# of you are already building:
#
# One app.
#
# Several LLM providers.
#
# Each with a different SDK.
#
# Next:
#
# 03_adapter_in_ai_systems.py
