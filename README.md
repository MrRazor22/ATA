# Axiomatic Triad Architecture (ATA)
## A Foundational Theory of Bedrock Primitives and Composition

---

## The Core Soul of ATA

> **"Correctly identifying the fundamental primitive of a system naturally minimizes its architecture, because unnecessary abstractions become redundant when the primitive itself correctly represents the underlying problem; once the primitive is correct, composition, injectable policies, and generic layers provide extensibility without requiring the core primitive to continuously grow new abstractions."**

Minimal code and zero architectural smells are not dogmatic quotas or tricks; they are the natural, inevitable side-effects of identifying the true primitive. 

Software bloat rarely comes from genuine domain complexity. It comes from **convenience-driven drift**—the path of least resistance where developers append helper overloads, boolean flags, pass-through wrappers, and ad-hoc scripts rather than re-examining the bedrock primitive. 

ATA does not invent an alien paradigm. It is grounded in proven, classic object-oriented and functional principles, providing a razor-sharp framework to enforce them. **Any classic code smell—whether tight coupling, hidden side-effects, leaky abstractions, mutable shared state, or God objects—is an immediate signal of an ATA violation.**

---

## 1. The Unified Foundation: Everything is a Primitive

At its bedrock, ATA reveals that **the Primitive is the sole behavioral atom of a system**. What we call the Triad is simply the three natural roles a primitive plays in composition:

