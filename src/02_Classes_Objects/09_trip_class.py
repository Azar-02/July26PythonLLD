"""
============================================================
LLD-2 : OOP-1
PART 9 - BUILDING THE TRIP CLASS
============================================================

Topics Covered
--------------
1. What is a Trip?
2. Trip Data
3. Custom Objects as Attributes
4. Building Trip Incrementally
5. start()
6. complete()
7. __str__()
8. from_dict()
9. Cross-Object Communication
10. State Propagation
11. Reference Semantics Revisited
"""

# ============================================================
# MOTIVATION
# ============================================================

# So far we have built:
#
# Driver
# Rider
#
# But an Uber ride is really represented by
# a Trip.
#
# A Trip connects a Driver and a Rider.
#
# This is the first time we will see one
# custom object storing references to
# other custom objects.

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
        print(f"{self.name} has accepted a ride.")

    def complete_ride(self):
        self.is_available = True
        print(
            f"{self.name} has completed the ride "
            f"and is available again."
        )


class Rider:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.rating = 5.0


# ============================================================
# DISCUSSION
# ============================================================

# Question:
#
# What does a Trip need to know about?
#
# Expected Answers:
#
# driver
# rider
# pickup
# dropoff
# status

# ============================================================
# STEP 1 - EMPTY CLASS
# ============================================================


class TripV1:
    pass


trip = TripV1()

print("Created TripV1")
print(type(trip))

# ============================================================
# STEP 2 - ADDING DATA
# ============================================================

# A Trip needs:
#
# - Driver
# - Rider
# - Pickup Location
# - Dropoff Location
# - Status


class TripV2:

    def __init__(
        self,
        driver,
        rider,
        pickup,
        dropoff
    ):
        self.driver = driver
        self.rider = rider
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = "requested"


driver = Driver("Ramesh", 4.8)

rider = Rider(
    "Priya",
    "9876543210"
)

trip = TripV2(
    driver,
    rider,
    "Koramangala",
    "Indiranagar"
)

print("\nTrip Created")
print(trip.status)

# ============================================================
# IMPORTANT DISCUSSION
# ============================================================

# Question:
#
# What type is self.driver ?
#
# Answer:
#
# It is a Driver object.
#
# Question:
#
# What type is self.rider ?
#
# Answer:
#
# It is a Rider object.
#
# This is a major OOP idea.
#
# Attributes are not limited to:
#
# int
# str
# bool
# list
#
# An attribute can also be another
# custom object.

print("\nType of trip.driver")
print(type(trip.driver))

print("\nType of trip.rider")
print(type(trip.rider))

# ============================================================
# STEP 3 - STARTING A TRIP
# ============================================================

# What should happen when a trip starts?
#
# The Driver should become unavailable.
#
# The Trip status should change.


class TripV3:

    def __init__(
        self,
        driver,
        rider,
        pickup,
        dropoff
    ):
        self.driver = driver
        self.rider = rider
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = "requested"

    def start(self):

        self.driver.accept_ride()

        self.status = "in_progress"

        print(
            f"Trip started: "
            f"{self.rider.name} -> "
            f"{self.dropoff}"
        )


driver = Driver("Mahesh", 4.6)

rider = Rider(
    "Anita",
    "9999999999"
)

trip = TripV3(
    driver,
    rider,
    "Airport",
    "City Center"
)

print("\nBefore Start")
print(driver.is_available)
print(trip.status)

trip.start()

print("\nAfter Start")
print(driver.is_available)
print(trip.status)

# ============================================================
# CROSS-OBJECT COMMUNICATION
# ============================================================

# Very important observation.
#
# Trip.start()
#
# called:
#
# driver.accept_ride()
#
# One object invoked a method
# on another object.
#
# This is OOP in practice.
#
# Objects collaborate with each other.

# ============================================================
# STEP 4 - COMPLETING A TRIP
# ============================================================


