"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 03_decorator_in_real_tools.py
============================================================

Topics Covered
--------------
1.  Where File 02 Left Us
2.  What open() Actually Hands You
3.  Proving It Is Layered
4.  What Each Layer Adds
5.  A Decorator Chain In The Standard Library
6.  Styling A Button With CSS
7.  The @ You Have Already Typed
8.  A Function Decorator
9.  Who Plays Mocha, Who Plays Espresso
10. Objects vs Functions
11. Key Takeaways
"""

# ============================================================
# WHERE FILE 02 LEFT US
# ============================================================

# Whip wrapping Mocha wrapping
# Espresso.
#
# One shared interface.
#
# A base that wraps nothing.
#
# Layers that each add one
# thing.
#
# That was a coffee shop.
#
# Now watch the same shape
# turn up somewhere you have
# been using for years.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# When you write:
#
#     open("notes.txt")
#
# to read a file —
#
# do you think Python hands
# you back one single object
# doing everything?
#
# Or something layered?
#
# The way we just built Whip
# wrapping Mocha wrapping
# Espresso.

# ============================================================
# THE HONEST ANSWER
# ============================================================

# Most people are not sure.
#
# And the usual guess is:
#
#     probably one single
#     object
#
# Since that is all we ever
# see, or think about.

# ============================================================
# IT IS ACTUALLY LAYERED
# ============================================================

# And we can prove it right
# now.

f = open("notes.txt", "w")
f.write("hello")
f.close()

f = open("notes.txt")

print("What open() Hands You")
print(f)
print(f.buffer)
print(f.buffer.raw)

# Expected output:
#
# <_io.TextIOWrapper name='notes.txt' mode='r' encoding='UTF-8'>
#
# <_io.BufferedReader name='notes.txt'>
#
# <_io.FileIO name='notes.txt' mode='rb' closefd=True>

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Three names.
#
# Three layers.
#
# Based on what we just built
# with Espresso, Mocha and
# Whip —
#
# what do you think each layer
# is adding?

# ============================================================
# THE THREE LAYERS
# ============================================================

# FileIO
#
#     The base.
#
#     Does the actual, raw work
#     of talking to the
#     operating system's file.
#
#     One raw byte at a time.
#
# BufferedReader
#
#     Wraps FileIO.
#
#     Adds buffering, so Python
#     isn't asking the
#     operating system for data
#     one byte at a time.
#
#     Which would be painfully
#     slow.
#
# TextIOWrapper
#
#     Wraps BufferedReader.
#
#     Adds text decoding —
#     turning raw bytes into
#     str.
#
#     Plus convenience like
#     readline(), and looping
#     over a file line by line.

# ============================================================
# WHAT THIS MEANS
# ============================================================

# This is a real decorator
# chain.
#
# Sitting inside Python's
# standard library.
#
# Running every single time
# any of you have ever opened
# a file.
#
# The base does the raw work.
#
# Each layer wraps the thing
# before it and adds one new
# behaviour on top.
#
# Exactly the shape of Whip
# wrapping Mocha wrapping
# Espresso.

f.close()

# ============================================================
# A QUICK VISUAL EXAMPLE
# ============================================================

# Think about styling an HTML
# button.
#
# You start with a plain
# <button>.
#
# Then CSS adds a border.
#
# Then a margin.
#
# Then a hover shadow.
#
# Is that the same idea?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# Yes.
#
# The button itself never
# changes.
#
# Each style rule adds one
# visual behaviour on top.
#
# The same way each layer in
# our file example adds one
# behaviour on top.

# ============================================================
# SOMETHING YOU HAVE ALREADY TYPED
# ============================================================

# Have any of you written
# something like:
#
#     @staticmethod
#
#     @property
#
# or a custom:
#
#     @login_required
#
# sitting right above a
# function definition?
#
# Most people have written at
# least @staticmethod.
#
# Probably others too.

# ============================================================
# WHAT THAT @ ACTUALLY IS
# ============================================================

# That @ syntax is literally
# named after this exact
# pattern.
#
# A function decorator wraps
# another function and adds
# behaviour around it.
#
# Before it runs.
#
# After it runs.
#
# Or both.
#
# Without changing the
# original function's own
# code.

# ============================================================
# A FUNCTION DECORATOR
# ============================================================


def logging_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper


@logging_decorator
def send_message(msg):
    print(f"Sending: {msg}")


print("\nA Function Decorator")

send_message("hello")

# Expected output:
#
# Calling send_message
#
# Sending: hello
#
# Finished send_message

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Where's the "wrapping"
# happening here?
#
# What's playing the role of
# Mocha?
#
# And what's playing the role
# of Espresso ?

# ============================================================
# THE ANSWER
# ============================================================

# wrapper is the decorator
# layer.
#
# Like Mocha.
#
# The original send_message
# function is the base being
# wrapped.
#
# Like Espresso.
#
# send_message itself never
# changes.
#
# wrapper runs code before and
# after calling it, then hands
# back the result.

# ============================================================
# OBJECTS vs FUNCTIONS
# ============================================================

# Worth flagging explicitly.
#
# Today's Beverage example
# decorates OBJECTS.
#
# By wrapping them in other
# objects that share a common
# type.
#
# Python's @decorator syntax
# decorates FUNCTIONS.
#
# By wrapping them in other
# functions.
#
# Same underlying idea.
#
#     wrap something,
#
#     add behaviour around it,
#
#     leave the original
#     untouched.
#
# Just applied to two
# different kinds of things.
#
# Students sometimes assume
# these are unrelated, because
# the code looks so different.
#
# They're really the same
# pattern, one level apart.

# ============================================================
# CHECKPOINT
# ============================================================

# Three sightings now.
#
# A coffee order.
#
# Every file you have ever
# opened.
#
# Every @ you have ever typed.
#
# One shape underneath all
# three.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# open() does not hand back
# one object.
#
# It hands back TextIOWrapper
# wrapping BufferedReader
# wrapping FileIO.
#
# The base does the raw work,
# and each layer adds exactly
# one behaviour.
#
# CSS styling a button is the
# same idea — the button never
# changes, each rule adds one
# visual behaviour.
#
# Python's @ syntax is named
# after this pattern.
#
# A function decorator wraps a
# function and runs code
# before, after, or both.
#
# Decorating objects and
# decorating functions are the
# same pattern, one level
# apart.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# So far: coffee, files, and
# the @ symbol.
#
# Next we build the version
# you will actually write at
# work.
#
# One service that sends a
# notification.
#
# And a business that keeps
# asking for one more thing —
#
#     log it,
#
#     retry it,
#
#     rate limit it.
#
# Next:
#
# 04_decorator_in_a_real_backend.py
