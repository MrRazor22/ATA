---
name: ata
description: >-
  The Axiomatic Triad Architecture (ATA) skill and specification. Activate when designing software,
  auditing systems for bloat, refactoring complex codebases, or executing the "Apply ATA" directive.
---

# Axiomatic Triad Architecture (ATA)
## The Theory of Primitives & Representation Reduction

---

## 1. The Core Soul of ATA

> **"Correct design will always be minimal. Minimal code is not code golf; it is the natural, inevitable side-effect of truth in representation. When a bedrock primitive accurately reflects reality, unnecessary abstractions evaporate; what remains is a complete, minimal basis where every capability is expressed through composition, orthogonal policy, and contract-preserving layers."**

* **Smell-less ≡ Minimal:** Bloat and code smells are the exact same phenomenon. Eliminating smells mathematically collapses a system to its irreducible minimum.
* **Reject the Append-Only Trap:** Never lazily append helper flags, pass-through overloads, or wrapper classes. Prefer updating and refining existing primitives in place.
* **Human Reviewability as True North:** Architecture must be effortlessly verifiable. Every line of code must have an unambiguous, self-evident purpose.

---

## 2. The Operational Triad

Every operational boundary encapsulates **exactly one root primitive** ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$):

```text
                  LAYERS  (λ: P ➔ P)
              Decorates what flows in & out
                          ▲
                          │ wraps
                          │
  CALLER  ────▶    PRIMITIVE (P)    ────▶  RESULT
                The Domain Bedrock
                          │
                          │ injects
                          ▼
                     POLICIES  (π)
              Supplies swappable strategy
```

1. **The Root Primitive ($P$):** The irreducible contract defining *what* the capability is.
   * *Subtraction Test:* Removing $P$ causes the domain capability to collapse entirely.
   * *Discovery Test (Merge-or-Split):* Unify fragmented interfaces around the true real-world metaphor.
2. **The Injected Policy ($\pi$):** Variable strategy injected across distinct contracts ($P_{\text{injected}} \to P$).
   * *Internal Delegation:* A primitive never hardcodes operational algorithms; swappable strategies are injected at initialization.
3. **The Composable Layer ($\lambda: P \to P$):** Transparent outer decorator of the **exact same contract** (Decorator pattern).
   * *External Flow Control:* Intercepting flow (caching, retries, metrics) belongs strictly in layers, never inside $P$.
   * *Forward Composition & Tier Ownership:* Primitives expose a stateless way to chain layers forward in execution order rather than nesting constructors inside-out. In multi-tier systems, each primitive decorates its own contract; higher-level boundaries consume clean public contracts without managing underlying layers.
4. **State ($S$) & Transforms ($T$):** Pure immutable schemas/DTOs with zero behavior. In-place performance buffers remain encapsulated within the owning boundary. Stateless pure functions ($f: S_1 \to S_2$).

---

## 3. The Code Completeness Quad

Every line of code across an entire codebase strictly belongs to one of four categories:
1. **Behavior:** The Axiom & Derivations ($P, \pi, \lambda$).
2. **State:** Pure, immutable schemas and DTOs ($S$).
3. **Transforms:** Stateless extension utilities and forward-chaining helpers ($T$).
4. **Wiring:** Zero-logic composition roots instantiating boundaries.

---

## 4. The "Apply ATA" Execution Runbook

When auditing, designing, or refactoring a system:
1. **Bedrock Isolation:** Scan the boundary, run the Subtraction Test, and eliminate fake interface splits.
2. **Policy Extraction:** Extract hardcoded operational algorithms into injected interfaces ($\pi$).
3. **Layer Decomposition:** Evict cross-cutting flow concerns into decorators ($\lambda$). Ensure forward composition.
4. **Representation Reduction:** Purge 1:1 pass-through wrappers, move helpers to stateless extensions, encapsulate in-place buffers, and align directory topology (co-locate derivations inside the boundary folder).

---

## 5. Conformance Verification Audit

| Test | Verification Criterion | Non-Conformance Signal |
| :--- | :--- | :--- |
| **Subtraction Test** | Validates $P$ irreducibility. | Capability still functions after removing $P$. |
| **Discovery Test** | Validates boundary cohesion. | Splitting one concept (e.g. registry vs. executor) into multiple fake interfaces. |
| **Endomorphism Test** | Validates layer contract purity. | A layer that alters method signatures, leaks mechanics, or nests backwards. |
| **Append-Only Test** | Validates anti-bloat discipline. | Appending pass-through wrappers or boolean helper flags to existing classes. |

---

## 6. Proving Grounds & Reference Implementations

ATA is proven in production across distinct programming paradigms:
* [**AgentCore (C#)**](https://github.com/MrRazor22/AgentCore): Production multi-agent runtime demonstrating zero-dependency primitives, extension-based layer composition (`ContextLayer`, `LLMLayer`), and boundary-isolated streaming.
* [**NanoLLM (Python)**](https://github.com/MrRazor22/NanoLLM): High-performance decision engine proving single-primitive inference and forward layer chaining.
