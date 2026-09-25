---
name: ata
description: >-
  The Axiomatic Triad Architecture (ATA) skill. Activate when designing software,
  auditing systems for bloat, refactoring complex codebases, or executing the
  "Apply ATA" directive to collapse architecture to its minimal representation.
---

# Axiomatic Triad Architecture (ATA) Skill
## The Operational Guide for Agents & Engineers

This skill equips coding agents with the **Theory of Primitives and Representation Reduction**. When activated, the agent operates as a rigorous anti-bloat architect, identifying irreducible domain primitives and eliminating incidental complexity.

---

## 1. Core Operating Principles

1. **Smell-less ≡ Minimal:** Correct design will always be minimal. Minimal code is not about brevity for brevity's sake, writing clever one-liners, or chasing line counts; it is the natural, inevitable side-effect of truth in representation.
2. **Reject the Append-Only Reflex:** Never lazily append helper flags, pass-through overloads, or wrapper classes. When a new requirement emerges, hesitate to add abstractions; refine existing primitives in place.
3. **Dual-Benefit Rule:** Fixing an inaccurate primitive improves both the existing system and the new requirement. Convenience wrappers leave original rot untouched while introducing new bloat.
4. **Human Reviewability as True North:** Every line of code must belong strictly to a bedrock primitive contract ($P$), an injected policy ($\pi$), an endomorphic layer ($\lambda$), pure state ($S$), or a stateless transform ($T$).

---

## 2. The Operational Triad

Every operational boundary encapsulates **exactly one primary root primitive**:

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

* **Root Primitive ($P$):** The irreducible capability contract defining *what* the domain does.
  * *The Subtraction Test:* Removing $P$ causes the domain capability to collapse.
  * *The Discovery Test (Merge-or-Split):* Unify fragmented candidate interfaces around the true real-world metaphor.
* **Injected Policy ($\pi$):** Internal delegation across different contracts ($P_{\text{injected}} \to P$).
  * Handles operational variation (strategies, formats, algorithms).
  * Injected as an interface at initialization; the primitive never hardcodes operational policies.
* **Composable Layer ($\lambda: P \to P$):** Transparent outer decorator of the **exact same contract**.
  * Handles external flow control (caching, retries, metrics, guardrails).
  * Preserves method signatures and semantics; forms an algebraic monoid $(\text{End}(P), \circ, \text{id})$.
  * Every layer carries the `*Layer` suffix.
* **State ($S$) & Transforms ($T$):** Pure immutable schemas/DTOs with zero behavior. Zero shared mutable state across primitives. Stateless pure functions ($f: S_1 \to S_2$).

---

## 3. The "Apply ATA" Execution Runbook

When commanded to **"Apply ATA"** or refactor a system, execute this 4-phase audit:

### Phase 1: Bedrock Isolation
1. Scan the domain boundary and identify the core capability.
2. Run the **Subtraction Test**: what component, if removed, destroys the domain function?
3. Run the **Discovery Test**: are candidate interfaces (e.g. registry vs. executor) actually one unified real-world concept? If so, merge them.

### Phase 2: Injected Policy Extraction
1. Inspect the primitive for hardcoded algorithms, formats, or operational choices.
2. Extract each variable strategy into an injected interface ($\pi$).
3. Ensure policies are orthogonal dependencies passed at initialization.

### Phase 3: Layer Decomposition
1. Inspect the primitive for cross-cutting flow concerns (caching, retry, logging, rate-limiting, guardrails).
2. Evict them from the primitive's internals into separate endomorphic decorators ($\lambda: P \to P$).
3. Verify that each layer preserves the exact contract of $P$.

### Phase 4: Representation Reduction & Cleanup
1. **Purge Convenience Wrappers:** Delete 1:1 pass-through wrappers and obsolete overloads.
2. **Move Helpers to Extensions:** Move syntactic conveniences to stateless extension functions outside the core interface.
3. **Enforce Immutability:** Replace mutable shared state between boundaries with pure immutable DTOs.
4. **Align Directory Topology:** Keep primitive, policies, layers, and schemas co-located within the boundary folder.

---

## 4. Practical Design Smoke Tests

Use these quantitative rules of thumb to detect architectural drift:
* **~2–4 Methods per Contract:** A contract with dozens of methods is a God contract in disguise.
* **~150 Lines per File:** Files exceeding ~150 lines usually harbor procedural glue or helper bloat.
* **~2–3 Files per Folder:** Never wrap a single file in a dedicated subfolder. Keep lean boundaries flat.
* **Functional Ownership:** Assets live where consumed, never scattered across generic root dumping grounds.
