---
name: ata
description: >-
  The Axiomatic Triad Architecture (ATA) skill and specification. Activate when designing software,
  auditing systems for bloat, refactoring complex codebases, or executing the "Apply ATA" directive.
---

# Axiomatic Triad Architecture (ATA)
## The Theory of Primitives & Representation Reduction

---

## 1. The Core Soul & Philosophy of ATA

> **"Correct design will always be minimal. Minimal code is not code golf; it is the natural, inevitable side-effect of truth in representation. When a bedrock primitive accurately reflects reality, unnecessary abstractions evaporate; what remains is a complete, minimal basis where every capability is expressed through composition, orthogonal policy, and contract-preserving layers."**

* **ATA is Simply Master-Crafted OOP:** ATA is not an exotic, alien paradigm or academic ceremony. If an engineer looks at an ATA codebase and finds it bizarre, confusing, or esoteric, **ATA has failed**. To any seasoned developer, an ATA project simply looks like a clean, master-designed system: clear domain primitives, swappable strategies injected via DI, clean extension/layer pipelines, and an intuitive directory layout.
* **The Supreme Question: "Who is actually using it?":** Every design decision begins and ends here. Never build abstractions, middleman primitives, or registries in a vacuum for speculative callers. If there is no concrete caller actively demanding the shape of an abstraction right now, it does not exist.
* **Smell-less ≡ Minimal:** Code bloat and architectural smells are the exact same phenomenon. Eliminating smells mathematically collapses a system to its irreducible minimum.
* **The ~150-Line Barometer:** Line sprawl is an empirical diagnostic, not a formatting rule. If a file crosses ~150 lines, do not celebrate its thoroughness—diagnose it. It almost invariably signals that policy heuristics (parsing, math, thresholds) were inlined, cross-cutting flow was hardcoded, or multiple responsibilities were bundled together.
* **Interface-First Collaborative Dialogue:** 80% of architecture is determined at interface boundaries ($P$ and $\pi$). Never rush into generating large implementation files based on an unverified contract. Interactively design and lock the core interfaces with the user first; when the primitive contract is true, the implementation is trivial.

---

## 2. The Operational Triad: Primitives, Policies, Layers

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
             Extracts volatile heuristics
