"""
============================================================
LLD-4 : OOP-3 (INHERITANCE)
PART 3 - COOPERATIVE SUPER()
============================================================

Topics Covered
--------------
1. The super() Misconception
2. Revisiting ElectricCab
3. Constructor Chaining
4. Multiple Inheritance Problem
5. Duplicate Initialization
6. Cooperative Inheritance
7. **kwargs Forwarding
8. super() and MRO
9. Constructor Trace
10. Key Takeaways

NOTE:
This file continues from:

02_multiple_inheritance_and_mro.py

The most important idea:

super() does NOT mean parent.

super() means:

"The next class in the MRO."
"""

# ============================================================
# MOTIVATION
# ============================================================

# Most developers learn:
#
# super()
#
# means:
#
# "Call the parent class."
#
# This explanation works for
# simple inheritance.
#
# Example:
#
# Vehicle
#   |
#   |
#  Car
#
# But:
#
# Multiple inheritance breaks
# this mental model.
#
# We need a deeper understanding.

# ============================================================
# SINGLE INHERITANCE
# ============================================================


class Vehicle:

    def __init__(self):

        print("Vehicle Constructor")


class Car(Vehicle):

    def __init__(self):

        print("Car Constructor")

        super().__init__()


print("Single Inheritance")

car = Car()

# Output:
#
# Car Constructor
# Vehicle Constructor
#
# Easy to believe:
#
# super() = parent

# ============================================================
# THE MISCONCEPTION
# ============================================================

# Many developers conclude:
#
# super()
#
# =
#
# parent
#
# This is not completely true.
#
# The real rule will become
# visible with multiple inheritance.

# ============================================================
# REVISITING ELECTRIC CAB
# ============================================================


class Vehicle:

    def __init__(self):

        print("Vehicle")


class ElectricVehicle(Vehicle):

    def __init__(self):

        print("ElectricVehicle")

        super().__init__()


class CommercialVehicle(Vehicle):

    def __init__(self):

        print("CommercialVehicle")

        super().__init__()


class ElectricCab(
    ElectricVehicle,
    CommercialVehicle
):

    def __init__(self):

        print("ElectricCab")

        super().__init__()


print("\nElectricCab Example")

cab = ElectricCab()

# ============================================================
# WHAT WAS EXECUTED?
# ============================================================

# Output:
#
# ElectricCab
# ElectricVehicle
# CommercialVehicle
# Vehicle
#
# Question:
#
# Why did:
#
# CommercialVehicle
#
# execute?
#
# ElectricVehicle's parent
# is Vehicle.
#
# Yet Vehicle did not execute next.
#
# This is the clue.

# ============================================================
# THE ANSWER IS MRO
# ============================================================

print("\nMRO")

print(
    [
        cls.__name__
        for cls
        in ElectricCab.mro()
    ]
)

# Output:
#
# ElectricCab
# ElectricVehicle
# CommercialVehicle
# Vehicle
# object

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# ElectricCab calls:
#
# super()
#
# Next class in MRO:
#
# ElectricVehicle
#
#
# ElectricVehicle calls:
#
# super()
#
# Next class in MRO:
#
# CommercialVehicle
#
#
# CommercialVehicle calls:
#
# super()
#
# Next class in MRO:
#
# Vehicle
#
#
# Vehicle calls:
#
# object

# ============================================================
# REAL DEFINITION
# ============================================================

# Wrong:
#
# super() = parent
#
# Correct:
#
# super() =
#
# next class
# in the MRO

# ============================================================
# THE DUPLICATE INITIALIZATION PROBLEM
# ============================================================

# Imagine:
#
# ElectricVehicle
#
# directly calls:
#
# Vehicle.__init__(self)
#
# and
#
# CommercialVehicle
#
# also calls:
#
# Vehicle.__init__(self)
#
# Vehicle might execute
# multiple times.
#
# That is dangerous.

# ============================================================
# NAIVE IMPLEMENTATION
# ============================================================


class VehicleV2:

    def __init__(self):

        print("VehicleV2")


