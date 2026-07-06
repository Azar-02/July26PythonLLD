"""
============================================================
LLD-2 : OOP-1
PART 2 - ANATOMY OF A CLASS
============================================================

Topics Covered
--------------
1. Driver Entity
2. Driver Data
3. Driver Behaviour
4. Empty Class
5. Why __init__ Exists
6. Understanding Special Methods
7. Understanding self
8. Building Driver Incrementally
9. Attributes vs Methods vs Members

"""

print("=" * 70)
print("PART 2 - ANATOMY OF A CLASS")
print("=" * 70)

# ============================================================
# MOTIVATION
# ============================================================

"""
MOTIVATION
----------

In the previous lecture we identified entities:

- Driver
- Rider
- Trip
- Vehicle
- Payment

Today we will convert one of those entities
into a Python class.

We will start with Driver.
"""

# ============================================================
# DRIVER DATA
# ============================================================

"""
DISCUSSION

What information describes a Driver?

Possible answers:

- name
- rating
- vehicle
- phone number
- availability
"""

# ============================================================
# DRIVER BEHAVIOUR
# ============================================================

"""
DISCUSSION

What can a Driver do?

Possible answers:

- accept_ride()
- complete_ride()
- go_offline()

Data + Behaviour together form a class.
"""

# ============================================================
# EMPTY CLASS
# ============================================================

print("""
STEP 1 - EMPTY CLASS
--------------------
""")


class Driver:
    pass


print("Driver class created successfully")

# ============================================================
# WHY __INIT__
# ============================================================

print("""
WHY DO WE NEED __init__ ?
-------------------------

Imagine a contractor building a house.

Every time a house is built,
some things are already installed.

Similarly, every Driver object should
already have:

- name
- rating
- availability

when it is created.

Python provides a special method for this.

That method is __init__.
""")

# ============================================================
# FIRST VERSION
# ============================================================

print("""
STEP 2 - ADDING __init__
------------------------
""")


class DriverV2:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True


driver_one = DriverV2("Ramesh", 4.8)

print("Name:", driver_one.name)
print("Rating:", driver_one.rating)
print("Available:", driver_one.is_available)

class Rider:
    def __init__(self, name):
        self.name = name

rider_one = Rider("Suresh")
print("Rider:", rider_one.name)
# ============================================================
# SPECIAL METHODS
# ============================================================

"""
SPECIAL METHODS
---------------

Methods with double underscores are called
special methods (dunder methods).

Examples:

__init__
__str__
__repr__

Python automatically calls them at the
appropriate time.
"""

# ============================================================
# UNDERSTANDING SELF
# ============================================================

"""
UNDERSTANDING self
------------------

Question:

Why not write:

name = name

instead of:

self.name = name ?

Because one class can create many objects.

Python must know WHICH object's name is
being assigned.

self refers to the current object.

You can use any name instead of self. Only thing is that it needs to be the first parameter of every instance method.
"""

driver_two = DriverV2("Suresh", 4.5)

print("Driver One:", driver_one.name)
print("Driver Two:", driver_two.name)

"""
Think of self as:

'this particular object'
"""

# ============================================================
# ADDING BEHAVIOUR
# ============================================================

print("""
STEP 3 - ADDING METHODS
-----------------------
""")


class DriverV3:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def accept_ride(self):
        if self.is_available:
            self.is_available = False
            print(f"{self.name} has accepted a ride.")
        else:
            print(f"{self.name} is not available.")

    def complete_ride(self):
        self.is_available = True
        print(
            f"{self.name} has completed the ride "
            f"and is available again."
        )


driver = DriverV3("Mahesh", 4.7)

print("Availability:", driver.is_available)

driver.accept_ride()

print("Availability:", driver.is_available)

driver.complete_ride()

print("Availability:", driver.is_available)

# ============================================================
# ATTRIBUTES VS METHODS
# ============================================================

"""
ATTRIBUTES
----------

name
rating
is_available

Attributes store data.
"""

"""
METHODS
-------

accept_ride()
complete_ride()

Methods define behaviour.
"""

"""
MEMBERS
-------

Members = Attributes + Methods
"""

# ============================================================
# FINAL DRIVER
# ============================================================

print("""
FINAL DRIVER CLASS
------------------
""")


class DriverFinal:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def accept_ride(self):
        if self.is_available:
            self.is_available = False
            print(f"{self.name} has accepted a ride.")
        else:
            print(f"{self.name} is not available.")

    def complete_ride(self):
        self.is_available = True
        print(f"{self.name} has completed the ride.")

print("""
KEY TAKEAWAYS
-------------

1. A class is a blueprint.
2. Objects are created from classes.
3. __init__ initializes objects.
4. self refers to the current object.
5. Attributes store data.
6. Methods define behaviour.
7. Members = Attributes + Methods.
""")