```text
┌─────────────────────────────────────────────────────────────┐
│                 THE AXIOMATIC TRIAD (BOUNDARY)              │
│                                                             │
│       ┌──────────────────────────────────────────────┐      │
│       │      Derived Layers: Composable Decorators   │      │
│       │      (Cross-cutting concerns wrapping P)     │      │
│       └──────────────────────┬───────────────────────┘      │
│                              │ wraps (λ: P -> P)            │
│       ┌──────────────────────▼───────────────────────┐      │
│       │      The Core Axiom / Primitive (P)          │      │
│       │      (Irreducible Bedrock: WHAT it does)     │      │
│       └──────────────────────▲───────────────────────┘      │
│                              │ injects (π)                  │
│       ┌──────────────────────┴───────────────────────┐      │
│       │      Derived Policies: Swappable Strategies  │      │
│       │      (HOW internal steps execute)            │      │
│       └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

1. **The Root Primitive ($P$):** The irreducible contract defining *what* the capability is. It exhibits behavior, maintains minimal method surface area, and contains zero hardcoded internal strategies.
   - **The Subtraction Test:** A primitive is truly irreducible if removing it causes the fundamental domain capability to collapse entirely. If the capability still functions by swapping an algorithm or default, that component is a policy or layer, not a root primitive.
2. **The Injected Policy ($\pi$):** When a primitive is injected into another primitive at a different level to drive an internal execution step, it acts as a **Policy** (e.g., an encoding primitive injected into an engine primitive).
   - **Policy Orthogonality:** Operational variation (*how* a step executes) must be isolated as swappable policies injected at initialization, leaving the primitive contract invariant. Policies are dependencies of the primitive, never subclasses or outer wrappers.
3. **The Composable Layer ($\lambda: P \to P$):** When a primitive wraps another primitive sharing the **exact same interface contract**, it acts as an endomorphic **Layer**—decorating cross-cutting operational concerns (retries, rate limiting, persistence, latency profiling, telemetry) externally without interface drift.
   - **Endomorphic Layer Sufficiency:** Layers form an algebraic monoid $(\text{End}(P), \circ, \text{id})$. Any capability added to a boundary must be a Layer, never a modification to the primitive or its internal execution loop. Every layer carries the `*Layer` suffix to clearly communicate its decorating role.

Along with primitives, a system consists only of:
- **State:** Pure, immutable data structures, schemas, and static domain assets passed across disjoint channels. **Never mutable shared or global state**, which immediately violates isolation and introduces hidden coupling smells.
- **Stateless Transforms:** Pure mathematical functions ($f(X) \to Y$) with zero side-effects.

---

## 2. Composition, Contracts & The Interface Mandate

### 2.1 Interface-First for Any Object That Exhibits Behavior
> **"Every class or object that performs computation, execution, transformation, or I/O must be defined by an explicit interface. Never expose or depend directly upon concrete classes."**

1. **Unchecked Bloat Creep:** Without an interface contract, classes casually accumulate convenience overloads, internal getters, and procedural mutations, ballooning into God objects.
2. **Hidden Internal Coupling:** Callers bind to implementation quirks and private data representations, making it impossible to swap substrates or evolve algorithms independently.
3. **Breakdown of Layering:** Endomorphic layering ($\lambda: P \to P$) mathematically requires a stable contract $P$. Without an interface, decoration degenerates into fragile subclassing, monkey-patching, or procedural glue.

### 2.2 The Anatomy of an Irreducible Contract
An interface in ATA is strictly **irreducible**:
1. **Minimal Surface Area:** Single-responsibility capability with focused methods (a healthy gauge is ~2–4 canonical methods). When an interface balloons to dozens of methods, it is an unmistakable signal of an unfocused God contract.
2. **Core Contract Purity vs. Extension Helpers:** 
   - The root contract must contain strictly the irreducible semantic operations. **Zero convenience bloat** or caller sugar on the core interface.
   - If convenience methods, fluent helpers, or secondary syntactic aliases are desired, they belong strictly in **stateless external extension functions** that wrap the canonical contract. The core interface remains pristine and invariant.
3. **Pure Semantic Intent:** Defines *what* is achieved in pure domain terms, completely abstracted from underlying hardware, transport, or storage mechanics.

### 2.3 The Rule of Two & The Multiple Primitives Fallacy
- **The Multiple Primitives Fallacy:** Every operational boundary encapsulates **exactly one primary root primitive** ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$). When an engineer believes a boundary requires multiple primitives, it is almost always a misconception: secondary candidates are either injected policies ($\pi$) or lower-level primitives injected into that single root primitive. Truly independent primitives demand separate boundaries.
- **The Rule of Two:** Never mirror a single concrete class 1:1 with an interface or intermediate wrapper unless there are at least two distinct concrete implementations or consumers (or an endomorphic layer target). Zero speculative abstractions.
- **Strict One-Way Dependency Flow:** High-level boundaries compose lower-level primitives. Primitives never import or depend upon their composable layers or callers. Circular dependencies between boundaries or layers are an immediate architectural violation.

---

## 3. Boundary Topology & Physical Hygiene

ATA enforces strict geometric alignment between **logical namespaces** and **physical directory structures**. 

### 3.1 The Canonical Topology: Boundary-First Cohesive Triad
Horizontal tier-first dumping (`core/`, `policies/`, `layers/` at the repository root) is an anti-pattern that destroys cohesion. Instead, each operational boundary commands its own cohesive Triad, centered around **exactly one irreducible primitive**:

```text
RepositoryRoot/
├── [DomainBoundaryA]/          # Boundary A: Encapsulates Primitive A (Cluttered Scale)
│   ├── primitive.ext           # THE ONE PRIMITIVE (Contract & Base Implementation)
│   ├── schema.ext              # Pure immutable domain value objects for Primitive A
│   ├── policies/               # Injected strategies (partitioned when >= 4-5 items)
│   │   ├── strategy_1.ext
│   │   └── strategy_2.ext
│   ├── layers/                 # Composable decorators (λ_A: A -> A)
│   │   ├── profiling_layer.ext
│   │   └── guardrail_layer.ext
│   └── data/                   # Boundary-owned assets (fixtures, baselines, weights)
├── [DomainBoundaryB]/          # Boundary B: Encapsulates Primitive B (Lean Scale: Flat)
│   ├── primitive.ext           # THE ONE PRIMITIVE (Contract & Base Implementation)
│   ├── objective.ext           # Injected policy (flat, no 1-file folder ceremony)
│   └── checkpoint_layer.ext    # Composable decorator (self-documenting via *Layer suffix)
├── cli.ext                     # Root external runner / orchestration entrypoint
└── tests/                      # Contract verification & regression tests
```

### 3.2 The Clutter-Threshold Gauge (When to Subfolder vs. Stay Flat)
A common failure mode in modular architectures is **Folder Ceremony**—creating nested directories that wrap only a single file (e.g., `training/policies/loss.py` or `evaluation/layers/profiling.py`):
- **Lean Boundaries ($\le 3–4$ sibling files):** Keep the boundary flat. The primitive, policy, and layer live side-by-side at the boundary root. The `*Layer` suffix already makes its decorating role self-documenting; a 1-file folder is pure ceremony.
- **Cluttered Boundaries ($\ge 4–5$ policies or layers):** Subordinate policies and layers into dedicated `policies/` and `layers/` subdirectories to prevent visual sprawl.
- **Zero Single-File Folders:** A directory or namespace must justify having at least 2–3 sibling files, or it should remain flat.

### 3.3 Functional Asset Ownership & The Pristine Root
- **The Ownership Test:** *"Which primitive or operational boundary produces or exclusively consumes this asset?"*
- **Horizontal Format Scattering (Smell):** Creating top-level dumping grounds based on superficial file formats (`data/`, `results/`, `output/`, `fixtures/`) breaks encapsulation. Assets consumed by execution testing belong with that execution boundary; assets consumed by optimization belong with the optimization boundary.
- **The Pristine Root Principle:** Any loose, untyped directory (`data/`, `checkpoints/`, `results/`) or dangling file at the repository root is an immediate design smell. A pristine root strictly contains:
  1. Primary operational domain packages
  2. Root orchestration entrypoint (`cli.ext`)
  3. Contract verification test suites (`tests/`)
  4. Standard packaging configurations (`pyproject.toml`, `.gitignore`, `README.md`, `AGENT.md`)
- **Zero Residual Debris:** Build caches, temporary logs, scratch runs, and disposable experiment debris must never linger in source trees.

---

## 4. External Consumers & Zero Non-ATA Code

### 4.1 External Consumers / Runners (Not a Fourth Tier)
Standalone CLI scripts, host applications, benchmark harnesses, worker loops, and entrypoints are **external consumers orchestrating boundaries**, NOT an internal fourth tier of the Triad:
- The Triad strictly contains three elements: the Primitive ($P$), Injected Policies ($\pi$), and Composable Layers ($\lambda$).
- Runners simply instantiate Primitives, inject Policies, compose Layers, and drive workflows.

### 4.2 The "No Unprincipled Scripts" Directive
Every capability in a repository (inference, training, data processing, evaluation) decomposes cleanly into the Triad. Operational tasks and evaluation workflows are not excuses for ad-hoc procedural hacks, unprincipled copy-paste loops, or loose script sinkholes:
- If an evaluation workflow requires metric calculation, that metric is a policy or layer owned by the evaluation boundary, driven cleanly by the runner.
- Domain logic never belongs inside loose scripts; it must be encapsulated within the Triad so it remains testable, composable, and reusable.

---

## 5. Diagnostic Smell Detector

Any classic code smell is a direct violation of ATA. When designing, reviewing, or refactoring a codebase, use this diagnostic matrix:

| Diagnostic Question | If YES (Clean ATA Design) | If NO (Architectural Smell Detected) |
|---|---|---|
| **What is the primitive?** | Irreducible contract defining pure domain capability ($P$) | **God Class / Interface Bloat:** Sprawling managers or multiple overlapping types |
| **How does it execute?** | Internal steps injected via swappable policies ($\pi$) | **Hardcoded Branching:** Boolean toggles, hardcoded algorithms, or inheritance subclasses |
| **How do we add features?** | Endomorphic layer ($\lambda: P \to P$) decorating the contract | **Core Mutation:** Mutating the execution loop or bloating the base contract |
| **Are behaviors behind interfaces?** | 100% of behavioral components defined by explicit interfaces | **Tight Coupling:** Callers directly dependent on concrete implementations |
| **Are contracts clean & pure?** | Minimal surface area (~2–4 methods); zero convenience bloat | **Contract Clutter:** Interfaces bloated with convenience aliases and redundant overloads |
| **Do interfaces mirror 1:1?** | Interfaces decouple polymorphism or layers ($\ge 2$ impls/consumers) | **Abstraction Theater:** 1:1 mechanical passthrough interfaces adding indirection without value |
| **How is state managed?** | Pure, immutable data structures passed across disjoint channels | **Mutable Shared State:** Shared mutable objects, global state, or hidden side-effects |
| **How many primitives per boundary?** | Exactly 1 root primitive per boundary; substrates injected cleanly | **Multiple Primitives Fallacy:** Competing primitives in one folder causing role ambiguity |
| **How is the repository partitioned?** | Boundary-first (`boundary/policies/`, `boundary/layers/`) | **Tier-First Dumping:** Giant horizontal dumping grounds (`core/`, `policies/` at root) |
| **Are there single-file folders?** | Lean boundaries stay flat; folders contain $\ge 2–3$ files | **Folder Ceremony:** Gratuitous nesting and namespaces wrapping a single file |
| **Where do assets & datasets live?** | Co-located inside the boundary that consumes/produces them | **Horizontal Format Scattering:** Loose `data/`, `results/`, or fixtures scattered at root |
| **Where do operational workflows live?** | Clean runners orchestrating domain primitives | **Script Sinkholes:** Sprawling procedural scripts with copy-pasted loops and ad-hoc math |

---

*A universal theory of representation reduction grounded in bedrock primitives, applicable across software architecture, data modeling, and systems design.*