class ElectricVehicleV2(VehicleV2):

    def __init__(self):

        print("ElectricVehicleV2")

        VehicleV2.__init__(self)


class CommercialVehicleV2(VehicleV2):

    def __init__(self):

        print("CommercialVehicleV2")

        VehicleV2.__init__(self)


class ElectricCabV2(
    ElectricVehicleV2,
    CommercialVehicleV2
):

    def __init__(self):

        print("ElectricCabV2")

        ElectricVehicleV2.__init__(self)

        CommercialVehicleV2.__init__(self)


print("\nNaive Chain")

cab = ElectricCabV2()

# Observe:
#
# VehicleV2 may execute
# more than once.
#
# This is one reason
# cooperative super()
# exists.

# ============================================================
# COOPERATIVE INHERITANCE
# ============================================================

# Rule:
#
# Every class should:
#
# 1. Do its work.
# 2. Call super().
#
# No direct parent calls.
#
# MRO manages everything.

# ============================================================
# THE KWARGS PATTERN
# ============================================================


class VehicleV3:

    def __init__(
        self,
        registration_number,
        **kwargs
    ):

        print("VehicleV3")

        self.registration_number = (
            registration_number
        )

        super().__init__(
            **kwargs
        )


class ElectricVehicleV3(VehicleV3):

    def __init__(
        self,
        battery_capacity,
        **kwargs
    ):

        print("ElectricVehicleV3")

        self.battery_capacity = (
            battery_capacity
        )

        super().__init__(
            **kwargs
        )


class CommercialVehicleV3(VehicleV3):

    def __init__(
        self,
        permit_id,
        **kwargs
    ):

        print("CommercialVehicleV3")

        self.permit_id = permit_id

        super().__init__(
            **kwargs
        )


class ElectricCabV3(
    ElectricVehicleV3,
    CommercialVehicleV3
):

    def __init__(
        self,
        **kwargs
    ):

        print("ElectricCabV3")

        super().__init__(
            **kwargs
        )


print("\nCooperative Inheritance")

cab = ElectricCabV3(
    battery_capacity=60,
    permit_id="PERMIT-101",
    registration_number="KA-01-EV"
)

# ============================================================
# EXECUTION FLOW
# ============================================================

# ElectricCabV3
#
#      |
#      v
#
# ElectricVehicleV3
#
#      |
#      v
#
# CommercialVehicleV3
#
#      |
#      v
#
# VehicleV3
#
#      |
#      v
#
# object

# ============================================================
# WHY KWARGS WORK
# ============================================================

# ElectricCabV3 receives:
#
# battery_capacity
# permit_id
# registration_number
#
#
# ElectricVehicleV3 consumes:
#
# battery_capacity
#
# forwards the rest.
#
#
# CommercialVehicleV3 consumes:
#
# permit_id
#
# forwards the rest.
#
#
# VehicleV3 consumes:
#
# registration_number

# ============================================================
# VERIFYING ATTRIBUTES
# ============================================================

print("\nVerification")

print(cab.battery_capacity)

print(cab.permit_id)

print(cab.registration_number)

# ============================================================
# SUPER FOLLOWS MRO
# ============================================================

print("\nElectricCabV3 MRO")

print(
    [
        cls.__name__
        for cls
        in ElectricCabV3.mro()
    ]
)

# This MRO determines:
#
# - method lookup
# - attribute lookup
# - super()

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Question:
#
# Why should we avoid:
#
# ParentClass.__init__(self)
#
# in multiple inheritance?
#
# Answer:
#
# Because:
#
# MRO is bypassed.
#
# Duplicate initialization
# may occur.
#
# Cooperative inheritance
# stops working.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# super() does NOT mean:
#
# parent
#
# super() means:
#
# next class in MRO
#
# MRO controls constructor flow.
#
# Every class should:
#
# - do its work
# - call super()
#
# Cooperative inheritance
# prevents duplicate execution.
#
# **kwargs forwarding allows
# multiple classes to participate
# in object construction.
