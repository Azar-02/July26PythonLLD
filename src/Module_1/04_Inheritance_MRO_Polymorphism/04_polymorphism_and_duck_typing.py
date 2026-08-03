"""
============================================================
LLD-4 : OOP-3 (INHERITANCE)
PART 4 - POLYMORPHISM AND DUCK TYPING
============================================================

Topics Covered
--------------
1. What is Polymorphism?
2. Poly + Morph
3. Same Action, Different Behaviour
4. Vehicle Fleet Example
5. Runtime Dispatch
6. Method Overriding Revisited
7. Duck Typing
8. Drone Example
9. MaintenanceTicket Bug Example
10. Key Takeaways

Based on Lecture 4 notes.
"""

# ============================================================
# WHAT DOES POLYMORPHISM MEAN?
# ============================================================

# Poly  = Many
# Morph = Forms
#
# Polymorphism means:
#
# One thing can take many forms.
#
# Same action.
#
# Different behaviour.

# ============================================================
# REAL LIFE EXAMPLE
# ============================================================

# Think about:
#
# open()
#
# Open a door.
# Open a file.
# Open a bank account.
# Open a conversation.
#
# Same instruction.
#
# Different behaviour.
#
# The receiver decides what
# "open" means.

# ============================================================
# VEHICLE HIERARCHY
# ============================================================


class Vehicle:

    def __init__(self, registration_number):

        self.registration_number = registration_number

    def calculate_fare(self, distance_km):

        return distance_km * 10


class Car(Vehicle):

    def calculate_fare(self, distance_km):

        return distance_km * 15


class Bike(Vehicle):

    def calculate_fare(self, distance_km):

        return distance_km * 7


class ElectricCab(Vehicle):

    def calculate_fare(self, distance_km):

        return distance_km * 18


# ============================================================
# SAME CALL
# DIFFERENT BEHAVIOUR
# ============================================================

print("Polymorphism")

car = Car("KA-01")
bike = Bike("KA-02")
cab = ElectricCab("KA-03")

print(car.calculate_fare(10))
print(bike.calculate_fare(10))
print(cab.calculate_fare(10))

# Observation:
#
# Same method:
#
# calculate_fare()
#
# Different results.
#
# Object decides behaviour.

# ============================================================
# FLEET EXAMPLE
# ============================================================

fleet = [
    Car("KA-01"),
    Bike("KA-02"),
    ElectricCab("KA-03")
]

print("\nFleet Dispatch")

for vehicle in fleet:

    print(
        vehicle.registration_number,
        "->",
        vehicle.calculate_fare(10)
    )

# The loop does not care
# whether the object is:
#
# Car
# Bike
# ElectricCab
#
# Same call.
#
# Different behaviour.

# ============================================================
# RUNTIME DISPATCH
# ============================================================

# Question:
#
# Which calculate_fare()
# runs?
#
# Answer:
#
# Decided at runtime.
#
# Python looks at the
# actual object.

# ============================================================
# POLYMORPHISM DEFINITION
# ============================================================

# Same action:
#
# calculate_fare()
#
# Different behaviour:
#
# Car  -> 150
# Bike -> 70
# Cab  -> 180
#
# Decided by:
#
# The object at runtime.

# ============================================================
# DUCK TYPING
# ============================================================

# Python has another idea.
#
# It cares less about
# what an object IS.
#
# It cares more about
# what an object CAN DO.
#
# Famous saying:
#
# If it walks like a duck
# and quacks like a duck,
# it is a duck.

# ============================================================
# START JOURNEY
# ============================================================


class VehicleV2:

    def start(self):

        print("Vehicle started")


def start_journey(vehicle):

    vehicle.start()


# ============================================================
# DRONE EXAMPLE
# ============================================================


class Drone:

    def start(self):

        print(
            "Drone spinning up rotors."
        )


print("\nDuck Typing")

start_journey(Drone())

# Drone is not a Vehicle.
#
# No inheritance.
#
# Still works.
#
# Why?
#
# It has start().

# ============================================================
# MAINTENANCE TICKET
# ============================================================

# Duck typing is powerful.
#
# But it can also hide bugs.


class MaintenanceTicket:

    def __init__(self, ticket_id):

        self.ticket_id = ticket_id

        self.status = "open"

    def start(self):

        self.status = "in_progress"

        print(
            f"Ticket "
            f"{self.ticket_id} "
            f"is now in progress."
        )


print("\nMaintenance Ticket")

ticket = MaintenanceTicket(
    "TICKET-42"
)

start_journey(ticket)

# Observation:
#
# No error occurred.
#
# Python saw:
#
# start()
#
# and executed it.
#
# But:
#
# start_journey()
#
# was intended for vehicles.

# ============================================================
# THE RISK
# ============================================================

# Python checks:
#
# Does the object have start()?
#
# Python does NOT check:
#
# Does start() mean what
# I expect it to mean?
#
# Therefore:
#
# Wrong object
# +
# Correct method name
#
# can create silent bugs.

# ============================================================
# DUCK TYPING SUMMARY
# ============================================================

# Benefit:
#
# Flexible
#
# No inheritance required.
#
# Cost:
#
# Wrong objects may
# accidentally work.

# ============================================================
# POLYMORPHISM VS DUCK TYPING
# ============================================================

# Polymorphism:
#
# Usually built using
# inheritance + overriding.
#
# Example:
#
# Vehicle
#   -> Car
#   -> Bike
#
#
# Duck Typing:
#
# No inheritance required.
#
# Only behaviour matters.
#
# Object just needs the
# expected methods.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Polymorphism:
#
# Same action.
# Different behaviour.
#
# Runtime decides.
#
# Method overriding enables
# polymorphism.
#
# Duck typing focuses on
# behaviour instead of type.
#
# Python asks:
#
# "Can you do this?"
#
# instead of:
#
# "What are you?"
#
# Flexible.
#
# Powerful.
#
# Must be used carefully.
