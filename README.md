# Axiomatic Triad Architecture (ATA)
## The Theory of Primitives & Representation Reduction

---

## 1. The Core Soul of ATA

> **"Correct design will always be minimal. Minimal code is not code golf; it is the natural, inevitable side-effect of truth in representation. When a bedrock primitive accurately reflects reality, unnecessary abstractions evaporate; what remains is a complete, minimal basis where every capability is expressed through composition, orthogonal policy, and contract-preserving layers."**

* **Smell-less ≡ Minimal:** Bloat and code smells are the exact same phenomenon. Eliminating smells mathematically collapses a system to its irreducible minimum.
* **Brevity as the Invariant:** Line count is the empirical metric of representational fidelity. When a primitive accurately mirrors reality, brevity is the natural result; sprawl indicates an incomplete abstraction.
* **Active Architectural Interrogation:** Continuously challenge the emerging design: *Why does this feel heavy? Where is the bloat hiding? Why hasn't this collapsed into the effortless clarity ATA demands?* If an interface or implementation does not feel immediately obvious and minimal, the true primitive has not yet been discovered.
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
             Extracts volatile heuristics
```

1. **The Root Primitive ($P$):** The irreducible contract defining *what* the capability is.
   * *The 80/20 Law of the Bedrock Contract:* 80% of architectural integrity is decided at the interface of $P$. This contract demands obsessive care: it must contain only the universal, irreducible operations that remain invariant across all composable layers, swappable policies, and higher-level consumers. Meaningless convenience methods or imprecise signatures in $P$ metastasize into bloat across the entire system.
   * *Contract Purity:* The primitive interface ($P$) defines domain capability only. It contains zero pipeline or composition mechanics; layer composition is executed strictly through external Transforms ($T$).
   * *Subtraction Test:* Removing $P$ causes the domain capability to collapse entirely.
   * *Discovery Test (Merge-or-Split):* Unify fragmented interfaces around the true real-world metaphor.
2. **The Injected Policy ($\pi$):** Volatile heuristics and strategies decoupled from the domain mechanism ($P_{\pi} \to P$).
   * *Decoupling from Mechanism:* Primitives represent irreducible domain mechanisms and must remain completely unopinionated. Policies exist to decouple volatile strategies, heuristics, and algorithmic variations from $P$, ensuring domain bedrock remains free of shifting assumptions.
   * *Policy as a Primitive:* Policies are subordinate primitives ($P_{\pi}$) governing internal operational steps. They demand the same 80/20 minimalism and Subtraction Test as root primitives.
   * *Fractal Boundaries:* When an extracted policy primitive expands in complexity to require its own layers or subordinate policies, it promotes into the root primitive ($P$) of an independent operational boundary.
3. **The Composable Layer ($\lambda: P \to P$):** Transparent outer decorator of the **exact same contract** (Decorator pattern).
   * *External Flow Control:* Intercepting flow (caching, retries, metrics) belongs strictly in layers, never inside $P$.
   * *Forward Composition & Tier Ownership:* Layers are composed around $P$ in forward execution order via external stateless transforms ($T$) rather than nesting constructors inside-out. In multi-tier systems, each primitive decorates its own contract; higher-level boundaries consume clean public contracts without managing underlying layers.
4. **State ($S$) & Transforms ($T$):** Pure immutable schemas/DTOs with zero behavior. In-place performance buffers remain encapsulated within the owning boundary. Stateless pure functions ($f: S_1 \to S_2$).

---

## 3. The Code Completeness Quad

Every line of code across an entire codebase strictly belongs to one of four categories:
1. **Behavior:** The Axiom & Derivations ($P, \pi, \lambda$).
2. **State:** Pure, immutable schemas and DTOs ($S$).
3. **Transforms:** Stateless extension utilities and forward-chaining helpers ($T$).
4. **Wiring:** Zero-logic composition roots instantiating boundaries.

---

## 4. The Derivation Methodology

Designing or refactoring a domain boundary follows a strict derivation sequence:
1. **Bedrock Isolation:** Uncover the irreducible root primitive ($P$) by unifying fragmented interfaces around the core domain metaphor and verifying via the Subtraction Test.
2. **Policy Extraction:** Isolate variable operational algorithms into injected interfaces ($\pi$), ensuring the primitive contains zero hardcoded operational strategies.
3. **Layer Decomposition:** Extract cross-cutting flow concerns (caching, retries, checkpointing, metrics) into homomorphic decorator layers ($\lambda$), preserving contract purity and forward composition.
4. **Representation Reduction:** Eliminate pass-through wrappers, keep state ($S$) strictly immutable, and express domain conversions as stateless pure transforms ($T$).

---

## 5. Conformance Verification Audit

| Test | Verification Criterion | Non-Conformance Signal |
| :--- | :--- | :--- |
| **Subtraction Test** | Validates $P$ irreducibility. | Capability still functions after removing $P$. |
| **Discovery Test** | Validates boundary cohesion. | Splitting one concept (e.g. registry vs. executor) into multiple fake interfaces. |
| **Endomorphism Test** | Validates layer contract purity. | A layer that alters method signatures, leaks mechanics, or nests backwards. |
| **Append-Only Test** | Validates anti-bloat discipline. | Appending pass-through wrappers or boolean helper flags to existing classes. |
| **Brevity Test** | Validates representational fidelity via line economy. | Excessive lines or ceremony required to express domain intent. |

---

## 6. Proving Grounds & Reference Implementations

ATA is proven in production across distinct programming paradigms:
* [**AgentCore (C#)**](https://github.com/MrRazor22/AgentCore): Production multi-agent runtime demonstrating zero-dependency primitives, extension-based layer composition (`ContextLayer`, `LLMLayer`), and boundary-isolated streaming.
* [**NanoLLM (Python)**](https://github.com/MrRazor22/NanoLLM): High-performance decision engine proving single-primitive inference and forward layer chaining.

---

## 7. Universal AI Skill Integration

ATA can be loaded as an on-demand skill by any modern AI coding assistant (Cursor, Antigravity, Claude, Copilot) to enforce minimal primitives and eliminate boilerplate during refactoring and architectural modeling. The skill specification is located at [`skills/ata/SKILL.md`](./skills/ata/SKILL.md).
