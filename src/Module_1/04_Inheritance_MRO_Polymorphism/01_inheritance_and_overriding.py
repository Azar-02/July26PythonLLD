"""
============================================================
LLD-4 : OOP-3 (INHERITANCE)
PART 1 - INHERITANCE AND METHOD OVERRIDING
============================================================

Topics Covered
--------------
1. Why Inheritance Exists
2. Code Duplication Problem
3. The "is-a" Relationship
4. Parent and Child Classes
5. Single Inheritance
6. Method Overriding
7. super()
8. type() vs isinstance()
9. Vehicle Example
10. Key Takeaways

NOTE:

The focus is:
- Inheritance
- Method Overriding
- super()
- isinstance()

Later files will cover:
- Multiple Inheritance
- MRO
- Polymorphism
"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider Uber.
#
# Uber has:
#
# - Cars
# - Bikes
# - Autos
#
# All of them have:
#
# - registration number
# - availability status
# - start()
# - stop()
#
# But they also differ.
#
# Example:
#
# Car fare calculation
# is different from
# Bike fare calculation.
#
# Question:
#
# Should we copy-paste
# the common code into
# every class?
#
# No.
#
# That creates duplication.
#
# Inheritance solves this problem.

# ============================================================
# UNDERSTANDING INHERITANCE
# ============================================================

# Real Life:
#
# Animal --> PARENT CLASS
#
# -> Dog --> CHILD CLASS
# -> Cat --> CHILD CLASS
# -> Eagle --> CHILD CLASS
#
# All animals:
#
# - eat
# - breathe
#
# But:
#
# Dog can bark
# Eagle can fly
#
# Shared behavior lives in
# Animal. ( parent class )
#
# Specific behavior lives in
# the child classes.

# ============================================================
# THE IS-A RELATIONSHIP
# ============================================================

# Question:
#
# Is a Car a Vehicle?
#
# Yes.
#
# Is a Bike a Vehicle?
#
# Yes.
#
# This is called:
#
# is-a relationship.
#
# Whenever:
#
# Child IS-A Parent
#
# inheritance is usually
# a good fit.

# ============================================================
# BUILDING THE BASE CLASS
# ============================================================


class Vehicle:

    def __init__(self, registration_number):

        self.registration_number = (
            registration_number
        )

        self.is_available = True

    def start(self):

        print(
            f"Vehicle "
            f"{self.registration_number} "
            f"is starting."
        )

    def stop(self):

        print(
            f"Vehicle "
            f"{self.registration_number} "
            f"has stopped."
        )

    def calculate_fare(
        self,
        distance_km
    ):

        base_rate = 10

        return base_rate * distance_km


# ============================================================
# FIRST CHILD CLASS
# ============================================================


class Car(Vehicle):

    pass


print("Car Inheritance")

car = Car("KA-01-1234")

car.start()

print(car.is_available)

print(car.calculate_fare(5))

# Observation:
#
# Car has no methods.
#
# Yet:
#
# start()
# calculate_fare()
# is_available
#
# all work.
#
# They are inherited from Vehicle.

# ============================================================
# SECOND CHILD CLASS
# ============================================================


class Bike(Vehicle):

    pass


print("\nBike Inheritance")

bike = Bike("KA-02-5678")

bike.start()

print(bike.calculate_fare(5))

# ============================================================
# WHAT THE CHILD RECEIVES
# ============================================================

# Child gets:
#
# - attributes
# - methods
#
# from the parent class.
#
# No copy-paste required.

# ============================================================
# METHOD OVERRIDING
# ============================================================

# Problem:
#
# Car and Bike should not
# calculate fares the same way.
#
# Therefore:
#
# Each child can provide
# its own implementation.

# ============================================================
# CAR OVERRIDE
# ============================================================


class CarV2(Vehicle):

    def calculate_fare(
        self,
        distance_km
    ):

        per_km_rate = 15

        return (
            per_km_rate *
            distance_km
        )


# ============================================================
# BIKE OVERRIDE
# ============================================================


class BikeV2(Vehicle):

    def calculate_fare(
        self,
        distance_km
    ):

        per_km_rate = 7

        return (
            per_km_rate *
            distance_km
        )


print("\nMethod Overriding")

car = CarV2("KA-11-1111")
bike = BikeV2("KA-22-2222")

print(car.calculate_fare(10))

print(bike.calculate_fare(10))

# Observation:
#
# Same method name.
#
# Different implementation.
#
# Child version wins.
#
# This is:
#
# Method Overriding.

# ============================================================
# OVERRIDING VISUALIZATION
# ============================================================

# Vehicle
#
# calculate_fare()
#
#        |
#        |
#        v
#
# CarV2
#
# calculate_fare()
#
# Child version replaces
# parent version for
# Car objects.

# ============================================================
# WHY SUPER EXISTS
# ============================================================

# Suppose Car needs:
#
# registration_number
#
# from Vehicle
#
# and additionally:
#
# num_seats
#
# We should not rewrite
# Vehicle initialization logic.

# ============================================================
# WITHOUT SUPER
# ============================================================

# Bad Idea:
#
# Copy parent logic
# into every child.
#
# That recreates the
# duplication problem.

# ============================================================
# WITH SUPER
# ============================================================


class CarV3(Vehicle):

    def __init__(
        self,
        registration_number,
        num_seats
    ):

        super().__init__(
            registration_number
        )

        self.num_seats = (
            num_seats
        )

    def calculate_fare(
        self,
        distance_km
    ):

        return (
            15 *
            distance_km
        )


print("\nsuper() Example")

car = CarV3(
    "KA-33-3333",
    4
)

print(car.registration_number)

print(car.num_seats)

print(car.is_available)

# Observation:
#
# Vehicle performs
# parent setup.
#
# Car performs
# child setup.

# ============================================================
# UNDERSTANDING SUPER
# ============================================================

# For now:
#
# Think of:
#
# super()
#
# as:
#
# "Call the parent implementation."
#
# Later:
#
# MRO will show that
# this explanation is
# incomplete.

# ============================================================
# TYPE VS ISINSTANCE
# ============================================================

car = CarV3(
    "KA-44-4444",
    4
)

print("\ntype() vs isinstance()")

print(
    type(car) == CarV3
)

print(
    type(car) == Vehicle
)

print(
    isinstance(
        car,
        CarV3
    )
)

print(
    isinstance(
        car,
        Vehicle
    )
)

# Output:
#
# True
# False
# True
# True

# ============================================================
# WHY TYPE FAILS
# ============================================================

# type()
#
# checks only the exact class.
#
# Exact type:
#
# CarV3
#
# not Vehicle.
#
# Therefore:
#
# type(car) == Vehicle
#
# returns False.

# ============================================================
# WHY ISINSTANCE WORKS
# ============================================================

# isinstance()
#
# understands inheritance.
#
# It asks:
#
# Is this object:
#
# - CarV3?
# OR
# - a parent of CarV3?
#
# Since:
#
# CarV3 IS-A Vehicle
#
# answer becomes True.

# ============================================================
# INTERVIEW RULE
# ============================================================

# Prefer:
#
# isinstance(obj, Class)
#
# over:
#
# type(obj) == Class
#
# because inheritance
# is respected.

# ============================================================
# IMPORTANT QUIZ
# ============================================================

# What happens here?
#
# class Bike(Vehicle):
#
#     def __init__(
#         self,
#         registration_number
#     ):
#
#         pass
#
# bike = Bike("KA-99")
#
# print(
#     bike.registration_number
# )
#
# Answer:
#
# AttributeError
#
# Why?
#
# Parent constructor
# never executed.
#
# super().__init__()
#
# was forgotten.

#if you override __init__ and still need parent setup, call super().__init__(). 
# If you are intentionally replacing all parent initialization, then you may not need it.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Inheritance removes
# duplication.
#
# Child classes inherit
# parent behavior.
#
# Method overriding lets
# children customize behavior.
#
# Child implementation wins.
#
# super() allows parent
# initialization reuse.
#
# type() checks exact class.
#
# isinstance() understands
# inheritance.
#
# Prefer isinstance()
# in real applications.
