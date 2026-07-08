"""
============================================================
LLD-3 : OOP-2 (ENCAPSULATION)
PART 9 - DRIVER REFACTORING
============================================================

Topics Covered
--------------
1. Revisiting Driver
2. Property-Based Validation
3. Name Validation
4. Rating Validation
5. Mutable Default Argument Fix
6. Named Constructors
7. from_dict()
8. from_string()
9. from_env()
10. Final Refactored Driver

NOTE:
This file combines the concepts learned so far:

- Encapsulation
- @property
- Validation
- Constructor Patterns

The goal is to refactor our Driver class
into a safer and more maintainable design.
"""

# ============================================================
# MOTIVATION
# ============================================================

# Earlier we had a Driver class.
#
# Example:
#
# driver = Driver("Ramesh", 4.8)
#
# The class worked.
#
# However several problems existed.
#
# Problem 1:
#
# Invalid ratings were possible.
#
# driver.rating = -999
#
# Problem 2:
#
# Empty names were possible.
#
# driver.name = ""
#
# Problem 3:
#
# Mutable default arguments can
# accidentally share state.
#
# Problem 4:
#
# Object creation could become
# repetitive when data comes from
# dictionaries or strings.
#
# Today's goal:
#
# Refactor Driver and fix all of them.

# ============================================================
# OLD DESIGN
# ============================================================


class DriverV1:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating


driver = DriverV1("Ramesh", 4.8)

driver.rating = -999

print("V1")

print(driver.rating)

# Observation:
#
# Invalid data is accepted.
#
# The object cannot protect itself.

# ============================================================
# ADDING NAME VALIDATION
# ============================================================


class DriverV2:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):

            raise ValueError(
                "Name must be a string"
            )

        if not value.strip():

            raise ValueError(
                "Name cannot be empty"
            )

        self._name = value


driver = DriverV2("Ramesh", 4.8)

print("\nName Validation")

print(driver.name)

# ============================================================
# ADDING RATING VALIDATION
# ============================================================


class DriverV3:

    def __init__(self, name, rating):

        self.name = name
        self.rating = rating

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):

            raise ValueError(
                "Name must be a string"
            )

        if not value.strip():

            raise ValueError(
                "Name cannot be empty"
            )

        self._name = value

    @property
    def rating(self):

        return self._rating

    @rating.setter
    def rating(self, value):

        if not (0.0 <= value <= 5.0):

            raise ValueError(
                "Rating must be between "
                "0.0 and 5.0"
            )

        self._rating = value


driver = DriverV3("Ramesh", 4.8)

print("\nRating Validation")

print(driver.rating)

# ============================================================
# VALIDATION DURING CREATION
# ============================================================

# Notice:
#
# Inside __init__ we write:
#
# self.name = name
# self.rating = rating
#
# These assignments go through
# the property setters.
#
# Therefore validation happens
# even while the object is being created.

# Example:
#
# DriverV3("Ramesh", -10)
#
# Raises ValueError immediately.

# ============================================================
# ADDING TRIPS
# ============================================================


class DriverV4:

    def __init__(
        self,
        name,
        rating,
        trips=None
    ):

        self.name = name
        self.rating = rating

        if trips is None:

            self.trips = []

        else:

            self.trips = trips

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):

            raise ValueError(
                "Name must be a string"
            )

        if not value.strip():

            raise ValueError(
                "Name cannot be empty"
            )

        self._name = value

    @property
    def rating(self):

        return self._rating

    @rating.setter
    def rating(self, value):

        if not (0.0 <= value <= 5.0):

            raise ValueError(
                "Rating must be between "
                "0.0 and 5.0"
            )

        self._rating = value


driver_one = DriverV4(
    "Ramesh",
    4.8
)

driver_two = DriverV4(
    "Suresh",
    4.5
)

driver_one.trips.append("trip_101")

print("\nTrips")

print(driver_one.trips)
print(driver_two.trips)

# Different drivers.
#
# Different lists.

# ============================================================
# ADDING REPRESENTATION
# ============================================================


