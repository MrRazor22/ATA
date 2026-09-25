# Axiomatic Triad Architecture (ATA)
## Formal Normative Specification — Version 1.0

---

## 1. Scope & Conformance

This specification defines the normative rules, structural invariants, and formal verification tests of the **Axiomatic Triad Architecture (ATA)**. Any software system, data pipeline, or AI agent implementation asserting ATA compliance must satisfy all normative criteria specified herein.

---

## 2. The Axiomatic Basis: The Primitive Triad

Every operational domain boundary decomposes into exactly one irreducible primitive and its derived structural relationships:

### 2.1 The Root Primitive ($P$)
* **Definition:** The single irreducible domain contract defining *what* the capability is.
* **Criterion of Irreducibility (Subtraction Test):** A component is a root primitive if and only if removing it causes the fundamental domain capability to collapse. If the capability survives by substituting a default algorithm or setting, that component is a policy or layer, not a root primitive.
* **Identity:** Exactly one root primitive per operational boundary ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$). Multiple candidates indicate subordinate policies or distinct domain boundaries.

### 2.2 The Injected Policy ($\pi$)
* **Definition:** A primitive injected into another primitive across distinct contracts ($P_{\text{injected}} \to P$) to handle internal operational variation.
* **Internal Delegation Invariant:** A primitive must not hardcode algorithmic choices, formatting, or strategies. Operational strategies are injected as interfaces at initialization, preserving primitive invariance.
* **Orthogonality:** Policies are dependencies of the primitive, never outer wrappers or subclass hierarchies.

### 2.3 The Composable Layer ($\lambda: P \to P$)
* **Definition:** A primitive that wraps another primitive of the **exact same contract**, acting as an endomorphic decorator.
* **Algebraic Monoid Invariant:** Layers form an algebraic monoid $(\text{End}(P), \circ, \text{id})$ under function composition. Every layer must preserve the exact method signatures, types, and semantics of $P$.
* **External Flow Invariant:** Cross-cutting concerns (caching, retries, rate-limiting, telemetry, guardrails) must reside exclusively in layers. They must never pollute the primitive's internals nor leak into caller orchestration.
* **Naming Standard:** Every layer implementation must carry the `*Layer` suffix.

### 2.4 State & Stateless Transforms
* **State ($S$):** Pure, immutable schemas and data transfer objects (DTOs). State carries zero behavior. Primitives communicate strictly via immutable data transfers; shared mutable state across primitives is non-conformant.
* **Transforms ($T$):** Pure functions ($f: S_1 \to S_2$) with zero side-effects.

---

## 3. Normative Laws of Representation

1. **Law of In-Place Refinement:** When requirements evolve, systems must refine existing primitives and policies in place. Appending convenience wrappers, helper flags, or pass-through overloads to avoid refactoring is non-conformant.
2. **Law of Contract Purity:** Root contracts must expose only essential domain operations (~2–4 canonical methods). Convenience aliases, fluent builders, and shorthand overloads belong strictly in stateless external extension utilities.
3. **Law of One-Way Dependency:** High-level boundaries compose lower-level primitives. A primitive must remain unaware of the layers decorating it or the callers driving it. Circular dependencies are strictly forbidden.
4. **Law of Boundary Topology:** Directory trees must align naturally with logical boundaries. Tier-first dumping grounds (`core/`, `policies/`, `layers/` at root) are non-conformant; derivations belong co-located within their owning boundary.

---

## 4. Illustrative Conceptual Deconstructions

### 4.1 Autonomous Agent Architecture
* **Bedrock Primitives:** `Context` (state & history), `Tools` (execution registry), `Model` (generation).
* **Injected Policies ($\pi$):** `Tokenizer` (token accounting), `Compactor` (context reduction).
* **Composable Layers ($\lambda$):** `CachingLayer`, `RetryLayer`, `TelemetryLayer`, `GuardrailLayer`.
* **State ($S$):** Immutable `Message`, `ToolCall`, `ExecutionResult` DTOs.

### 4.2 Structured Decision Engine
* **Bedrock Primitives:** Non-autoregressive decision evaluators.
* **Typed Primitives ($P$):** `Choice` (categorical), `Score` (ordinal/regression), `Noul` (calibrated probability).
* **Injected Policies ($\pi$):** `Calibrator` (loss & probability mapping).
* **Composable Layers ($\lambda$):** `BatchingLayer`, `AuditLayer`.

---

## 5. Compliance Verification Audit

A system is verified as ATA-compliant if it passes all four audit tests:

| Test | Objective | Failure Condition |
| :--- | :--- | :--- |
| **Subtraction Test** | Validates $P$ irreducibility. | Capability still functions after removing $P$. |
| **Merge-or-Split Test** | Validates boundary cohesion. | Spurious interfaces that should be one unified primitive. |
| **Endomorphism Test** | Validates layer contract purity. | Layer changes method signatures or leaks mechanics. |
| **Append-Only Test** | Validates anti-bloat discipline. | Pass-through wrappers or boolean helper flags appended. |

---

*ATA Normative Specification — Establishing minimal representation through irreducible primitives.*
