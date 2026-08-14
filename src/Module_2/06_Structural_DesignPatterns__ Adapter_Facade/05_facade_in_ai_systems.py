"""
============================================================
DESIGN PATTERNS : STRUCTURAL FAMILY
FILE : 05_facade_in_ai_systems.py
============================================================

Topics Covered
--------------
1. Where File 04 Left Us
2. One Message In, One Answer Out
3. How Many Steps Really Happen
4. How Many Of Them You See
5. The Pieces Behind The Curtain
6. The Agent Facade
7. The Complete Runtime Flow
8. How Real Frameworks Are Built
9. Key Takeaways
"""

# ============================================================
# WHERE FILE 04 LEFT US
# ============================================================

# One entry point.
#
# Several subsystems behind
# it.
#
# The caller knowing none of
# them.
#
# We built that for an order
# flow.
#
# Nothing about it was order
# specific.

# ============================================================
# THE SCENE
# ============================================================

# Think about what happens
# when you send ONE message
# to an AI coding assistant.
#
# It edits three files.
#
# It runs your tests.
#
# It reports back.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# How many small steps do you
# think actually happen behind
# that one message?
#
# Pulling context.
#
# Deciding which tool to call.
#
# Calling it.
#
# Reading the result.
#
# Deciding the next step.
#
# Writing the final reply.
#
# Count them.

# ============================================================
# THE ANSWER
# ============================================================

# Many.
#
# Probably a loop of several
# LLM calls.
#
# Tool calls.
#
# And state updates.
#
# Not one step.
#
# A loop of them.

# ============================================================
# THINK BEFORE READING ON
# ============================================================

# Second question.
#
# As the user, do you see any
# of that?
#
# Or do you just see:
#
#     one message in,
#
#     one clean answer out?

# ============================================================
# THE ANSWER
# ============================================================

# Just the clean message in.
#
# Answer out.
#
# All the orchestration is
# hidden.
#
# You have been on the client
# side of a Facade this whole
# time.

# ============================================================
# THE PIECES BEHIND THE CURTAIN
# ============================================================

# Retrieval.
#
# Planning.
#
# Tool execution.
#
# Memory.
#
# Formatting.
#
# All separate, complex
# pieces.


class Retriever:

    def get_relevant_context(self, user_request):
        print(f"  [retriever] context for: {user_request}")
        return f"context::{user_request}"


class Plan:

    def __init__(self, steps):
        self.steps = steps


class Planner:

    def decide_steps(self, user_request, ctx):
        print("  [planner] deciding steps")
        return Plan(["read_file", "edit_file", "run_tests"])


class ToolExecutor:

    def execute(self, step):
        print(f"  [tools] executing {step}")
        return f"{step}::ok"


class Memory:

    def __init__(self):
        self.entries = []

    def record(self, step, result):
        print(f"  [memory] recorded {step}")
        self.entries.append((step, result))


class ResponseFormatter:

    def format(self, memory):
        print("  [formatter] writing the reply")
        return f"finished {len(memory.entries)} steps"


# ============================================================
# THE FACADE
# ============================================================


class AgentFacade:

    def __init__(self, retriever, planner, tool_executor,
                 memory, response_formatter):
        self.retriever = retriever
        self.planner = planner
        self.tool_executor = tool_executor
        self.memory = memory
        self.response_formatter = response_formatter

    def run(self, user_request):
        ctx = self.retriever.get_relevant_context(user_request)
        plan = self.planner.decide_steps(user_request, ctx)

        for step in plan.steps:
            result = self.tool_executor.execute(step)
            self.memory.record(step, result)

        return self.response_formatter.format(self.memory)


# ============================================================
# RUNNING IT
# ============================================================

print("Agent Facade")

agent = AgentFacade(
    Retriever(),
    Planner(),
    ToolExecutor(),
    Memory(),
    ResponseFormatter()
)

print(agent.run("fix the failing test"))

# Observation:
#
# Count the printed lines.
#
# Then count the lines the
# caller wrote.
#
# One.

# ============================================================
# HOW REAL FRAMEWORKS ARE BUILT
# ============================================================

# This is close to how most
# real AI agent frameworks
# work under the hood.
#
# Retrieval, planning, tool
# execution, memory, and
# formatting are all separate,
# complex pieces.
#
# The framework shows you
# exactly one simple entry
# point.
#
# Often called:
#
#     run()
#
# or:
#
#     invoke()
#
# That is the Facade.

# ============================================================
# YOU HAVE ALREADY USED ONE
# ============================================================

# You have likely already used
# a Facade like this.
#
# Every time you have used an
# AI coding tool.
#
# Without seeing any of it.

# ============================================================
# CHECKPOINT
# ============================================================

# Two domains now.
#
# An order flow.
#
# An AI agent.
#
# Same structure underneath.
#
# One entry point.
#
# Many subsystems, hidden.

# ============================================================
# KEY TAKEAWAYS
# ============================================================

# One message to an AI coding
# assistant is not one step.
#
# It is a loop of LLM calls,
# tool calls, and state
# updates.
#
# The user sees none of it.
#
# Retrieval, planning, tool
# execution, memory and
# formatting are five separate
# pieces.
#
# The framework exposes one
# entry point over all five.
#
# Usually named run() or
# invoke().
#
# That single method is the
# Facade.

# ============================================================
# BRIDGE TO THE NEXT FILE
# ============================================================

# Both patterns are now on the
# table.
#
# Adapter.
#
# Facade.
#
# Both wrap something.
#
# Both give the client a
# cleaner surface to talk to.
#
# So how would you tell them
# apart in a design review?
#
# And what happens when a
# wrapper only LOOKS like the
# right pattern?
#
# Next:
#
# 06_adapter_vs_facade_and_ai_corner.py