class DriverV5:

    def __init__(
        self,
        name,
        rating,
        trips=None
    ):

        self.name = name
        self.rating = rating

        self.trips = (
            trips
            if trips is not None
            else []
        )

        self.is_available = True

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):

            raise ValueError(
                "Name must be a string"
            )

        if not value.strip():

            raise ValueError(
                "Name cannot be empty"
            )

        self._name = value

    @property
    def rating(self):

        return self._rating

    @rating.setter
    def rating(self, value):

        if not (0.0 <= value <= 5.0):

            raise ValueError(
                "Rating must be between "
                "0.0 and 5.0"
            )

        self._rating = value

    def __str__(self):

        return (
            f"Driver("
            f"name={self.name}, "
            f"rating={self.rating}, "
            f"available={self.is_available}"
            f")"
        )


driver = DriverV5(
    "Ramesh",
    4.8
)

print("\nString Representation")

print(driver)

# ============================================================
# ADDING NAMED CONSTRUCTORS
# ============================================================

import os


class Driver:

    def __init__(
        self,
        name,
        rating,
        trips=None
    ):

        self.name = name
        self.rating = rating

        self.trips = (
            trips
            if trips is not None
            else []
        )

        self.is_available = True

    # ------------------------------------------------
    # name property
    # ------------------------------------------------

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):

            raise ValueError(
                "Name must be a string"
            )

        if not value.strip():

            raise ValueError(
                "Name cannot be empty"
            )

        self._name = value

    # ------------------------------------------------
    # rating property
    # ------------------------------------------------

    @property
    def rating(self):

        return self._rating

    @rating.setter
    def rating(self, value):

        if not (0.0 <= value <= 5.0):

            raise ValueError(
                "Rating must be between "
                "0.0 and 5.0"
            )

        self._rating = value

    # ------------------------------------------------
    # behaviour
    # ------------------------------------------------

    def accept_ride(self):

        if self.is_available:

            self.is_available = False

            print(
                f"{self.name} "
                f"accepted a ride."
            )

        else:

            print(
                f"{self.name} "
                f"is not available."
            )

    def complete_ride(self):

        self.is_available = True

        print(
            f"{self.name} "
            f"completed the ride."
        )

    # ------------------------------------------------
    # representations
    # ------------------------------------------------

    def __str__(self):

        return (
            f"Driver("
            f"name={self.name}, "
            f"rating={self.rating}, "
            f"available={self.is_available}"
            f")"
        )

    def __repr__(self):

        return (
            f"Driver("
            f"name='{self.name}', "
            f"rating={self.rating}"
            f")"
        )

    # ------------------------------------------------
    # named constructors
    # ------------------------------------------------

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["name"],
            data["rating"]
        )

    @classmethod
    def from_string(cls, text):

        name, rating = text.split(",")

        return cls(
            name,
            float(rating)
        )

    @classmethod
    def from_env(cls):

        name = os.environ.get(
            "DRIVER_NAME",
            "TestDriver"
        )

        rating = float(
            os.environ.get(
                "DRIVER_RATING",
                "5.0"
            )
        )

        return cls(
            name,
            rating
        )

    # ------------------------------------------------
    # utility
    # ------------------------------------------------

    @staticmethod
    def is_valid_license(
        license_number
    ):

        return (
            isinstance(
                license_number,
                str
            )
            and len(license_number) == 16
        )


# ============================================================
# USING NAMED CONSTRUCTORS
# ============================================================

driver_a = Driver.from_dict(
    {
        "name": "Ramesh",
        "rating": 4.8
    }
)

driver_b = Driver.from_string(
    "Suresh,4.5"
)

driver_c = Driver.from_env()

print("\nNamed Constructors")

print(driver_a)
print(driver_b)
print(driver_c)

# ============================================================
# FINAL RESULT
# ============================================================

# Earlier:
#
# driver.rating = -999
#
# was accepted.
#
# Now:
#
# ValueError is raised.
#
# Earlier:
#
# Empty names were allowed.
#
# Now:
#
# Validation prevents it.
#
# Earlier:
#
# trips=[] could create
# shared state.
#
# Now:
#
# Each driver gets its own list.
#
# Earlier:
#
# Creating objects from
# different data sources
# required repetitive code.
#
# Now:
#
# Named constructors make
# object creation explicit.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Use properties to protect data.
#
# Validation should happen inside
# the object itself.
#
# Use:
#
# trips=None
#
# instead of:
#
# trips=[]
#
# Use named constructors when
# objects can be created from
# multiple data sources.
#
# Refactoring is the process of
# improving design without changing
# the external behaviour.
