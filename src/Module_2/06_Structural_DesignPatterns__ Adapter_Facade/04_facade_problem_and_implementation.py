"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 04_facade_problem_and_implementation.py
============================================================

Topics Covered
--------------
1.  Where File 03 Left Us
2.  What "Facade" Means
3.  Walking Into A Bank
4.  Facade : The General Idea
5.  The Amazon Order Problem
6.  The Obvious Version
7.  What Is Wrong With It
8.  Who Takes Over Coordination
9.  Pulling It Into Its Own Class
10. What The Caller Needs To Know
11. The Facade With Real Dependencies
12. Dependency Injection Inside A Facade
13. Quiz : Adapter vs Facade
14. Key Takeaways
"""

# ============================================================
# WHERE FILE 03 LEFT US
# ============================================================

# Adapter is finished.
#
# It solved one kind of
# problem:
#
#     two things that do not
#     fit together.
#
# Today's second pattern
# solves a different one.
#
# Not incompatibility.
#
# Too much complexity sitting
# in one place.

# ============================================================
# WHAT THE WORD MEANS
# ============================================================

# "Facade" literally means the
# outer face of a building.
#
# It is the clean, simple thing
# you see from the street.
#
# Hiding everything messy
# behind it.
#
# That is the idea we are
# borrowing today.

# ============================================================
# WALKING INTO A BANK
# ============================================================

# You walk into a bank to open
# an account.
#
# Behind the scenes, that
# touches:
#
# KYC checks.
#
# A core banking database.
#
# A card issuing system.
#
# A notifications service.
#
# Question:
#
#     Do you, the customer,
#     talk to all four systems
#     yourself?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# No.
#
# You talk to one relationship
# manager.
#
# They coordinate everything
# for you.
#
# That manager is acting as a
# Facade.
#
# One simple entry point.
#
# Hiding several complex
# systems behind it.

# ============================================================
# BOARD SUMMARY
# ============================================================

# FACADE (general idea)
#
#     One simple entry point
#     that hides the
#     coordination of several
#     complex systems behind
#     it.

# ============================================================
# NOW PUT IT IN CODE
# ============================================================

# Think about Amazon's
# order_place().
#
# Placing an order needs to
# trigger several things
# behind the scenes.
#
# What comes to mind?
#
# Think before reading on.

# ============================================================
# THE FOUR THINGS
# ============================================================

# Generate an invoice.
#
# Update the warehouse.
#
# Update inventory.
#
# Send a confirmation email.

# ============================================================
# THE SUBSYSTEMS
# ============================================================

# Four separate systems.
#
# None of them knows about the
# others.


class WMS:

    def update(self):
        print("  [wms] warehouse updated")


class IMS:

    def update(self):
        print("  [ims] inventory updated")


class Emails:

    def send_email(self):
        print("  [emails] confirmation sent")


# ============================================================
# THE OBVIOUS VERSION
# ============================================================


class Amazon:

    def __init__(self, wms, ims, emails):
        self.wms = wms
        self.ims = ims
        self.emails = emails

    def invoice_generation(self):
        print("  [invoice] invoice generated")

    def order_place(self):
        self.invoice_generation()
        self.wms.update()
        self.ims.update()
        self.emails.send_email()


print("The Obvious Version")

amazon = Amazon(WMS(), IMS(), Emails())
amazon.order_place()

# Observation:
#
# It works.
#
# All four things happened.
#
# Again, working is not the
# question.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What is actually wrong here?
#
# Think back to Single
# Responsibility.

# ============================================================
# WHAT IS WRONG
# ============================================================

# Amazon.order_place() is now
# doing the job of four
# unrelated systems.
#
# Invoicing.
#
# Warehousing.
#
# Inventory.
#
# Email.
#
# That is too much
# responsibility for one
# method in one class.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# So what should take over
# this coordination job?
#
# So that Amazon stays clean.

# ============================================================
# THE ANSWER
# ============================================================

# A separate class.
#
# Whose only job is:
#
#     "coordinate what happens
#      when an order is placed"
#
# Pull all of it into its own
# Facade class.

# ============================================================
# THE SHAPE OF THE REFACTOR
# ============================================================

#     class Amazon:
#         def order_place(self):
#             self.order_placed_facade.on_order_place()
#
#
#     class OrderPlacedFacade:
#         def on_order_place(self):
#             self.invoice_generation()
#             self.wms.update()
#             self.ims.update()
#             self.emails.send_email()
#
# Amazon now has just one line.
#
# It delegates to the Facade.
#
# All four subsystem calls,
# and any future ones, live in
# exactly one place.

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on why the
# coordination moved out?
#
# Now we build it with real
# dependencies.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# What does the CALLER of
# Amazon.order_place() —
#
# say, a web request handler —
#
# actually need to know about
# invoices, warehouses, or
# emails?

# ============================================================
# THE ANSWER
# ============================================================

# Nothing at all.
#
# That is the whole point.
#
# The complexity is fully
# hidden behind the Facade.

# ============================================================
# THE REAL SUBSYSTEMS
# ============================================================


class InvoiceService:

    def generate(self, order):
        print(f"  [invoice] generated for {order}")


class WarehouseService:

    def update(self, order):
        print(f"  [wms] shipment arranged for {order}")


class InventoryService:

    def update(self, order):
        print(f"  [ims] stock decreased for {order}")


class EmailService:

    def send_confirmation(self, order):
        print(f"  [email] confirmation sent for {order}")


# ============================================================
# THE FACADE
# ============================================================


class OrderPlacedFacade:

    def __init__(self, invoice_service, wms, ims, email_service):
        self.invoice_service = invoice_service
        self.wms = wms
        self.ims = ims
        self.email_service = email_service

    def on_order_place(self, order):
        self.invoice_service.generate(order)
        self.wms.update(order)
        self.ims.update(order)
        self.email_service.send_confirmation(order)


# ============================================================
# RUNNING IT
# ============================================================

print("\nThe Facade")

facade = OrderPlacedFacade(
    InvoiceService(),
    WarehouseService(),
    InventoryService(),
    EmailService()
)

facade.on_order_place("ORDER-42")

# Observation:
#
# One call went in.
#
# Four subsystems fired.
#
# The caller named none of
# them.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Notice the constructor.
#
# It takes each subsystem in
# from outside.
#
# Instead of creating them
# itself.
#
# Which principle is this?
#
# And why does it matter even
# here —
#
# in a class whose whole job
# is "hide complexity"?

# ============================================================
# THE ANSWER
# ============================================================

# Dependency Injection.
#
# Even a Facade should not
# lock itself to one concrete
# subsystem.
#
# It should depend on
# abstractions.
#
# Handed in from outside.

# ============================================================
# QUIZ
# ============================================================

# What is the core difference
# in intent between Adapter
# and Facade, based on
# everything so far?
#
# A) Adapter simplifies a
#    complex system; Facade
#    makes two incompatible
#    interfaces compatible
#
# B) Adapter makes two
#    incompatible interfaces
#    compatible; Facade
#    simplifies access to a
#    complex system
#
# C) They solve the exact
#    same problem
#
# D) Facade is only used with
#    third-party APIs
#
# Answer:
#
# B)
#
# We will dig into this
# properly later, in the
# Adapter vs Facade file.

# ============================================================
# CHECKPOINT
# ============================================================

# Is the Facade shape clear?
#
# One entry point.
#
# Several subsystems behind
# it.
#
# Handed in, not created
# inside.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# A Facade is one simple entry
# point that hides the
# coordination of several
# complex systems.
#
# The relationship manager at
# a bank is the everyday
# version.
#
# Amazon.order_place() doing
# invoicing, warehousing,
# inventory and email itself
# is too much responsibility
# for one method.
#
# The coordination moves into
# a class whose only job is
# coordinating.
#
# The caller then needs to
# know nothing about the
# subsystems.
#
# Even a Facade takes its
# subsystems in from outside.
#
# Dependency Injection applies
# to the class that hides
# complexity too.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We built this for an order
# flow.
#
# Like Adapter, nothing about
# it was domain specific.
#
# Next we point the same
# structure at something you
# have almost certainly used
# this week without seeing any
# of it.
#
# Next:
#
# 05_facade_in_ai_systems.py
