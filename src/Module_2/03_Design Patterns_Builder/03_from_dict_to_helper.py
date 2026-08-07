"""
============================================================
LLD-6 : DESIGN PATTERNS - BUILDER
FILE : 03_from_dict_to_helper_v1.py
============================================================

Topics Covered
--------------
1. Why a Dictionary Looks Attractive
2. Building Objects Gradually
3. Problems with Dictionaries
4. Silent Typo Bugs
5. Replacing dict with a Helper Class
6. Why a Normal Class Still Fails
7. Understanding __dict__
8. Restricting Attributes with __slots__
9. Why Helper Has No Validation
10. Bridge Towards Builder
"""

# ============================================================
# MOTIVATION
# ============================================================

# Our constructor has reached a practical limit.
#
# Validation works.
#
# Keyword arguments improve readability.
#
# Default values make some parameters optional.
#
# Yet one important problem still remains.
#
# Information rarely arrives all at once.
#
# A constructor is a single event.
#
# Real applications often receive information in stages.

# ============================================================
# BUILDING INFORMATION GRADUALLY
# ============================================================

registration = {}

registration["name"] = "Naman"
registration["age"] = 21

print("After Registration")
print(registration)

registration["psp"] = 89.21
registration["batch"] = "April"

print("\nAfter Academic Details")
print(registration)

registration["university_name"] = "ABC University"

print("\nAfter University Lookup")
print(registration)

# ============================================================
# OBSERVATION
# ============================================================

# A dictionary naturally supports gradual construction.
#
# New information can be added whenever it becomes available.
#
# Unlike constructors, there is no requirement to know
# every value at one point in time.

# ============================================================
# USING THE DICTIONARY
# ============================================================

class StudentV1:

    def __init__(self, data):
        self.name = data["name"]
        self.age = data["age"]
        self.psp = data["psp"]

student = StudentV1(registration)

print("\nStudent Created")
print(student.__dict__)

# ============================================================
# THE FIRST WEAKNESS
# ============================================================

bad = {}

bad["nmae"] = "Naman"
bad["age"] = 21
bad["psp"] = 90

print("\nTypo Dictionary")
print(bad)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Dictionaries never know that "nmae" is a typo.
#
# They simply accept another key.
#
# The bug remains hidden until someone later tries to
# read "name".

try:
    StudentV1(bad)
except Exception as e:
    print(type(e).__name__, e)

# ============================================================
# BEFORE VS AFTER
# ============================================================

# Gradual Building
# ----------------
# ✔ Excellent
#
# Type Safety
# -----------
# ✘ None
#
# Typo Detection
# --------------
# ✘ None

# ============================================================
# REPLACING THE DICTIONARY
# ============================================================

class HelperV1:

    def __init__(self):
        self.name = None
        self.age = None
        self.psp = None

helper = HelperV1()
helper.name = "Naman"
helper.age = 21
helper.psp = 89.2

print("\nHelper Object")
print(helper.__dict__)

# ============================================================
# THIS LOOKS BETTER...
# ============================================================

# A class is usually easier to understand than a collection
# of string keys.
#
# IDEs can also autocomplete attributes.

# ============================================================
# ...BUT THE SAME BUG RETURNS
# ============================================================

helper2 = HelperV1()
helper2.nmae = "Riya"

print("\nUnexpected Attributes")
print(helper2.__dict__)

# ============================================================
# RUNTIME OBSERVATION
# ============================================================

# Python accepted the misspelled attribute.
#
# Why?
#
# Because ordinary Python objects internally store
# attributes inside a dictionary called __dict__.

print("\nInternal Attribute Dictionary")
print(helper2.__dict__)

# ============================================================
# MEMORY MODEL
# ============================================================

# helper2
#    |
#    v
#  __dict__
#  -----------------------
#  nmae : "Riya"
#
# Since __dict__ is itself a dictionary,
# unknown attribute names are simply inserted.

# ============================================================
# RESTRICTING ATTRIBUTES
# ============================================================

class HelperV2:

    __slots__ = (
        "name",
        "age",
        "psp",
    )

    def __init__(self):
        self.name = None
        self.age = None
        self.psp = None

good = HelperV2()
good.name = "Naman"

print("\nSlots Example")
print(good.name)

try:
    good.nmae = "Wrong"
except AttributeError as e:
    print(type(e).__name__, e)

# ============================================================
# OBSERVATION
# ============================================================

# __slots__ removes the freedom to invent arbitrary
# attribute names.
#
# Mistakes are detected immediately instead of hiding
# inside an object's attribute dictionary.

# ============================================================
# WHY NO VALIDATION HERE?
# ============================================================

# Helper is only a temporary container.
#
# It collects information gradually.
#
# The final business object should decide whether
# the collected information is valid.
#
# Validation belongs at the final construction step,
# not while values are still being collected.

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# __slots__ is commonly discussed for memory savings.
#
# Another practical benefit is catching accidental
# attribute creation.

# ============================================================
# BOARD SUMMARY
# ============================================================

# dict
#  ✔ Gradual
#  ✘ Typo safety
#
# Helper
#  ✔ Cleaner API
#  ✘ Still accepts typos
#
# Helper + __slots__
#  ✔ Gradual
#  ✔ Immediate typo detection

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Dictionaries solve gradual construction but sacrifice safety.
#
# A normal helper class improves readability but still
# accepts misspelled attributes.
#
# __slots__ gives us gradual construction together with
# attribute-name protection.
#
# We are now very close to the Builder pattern.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# The Helper class already resembles a Builder.
#
# In the next file we rename it, move validation to the
# construction step and arrive at the first Builder
# implementation.
