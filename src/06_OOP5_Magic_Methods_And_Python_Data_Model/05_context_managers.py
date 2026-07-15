"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 05_context_managers.py
============================================================

Topics Covered
--------------
1. Resource Management Problem
2. The try-finally Pattern
3. Motivation For Context Managers
4. The with Statement
5. __enter__
6. __exit__
7. Building A Custom Context Manager
8. Exception Handling
9. Multiple Context Managers
10. Real World Use Cases
11. Interview Questions
12. Key Takeaways
"""

# ============================================================
# MOTIVATION
# ============================================================

# Consider the following situation:
#
# Open a file.
#
# Read data.
#
# Close the file.
#
# Sounds simple.
#
# The problem appears when:
#
# Exceptions occur.
#
# Early returns happen.
#
# Developers forget cleanup.
#
# Resource leaks become possible.

# ============================================================
# THE CLASSIC APPROACH
# ============================================================

file = None

try:

    file = open(__file__, "r")

    first_line = file.readline()

    print("First Line Read Successfully")

finally:

    if file:
        file.close()

print("File Closed")

# Observation:
#
# Cleanup happens inside finally.
#
# This works.
#
# But the code becomes repetitive.

# ============================================================
# THE REAL PROBLEM
# ============================================================

# Imagine:
#
# Database Connections
# Network Sockets
# Locks
# Files
#
# Every resource requires:
#
# Acquire
# Use
# Release
#
# Repeating try-finally
# everywhere is tedious.

# ============================================================
# THE PATTERN
# ============================================================

# Resource Lifecycle:
#
# Step 1
#
# Acquire Resource
#
# Step 2
#
# Use Resource
#
# Step 3
#
# Release Resource
#
# This pattern appears constantly.

# ============================================================
# ENTER CONTEXT MANAGERS
# ============================================================

# Python provides:
#
# with
#
# to manage this pattern.
#
# Example:
#
# with open(...) as file:
#     ...
#
# Cleanup happens automatically.

# ============================================================
# SIMPLE WITH EXAMPLE
# ============================================================

with open(__file__, "r") as file:

    first_line = file.readline()

    print("\nUsing with")

    print(first_line.strip())

# Observation:
#
# File automatically closes.
#
# No explicit close() call needed.

# ============================================================
# IMPORTANT IDEA
# ============================================================

# with is not special-cased
# only for files.
#
# Any object can participate.
#
# Requirement:
#
# Implement a protocol.

# ============================================================
# THE CONTEXT MANAGER PROTOCOL
# ============================================================

# Required Methods:
#
# __enter__
# __exit__
#
# If these methods exist,
# the object can be used
# with the with statement.

# ============================================================
# FIRST CUSTOM CONTEXT MANAGER
# ============================================================


class DatabaseConnection:

    def __enter__(self):

        print("\nOpening Database Connection")

        return self

    def query(self):

        print("Executing Query")

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        print("Closing Database Connection")


# ============================================================
# USING THE CONTEXT MANAGER
# ============================================================

with DatabaseConnection() as db:

    db.query()

# Observation:
#
# __enter__ runs first.
#
# __exit__ runs last.

# ============================================================
# UNDERSTANDING __enter__
# ============================================================

# __enter__ is responsible for:
#
# Acquiring resources.
#
# It returns the object
# assigned after:
#
# as

# ============================================================
# DEMO
# ============================================================


class DriverRegistry:

    def __enter__(self):

        print("\nLoading Driver Registry")

        return self

    def show(self):

        print("Drivers Loaded")

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        print("Registry Cleanup Complete")


with DriverRegistry() as registry:

    registry.show()

# Observation:
#
# Value returned by __enter__
# becomes registry.

# ============================================================
# UNDERSTANDING __exit__
# ============================================================

# __exit__ is responsible for:
#
# Cleanup.
#
# Releasing resources.
#
# Final actions.

# ============================================================
# EXCEPTION INFORMATION
# ============================================================

# __exit__ receives:
#
# exc_type
# exc_value
# traceback
#
# These contain exception details.

# ============================================================
# EXCEPTION DEMO
# ============================================================


class PaymentSession:

    def __enter__(self):

        print("\nOpening Payment Session")

        return self

    def process(self):

        print("Processing Payment")

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        print("Cleaning Payment Session")

        print("Exception Type:", exc_type)

        print("Exception Value:", exc_value)


try:

    with PaymentSession() as session:

        session.process()

        raise ValueError("Invalid Fare")

except ValueError:

    print("Exception Handled Outside")

# Observation:
#
# __exit__ still executes.
#
# Cleanup is guaranteed.

# ============================================================
# WHY THIS IS IMPORTANT
# ============================================================

# Imagine:
#
# Database Connection Open
#
# Then Exception Occurs.
#
# Without cleanup:
#
# Connection Leak.
#
# Context managers prevent this.

# ============================================================
# SUPPRESSING EXCEPTIONS
# ============================================================

# Returning True from __exit__
# suppresses exceptions.

# ============================================================
# DEMO
# ============================================================


class SafeSession:

    def __enter__(self):

        print("\nSession Started")

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        print("Session Closed")

        return True


with SafeSession():

    raise ValueError("Hidden Error")

print("Program Continued")

# Observation:
#
# Exception was suppressed.

# ============================================================
# MULTIPLE CONTEXT MANAGERS
# ============================================================

# Multiple resources can be
# managed together.


class ResourceA:

    def __enter__(self):

        print("\nAcquire A")

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        print("Release A")


class ResourceB:

    def __enter__(self):

        print("Acquire B")

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        print("Release B")


with ResourceA(), ResourceB():

    print("Using Resources")

# Observation:
#
# Resources release in reverse order.

# ============================================================
# REAL WORLD EXAMPLES
# ============================================================

# Files
#
# with open(...)
#
#
# Database Transactions
#
# with transaction:
#
#
# Locks
#
# with lock:
#
#
# Network Connections
#
# with socket:

# ============================================================
# CONTEXT MANAGERS AND LLD
# ============================================================

# Context Managers provide:
#
# Encapsulation
# Safety
# Predictable Cleanup
#
# They are an example of
# protocol-based design.

# ============================================================
# COMMON MISTAKE
# ============================================================

# Forgetting that __exit__
# executes even when exceptions occur.

# ============================================================
# INTERVIEW QUESTION #1
# ============================================================

# Which methods must be implemented
# to support the with statement?
#
# Answer:
#
# __enter__
# __exit__

# ============================================================
# INTERVIEW QUESTION #2
# ============================================================

# Which method receives exception
# information?
#
# Answer:
#
# __exit__

# ============================================================
# INTERVIEW QUESTION #3
# ============================================================

# What happens if __exit__
# returns True?
#
# Answer:
#
# The exception is suppressed.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Context Managers solve
# resource management problems.
#
# with implements:
#
# Acquire
# Use
# Release
#
# __enter__ acquires.
#
# __exit__ cleans up.
#
# Cleanup happens even when
# exceptions occur.
#
# Context Managers are based on
# a protocol.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# So far we have explored:
#
# __len__
# __eq__
# __hash__
# __enter__
# __exit__
#
# Next we study another
# powerful protocol:
#
# Callable Objects.
#
# Next:
#
# 06_callable_objects.py
