"""
============================================================
LLD-5 : MAGIC METHODS & PYTHON DATA MODEL
FILE : 07_deck_container_protocol.py
============================================================

Topics Covered
--------------
1. Container Protocol Motivation
2. Building Card
3. Building Deck
4. __len__
5. __getitem__
6. __setitem__
7. __contains__
8. Card Equality
9. Container Fallback Behaviour
10. __iter__
11. Why Protocols Matter
11. Key Takeaways
"""

import itertools

# ============================================================
# MOTIVATION
# ============================================================

# So far we have explored:
#
# __len__
# __eq__
# __hash__
# __enter__
# __exit__
# __call__
#
# Now we combine multiple protocols
# inside a single object.
#
# Goal:
#
# Build a Deck that behaves like
# a native Python container.

# ============================================================
# WHAT SHOULD A CONTAINER SUPPORT?
# ============================================================

# Consider:
#
# len(deck)
# deck[0]
# card in deck
# for card in deck
#
# Native collections support these.
#
# Our Deck should support them too.

# ============================================================
# CARD
# ============================================================


class Card:

    def __init__(self, rank, suit):

        self.rank = rank
        self.suit = suit

    def __repr__(self):

        return (
            f"Card({self.rank!r}, "
            f"{self.suit!r})"
        )


# ============================================================
# DECK V1
# ============================================================

RANKS = [
    "2", "3", "4", "5", "6",
    "7", "8", "9", "10",
    "J", "Q", "K", "A"
]

SUITS = [
    "Spades",
    "Hearts",
    "Diamonds",
    "Clubs"
]


