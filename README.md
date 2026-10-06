# Primitive-First Design (PFD)

> **A philosophy for building minimal, high-signal, zero-smell software architectures.**  
> *Case Study:* [AgentCore on GitHub](https://github.com/your-username/AgentCore) | *Technical Skill & Audit Rules:* [`skill/primitive-first-design.md`](skill/primitive-first-design.md)

---

## The Core Idea

**NO all minimal code is correct code, but correct code is usually will be minimal.**

Most design patterns, wrappers, abstractions, bloats and boilerplate exist purely to patch or support poorly conceived foundational primitives. When you get the foundational primitives right:
* Your code naturally stays small and clean.
* Code smells disappear before they even start.
* The system is easy to read, scale, and maintain without extra bloat.

---

## The Mental Model: Four Pure Boundaries

PFD organizes every element of a system into four clear concepts:

```text
┌─────────────────────────────────────────────────────────────┐
│ LAYER  (Decorated Outside)                                  │
│ Wraps the primitive to observe, intercept, persist, or adapt│
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ CORE PRIMITIVE  (The Contract)                      │   │
│   │ The irreducible domain boundary & universal truth   │   │
│   │                                                     │   │
│   │   ┌─────────────────────────────────────────────┐   │   │
│   │   │ POLICY  (Injected Inside)                   │   │   │
│   │   │ Completes the primitive: strategy, limits   │   │   │
│   │   └─────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

                  [ DTO: Passive State Binder ]
            Pure data carriers holding zero business logic
```

> **The Core Idea:**  
> A **Policy** is just a building block on the inside.  
> A **Layer** is just a building block on the outside.  
> **DTOs and helper functions** are the glue that holds them together.

---

## Core Principles at a Glance

* **The Interface is the Truth:** Talk to interfaces (or traits in Rust), never directly to concrete classes. No secret backdoors.
* **Don't Guess the Future; Just Don't Block It:** Future-proofing does not mean writing complex guessing code for tomorrow. It means **removing silly limits today**. If your core piece is clean and unconstrained, future features fit right in without breaking anything.
* **Policy vs. Layer (The Simple Test):**
  * Can the core piece work without it? **NO** -> It is a **Policy** (plugged inside, like an internal rule or algorithm).
  * Can the core piece work without it? **YES** -> It is a **Layer** (wrapped outside, like saving to a database or logging).
* **DTOs are Just Data:** A DTO only holds data. If your data object starts running logic or assembling pieces, that work belongs somewhere else.
* **Look for Symmetry:** If two pieces do similar work, make them look and act the same way. This removes messy middleman classes and glue code.

---

## Practical Rules of Thumb

* **$\le$ 4–5 Methods per Interface:** A warning signal that a contract is doing too much or conflating helpers with boundaries.
* **Colocated Extensions ("Useful != Fundamental"):** Convenience helpers and query methods belong in extensions beside the primitive, never in the core contract.
* **~150 Lines per Cohesive Scope:** A primitive implementation scope should hover around ~150 lines max. Exceeding this warns of hidden god-objects or un-extracted policies.
* **Rough Scale Benchmarks:** A bare-bones core engine usually sits around **1k–1.5k LoC**, and an entire end-to-end system hovers around **~5k LoC** without bloat.

---

## Learn More

* **[AgentCore Case Study](https://github.com/your-username/AgentCore):** See how PFD was discovered and applied in an experimental agent framework.
* **[PFD Agent Skill (`skill/primitive-first-design.md`)](skill/primitive-first-design.md):** The complete technical specification, audit checklist, and execution prompts for automated architecture reviews.