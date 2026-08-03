"""
============================================================
LLD-2 : OOP-1
PART 10 - MAIN INTEGRATION
============================================================

Topics Covered
--------------
1. Bringing Driver, Rider and Trip Together
2. Creating Objects from Real Data
3. Wiring Objects Together
4. Starting a Trip
5. Completing a Trip
6. Observing State Changes
7. Object Collaboration
"""

# ============================================================
# MOTIVATION
# ============================================================

# So far we have built three entities:
#
# Driver
# Rider
# Trip
#
# Individually they work.
#
# But real systems are not built from isolated
# classes.
#
# Real systems are built from objects
# collaborating with each other.
#
# This file brings everything together
# into one complete Uber flow.

# ============================================================
# DRIVER
# ============================================================


class Driver:

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.is_available = True

    def accept_ride(self):

        if self.is_available:

            self.is_available = False

            print(
                f"{self.name} has accepted a ride."
            )
        else:

            print(
                f"{self.name} is not available."
            )

    def complete_ride(self):

        self.is_available = True

        print(
            f"{self.name} has completed the ride "
            f"and is available again."
        )

    def __str__(self):

        return (
            f"Driver(name={self.name}, "
            f"rating={self.rating}, "
            f"available={self.is_available})"
        )

    def __repr__(self):

        return (
            f"Driver(name='{self.name}', "
            f"rating={self.rating})"
        )

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["name"],
            data["rating"]
        )


# ============================================================
# RIDER
# ============================================================


class Rider:

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


# ============================================================
# TRIP
# ============================================================


class Trip:

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


# ============================================================
# STEP 1 - CREATE DRIVER
# ============================================================

# In a real system this data may arrive
# from an API response.

driver_data = {
    "name": "Ramesh",
    "rating": 4.8
}

driver = Driver.from_dict(driver_data)

print("Driver Created")
print(driver)

# ============================================================
# STEP 2 - CREATE RIDER
# ============================================================

rider = Rider(
    "Priya",
    "9876543210"
)

print("\nRider Created")
print(rider)

# ============================================================
# STEP 3 - CREATE TRIP
# ============================================================

trip = Trip(
    driver,
    rider,
    pickup="Koramangala",
    dropoff="Indiranagar"
)

print("\nTrip Created")
print(trip)

# Expected Output:
#
# Trip(
#     driver=Ramesh,
#     rider=Priya,
#     status=requested
# )

# ============================================================
# IMPORTANT OBSERVATION
# ============================================================

# Trip stores:
#
# self.driver
# self.rider
#
# These are references to objects.
#
# Not copies.
#
# There is only one Driver object.
#
# Both:
#
# driver
#
# and
#
# trip.driver
#
# point to the same object.

print("\nReference Check")

print(id(driver))
print(id(trip.driver))

# Same address.
#
# Same object.

# ============================================================
# STEP 4 - START THE TRIP
# ============================================================

print("\nBefore Trip Start")

print("Driver Available:", driver.is_available)
print("Trip Status:", trip.status)

trip.start()

print("\nAfter Trip Start")

print("Driver Available:", driver.is_available)
print("Trip Status:", trip.status)

# Observation:
#
# Trip called:
#
# self.driver.accept_ride()
#
# The Driver state changed.
#
# is_available:
#
# True -> False

# ============================================================
# CROSS-OBJECT COMMUNICATION
# ============================================================

# This is one of the most important ideas
# in the entire lecture.
#
# Trip reached into Driver
# and changed Driver state.
#
# Two objects communicating.
#
# Two objects collaborating.
#
# This is OOP in practice.

# ============================================================
# STEP 5 - COMPLETE THE TRIP
# ============================================================

trip.complete()

print("\nAfter Trip Completion")

print("Driver Available:", driver.is_available)
print("Trip Status:", trip.status)

# Observation:
#
# Driver state:
#
# False -> True
#
# Trip state:
#
# in_progress -> completed

# ============================================================
# STATE PROPAGATION
# ============================================================

# Notice that the call started from:
#
# trip.complete()
#
# Yet Driver changed.
#
# Why?
#
# Because Trip holds a reference
# to the actual Driver object.
#
# There is only one Driver object
# in memory.

# ============================================================
# FINAL OUTPUT
# ============================================================

print("\nFinal Trip")

print(trip)

# Expected Output:
#
# Trip(
#     driver=Ramesh,
#     rider=Priya,
#     status=completed
# )

# ============================================================
# COMPLETE FLOW
# ============================================================

# Driver Created
# Rider Created
# Trip Created
#
# Trip Started
#
# Driver became unavailable
#
# Trip Completed
#
# Driver became available again

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Classes become useful when they
# work together.
#
# Driver, Rider and Trip are not isolated.
#
# They collaborate.
#
# Trip contains references to:
#
# - Driver
# - Rider
#
# Starting a Trip changes Driver state.
#
# Completing a Trip changes Driver state.
#
# Objects communicate through methods.
#
# This is the foundation on which
# larger OOP systems are built.