class Deck:

    def __init__(self):

        self._cards = [
            Card(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]


deck = Deck()

# ============================================================
# FIRST LIMITATION
# ============================================================

print("Deck Created")

print(type(deck))

# Observation:
#
# Deck exists.
#
# But it does not yet behave
# like a container.

# ============================================================
# __len__
# ============================================================

print("\nTesting len()")

try:

    print(len(deck))

except TypeError as error:

    print(error)

# Observation:
#
# Python does not know how to
# calculate the length.

# ============================================================
# FIXING __len__
# ============================================================


class DeckV2:

    def __init__(self):

        self._cards = [
            Card(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]

    def __len__(self):

        return len(self._cards)


deck = DeckV2()

print("\nAfter __len__")

print(len(deck))

# Observation:
#
# len(deck)
#
# now works.

# ============================================================
# SECOND LIMITATION
# ============================================================

print("\nTesting Indexing")

try:

    print(deck[0])

except TypeError as error:

    print(error)

# Observation:
#
# Deck is not subscriptable.

# ============================================================
# __getitem__
# ============================================================


class DeckV3:

    def __init__(self):

        self._cards = [
            Card(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]

    def __len__(self):

        return len(self._cards)

    def __getitem__(
        self,
        index
    ):

        return self._cards[index]


deck = DeckV3()

print("\nIndexing Works")

print(deck[0])

# Observation:
#
# __getitem__
#
# enables:
#
# deck[index]

# ============================================================
# SLICING
# ============================================================

print("\nSlicing")

print(deck[0:3])

# Observation:
#
# Slicing works automatically.
#
# We delegated to the underlying list.

# ============================================================
# THIRD LIMITATION
# ============================================================

# Reading works.
#
# What about writing?

print("\nTesting Assignment")

try:

    deck[0] = Card("A", "Spades")

except TypeError as error:

    print(error)

# Observation:
#
# Assignment fails.

# ============================================================
# __setitem__
# ============================================================


class DeckV4:

    def __init__(self):

        self._cards = [
            Card(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]

    def __len__(self):

        return len(self._cards)

    def __getitem__(
        self,
        index
    ):

        return self._cards[index]

    def __setitem__(
        self,
        index,
        card
    ):

        self._cards[index] = card


deck = DeckV4()

deck[0] = Card("A", "Spades")

print("\nAfter __setitem__")

print(deck[0])

# Observation:
#
# Writing now works.

# ============================================================
# MEMBERSHIP TESTING
# ============================================================

print("\nMembership Test")

print(
    Card("A", "Spades") in deck
)

# Observation:
#
# False.
#
# Interesting.
#
# A fresh deck should contain
# Ace of Spades.

# ============================================================
# WHY FALSE?
# ============================================================

# The deck contains:
#
# Card("A", "Spades")
#
# But membership still fails.
#
# The problem is not the Deck.
#
# The problem is Card equality.

# ============================================================
# CARD EQUALITY
# ============================================================


class BetterCard:

    def __init__(
        self,
        rank,
        suit
    ):

        self.rank = rank
        self.suit = suit

    def __repr__(self):

        return (
            f"Card({self.rank!r}, "
            f"{self.suit!r})"
        )

    def __eq__(
        self,
        other
    ):

        return (
            self.rank == other.rank
            and
            self.suit == other.suit
        )


class DeckV5:

    def __init__(self):

        self._cards = [
            BetterCard(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]

    def __len__(self):

        return len(self._cards)

    def __getitem__(
        self,
        index
    ):

        return self._cards[index]

    def __setitem__(
        self,
        index,
        card
    ):

        self._cards[index] = card


deck = DeckV5()

print("\nMembership Test Again")

print(
    BetterCard("A", "Spades")
    in deck
)

# Observation:
#
# Now returns True.

# ============================================================
# IMPORTANT DISCUSSION
# ============================================================

# Because __getitem__ exists,
# Python can fall back to
# scanning the collection.
#
# Index 0
# Index 1
# Index 2
# ...
#
# Until a match is found.
#
# Without Card.__eq__,
# identity comparison was used.

# ============================================================
# __contains__
# ============================================================

# The fallback works.
#
# But we can still define
# __contains__ explicitly.


class DeckV6:

    def __init__(self):

        self._cards = [
            BetterCard(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]

    def __len__(self):

        return len(self._cards)

    def __getitem__(
        self,
        index
    ):

        return self._cards[index]

    def __setitem__(
        self,
        index,
        card
    ):

        self._cards[index] = card

    def __contains__(
        self,
        card
    ):

        return card in self._cards


deck = DeckV6()

print("\nExplicit __contains__")

print(
    BetterCard("A", "Spades")
    in deck
)

# Observation:
#
# Membership logic is now
# fully under our control.

# ============================================================
# ITERATION
# ============================================================

print("\nIteration")

for card in deck:

    print(card)

    break

# Observation:
#
# Iteration already works.
#
# Python uses __getitem__
# fallback behaviour.

# ============================================================
# WHY DEFINE __iter__?
# ============================================================

# Explicit __iter__
#
# is clearer.
#
# It also works for containers
# that are not index based.

# ============================================================
# __iter__
# ============================================================


class DeckV7:

    def __init__(self):

        self._cards = [
            BetterCard(rank, suit)
            for rank, suit in itertools.product(
                RANKS,
                SUITS
            )
        ]

    def __len__(self):

        return len(self._cards)

    def __getitem__(
        self,
        index
    ):

        return self._cards[index]

    def __setitem__(
        self,
        index,
        card
    ):

        self._cards[index] = card

    def __contains__(
        self,
        card
    ):

        return card in self._cards

    def __iter__(self):

        return iter(self._cards)


deck = DeckV7()

print("\nExplicit Iteration")

for card in deck:

    print(card)

    break

# Observation:
#
# Iteration now has a dedicated
# implementation.

# ============================================================
# CONTAINER PROTOCOL RECAP
# ============================================================

# __len__
#
# len(deck)
#
#
# __getitem__
#
# deck[index]
#
#
# __setitem__
#
# deck[index] = value
#
#
# __contains__
#
# value in deck
#
#
# __iter__
#
# for value in deck

# ============================================================
# BIG IDEA
# ============================================================

# Python never learned
# what a Deck is.
#
# Python never learned
# what a Card is.
#
# Yet:
#
# len()
# []
# in
# for
#
# all work.
#
# Why?
#
# Protocols.

# ============================================================
# INTERVIEW QUESTION
# ============================================================

# Which dunder enables:
#
# deck[0]
#
# Answer:
#
# __getitem__
#
#
# Which dunder enables:
#
# len(deck)
#
# Answer:
#
# __len__

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# Container behaviour comes from
# special methods.
#
# __len__
# __getitem__
# __setitem__
# __contains__
# __iter__
#
# Together they make custom
# objects feel like native
# Python collections.
#
# This is protocol-based design.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# The Deck now behaves like
# a real Python container.
#
# Next we complete the lab by
# adding shuffling behaviour,
# validating protocol support,
# and exploring why
# random.shuffle()
# works automatically.
#
# Next:
#
# 08_deck_lab_completion.py
