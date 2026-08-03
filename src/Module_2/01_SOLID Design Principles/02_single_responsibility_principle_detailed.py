"""
PART 02 - SINGLE RESPONSIBILITY PRINCIPLE (SRP)

Topics Covered
1. Revisiting the naive Bird design
2. Discovering the real problem
3. Single Responsibility Principle
4. One reason to change
5. Three common SRP traps
6. Quiz
7. Bridge to Open/Closed Principle
"""

# ============================================================
# MOTIVATION
# ============================================================

# In the previous file, we created a single Bird class with one fly()
# method containing multiple if-elif branches.
#
# The program worked correctly.
#
# But then we imagined adding Falcon, Penguin, Parrot, Ostrich...
#
# The fly() method continued growing.
#
# Instead of asking:
#
# "How do we make fly() bigger?"
#
# let's ask a much better question...
#
# "Why is one method responsible for every bird?"

# ============================================================
# STOP AND THINK
# ============================================================

# Imagine you work in a company.
#
# One employee is expected to:
#
# • Handle accounting
# • Fix computers
# • Clean the office
# • Receive customers
#
# Question:
#
# Does this sound like a good design?

# ============================================================
# DISCUSSION
# ============================================================

# Initially it may look efficient.
#
# "One person can do everything."
#
# But imagine this situation:
#
# • The printer stops working.
# • A customer arrives.
# • Salary processing is pending.
# • The office needs cleaning.
#
# Which task should that employee perform first?
#
# Eventually something gets delayed.
#
# The problem is not that the employee is bad.
#
# The problem is that we gave one person
# too many unrelated responsibilities.

# ============================================================
# RELATING THE ANALOGY TO CODE
# ============================================================

# Now think about Bird.fly().
#
# Question:
#
# Every time a bird changes its flying style,
# which method changes?
#
# Think before reading further.

# ============================================================
# DISCUSSION
# ============================================================

# Answer:
#
# Bird.fly()
#
# Pigeon changes?
# -> Bird.fly() changes.
#
# Sparrow changes?
# -> Bird.fly() changes.
#
# Eagle changes?
# -> Bird.fly() changes.
#
# Falcon added?
# -> Bird.fly() changes.
#
# One method has many unrelated reasons to change.

# ============================================================
# KEY IDEA
# ============================================================

# Single Responsibility Principle (SRP)
#
# Every piece of code should have ONE responsibility.
#
# Another way of saying the same thing:
#
# Every piece of code should have only ONE reason to change.

# ============================================================
# DEMO
# ============================================================

class Pigeon:
    def fly(self):
        print("Pigeon flies using short bursts.")

class Sparrow:
    def fly(self):
        print("Sparrow flies using fluttering movements.")

class Eagle:
    def fly(self):
        print("Eagle soars using long glides.")

# THINK BEFORE RUNNING
#
# Which class changes if Sparrow changes its flying style?

Pigeon().fly()
Sparrow().fly()
Eagle().fly()

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Notice that every bird owns its own behaviour.
#
# A Sparrow change affects Sparrow.
#
# An Eagle change affects Eagle.
#
# Unrelated classes remain untouched.

# ============================================================
# THREE COMMON SRP TRAPS
# ============================================================

# Trap 1
# ------------------------------------------------------------
# Very large if-elif chains where each branch represents
# a different responsibility.

# Trap 2
# ------------------------------------------------------------
# A "does everything" method.
#
# Example:
#
# save_to_database()
#
# which:
# • opens connection
# • builds SQL
# • executes query
# • maps objects
# • closes connection
#
# Better approach:
#
# Split into smaller focused methods.

# Trap 3
# ------------------------------------------------------------
# utils.py
#
# After years it often contains:
#
# • String helpers
# • Date helpers
# • File helpers
# • Network helpers
#
# Better:
#
# string_utils.py
# date_utils.py
# file_utils.py

# ============================================================
# SELF CHECK
# ============================================================

# Which violates SRP more?
#
# A method validating three rules of one order.
#
# OR
#
# A method that:
# • validates
# • charges payment
# • updates inventory
# • sends email
#
# Think first.

# ============================================================
# ANSWER
# ============================================================

# The second method.
#
# These are unrelated responsibilities.
#
# They should evolve independently.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# SRP does NOT mean:
#
# Every method must contain only one line.
#
# It means:
#
# Every unit of code should change
# for only one kind of reason.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# One of the most common interview questions:
#
# "What does SRP actually mean?"
#
# Avoid answering:
#
# "One class should do one thing."
#
# Better answer:
#
# "A class should have only one reason to change."

# ============================================================
# BOARD SUMMARY
# ============================================================

# SRP
#
# One responsibility
# =
# One reason to change
#
# Unrelated changes
# should happen
# in unrelated classes.

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# SRP tells us to separate responsibilities.
#
# But another question remains.
#
# Suppose tomorrow we add Falcon.
#
# Even after splitting responsibilities,
# do we still need to modify existing code?
#
# That question leads us to the
# Open / Closed Principle.
