"""
PART 01 - NAIVE BIRD DESIGN

Topics Covered
1. The problem statement
2. First instinctive design
3. Adding behaviour
4. Why the design looks correct initially
5. Discovering the pain
6. Bridge to Single Responsibility Principle

==================================================================

"""

# ============================================================
# MOTIVATION
# ============================================================

# Imagine your interviewer gives you the following requirement:
#
#     "Design a Bird entity."
#
# Notice something interesting.
#
# They did NOT ask you to use SOLID.
# They did NOT ask you to use Design Patterns.
# They did NOT ask you to use inheritance.
#
# They simply asked:
#
#     Design a Bird.
#
# If this is your first OOP project, what would you naturally build?
#
# Do not worry about writing the "perfect" design.
#
# Our objective is to think exactly the way most beginners think.
#
# Every good software design principle was invented because people first
# experienced the pain of simpler designs.
#
# Therefore...
#
# We will intentionally build the simple design first.

# ============================================================
# STOP AND THINK
# ============================================================

# Before reading further, pause for a minute.
#
# Question:
#
# If YOU had to design a Bird class today,
# what would your design look like?
#
# Which attributes would you store?
#
# Which methods would you create?
#
# Think first.
# Then continue reading.

# ============================================================
# COMMON FIRST THOUGHT
# ============================================================

# Most developers usually think something like this:
#
# "Let's create one Bird class.
#  Every bird is represented using this class.
#  We will store all common information inside it."

class BirdV1:

    def __init__(self, name: str, age: int, color: str, type_: str):
        self.name = name
        self.age = age
        self.color = color
        self.type = type_


# ============================================================
# DISCUSSION
# ============================================================

# Does BirdV1 look wrong?
#
# No.
#
# In fact, it looks perfectly reasonable.
#
# There is absolutely nothing wrong with storing:
#
# • name
# • age
# • color
# • type
#
# So far our design is clean.

# ============================================================
# THINK ABOUT THE NEXT STEP
# ============================================================

# A Bird is not useful if it only stores information.
#
# Objects should also have behaviour.
#
# Question:
#
# What is the first behaviour that naturally comes to mind?
#
# Most people answer:
#
#     fly()

class BirdV2:

    def __init__(self, name: str, age: int, color: str, type_: str):
        self.name = name
        self.age = age
        self.color = color
        self.type = type_

    def fly(self):

        if self.type == "pigeon":
            print(f"{self.name} flies using short bursts near the ground.")

        elif self.type == "sparrow":
            print(f"{self.name} flies using quick fluttering movements.")

        elif self.type == "eagle":
            print(f"{self.name} soars using long glides.")

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Before executing...
#
# Predict:
#
# What will each object print?
#
# More importantly...
#
# Does this design look good?
#
# Most beginners answer:
#
# "Yes."

p1 = BirdV2("Oliver",2,"Grey","pigeon")
s1 = BirdV2("Max",1,"Brown","sparrow")
e1 = BirdV2("Sky",5,"Black","eagle")

p1.fly()
s1.fly()
e1.fly()

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# The program behaves correctly.
#
# This is an important lesson.
#
# Good output does NOT automatically imply good design.
#
# Design quality is tested when requirements change.

# ============================================================
# SELF CHECK
# ============================================================

# Imagine the project grows.
#
# New birds arrive:
#
# • Falcon
# • Penguin
# • Parrot
# • Ostrich
#
# Question:
#
# Where will their flying behaviour be written?
#
# Pause before reading further.

# ============================================================
# DISCUSSION
# ============================================================

# Answer:
#
# We will modify fly().
#
# Every new bird adds one more elif block.
#
# The method keeps growing forever.
#
# Today:
#
# if...
# elif...
# elif...
#
# Six months later:
#
# if...
# elif...
# elif...
# elif...
# elif...
# elif...
#
# One method slowly becomes responsible for
# every bird in the application.

# ============================================================
# WHY THIS BECOMES A PROBLEM
# ============================================================

# As the application grows:
#
# 1. Reading fly() becomes difficult.
# 2. Testing every branch becomes difficult. 
# 3. Every new bird requires modifying old code.
# 4. Different bird behaviours become tightly mixed together.
#
# Interestingly...
#
# None of these problems appear on Day 1.
#
# They appear months later.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# "The program works, therefore the design is good."
#
# Incorrect.
#
# Software design is about making future changes easier,
# not merely making today's program run.

# ============================================================
# MEMORY DIAGRAM
# ============================================================

#
# p1 ------------------------+
#                            |
#                            v
#                     +---------------+
#                     | BirdV2 Object |
#                     +---------------+
#                     | name          |
#                     | age           |
#                     | color         |
#                     | type          |
#                     +---------------+
#                             |
#                             v
#                       fly()
#                          |
#             ------------------------------
#             |      if / elif chain       |
#             ------------------------------

# ============================================================
# BOARD SUMMARY
# ============================================================

# First design
#
# ✔ One Bird class
# ✔ One fly() method
# ✔ Behaviour selected using if-elif
#
# Initially:
#     Looks simple
#
# As project grows:
#     Method keeps growing.

# ============================================================
# BRIDGE TO THE NEXT TOPIC
# ============================================================

# We have discovered our first design problem.
#
# The question is no longer:
#
#     "How do we make fly() larger?"
#
# The better question is:
#
#     "Why is one method responsible for
#      every bird?"
#
# That question naturally leads us to the
# Single Responsibility Principle (SRP).
