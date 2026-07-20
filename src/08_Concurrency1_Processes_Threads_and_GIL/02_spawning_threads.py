"""
============================================================
CONCURRENCY-1
FILE : 02_spawning_threads.py
============================================================

Topics Covered
--------------
1. Why Create Multiple Threads?
2. Creating a Thread
3. target Parameter
4. args Parameter
5. start()
6. join()
7. Main Thread vs Child Threads
8. Thread Execution Order
9. Common Mistakes
10. Interview Questions
11. Key Takeaways

"""

import threading
import time

# ============================================================
# MOTIVATION
# ============================================================

# Suppose a delivery partner
# gets assigned an order.
#
# We need to:
#
# - Assign order
# - Send SMS
# - Send Push Notification
#
# If everything runs one after another,
# the user may wait unnecessarily.
#
# Multiple threads allow different
# tasks to progress independently.

# ============================================================
# FIRST THREAD
# ============================================================

def notify_partner(partner_id):

    print(f"Notifying {partner_id}...")

    time.sleep(1)

    print(f"{partner_id} notified.")


# Thread object creation

t1 = threading.Thread(
    target=notify_partner,
    args=("P101",)
)

# Observation:
#
# Thread object is created.
#
# Function has NOT started yet.

# ============================================================
# TARGET PARAMETER
# ============================================================

# target specifies:
#
# Which function should run
# inside the new thread.

# Example:
#
# threading.Thread(
#     target=my_function
# )

# ============================================================
# ARGS PARAMETER
# ============================================================

# args specifies:
#
# Arguments passed to the target function.

# Example:
#
# threading.Thread(
#     target=notify_partner,
#     args=("P101",)
# )

# Important:
#
# args must be a tuple.

# Single value tuple:
#
# ("P101",)

# Not:
#
# ("P101")

# ============================================================
# STARTING A THREAD
# ============================================================

print("Starting Thread")

t1.start()

# Observation:
#
# start() creates a new path
# of execution.
#
# The function begins running
# inside the thread.

# ============================================================
# MULTIPLE THREADS
# ============================================================

def send_notification(partner_id):

    print(f"Sending notification to {partner_id}")

    time.sleep(1)

    print(f"Notification sent to {partner_id}")


t2 = threading.Thread(
    target=send_notification,
    args=("P102",)
)

t2.start()

# Observation:
#
# Multiple threads can run
# within the same process.

# ============================================================
# EXECUTION ORDER
# ============================================================

# Question:
#
# Which thread finishes first?
#
# Answer:
#
# No guaranteed order.

# Thread scheduling is controlled by:
#
# - Python runtime
# - Operating System

# Therefore:
#
# Execution order should never
# be assumed.

# ============================================================
# MAIN THREAD
# ============================================================

print("Main Thread Continues")

# Observation:
#
# Main thread does NOT wait
# automatically.
#
# It continues executing
# the next statement.

# ============================================================
# WHAT DOES start() DO?
# ============================================================

# start()
#
# Means:
#
# Launch the thread.
#
# Do not wait.

# Important:
#
# start() does NOT execute
# the function directly.
#
# Instead:
#
# It asks Python to schedule
# a new thread.

# ============================================================
# THE PROBLEM
# ============================================================

# Suppose main thread finishes.
#
# Background work may still
# be running.
#
# Sometimes we need to wait.

# ============================================================
# JOIN
# ============================================================

# join()
#
# Means:
#
# Wait until this thread
# completes execution.

# Example

t1.join()
t2.join()

print("All Threads Finished")

# Observation:
#
# Main thread pauses here
# until both threads complete.

# ============================================================
# START VS JOIN
# ============================================================

# start()
#
# Launch thread.
#
# Do not wait.

# join()
#
# Wait for completion.

# Quick Memory Trick:
#
# start() = Begin
#
# join() = Wait

# ============================================================
# PRACTICAL SCENARIO
# ============================================================

# Consider:
#
# User places order.
#
# Backend:
#
# - Save order
# - Send email
# - Send SMS
#
# If email takes time,
# we may use a background thread.
#
# Main response can be sent
# immediately.

# ============================================================
# COMMON MISTAKE #1
# ============================================================

# Calling function directly.

# Wrong:
#
# threading.Thread(
#     target=notify_partner()
# )
#
# Function executes immediately.

# Correct:
#
# threading.Thread(
#     target=notify_partner
# )

# ============================================================
# COMMON MISTAKE #2
# ============================================================

# Forgetting comma in args.

# Wrong:
#
# args=("P101")
#
# Correct:
#
# args=("P101",)

# ============================================================
# COMMON MISTAKE #3
# ============================================================

# Assuming thread order.

# Wrong:
#
# Expecting:
#
# Thread1
# Thread2
# Thread3
#
# every time.
#
# Order may change.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Difference between:
#
# start()
#
# and
#
# join()
#
# start():
# Launches thread.
#
# join():
# Waits for thread completion.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Thread object:
#
# threading.Thread()

# target:
#
# Function to execute.

# args:
#
# Function arguments.

# start():
#
# Creates a new thread
# and begins execution.

# join():
#
# Waits for completion.

# Main thread:
#
# Does not automatically wait.

# Thread execution order:
#
# Not guaranteed.

# Multiple threads:
#
# Can exist inside
# the same process.
