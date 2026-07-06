"""
============================================================
LLD-2 : OOP-1
PART 3 - OBJECT MEMORY AND STATE
============================================================

Topics Covered
--------------
1. Reference Variables
2. Objects in Memory
3. id()
4. Shared References
5. Object State
6. __dict__
7. State Changes

"""

print("=" * 70)
print("PART 3 - OBJECT MEMORY AND STATE")
print("=" * 70)

# ============================================================
# SETUP
# ============================================================

class Driver:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def accept_ride(self):
        self.is_available = False

    def complete_ride(self):
        self.is_available = True


# ============================================================
# MOTIVATION
# ============================================================

"""
MOTIVATION
----------

Many beginners think:

driver_one IS the object.

This is not true.

driver_one is only a reference variable.

The actual object lives somewhere in memory.
"""

# ============================================================
# OBJECT CREATION
# ============================================================

print("""
OBJECT CREATION
---------------
""")

driver_one = Driver("Ramesh", 4.8)
driver_two = Driver("Suresh", 4.5)

print("driver_one:", driver_one)
print("driver_two:", driver_two)

"""
Two Driver objects have been created.

Question:

Are these the same object?

No.

They are completely different objects
living at different memory locations.
"""

# ============================================================
# MEMORY MODEL
# ============================================================

print("""
MEMORY MODEL
------------

Conceptually:

driver_one -----> Driver Object (Ramesh)

driver_two -----> Driver Object (Suresh)

Variables are labels.

Objects live in memory.
""")

# ============================================================
# id()
# ============================================================

"""
USING id()
----------

id() returns the memory address of an object.
"""

print("driver_one address:", id(driver_one))
print("driver_two address:", id(driver_two))

"""
Notice that the numbers are different.

Different address.
Different object.
"""

# ============================================================
# SHARED REFERENCES
# ============================================================

"""
SHARED REFERENCES
-----------------

Let's do something interesting.
"""

driver_three = driver_one
#driver_three = Driver("Ramesh", 4.8)

"""
Question:

Did Python create a new object?

Answer:

No.

Two labels.
One object.
"""

print("driver_one address :", id(driver_one))
print("driver_three address:", id(driver_three))

print("""
Same address.

Therefore:

driver_one and driver_three point
to the SAME object.
""")

# ============================================================
# MUTATION THROUGH ANOTHER REFERENCE
# ============================================================

print("""
MUTATION THROUGH ANOTHER REFERENCE
----------------------------------
""")

print("Before Change")

print("driver_one.rating =", driver_one.rating)
print("driver_three.rating =", driver_three.rating)

driver_three.rating = 2.1

print("\nAfter Change")

print("driver_one.rating =", driver_one.rating)
print("driver_three.rating =", driver_three.rating)

"""
Aha Moment:

We changed driver_three.

Yet driver_one changed too.

Why?

Because both references point
to the same object.
"""

# ============================================================
# OBJECT STATE
# ============================================================

"""
OBJECT STATE
------------

Definition:

State = Values of all attributes
of an object at a particular moment.
"""

print("Current State of driver_one")

print(driver_one.__dict__)

# ============================================================
# __dict__
# ============================================================

"""
UNDERSTANDING __dict__
----------------------

__dict__ contains all instance attributes.

It gives us a snapshot of the object's state. ( not class attributes )
"""

print(driver_one.__dict__)

# ============================================================
# STATE CHANGE
# ============================================================

print("""
STATE CHANGE
------------

Let's observe state before and after
accepting a ride.
""")

print("\nBefore accept_ride()")

print(driver_one.__dict__)

driver_one.accept_ride()

print("\nAfter accept_ride()")

print(driver_one.__dict__)

"""
Notice:

is_available changed:

True -> False

This is called a state change.
"""

# ============================================================
# ANOTHER STATE CHANGE
# ============================================================

print("""
ANOTHER STATE CHANGE
--------------------
""")

driver_one.complete_ride()

print(driver_one.__dict__)

"""
Now:

False -> True

The same object exists.

Only its state changed.
"""

# ============================================================
# IMPORTANT INTERVIEW POINT
# ============================================================

"""
IMPORTANT POINT
---------------

Variables store references.

Variables do NOT store objects.

This idea becomes extremely important
when working with:

- Lists
- Dictionaries
- Mutable Objects
- Function Arguments
"""

# ============================================================
# KEY TAKEAWAYS
# ============================================================

"""
KEY TAKEAWAYS
-------------

1. Variables hold references.
2. Objects live in memory.
3. id() shows memory address.
4. Two variables can point to one object.
5. Changing one reference affects the same object.
6. State = values of all attributes.
7. __dict__ shows object state.
8. Methods can change state.
"""
