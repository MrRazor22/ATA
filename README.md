# Primitive-First Design (PFD)

> **A philosophy for building minimal, high-signal, zero-smell software architectures.**  
> *Case Studies:* [AgentCore](https://github.com/MrRazor22/AgentCore) | [NanoLLM](https://github.com/MrRazor22/NanoLLM)  
> *Technical Skill & Audit Rules:* [`skills/pfd/SKILL.md`](skills/pfd/SKILL.md)

---

## The Core Thesis

**Not all minimal code is correct, but correct code will usually be minimal.**

Most architectural complexity does not solve genuine domain problems—it solves structural problems created by flawed foundations. Wrappers, accumulators, intermediate adapters, and sprawling patterns exist primarily to patch or support poorly conceived primitives. 

A poor foundational primitive causes the surrounding abstraction bloat. When the fundamental boundary is modeled correctly:
* Surrounding bloat disappears because there is nothing broken left to patch.
* Codebases contract naturally to their minimal theoretical footprint without cosmetic tricks.
* Many code smells disappear before they emerge.
* Scalability, readability, and composability emerge organically without defensive scaffolding.

Minimality in PFD means the **minimum structural complexity required to express domain truth cleanly**—not code-golfing or textual compression. Cramming an entire system into one god class or abusing language gimmicks to claim fewer files violates PFD. Lines of code (LoC) serve merely as an observational end-to-end signal of structural complexity, never a design target or a rigid law.

---

## Primitives & Interface Contract Law

* **The Interface is the Truth:** Every operational boundary is defined by its contract across any paradigm (C#/Java `interface`, Rust `trait`, Go `interface`, C++ concept). Concrete implementations are never directly exposed across boundaries; zero backdoor access. Passive representations (DTOs) carry state and are the only exception.
* **The Cognitive Forcing Mechanism:** Concrete access tempts developers to casually leak ad-hoc public methods for temporary convenience. Enforcing strict interface contracts serves as a cognitive forcing function, compelling you to decide upfront whether a capability genuinely belongs to the domain boundary.
* **Logical Boundaries vs. OOP Objects:** A primitive represents an irreducible logical boundary of conceptual responsibility, not an arbitrary object-oriented class or physical noun. (In an illustrative vehicle model, the *Engine* represents a primitive boundary, while a *piston* is an internal component. Every class is not a primitive).
* **Foundational Leverage:** The primitive contract determines most of the architecture that follows. When foundational boundaries are sound, downstream implementation flows naturally downhill.

---

## Future-Proofing by Subtraction

> **Future-Proofing is the removal of unnecessary restrictions from today's boundary, not the addition of speculative future capabilities.**

Developers often overfit abstractions to narrow, immediate needs, only to break them when requirements evolve. A true primitive simultaneously balances three criteria:
1. **Zero Speculative Bloat:** Nothing is added for an imagined future use case.
2. **Zero Future Blindspots:** No artificial constraints lock out natural domain capabilities.
3. **Natural Adaptability:** Present needs are satisfied completely while future expansion remains natural without contract breakage.

### Contract Scrutiny & Universal Opinions
Every element of a contract must be scrutinized: method existence, parameters, return shapes, sync/async, lifecycle, and what is deliberately *not* exposed. Before adding another method to handle a new need, ask whether the existing primitive can express it by generalizing its fundamental shape.

Purity does not mean having zero opinions:
* **Universal Domain Truths** belong directly in the **Core Primitive Contract**.
* **Variable Strategies & Rules** belong in injected **Policies**.
* **Convenience Transformations** do not belong in the primitive contract.

---

## The Architectural Model: Four Pure Boundaries

PFD classifies architectural responsibilities into four distinct roles:

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

* **Universal Truth** $\longrightarrow$ **Core Primitive**
* **Variable Strategy** $\longrightarrow$ **Policy**
* **External Concern** $\longrightarrow$ **Layer**
* **Passive State** $\longrightarrow$ **DTO**

> **The Architectural Triad Axiom:**  
> A **Policy** is just a primitive on the inside.  
> A **Layer** is just the same primitive on the outside.  
> **DTOs and pure transformations** provide the passive binding (**binder**) holding boundaries together.

---

## Policies vs. Layers: The Boundary Diagnostics

* **Policy (Inside):** Completes the primitive from within. Governs internal strategy, algorithms, and meaningful operating thresholds.
* **Layer (Outside):** Extends an already complete primitive from the outside. Acts like an instrument attached directly to the primitive's inputs and outputs, gaining direct access to inspect, monitor, persist, or adapt complete I/O flow without polluting internal mechanics.

### The Diagnostic Sequence: Functional Completeness

```text
Can the primitive function meaningfully without it?
        │
        ├── NO ──► First ask: Is the primitive itself incomplete?
        │            ├── YES ──► Fix the primitive contract (missing core responsibility)
        │            └── NO  ──► POLICY (injected strategy or limit completing the mechanism)
        │
        └── YES ──► LAYER (external concern: logging, persistence, telemetry, caching)
```

> **Poor Primitive Diagnostic:** If something is external to the primitive and the primitive remains functionally complete without it, it is a Layer. But if the primitive cannot meaningfully function without the concern, investigate whether the primitive itself is incomplete before automatically inventing a wrapper or policy. A missing fundamental responsibility often masquerades as an external abstraction.

---

## Recursive Implementation Discipline

A concrete implementation is itself an opinion. The same minimality and purity discipline applies recursively inside the implementation:

* When an implementation becomes large or complex, do not simply split files. Identify the hidden opinion, strategy, or responsibility inside, and extract it as an injected **Opinion Sub-Primitive (Policy)** when it genuinely warrants a boundary.
* A large cohesive implementation is a smell signal worth investigating for hidden policies or god-object behavior. Lines of code serve as an observational smell detector, never a target.
* The anti-gaming principle holds that physical code shapes (arbitrary file fragmentation, partial classes, deep inheritance, helper indirection) must never be used merely to conceal architectural sprawl. Cohesive units remain together.

---

## Architectural Purity, Symmetry & Topology

* **Purity Defined:** Purity is achieved by removing responsibilities until each construct represents exactly what it fundamentally is.
* **Symmetry as a Discovery Tool:** Correctly identifying the fundamental boundary often causes naturally symmetrical responsibilities to emerge. When two responsibilities produce or consume the same conceptual flow, their asymmetry may reveal a false boundary. Natural symmetry emerges from correct boundaries, eliminating intermediate accumulators, adapters, and orchestration glue.
* **Physical Topology:** Conceptual boundaries naturally influence physical directory structure. Folder hierarchies should roughly resemble the architectural trie drawn from actual boundaries—not "every primitive gets a folder." Small scopes stay flat; structure is never manufactured for its own sake.
* **Universal Scope:** PFD is not a coding pattern; the same primitive, policy, layer, and state reasoning applies wherever structured work is produced (UI components, system architecture, documentation, and creative work).

---

## Learn More

* **[AgentCore Case Study](https://github.com/MrRazor22/AgentCore):** See how PFD was discovered and applied in an experimental agent framework.
* **[NanoLLM Case Study](https://github.com/MrRazor22/NanoLLM):** See PFD applied to high-performance model inference and lightweight runtime boundaries.
* **[PFD Agent Skill (`skills/pfd/SKILL.md`)](skills/pfd/SKILL.md):** The machine-executable technical specification, audit rules, and automation directives.