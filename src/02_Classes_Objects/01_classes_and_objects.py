
"""
============================================================
LLD-2 : OOP-1
PART 1 - CLASSES AND OBJECTS
============================================================
"""

print("=" * 60)
print("PART 1 - CLASSES AND OBJECTS")
print("=" * 60)

"""
MOTIVATION
----------
Suppose we are building Uber.
Driver, Rider, Trip, Vehicle, Payment are entities.
Classes help Python understand these entities.
"""

class Driver:
    pass

class Rider:
    pass

driver_one = Driver()
driver_two = Driver()
rider_one = Rider()

# Python creates these attributes dynamically at runtime. Different objects can have different attributes.
driver_one.name = "Ramesh"
driver_two.name = "Suresh"
driver_one.rating = 4.8

print(driver_one)
print(driver_two)
print(rider_one)

print(driver_one.name)
print(driver_two.name)