class TripV4:

    def __init__(
        self,
        driver,
        rider,
        pickup,
        dropoff
    ):
        self.driver = driver
        self.rider = rider
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = "requested"

    def start(self):

        self.driver.accept_ride()

        self.status = "in_progress"

    def complete(self):

        self.driver.complete_ride()

        self.status = "completed"

        print(
            f"Trip completed for "
            f"{self.rider.name}."
        )


driver = Driver("Suresh", 4.5)

rider = Rider(
    "Kavya",
    "8888888888"
)

trip = TripV4(
    driver,
    rider,
    "Office",
    "Home"
)

trip.start()

trip.complete()

print(driver.is_available)
print(trip.status)

# ============================================================
# STATE PROPAGATION
# ============================================================

# The call originated from Trip.
#
# Yet Driver state changed.
#
# Before:
#
# driver.is_available = True
#
# During trip:
#
# driver.is_available = False
#
# After completion:
#
# driver.is_available = True
#
# Two objects.
#
# Shared behaviour.
#
# Shared state changes.

# ============================================================
# STEP 5 - STRING REPRESENTATION
# ============================================================


class TripV5:

    def __init__(
        self,
        driver,
        rider,
        pickup,
        dropoff
    ):
        self.driver = driver
        self.rider = rider
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = "requested"

    def __str__(self):

        return (
            f"Trip("
            f"driver={self.driver.name}, "
            f"rider={self.rider.name}, "
            f"status={self.status})"
        )


driver = Driver("Ramesh", 4.8)

rider = Rider(
    "Priya",
    "9876543210"
)

trip = TripV5(
    driver,
    rider,
    "Koramangala",
    "Indiranagar"
)

print("\nUsing __str__")
print(trip)

# ============================================================
# STEP 6 - ALTERNATIVE CONSTRUCTOR
# ============================================================

# Imagine Trip information arrives
# from an API.

trip_data = {
    "pickup": "Koramangala",
    "dropoff": "Indiranagar"
}


class TripFinal:

    def __init__(
        self,
        driver,
        rider,
        pickup,
        dropoff
    ):
        self.driver = driver
        self.rider = rider
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = "requested"

    def start(self):

        self.driver.accept_ride()

        self.status = "in_progress"

        print(
            f"Trip started: "
            f"{self.rider.name} -> "
            f"{self.dropoff}"
        )

    def complete(self):

        self.driver.complete_ride()

        self.status = "completed"

        print(
            f"Trip completed for "
            f"{self.rider.name}."
        )

    def __str__(self):

        return (
            f"Trip("
            f"driver={self.driver.name}, "
            f"rider={self.rider.name}, "
            f"status={self.status})"
        )

    @classmethod
    def from_dict(
        cls,
        data,
        driver,
        rider
    ):

        return cls(
            driver,
            rider,
            data["pickup"],
            data["dropoff"]
        )


driver = Driver("Amit", 4.7)

rider = Rider(
    "Neha",
    "7777777777"
)

trip = TripFinal.from_dict(
    trip_data,
    driver,
    rider
)

print("\nCreated Using from_dict()")
print(trip)

# ============================================================
# REFERENCE SEMANTICS REVISITED
# ============================================================

# Earlier we learned:
#
# driver_three = driver_one
#
# creates another reference.
#
# Now consider:
#
# self.driver = driver
#
# Are we storing a copy?
#
# No.
#
# We are storing a reference.
#
# There is only one Driver object.
#
# The variable driver refers to it.
#
# The Trip object also refers to it.
#
# Both point to the same object.

print("\nReference Check")

print(id(driver))
print(id(trip.driver))

# Same address.
#
# Same object.

# ============================================================
# FINAL DEMO
# ============================================================

print("\nBefore Trip Start")
print(driver.is_available)

trip.start()

print(driver.is_available)

trip.complete()

print(driver.is_available)

print(trip)

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Trip introduced a very important OOP idea.
#
# Objects can contain references to
# other objects.
#
# self.driver -> Driver Object
# self.rider  -> Rider Object
#
# Trip.start() can call:
#
# self.driver.accept_ride()
#
# This is cross-object communication.
#
# A Trip does not store copies.
#
# It stores references.
#
# There is only one Driver object
# in memory.
#
# Multiple objects can refer to it.
