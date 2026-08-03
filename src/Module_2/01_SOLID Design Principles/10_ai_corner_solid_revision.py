"""
============================================================
PART 10
AI CORNER, SOLID REVISION & DESIGN CHECKLIST
============================================================

Topics Covered
1. Revising all SOLID principles
2. Using AI to review designs
3. Good vs bad prompts
4. AI as a design assistant
5. Complete Bird revision
6. Interview revision
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# Throughout this module we gradually improved the Bird design.
#
# We never started by memorizing SOLID.
#
# Instead, every principle emerged because
# the previous design started showing limitations.
#
# This final lesson is a revision of the complete journey.
#
# It also demonstrates how AI can help us think about
# software design without replacing our understanding.

# ============================================================
# REVISION OF THE JOURNEY
# ============================================================

# STEP 1
#
# One Bird class.
#
# Problem:
# Large if-elif chains.
#
# Solution:
# SRP.

# ------------------------------------------------------------

# STEP 2
#
# New birds required editing old code.
#
# Solution:
# OCP.

# ------------------------------------------------------------

# STEP 3
#
# Penguin exposed problems in inheritance.
#
# Solution:
# LSP.

# ------------------------------------------------------------

# STEP 4
#
# Giant interfaces forced fake methods.
#
# Solution:
# ISP.

# ------------------------------------------------------------

# STEP 5
#
# Business logic depended on concrete classes.
#
# Solution:
# DIP.

# ------------------------------------------------------------

# STEP 6
#
# Objects created their own dependencies.
#
# Solution:
# Dependency Injection.

# ============================================================
# COMPLETE EXAMPLE
# ============================================================

class Flyable(ABC):

    @abstractmethod
    def fly(self):
        pass


class FlyingStyle(Flyable):

    def fly(self):
        print("Flying...")


class Bird:

    def __init__(self, name, flying_style: Flyable):
        self.name = name
        self.flying_style = flying_style

    def perform_flight(self):
        print(self.name)
        self.flying_style.fly()

bird = Bird("Sparrow", FlyingStyle())
bird.perform_flight()

# ============================================================
# THINK LIKE A DESIGNER
# ============================================================

# Whenever someone gives you a new requirement,
# avoid immediately writing code.
#
# Instead ask:
#
# • Which responsibility is changing?
# • Am I modifying working code?
# • Does inheritance still make sense?
# • Am I forcing unnecessary methods?
# • Is business logic coupled to implementation?
# • Who should create this dependency?

# ============================================================
# USING AI EFFECTIVELY
# ============================================================

# AI is an assistant.
#
# AI is NOT responsible for design decisions.
#
# Instead of asking:
#
# "Write code."
#
# Ask better questions.

bad_prompt = """
Create Bird classes.
"""

good_prompt = """
Review this Bird design.

1. Does it violate SRP?
2. Does it violate OCP?
3. Can Penguin substitute Bird?
4. Are interfaces too large?
5. Are dependencies inverted?
6. Suggest improvements.
"""

print("\nPrompt Quality Demo")
print("Bad Prompt")
print(bad_prompt)

print("\nGood Prompt")
print(good_prompt)

# ============================================================
# WHY THIS IS BETTER
# ============================================================

# AI gives significantly better answers
# when we provide context and specific goals.
#
# Instead of replacing your thinking,
# AI should challenge your thinking.

# ============================================================
# DESIGN REVIEW CHECKLIST
# ============================================================

CHECKLIST = [
    "Single responsibility?",
    "Open for extension?",
    "Substitutable subclasses?",
    "Small focused interfaces?",
    "Depends on abstractions?",
    "Dependencies injected?",
]

print("\nSOLID Checklist")
for item in CHECKLIST:
    print("-", item)

# ============================================================
# MINI EXERCISE
# ============================================================

# Consider a PaymentService that:
#
# - validates payment
# - deducts balance
# - sends email
# - prints invoice
# - updates analytics
#
# Questions:
#
# 1. Which SOLID principle is violated first?
# 2. Would adding another payment mode
#    require modifying existing code?
# 3. Which responsibilities can be separated?
# 4. Which abstractions would improve the design?
#
# Discuss before coding.

# ============================================================
# INTERVIEW RAPID REVISION
# ============================================================

# SRP
# One reason to change.
#
# OCP
# Extend, don't modify.
#
# LSP
# Child must honour parent behaviour.
#
# ISP
# Don't force unused methods.
#
# DIP
# Depend on abstractions.
#
# DI
# Dependencies supplied from outside.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# SOLID does NOT guarantee perfect software.
#
# SOLID does NOT mean every project needs
# dozens of interfaces.
#
# SOLID is a set of guidelines that helps
# software evolve with fewer surprises.

# ============================================================
# FINAL BOARD SUMMARY
# ============================================================

# Requirements Change
#          |
#          v
#  Good Design Adapts
#
# SRP  -> Focus
# OCP  -> Extension
# LSP  -> Trust
# ISP  -> Small Contracts
# DIP  -> Abstractions
# DI   -> Supply Dependencies
#
# Build software that welcomes change
# instead of fearing it.

print("\nCongratulations!")
print("You have completed the SOLID Principles module.")
