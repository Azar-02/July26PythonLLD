"""
===============================================================================
PART 09 - ENUM
Kill the Magic Strings
===============================================================================

Topics Covered
--------------
1. The magic-string problem
2. Enum - a fixed menu of allowed values
3. .value
4. Typos become AttributeError, not silent bugs
5. IntEnum
6. auto()

"""

from enum import Enum, IntEnum, auto

# =============================================================================
# MOTIVATION
# =============================================================================
#
# Our failures now have names.
#
# BookNotAvailable.
#
# BorrowLimitExceeded.
#
# But our VALUES still don't.
#
# Look at how status gets stored in the Library:
#
#     loan.status = "active"
#
# A raw string.
#
# Written by hand.
#
# Everywhere.
#
# That is a typo waiting to happen.
#
# "activ"?
#
# "Active"?
#
# "ACTIVE"?


# =============================================================================
# ASK LEARNERS
# =============================================================================
#
# What breaks if someone writes "activ" in one place
#
# and "active" in another?
#
# Expected Answer:
#
# Silent bug.
#
# They don't match.
#
# Nothing errors.
#
# The logic just quietly fails.
#


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Below is the magic-string version.
#
# One of the two spellings has a typo.
#
# Predict:
#
# does Python warn us?
#

status_written = "activ"          # the typo
status_checked = "active"         # what the rest of the code expects

print("Do they match? :", status_written == status_checked)
print("Did Python complain?", "No - it just returned False")

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# No error.
#
# No warning.
#
# Just False.
#
# And somewhere downstream, a loan silently never counts as active.
#
# This is the worst kind of bug -
#
# the kind that does not announce itself.


# =============================================================================
# THEORY - Enum
# =============================================================================
#
# Fix - an Enum.
#
# A fixed menu of allowed values.
#
# Analogy:
#
# A menu at a restaurant.
#
# You pick from the list.
#
# You can't invent a dish.
#


class LoanStatus(Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


loan_status = LoanStatus.ACTIVE

print("\nmember       :", loan_status)          # LoanStatus.ACTIVE
print("member.value :", .valueloan_status)      # "active"

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Two different things printed.
#
# LoanStatus.ACTIVE
#
#        the MEMBER - what your code passes around
#
# "active"
#
#        the VALUE - what you store or send over the wire
#
# The member is the name you use in code.
#
# The value is the raw data behind it.


# =============================================================================
# THINK BEFORE RUNNING
# =============================================================================
#
# Now the payoff.
#
# We deliberately misspell the member name.
#
# Predict what Python does this time.
#

try:
    bad = LoanStatus.ACTIV        # the same typo as before
except AttributeError as e:
    print("\ntypo result  : AttributeError -", e)

# =============================================================================
# RUNTIME OBSERVATION
# =============================================================================
#
# Compare the two experiments.
#
# Magic string typo   ->  False, silently, much later.
#
# Enum typo           ->  AttributeError, immediately, right here.
#
# The bug did not disappear.
#
# It became LOUD.
#
# That is the entire point of an Enum.


# =============================================================================
# COMMON MISCONCEPTIONS
# =============================================================================
#
# Misconception 1:
#
# "LoanStatus.ACTIVE is the string 'active'."
#
# It is not. It is a member.
#
# Use .value when you need the raw string.
#

print("\nmember == string :", LoanStatus.ACTIVE == "active")
print("value  == string :", LoanStatus.ACTIVE.value == "active")

#
# Misconception 2:
#
# "An Enum stops all typos."
#
# It catches typos in the MEMBER NAME.
#
# The values themselves are still written by hand - once, in one place.
#
# Which is exactly the improvement: one place to get right, not fifty.
#


# =============================================================================
# THEORY - two variants
# =============================================================================
#
# IntEnum
#
#        ↓
#
# enum values that are also integers.
#
# Which means you can compare them with < and >.
#


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


print("\nHIGH > LOW      :", Priority.HIGH > Priority.LOW)
print("MEDIUM == 2     :", Priority.MEDIUM == 2)

#
# auto()
#
#        ↓
#
# when you don't care about the values, just the names.
#


class BookType(Enum):
    NOVEL = auto()       # value auto-assigned (1, 2, 3...)
    TEXTBOOK = auto()


print("\nNOVEL    :", BookType.NOVEL, "value:", BookType.NOVEL.value)
print("TEXTBOOK :", BookType.TEXTBOOK, "value:", BookType.TEXTBOOK.value)

# Runtime Observation
#
# auto() numbered them 1 and 2.
#
# We never wrote those numbers.
#
# Because we never needed to care what they were -
#
# only that NOVEL and TEXTBOOK are different from each other.


# =============================================================================
# INTERVIEW OBSERVATION
# =============================================================================
#
# Frequently asked:
#
# - "Why not just use strings?"       -> Typos become silent bugs.
# - "Member vs value?"                -> The name you code with, vs the raw data.
# - "When would you use IntEnum?"     -> When the values need ordering or comparison.
# - "What does auto() give you?"      -> Values you don't have to invent or maintain.
# - "Where do Enums show up?"         -> Status fields, roles, states, categories.
#
# Any field with a small fixed set of legal values
#
# is an Enum waiting to happen.
#


# =============================================================================
# BOARD SUMMARY
# =============================================================================
#
# Magic strings / numbers
#
#        ↓
#
# typos become SILENT bugs.
#
#
# Enum
#
#        ↓
#
# a fixed menu of allowed values.
#
# Typo -> instant AttributeError.
#
#
# .value
#
#        ↓
#
# the raw data behind the member.
#
#
# IntEnum
#
#        ↓
#
# also behaves like ints - compare with < and >.
#
#
# auto()
#
#        ↓
#
# auto-number when the values don't matter.
#


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
#
# ✓ A magic-string typo fails silently; an Enum typo fails immediately.
# ✓ Enum = a fixed menu. You pick from the list, you can't invent a dish.
# ✓ LoanStatus.ACTIVE is the member; .value is the raw string behind it.
# ✓ LoanStatus.ACTIV raises AttributeError - the bug becomes loud.
# ✓ IntEnum members are also ints, so they compare with < and >.
# ✓ auto() assigns the values when you only care about the names.
#
#
# =============================================================================
# BRIDGE TO THE NEXT TOPIC
# =============================================================================
#
# That completes the toolkit.
#
# collections    - better containers.
#
# @dataclass     - structure without boilerplate.
#
# Type hints     - labels for humans and tools.
#
# Exceptions     - failures with names.
#
# Enum           - values with names.
#
# Now we take the Library System you built by hand in the OOP capstone
#
# and make it Pythonic with every one of these.
#
# Next: the lab - refactoring the Library System. The loop closes.