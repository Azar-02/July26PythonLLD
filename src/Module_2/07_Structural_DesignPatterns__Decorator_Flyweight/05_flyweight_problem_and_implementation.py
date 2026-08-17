"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 05_flyweight_problem_and_implementation.py
============================================================

Topics Covered
--------------
1.  Where File 04 Left Us
2.  One Book, Hundreds Of Readers
3.  Flyweight : The General Idea
4.  The PUBG Bullet Problem
5.  The Naive Bullet
6.  Doing The Memory Maths
7.  Why 100 MB Is The Wrong Complaint
8.  Splitting The Fields
9.  Intrinsic vs Extrinsic
10. Coding The Shared Half
11. The Factory That Guarantees Sharing
12. Coding The Unique Half
13. Proving Only One Copy Exists
14. Quiz
15. Key Takeaways
"""

# ============================================================
# WHERE FILE 04 LEFT US
# ============================================================

# Decorator answered:
#
#     "how do I keep adding
#      behaviour without
#      editing the original
#      class?"
#
# Today's second pattern
# answers something else
# entirely.
#
# Not behaviour.
#
# Memory.

# ============================================================
# WARM UP : THE LIBRARY
# ============================================================

# Think about a library.
#
# There's one physical copy of
# a popular book.
#
# And hundreds of students
# read it across the year.
#
# What would it cost the
# library — in money and shelf
# space — if instead they
# bought a brand-new copy for
# every single student who
# wanted to read it?
#
# Think before reading on.

# ============================================================
# THE ANSWER
# ============================================================

# Way too expensive.
#
# And wasteful.
#
# Almost all the content is
# identical.
#
# The only thing that changes
# is who's currently holding
# it.
#
# And when they'll return it.

# ============================================================
# THE IDEA
# ============================================================

# Share the heavy, unchanging
# part of something across
# many copies.
#
# And only keep separate
# whatever's actually
# different per copy.

# ============================================================
# BOARD SUMMARY
# ============================================================

# FLYWEIGHT (the general idea)
#
#     When you have a huge
#     number of
#     nearly-identical
#     objects, split each one
#     into two parts:
#
#     INTRINSIC data
#
#         the shared part,
#         identical across many
#         objects
#
#     EXTRINSIC data
#
#         the unique part,
#         different for every
#         object
#
#     Store the intrinsic part
#     ONCE and reuse it,
#     instead of copying it
#     into every single object.

# ============================================================
# THE PUBG PROBLEM
# ============================================================

# You're building the backend
# for PUBG.
#
# There are 100 players.
#
# Each firing hundreds of
# bullets.
#
# Take a single Bullet.
#
# What data does it need to
# keep track of?
#
# Think before reading on.

# ============================================================
# THE FIELDS
# ============================================================

# Color.
#
# Weight.
#
# Radius.
#
# Max damage.
#
# Direction.
#
# Speed.
#
# Max range.
#
# Current position.
#
# Target position.
#
# And an image showing what
# the bullet looks like.

# ============================================================
# THE NAIVE BULLET
# ============================================================


class NaiveBullet:

    def __init__(self, color, weight, radius, max_damage, direction,
                 speed, max_range, current_coordinate, target_coordinate,
                 image_of_bullet):
        self.color = color
        self.weight = weight
        self.radius = radius
        self.max_damage = max_damage
        self.direction = direction
        self.speed = speed
        self.max_range = max_range
        self.current_coordinate = current_coordinate
        self.target_coordinate = target_coordinate
        self.image_of_bullet = image_of_bullet   # actual image data — the big one


print("One Naive Bullet")

one_bullet = NaiveBullet(
    "black", 0.008, 0.03, 40, (1, 0),
    900, 400, (12, 45), (80, 90),
    bytes(1024)
)

print(len(one_bullet.image_of_bullet), "bytes of image, per bullet")

# ============================================================
# A NOTE ON SIZE
# ============================================================

# We won't get into the exact
# number of bytes this takes
# internally.
#
# That depends on
# implementation details that
# don't matter for today's
# point.
#
# What matters is simpler.
#
# Most of these fields are
# tiny.
#
# A color name.
#
# A few numbers.
#
# One field is not tiny at
# all.
#
#     image_of_bullet
#
# It holds actual image data.
#
# Easily a kilobyte or more,
# by itself, per bullet.
#
# So let's say, roughly, each
# Bullet object ends up
# costing about 1 KB of
# memory.
#
# Mostly because of that one
# field.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Now say a match has 100,000
# bullets in play at once.
#
# One for every shot fired,
# across every player.
#
# What's the total memory
# used, just for bullets?

# ============================================================
# THE MATHS
# ============================================================

# 100,000 bullets
#
#     x roughly 1 KB each
#
#     ≈ 100 MB
#
# Just to hold bullet data in
# memory.

print("\nThe Maths")
print(100_000 * 1024 / (1024 * 1024), "MB just for bullets")

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# 100 MB doesn't sound huge.
#
# Not compared to a modern
# phone or laptop's RAM.
#
# So why is this actually a
# problem?

# ============================================================
# THE REAL PROBLEM
# ============================================================

# The problem isn't the total
# size by itself.
#
# It's that almost all of it
# is repeated, wasted
# duplication.
#
# Most of these 100,000
# objects are storing the
# exact same color, radius,
# weight, and image.
#
# Over and over.
#
# When there are really only a
# handful of gun types in the
# whole game.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Let's go field by field.
#
# Take two different Bullet
# objects.
#
# Say, two AKM bullets fired
# by two different players.
#
# Which fields would actually
# hold different values?
#
# And which fields would hold
# the exact same value?

# ============================================================
# THE SPLIT
# ============================================================

# Different every time
#
#     depends on this specific
#     bullet, right now
#
#         current_coordinate
#
#         target_coordinate
#
#         direction
#
#         speed
#
# Exactly the same
#
#     depends only on "this is
#     an AKM bullet", not on
#     which player or which
#     shot
#
#         color
#
#         radius
#
#         weight
#
#         max_damage
#
#         max_range
#
#         image_of_bullet

# ============================================================
# NAMING THE TWO HALVES
# ============================================================

# This is exactly the split
# Flyweight is built on.
#
# The fields that are always
# different
#
#     -> EXTRINSIC
#
#     Keep one small copy of
#     these per bullet.
#
# The fields that repeat
# identically across many
# bullets
#
#     -> INTRINSIC
#
#     Store this heavy data
#     just ONCE per gun type.
#
#     And let every bullet of
#     that type point to that
#     one shared copy.
#
#     Instead of every bullet
#     carrying its own
#     duplicate.

# ============================================================
# BOARD SUMMARY
# ============================================================

# INTRINSIC (shared, heavy)
#
#     color, radius, weight,
#     max_damage, max_range,
#     image
#
#     -> store ONCE per gun
#        type
#
#     -> every bullet just
#        points to it
#
# EXTRINSIC (unique, light)
#
#     current_coordinate,
#     target_coordinate,
#     direction, speed
#
#     -> store fresh for every
#        single bullet

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# With this split, roughly how
# many copies of the heavy
# intrinsic data — image,
# color, and the rest — do we
# now need in memory?
#
# Say, for 5 different gun
# types in the game.

# ============================================================
# THE ANSWER
# ============================================================

# Just 5.
#
# One shared copy per gun
# type.
#
# No matter how many bullets
# get fired.
#
# Only the small extrinsic
# part — position, direction,
# speed — gets created fresh
# per bullet.

# ============================================================
# BOARD SUMMARY
# ============================================================

# BEFORE (naive)
#
#     100,000 full Bullet
#     objects
#
#     ≈ 100 MB total
#
# AFTER (flyweight)
#
#     100,000 tiny "position"
#     objects
#
#     + just 5 shared
#     "BulletType" objects
#
#     (one per gun, reused
#     everywhere)

# ============================================================
# CHECKPOINT
# ============================================================

# Clear on the split before we
# code it?
#
# Heavy and repeated
#
#     -> share it.
#
# Light and unique
#
#     -> keep it per object.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Based on what we just split.
#
# What goes into the shared,
# intrinsic class?
#
# And what stays in the
# per-bullet, extrinsic class?

# ============================================================
# THE ANSWER
# ============================================================

# Intrinsic (shared)
#
#     color, radius, weight,
#     max_damage, max_range,
#     image
#
# Extrinsic (unique per
# bullet)
#
#     current_coordinate,
#     target_coordinate,
#     direction, speed

# ============================================================
# THE INTRINSIC CLASS
# ============================================================

# Shared, heavy, identical
# across every bullet of the
# same gun.


class BulletType:

    def __init__(self, color, radius, weight, max_damage, max_range, image):
        self.color = color
        self.radius = radius
        self.weight = weight
        self.max_damage = max_damage
        self.max_range = max_range
        self.image = image


# ============================================================
# THE FACTORY
# ============================================================

# It makes sure we only ever
# create ONE BulletType per
# gun.
#
# No matter how many bullets
# get fired.


class BulletTypeFactory:
    _cache = {}

    @staticmethod
    def get_bullet_type(gun_name):
        if gun_name not in BulletTypeFactory._cache:
            # built only once per gun, the very first time it's needed
            BulletTypeFactory._cache[gun_name] = BulletTypeFactory._load_from_config(gun_name)
        return BulletTypeFactory._cache[gun_name]

    @staticmethod
    def _load_from_config(gun_name):
        # pretend this loads the real color/radius/weight/image for this gun
        return BulletType("black", 0.03, 0.008, 40, 400, bytes(1024))


# ============================================================
# THE EXTRINSIC CLASS
# ============================================================

# Small, unique per bullet,
# changes constantly during
# flight.


class Bullet:

    def __init__(self, gun_name, current_coordinate, direction, speed):
        self.type = BulletTypeFactory.get_bullet_type(gun_name)   # reused, not rebuilt
        self.current_coordinate = current_coordinate
        self.direction = direction
        self.speed = speed


# ============================================================
# FIRING A LOT OF BULLETS
# ============================================================

print("\nFiring 1,000 AKM Bullets")

bullets = [
    Bullet("AKM", (i, i), (1, 0), 900)
    for i in range(1000)
]

print(len(bullets), "bullets created")
print(len(BulletTypeFactory._cache), "BulletType object in memory")

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# If 10,000 players all fire
# an AKM bullet, how many
# BulletType objects actually
# get created in memory?

# ============================================================
# THE ANSWER
# ============================================================

# Just one.
#
# The factory checks its cache
# and hands back the same
# shared BulletType every
# time.
#
# Only the small Bullet object
# — position, direction, speed
# — is created fresh each
# time.

# ============================================================
# FIVE GUN TYPES
# ============================================================

print("\nFive Different Guns")

for gun in ["AKM", "M416", "AWM", "UMP45", "Kar98k"]:
    Bullet(gun, (0, 0), (1, 0), 900)

print(len(BulletTypeFactory._cache), "BulletType objects in memory")

# Observation:
#
# 1,005 bullets fired.
#
# 5 heavy objects in memory.

# ============================================================
# QUIZ
# ============================================================

# Which is the correct
# intrinsic/extrinsic split
# for a text editor rendering
# millions of characters on
# screen —
#
# where every character has a
# font, size, color, and a
# row/column position on the
# page?
#
# A) Intrinsic: row/column
#    position.
#    Extrinsic: font, size,
#    color
#
# B) Intrinsic: font, size,
#    color.
#    Extrinsic: row/column
#    position
#
# C) Everything is intrinsic
#
# D) Everything is extrinsic
#
# Answer:
#
# B)
#
# font/size/color repeat
# across thousands of
# characters and should be
# shared.
#
# row/column is unique to each
# character.

# ============================================================
# CHECKPOINT
# ============================================================

# Solid on the split?
#
# One class for what repeats.
#
# One class for what doesn't.
#
# A factory in between,
# guaranteeing the sharing.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# One library book read by
# hundreds of students is the
# everyday version.
#
# 100,000 bullets at roughly
# 1 KB each is about 100 MB.
#
# The complaint is not the
# total size.
#
# It's that nearly all of it
# is the same data, repeated.
#
# Intrinsic fields depend only
# on the gun type, and get
# stored once.
#
# Extrinsic fields depend on
# this specific bullet right
# now, and stay per object.
#
# A factory with a cache is
# what guarantees only one
# shared copy per type ever
# gets built.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# We built the factory
# ourselves here.
#
# But this pattern is already
# running underneath you.
#
# Inside Python itself.
#
# And inside code you have
# almost certainly written
# without naming it.
#
# Next:
#
# 06_flyweight_in_a_real_backend.py
