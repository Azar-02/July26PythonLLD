"""
============================================================
PART 09
DEPENDENCY INJECTION (DI)
============================================================

Topics Covered
1. Why DIP alone is not enough
2. What is Dependency Injection?
3. Constructor Injection
4. Setter Injection
5. Method Injection
6. Manual Wiring
7. DI vs DIP
8. Interview Discussion
"""

from abc import ABC, abstractmethod

# ============================================================
# MOTIVATION
# ============================================================

# In the previous lesson we learned that high-level modules
# should depend on abstractions instead of concrete classes.
#
# Excellent.
#
# But a practical question still remains.
#
# If NotificationService depends upon NotificationChannel,
# then...
#
# Who creates the EmailChannel object?
#
# Who creates the SMSChannel object?
#
# Who decides which implementation should be supplied?
#
# That responsibility belongs outside the business class.

# ============================================================
# WITHOUT DEPENDENCY INJECTION
# ============================================================

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message):
        pass


class EmailChannel(NotificationChannel):

    def send(self, message):
        print(f"[Email] {message}")


class NotificationServiceV1:

    def __init__(self):
        # Business logic creates its own dependency.
        self.channel = EmailChannel()

    def notify(self, message):
        print("Processing notification...")
        self.channel.send(message)

print("=== Without Dependency Injection ===")
NotificationServiceV1().notify("Welcome!")

# ============================================================
# DISCUSSION
# ============================================================

# Problems:
#
# 1. NotificationService decides WHICH channel to use.
# 2. Testing becomes harder.
# 3. Replacing Email with SMS requires editing the class.
#
# The object has two responsibilities:
#
# - Business logic
# - Dependency creation
#
# We can improve this.

# ============================================================
# CONSTRUCTOR INJECTION
# ============================================================

class SMSChannel(NotificationChannel):

    def send(self, message):
        print(f"[SMS] {message}")


class WhatsAppChannel(NotificationChannel):

    def send(self, message):
        print(f"[WhatsApp] {message}")


class NotificationService:

    def __init__(self, channel: NotificationChannel):
        self.channel = channel

    def notify(self, message):
        print("Processing notification...")
        self.channel.send(message)

print("\n=== Constructor Injection ===")

email_service = NotificationService(EmailChannel())
sms_service = NotificationService(SMSChannel())
wa_service = NotificationService(WhatsAppChannel())

email_service.notify("Order Confirmed")
sms_service.notify("OTP Sent")
wa_service.notify("Package Delivered")

# ============================================================
# OBSERVATION
# ============================================================

# NotificationService never creates EmailChannel().
#
# Someone else creates the dependency and injects it.
#
# This is Constructor Injection.
#
# Constructor Injection is the most commonly used form
# of Dependency Injection because objects are fully
# initialized immediately after construction.

# ============================================================
# SETTER INJECTION
# ============================================================

class ReportGenerator:

    def __init__(self):
        self.channel = None

    def set_channel(self, channel: NotificationChannel):
        self.channel = channel

    def send_report(self):
        if self.channel:
            self.channel.send("Weekly Report")
        else:
            print("No channel configured.")

print("\n=== Setter Injection ===")

report = ReportGenerator()
report.send_report()

report.set_channel(EmailChannel())
report.send_report()

# ============================================================
# DISCUSSION
# ============================================================

# Setter Injection is useful when the dependency
# is optional or may change after object creation.
#
# However...
#
# Objects can temporarily exist in an incomplete state.

# ============================================================
# METHOD INJECTION
# ============================================================

class AlertService:

    def send_alert(self, message, channel: NotificationChannel):
        print("Alert Generated")
        channel.send(message)

print("\n=== Method Injection ===")

alert = AlertService()

alert.send_alert("Disk Space Low", EmailChannel())
alert.send_alert("CPU Usage High", SMSChannel())

# ============================================================
# DISCUSSION
# ============================================================

# Method Injection is useful when a dependency
# is needed only for one operation.
#
# The object does not permanently store it.

# ============================================================
# MANUAL WIRING
# ============================================================

# Imagine this file acts as main.py

def build_application():

    channel = WhatsAppChannel()

    notification_service = NotificationService(channel)

    return notification_service

print("\n=== Manual Wiring ===")

app = build_application()
app.notify("Application Started")

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# What happens if build_application()
# returns SMSChannel instead?
#
# Will NotificationService change?
#
# No.
#
# Only the wiring changes.

# ============================================================
# DI VS DIP
# ============================================================

# Many students confuse these concepts.
#
# DIP (Dependency Inversion Principle)
#
# -> Design Principle
#
# High-level modules should depend upon abstractions.
#
#
# DI (Dependency Injection)
#
# -> Implementation Technique
#
# Someone else provides those abstractions.

# ============================================================
# SMALL EXPERIMENT
# ============================================================

class MockChannel(NotificationChannel):

    def send(self, message):
        print(f"[MOCK] {message}")

print("\n=== Testing ===")

test_service = NotificationService(MockChannel())
test_service.notify("Unit Test")

# ============================================================
# WHY MOCK OBJECTS?
# ============================================================

# During testing we often do not want to:
#
# • Send real emails.
# • Send real SMS messages.
# • Contact external systems.
#
# Dependency Injection makes testing simple because
# fake implementations can be injected.

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# 1. DI is NOT the same as DIP.
#
# 2. A framework is NOT required for DI.
#
# 3. Spring Boot performs Dependency Injection,
#    but the concept itself is framework-independent.

# ============================================================
# INTERVIEW CORNER
# ============================================================

# Q. Which type of DI is most commonly used?
#
# A. Constructor Injection.
#
# Q. Why?
#
# Because dependencies become mandatory,
# objects remain immutable where possible,
# and testing becomes easier.
#
# Q. Is DI a SOLID principle?
#
# No.
#
# DI is a design technique that helps
# implement the Dependency Inversion Principle.

# ============================================================
# BOARD SUMMARY
# ============================================================

# Without DI
#
# Business Class
#      |
#      v
# Creates Dependency
#
#
# With DI
#
# External Builder
#        |
#        v
# Supplies Dependency
#        |
#        v
# Business Class
#
# Result:
# Cleaner, flexible, testable design.

# ============================================================
# BRIDGE TO NEXT TOPIC
# ============================================================

# We have now completed the five SOLID principles
# along with Dependency Injection.
#
# The final lesson brings everything together using
# practical AI-assisted design discussions and
# complete SOLID revision examples.
