"""
PART 10 - ITERTOOLS AND PRACTICAL LABS

Topics Covered

1. Why itertools exists
2. chain()
3. islice()
4. groupby()
5. Practical @timer decorator
6. Practical @retry decorator
7. Lazy file reader
"""

# ============================================================
# MOTIVATION
# ============================================================

# We have learned iterators and generators.
#
# Python's standard library builds on these ideas and provides
# powerful iterator utilities in the itertools module.
#
# They help us write cleaner, faster and more memory-efficient
# code.

# ============================================================
# THEORY
# ============================================================

# itertools contains ready-made iterator building blocks.
#
# These tools create values lazily instead of building large
# intermediate collections.

from itertools import chain, islice, groupby
from functools import wraps
import time

# ============================================================
# DEMO 1 - chain()
# ============================================================

print("chain() Demo")

frontend = ["HTML", "CSS"]
backend = ["Python", "SQL"]

for topic in chain(frontend, backend):
    print(topic)

# Runtime Observation:
# chain() lets us iterate over multiple iterables as though
# they were one continuous sequence.

# ============================================================
# THINK BEFORE RUNNING
# ============================================================

# Predict:
#
# Does islice() create a new list?
#
# Or does it lazily expose only the requested elements?

# ============================================================
# DEMO 2 - islice()
# ============================================================

numbers = range(100)

print("\nislice() Demo")

for value in islice(numbers, 5):
    print(value)

# Runtime Observation:
# Only the requested elements are produced.

# ============================================================
# DEMO 3 - groupby()
# ============================================================

animals = ["ant","ant","bat","bat","cat","cat"]

print("\ngroupby() Demo")

for key, group in groupby(animals):
    print(key, list(group))

# ============================================================
# PRACTICAL LAB 1 - TIMER DECORATOR
# ============================================================

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end-start:.6f} seconds")
        return result
    return wrapper

@timer
def compute():
    total = 0
    for i in range(100000):
        total += i
    return total

print("\nTimer Decorator Demo")
print(compute())

# ============================================================
# PRACTICAL LAB 2 - RETRY DECORATOR
# ============================================================

def retry(attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, attempts + 1):
                try:
                    print(f"Attempt {attempt}")
                    return func(*args, **kwargs)
                except Exception as ex:
                    last_error = ex
                    print("Failed:", ex)
            raise last_error
        return wrapper
    return decorator

counter = {"tries": 0}

@retry(3)
def unstable():
    counter["tries"] += 1
    if counter["tries"] < 3:
        raise ValueError("Temporary failure")
    return "Success"

print("\nRetry Decorator Demo")
print(unstable())

# ============================================================
# PRACTICAL LAB 3 - LAZY FILE READER
# ============================================================

# A generator can read large files one line at a time instead
# of loading the entire file into memory.

def lazy_reader(lines):
    for line in lines:
        yield line.strip()

print("\nLazy Reader Demo")

sample = ["First\n", "Second\n", "Third\n"]

for line in lazy_reader(sample):
    print(line)

# ============================================================
# COMMON MISCONCEPTIONS
# ============================================================

# itertools utilities generally produce iterators.
#
# They do not usually build complete collections.

# ============================================================
# SMALL EXPERIMENTS
# ============================================================

print("\nExperiments")
iterator = chain([1], [2])
print(type(iterator))
print(hasattr(iterator, "__next__"))

# ============================================================
# INTERVIEW OBSERVATION
# ============================================================

# Frequently Asked:
#
# Why use generators and itertools together?
#
# Because both support lazy evaluation and help reduce
# unnecessary memory usage.

# ============================================================
# BOARD SUMMARY
# ============================================================

# itertools
#     ├── chain()
#     ├── islice()
#     └── groupby()
#
# Practical decorators:
#     timer
#     retry
#
# Lazy processing:
#     yield

# ============================================================
# COURSE WRAP-UP
# ============================================================

# We began by learning that functions are first-class objects.
#
# Then we explored:
#
# - Closures
# - Decorators
# - Singleton decorators
# - Iterators
# - Generators
# - itertools
#
# Together these form an important part of writing
# idiomatic, Pythonic code.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# ✓ itertools provides reusable iterator utilities.
# ✓ chain() combines iterables lazily.
# ✓ islice() lazily selects a range.
# ✓ groupby() groups consecutive values.
# ✓ Decorators solve practical problems like timing and retries.
# ✓ Generators and itertools work well together.
