"""
============================================================
LLD-2 : OOP-1
PART 8 - BUILDING THE RIDER CLASS
============================================================

Topics Covered
--------------
1. Identifying Rider Data
2. Building Rider Incrementally
3. request_ride()
4. __str__
5. __repr__
6. from_dict()
7. Creating Rider Objects
8. Rider Behaviour
"""

# ============================================================
# MOTIVATION
# ============================================================

# So far our Uber system has a Driver.
#
# But a Driver alone is not enough.
#
# Every ride also involves a Rider.
#
# Before writing any code,
# let's identify what information
# a Rider should carry.

# ============================================================
# DISCUSSION
# ============================================================

# Question:
#
# What data does a Rider carry?
#
# Expected Answers:
#
# - name
# - phone_number
# - rating
#
# Just like Driver had data and behaviour,
# Rider will also have data and behaviour.

# ============================================================
# STEP 1 - EMPTY CLASS
# ============================================================

# Let's start with the simplest possible class.


class RiderV1:
    pass


rider = RiderV1()

print("Created RiderV1 Object")
print(type(rider))

# ============================================================
# STEP 2 - ADDING DATA
# ============================================================

# A Rider should immediately have:
#
# - name
# - phone_number
# - rating
#
# New riders start with a perfect rating.


class RiderV2:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.rating = 5.0


rider = RiderV2(
    "Priya",
    "9876543210"
)

print("\nRider Data")
print(rider.name)
print(rider.phone_number)
print(rider.rating)

# ============================================================
# STEP 3 - ADDING BEHAVIOUR
# ============================================================

# Question:
#
# What behaviour does a Rider have?
#
# One obvious behaviour:
#
# request_ride()


class RiderV3:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.rating = 5.0

    def request_ride(self):
        print(
            f"{self.name} is requesting a ride."
        )


rider = RiderV3(
    "Priya",
    "9876543210"
)

print("\nRider Behaviour")
rider.request_ride()

# ============================================================
# STEP 4 - HUMAN READABLE OUTPUT
# ============================================================

# Earlier we learned that print(obj)
# calls __str__().


class RiderV4:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.rating = 5.0

    def request_ride(self):
        print(
            f"{self.name} is requesting a ride."
        )

    def __str__(self):
        return (
            f"Rider(name={self.name}, "
            f"rating={self.rating})"
        )


rider = RiderV4(
    "Priya",
    "9876543210"
)

print("\nUsing __str__")
print(rider)

# ============================================================
# STEP 5 - DEVELOPER REPRESENTATION
# ============================================================

# __repr__ is intended for developers.
#
# It is generally more precise.


class RiderV5:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.rating = 5.0

    def request_ride(self):
        print(
            f"{self.name} is requesting a ride."
        )

    def __str__(self):
        return (
            f"Rider(name={self.name}, "
            f"rating={self.rating})"
        )

    def __repr__(self):
        return (
            f"Rider(name='{self.name}', "
            f"phone='{self.phone_number}')"
        )


rider = RiderV5(
    "Priya",
    "9876543210"
)

print("\nUsing repr()")
print(repr(rider))

# ============================================================
# STEP 6 - ALTERNATIVE CONSTRUCTOR
# ============================================================

# Imagine Rider data arrives from an API.
#
# Example:

rider_data = {
    "name": "Amit",
    "phone_number": "9999999999"
}

# Instead of manually extracting fields
# everywhere in the codebase,
# Rider can know how to create itself.


class RiderFinal:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.rating = 5.0

    def request_ride(self):
        print(
            f"{self.name} is requesting a ride."
        )

    def __str__(self):
        return (
            f"Rider(name={self.name}, "
            f"rating={self.rating})"
        )

    def __repr__(self):
        return (
            f"Rider(name='{self.name}', "
            f"phone='{self.phone_number}')"
        )

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["name"],
            data["phone_number"]
        )


rider = RiderFinal.from_dict(rider_data)

print("\nCreated Using from_dict()")
print(rider)

# ============================================================
# OBSERVING STATE
# ============================================================

# Just like Driver,
# Rider also has state.
#
# State = values of all attributes
# at a particular moment.

print("\nRider State")
print(rider.__dict__)

# ============================================================
# FINAL DEMO
# ============================================================

rider.request_ride()

print(repr(rider))

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Rider is another example of modelling
# a real-world entity using OOP.
#
# Rider contains:
#
# Attributes
#     name
#     phone_number
#     rating
#
# Methods
#     request_ride()
#
# Special Methods
#     __str__()
#     __repr__()
#
# Class Methods
#     from_dict()
#
# The same OOP concepts used for Driver
# can be reused for any entity.