```

### 1. The Root Primitive ($P$): Bedrock Domain Mechanism
* **Irreducible Domain Responsibility:** Defines *what* the capability is. Contains only universal operations invariant across callers and layers.
* **Direct Policy Consumption (Banish Middlemen):** When multiple concrete policies share a common interface (e.g. various data sources), the consumer primitive or high-level caller directly accepts the required policy. Do not invent fake "middleman" primitives or wrapper services unless genuine aggregation or merge logic across multiple sources is required.
* **Reject Registry/Factory Bloat:** Hardcoded switch-case registries or factories masquerading as abstractions are smells that hide missing domain ownership. Inject policies cleanly via DI or caller selection.

### 2. The Injected Policy ($\pi$): Swappable Volatility
* **Mechanism vs. Heuristic:** Primitives implement unopinionated mechanics; policies encapsulate opinionated strategies, scoring criteria, thresholds, and provider-specific details ($P_{\pi} \to P$).
* **The Policy Composition Rule:** A policy must remain atomic. If a policy begins needing subordinate policies of its own, **it cannot secretly juggle them**. It must either be split into two orthogonal policies injected into the parent primitive, or it has matured into its own autonomous child primitive managing a sub-boundary.
* **Beware the Composite Policy Trap:** Avoid forcing an aggregation of multiple policies into a single composite class implementing that same policy interface (`CompositeSource : ISource`), unless the domain genuinely represents a monoid/reduction. Forcing multi-source orchestration, batching, or concurrency into an atomic heuristic interface leaks coordination smells into pure strategies.

### 3. The Composable Layer ($\lambda: P \to P$): Transparent Flow Decorators
* **Contract-Preserving Decorators:** Transparently wrap the exact same contract ($P \to P$). Handle cross-cutting flow (caching, retries, rate limits, circuit breakers, telemetry) strictly outside the primitive.
* **Forward Composition:** Composed outside-in via clean pipeline extensions or transforms ($T$). The primitive has zero awareness of its decorators.

### 4. State ($S$) & Transforms ($T$): Purpose-Fit Data & Pure Functions
* **Zero DTO/Schema Sprawl:** State schemas and DTOs must carry strictly what is needed and consumed. Zero speculative properties ("just in case"), zero pass-through baggage.
* **Zero Method Redundancy:** Eliminate redundant API overloads (e.g. `Add` vs `AddBatch`, `Process` vs `ProcessBatch`). Accept universal collection/span representations so a single item and a batch flow through the exact same minimal signature.
* **Pure Stateless Mathematical Functions ($T$):** Pure calculations, normalization math, formatting, and data mappings must live as stateless functions ($f: S_1 \to S_2$) outside domain contracts. Never pollute primitive interfaces with calculation helpers.

---

## 3. Natural Directory Topology & Fractal Boundary Promotion

Topology should reflect natural, timeless software engineering rather than rigid framework dogmas:

* **Flat First within Boundaries:** Forcing single files into dogmatic `/policies/` and `/layers/` folders creates ceremony and noise. Within a boundary, start flat:
  * Concrete strategies are named naturally for what they actually are (`sqlite_source.py`, `cosine_similarity.py`), without forcing redundant `_policy` suffixes.
  * For decorators, a `_layer` or `Layer` naming hint (`retry_layer.py`, `caching_layer.py`) is helpful because it instantly distinguishes transparent decorators from standalone primitives sharing the same interface.
  * Grouping into subfolders is an optional human choice when implementations multiply, not a mandatory dogmatic ritual.
* **Fractal Boundary Promotion:** When a policy grows rich and complex—requiring internal sub-policies or dedicated layers—it naturally **promotes into its own primitive boundary folder** nested directly inside the parent boundary that owns it:
  ```text
  evaluator/
    evaluator_primitive.py
    heuristics/              # Promoted policy boundary
      heuristic_primitive.py
      threshold_policy.py
  ```
* **Natural Sibling Placement for Shared Primitives:** Boundary hierarchy mirrors usage hierarchy. If a primitive is consumed by multiple peer primitives, it naturally belongs at their shared sibling level. Never bury a shared dependency deep inside one of its consumers.

---

## 4. The Code Completeness Quad

Every line of code across a codebase strictly belongs to one of four categories:
1. **Behavior:** The Axiom & Derivations ($P, \pi, \lambda$).
2. **State ($S$):** Pure, immutable schemas and DTOs with zero methods.
3. **Transforms ($T$):** Pure, stateless functions and forward composition helpers ($f: S_1 \to S_2$).
4. **Wiring:** Zero-logic composition roots instantiating boundaries and injecting dependencies via DI.

---

## 5. Conformance Verification Audit

| Test | Verification Criterion | Non-Conformance Signal |
| :--- | :--- | :--- |
| **Teleological Test** | Validates consumer necessity. | Inventing a middleman or registry without an immediate caller needing it. |
| **Brevity/Barometer Test** | Validates structural decomposition. | Files crossing ~150 lines due to inlined heuristics or hardcoded cross-cutting flows. |
| **Subtraction Test** | Validates $P$ irreducibility. | Capability still functions after removing $P$. |
| **Discovery Test** | Validates boundary cohesion. | Splitting one concept (e.g. registry vs. executor) into multiple fake interfaces. |
| **Policy Atomicity Test** | Validates strategy simplicity. | A policy internally juggling multiple sub-policies or hiding orchestration. |
| **Endomorphism Test** | Validates layer contract purity. | A layer that alters method signatures, leaks mechanics, or nests backwards. |
| **Redundancy Test** | Validates API economy. | Duplicate convenience overloads (e.g., `Add` vs `AddBatch`) or speculative DTO fields. |
