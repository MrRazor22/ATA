# Axiomatic Triad Architecture (ATA)
## Technical Specification — Version 1.0

---

## 1. Scope & Purpose

This specification defines the formal technical standard and conformance criteria for the **Axiomatic Triad Architecture (ATA)**. ATA is an architectural and representation-reduction paradigm establishing that any operational capability decomposes into exactly one irreducible primitive, swappable injected policies, and contract-preserving composable layers.

---

## 2. The Axiomatic Basis

Every operational domain boundary encapsulates exactly one bedrock capability ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$):

### 2.1 The Root Primitive ($P$)
* **Definition:** The invariant capability contract defining *what* the domain does.
* **Criterion of Irreducibility (Subtraction Test):** A component is a root primitive if and only if removing it causes the fundamental domain capability to collapse. If the capability survives by substituting a default algorithm or setting, that component is a policy or layer, not a root primitive.
* **Invariant of Invariance:** Once discovered, the root contract remains invariant across operational variations.

### 2.2 The Injected Policy ($\pi$)
* **Definition:** A primitive injected across distinct contracts ($P_{\text{injected}} \to P$) to handle internal operational variation (*how* an internal step executes).
* **Internal Delegation Invariant:** A primitive must not hardcode algorithmic choices, formatting, or strategies. Variable strategies are injected as interfaces at initialization.
* **Orthogonality:** Policies are dependencies of the primitive, never outer wrappers or subclass hierarchies.

### 2.3 The Composable Layer ($\lambda: P \to P$)
* **Definition:** An endomorphic decorator wrapping a primitive using the **exact same contract**.
* **Algebraic Monoid Invariant:** Layers form an algebraic monoid $(\text{End}(P), \circ, \text{id})$ under function composition. Every layer must preserve the exact method signatures, types, and semantics of $P$.
* **External Flow Invariant:** Cross-cutting flow mechanics (caching, retries, rate-limiting, telemetry, guardrails) reside exclusively in layers. They must never pollute the primitive's internals nor leak into caller orchestration.
* **Naming Standard:** Every layer implementation must carry the `*Layer` suffix.

### 2.4 State ($S$) & Stateless Transforms ($T$)
* **Pure State ($S$):** Pure, immutable schemas and data transfer objects (DTOs). State carries zero behavior. Primitives communicate strictly via immutable data transfers; shared mutable state across boundaries is non-conformant.
* **Stateless Transforms ($T$):** Pure mathematical functions ($f: S_1 \to S_2$) with zero side-effects.

---

## 3. Normative Laws of Representation

1. **Law of In-Place Refinement:** When requirements evolve, systems must refine existing primitives and policies in place. Appending convenience wrappers, helper flags, or pass-through overloads to avoid refactoring is non-conformant.
2. **Law of Contract Purity:** Root contracts must expose only essential domain operations (~2–4 canonical methods). Convenience aliases, fluent builders, and shorthand overloads belong strictly in stateless external extension utilities.
3. **Law of One-Way Dependency:** High-level boundaries compose lower-level primitives. A primitive must remain strictly unaware of the layers decorating it or the callers driving it. Circular dependencies are strictly forbidden.
4. **Law of Boundary Topology:** Directory trees must align naturally with logical boundaries (1:1 boundary-to-folder parity). Tier-first dumping grounds (`core/`, `policies/`, `layers/` at root) are non-conformant; derivations belong co-located within their owning boundary.

---

## 4. Conformance Verification Audit

An implementation or refactor is verified as ATA-compliant if it satisfies all four audit tests:

| Test | Verification Criterion | Non-Conformance Signal |
| :--- | :--- | :--- |
| **Subtraction Test** | Validates $P$ irreducibility. | Capability still functions after removing $P$. |
| **Discovery Test** | Validates boundary cohesion. | Splitting one concept (e.g. registry vs. executor) into multiple fake interfaces. |
| **Endomorphism Test** | Validates layer contract purity. | A layer that changes method signatures or leaks internal mechanics. |
| **Append-Only Test** | Validates anti-bloat discipline. | Appending pass-through wrappers or boolean helper flags to existing classes. |

---

*ATA Technical Specification — Establishing minimal representation through irreducible primitives.*
