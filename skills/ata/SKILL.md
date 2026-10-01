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
>
> *(The Plain-English Bottom Line: ATA is not code golf. The ultimate goal is **zero code smell**. Radically reduced line count is merely the natural mathematical side-effect of eliminating smells and modeling domain reality truthfully. ATA is simply the directional compass to get there).*

### I. The Invariant of Representation (Smell-less ≡ Minimal)
* **Code Smell = Anti-ATA:** Bloat and code smells are the exact same phenomenon. ATA's ultimate goal is zero code smell; if a design claims to follow ATA but introduces code smells, **ATA has failed**. Eliminating smells mathematically collapses a system to its irreducible minimum.
* **10x Signal Compression & Brevity Barometer:** Line count is an empirical metric of representational fidelity. When primitives, policies, and layers are modeled cleanly, codebases compress to **~1/10th of their typical size** (proven in `AgentCore` matching full feature parity of LangChain and Microsoft Agent Framework at ~1/10th the SLOC with zero smells). If a file crosses ~150 lines, do not celebrate its thoroughness—diagnose it. It almost invariably signals that policy heuristics were inlined, cross-cutting flow was hardcoded, or multiple responsibilities were bundled together.
* **Minimality Is Measured:** Fewer types, files, and lines at equal capability. Never introduce a file, type, DTO, helper, or transform unless the Subtraction Test fails without it; a category in the Quad is a classification, not a licence to create a unit for it.
* **Zero Space for "Convenience" (Every Character Earns Its Place):** Convenience methods and wrappers are the root seed of software bloat and anti-ATA smells. Bloat starts from two failure modes: (1) lazy convenience additions, and (2) fear of breaking backward compatibility. ATA solves both: every line and character must strictly earn its existence (zero convenience methods), and bedrock primitives ($P$) are designed so meticulously up front that their contracts remain invariant—all future variance is absorbed entirely through injected policies ($\pi$, subordinate primitive) or composable layers ($\lambda$, layered primitive).
* **Two-Page Architectural Comprehension:** Because every operational boundary is governed by an explicit interface contract, the entire design blueprint of any project—regardless of scale—must be effortlessly readable and comprehensible within at most 1 to 2 pages of documentation.

### II. Human-AI Synthesis & Operational Discipline
* **Universal Discipline for Humans and AI Alike:** ATA is not merely an AI agent prompt or a coder's trick; it is a universal intellectual discipline for humans and AI alike. Both humans and LLMs tend toward the lazy append-only trap—adding wrapper classes, helper flags, and convenience layers rather than thinking deeply to discover the irreducible primitive. ATA stops this decay, saving massive context tokens and computational cost while preserving radical maintainability.
* **Unified Representation, Not a Patchwork of Ideas:** ATA is not a loose assembly of disparate design patterns; it is a unified theory of representational truth. Token efficiency, compute savings, radical maintainability, human verifiability, and zero code smell are not separate goals—they are one-to-one complementary mathematical side-effects of bedrock primitives accurately mirroring reality.
* **Reject the Append-Only Trap (Resist Production Convenience Band-Aids):** When adapting to new requirements or production changes, resist the lazy reflex to append convenience wrapper layers, adapter classes, or boolean flags. Slapping on convenience layers evades the hard thinking needed to uncover flaws in the bedrock primitive contract, snowballing technical debt. Always diagnose the root contract flaw and refine the existing primitive in place.
* **The Supreme Question: "Who is actually using it?":** Every design decision begins and ends here. Never build abstractions, middleman primitives, or registries in a vacuum for speculative callers. If there is no concrete caller actively demanding the shape of an abstraction right now, it does not exist.

### III. Disciplined Modeling over Dogma
* **Intellectual Honesty Over Dogma:** Never apply ATA blindly or religiously. If applying an ATA rule creates practical friction, awkward ceremony, or a design smell in a specific scenario, honestly identify and challenge it rather than force-fitting dogma.
* **Triad Components Are Distinct Roles, Not Mandatory Rituals:** Primitives ($P$), policies ($\pi$), and layers ($\lambda$) model distinct structural dimensions (mechanism vs. heuristic vs. flow). If a capability has no volatile heuristics or cross-cutting flow, the bedrock primitive contract ($P$) is already 100% complete. Fabricating policies or decorator layers when none are demanded by domain reality is dogmatic bloat.
* **Interface-First Collaborative Dialogue:** 80% of architecture is determined at interface boundaries ($P$ and $\pi$). Never rush into generating large implementation files based on an unverified contract. Interactively design and lock the core interfaces with the user first; when the primitive contract is true, the implementation is trivial.
* **ATA is Timeless Engineering Restraint:** ATA is not an esoteric ceremony or alien syntax. To any seasoned engineer or thinker, an ATA system simply looks like master-crafted architecture: irreducible bedrock primitives, decoupled volatile heuristics, clean transparent pipelines, and intuitive domain boundaries.

---

## 2. The Operational Triad: Primitives, Policies, Layers

Every operational boundary encapsulates **exactly one root primitive** ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$). *(Note: $P, \pi, \lambda$ model distinct structural roles, not ceremonial boilerplate. Never force policies or layers into a boundary where the bedrock primitive contract ($P$) is already complete).*

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
* **Mandatory Interface Contract (Non-Negotiable Boundary Discipline):** Every root primitive ($P$) and policy ($\pi$) **must** define an explicit formal contract (interface, protocol, trait, or abstract contract) — even with a single concrete implementation. The contract captures the primitive's domain concept in its purest form: reading the contract alone tells you exactly what the primitive is and does, with zero knowledge of its concrete implementation. All callers and consumers depend exclusively on this contract. Accessing or depending on the concrete class directly — bypassing the contract in any way — is unconditionally forbidden. Composable layers ($\lambda: P \to P$), swappable policies, and all future extensions attach strictly through this contract. As an inevitable side-effect, this enforces total decoupling, effortless testing, clean extensibility, and zero code smell across the entire system.
* **Primitive Stability vs. Churn Diagnostic (The Dual Necessity Test):** Continual churn of a root primitive contract for new requirements is a severe code smell indicating lazy, shallow initial domain modeling. While evolving $P$ during design or refactoring to better reflect real-world truth is essential, a well-modeled primitive is invariant: it provides an irreducible, complete foundation where future capabilities attach naturally via policies ($\pi$) and layers ($\lambda$)—without speculative YAGNI methods and without constant contract churn. A modification to $P$ is legitimate if and only if it satisfies both conditions:
  1. **Universal Enablement:** The revision completes the primitive's domain metaphor such that all potential extensions benefit as a natural, necessary side-effect of a complete abstraction.
  2. **Irreducible Necessity:** If the proposed change were removed, the bedrock primitive contract would be fundamentally incomplete in itself.
* **No Callbacks, Events, or Notifications in Core Primitives:** Inlining callbacks, event emitters, lifecycle hooks, or notification handlers inside a root primitive is a severe anti-ATA smell indicating incorrect output granularity. Primitives yield state naturally via their contract stream; downstream consumers, layers, or reactive extensions attach to that stream externally.
* **Ban Static Classes & Global Mutable State:** Static utility classes and global mutable state are anti-ATA smells that obscure dependencies and prevent testing. Manage state strictly through explicit boundaries and DI composition roots. Monolithic static helper classes that accumulate arbitrary behavior without interfaces are strictly prohibited.
* **Irreducible Domain Responsibility:** Defines *what* the capability is. Contains only universal operations invariant across callers and layers.
* **Direct Policy Consumption (Banish Middlemen):** When multiple concrete policies share a common interface (e.g. various data sources), the consumer primitive or high-level caller directly accepts the required policy. Do not invent fake "middleman" primitives or wrapper services unless genuine aggregation or merge logic across multiple sources is required.
* **Reject Registry/Factory Bloat:** Hardcoded switch-case registries or factories masquerading as abstractions are smells that hide missing domain ownership. Inject policies cleanly via DI or caller selection.

### 2. The Injected Policy ($\pi$): Swappable Volatility
* **Mechanism vs. Heuristic:** Primitives implement unopinionated mechanics; policies encapsulate opinionated strategies, scoring criteria, thresholds, and provider-specific details ($P_{\pi} \to P$).
* **The Policy Composition Rule:** A policy must remain atomic. If a policy begins needing subordinate policies of its own, **it cannot secretly juggle them**. It must either be split into two orthogonal policies injected into the parent primitive, or it has matured into its own autonomous child primitive managing a sub-boundary.
* **Beware the Composite Policy Trap:** Avoid forcing an aggregation of multiple policies into a single composite class implementing that same policy interface (e.g. `CompositeSource` wrapping multiple `Source` policies), unless the domain genuinely represents a monoid/reduction. Forcing multi-source orchestration, batching, or concurrency into an atomic heuristic interface leaks coordination smells into pure strategies.

### 3. The Composable Layer ($\lambda: P \to P$): Transparent Flow Decorators
* **Contract-Preserving Decorators:** Transparently wrap the exact same contract ($P \to P$). Handle cross-cutting flow (caching, retries, rate limits, circuit breakers, telemetry) strictly outside the primitive.
* **Forward Composition:** Composed outside-in via clean pipeline extensions or transforms ($T$). The primitive has zero awareness of its decorators.

### 4. State ($S$) & Transforms ($T$): Purpose-Fit Data & Pure Functions
* **Zero DTO/Schema Sprawl:** State schemas and DTOs must carry strictly what is needed and consumed. Zero speculative properties ("just in case"), zero pass-through baggage.
* **DTOs Carry Zero Behavior (Behavior on State is a Primitive Smell):** If a DTO or data schema has methods, mutating behavior, or business calculations, it is an anti-ATA smell indicating poor primitive design. State is strictly inert data representation; all operational logic belongs exclusively inside $P$ or pure transforms $T$.
* **Zero Method Redundancy:** Eliminate redundant API overloads (e.g. `Add` vs `AddBatch`, `Process` vs `ProcessBatch`). Accept universal collection/span representations so a single item and a batch flow through the exact same minimal signature.
* **Single-File Co-location & The 150-Line Barometer:** Transforms, extension methods, and state DTOs belong in the **exact same file** as the contract or type they extend. This co-location implicitly forces respect for the ~150-line barometer: if convenience extensions multiply, the file breaches 150 lines and immediately rings the alarm, preventing extension sprawl and completely eliminating monolithic static helper dumping grounds.
* **Transform Restraint & Mathematical Purity ($T$):** Pure calculations, normalization math, formatting, and data mappings must live as stateless pure functions ($f: S_1 \to S_2$) outside domain contracts. Transforms must never be abused as an escape hatch to smuggle domain mechanics or volatile heuristics outside of $P$ and $\pi$; they exist strictly for pure representation mapping and forward layer composition.

---

## 3. Natural Directory Topology & Fractal Boundary Promotion

Topology should reflect natural, timeless software engineering rather than rigid framework dogmas:

* **Flat First within Boundaries & Co-located Derivations:** Keep derivations beside their boundary; do not split into one-type-per-file or extra folders when a single file stays readable. Forcing single files into dogmatic `/policies/` and `/layers/` folders creates ceremony and noise. Within a boundary, start flat:
  * Concrete strategies are named naturally for what they actually are (`SqliteSource`, `CosineSimilarity`), without forcing redundant `Policy` suffixes.
  * For decorators, a `Layer` naming hint (`RetryLayer`, `CachingLayer`) is helpful because it instantly distinguishes transparent decorators from standalone primitives sharing the same interface.
  * Grouping into subfolders is an optional human choice when implementations multiply, not a mandatory dogmatic ritual.
* **Namespace & Folder Storytelling (The Directory Barometer):** Namespaces and folders must visually narrate the domain story rather than technical stereotypes (`/models`, `/controllers`, `/services`). Just as a file crossing ~150 lines is questionable, a cluttered root or boundary folder filled with miscellaneous non-Triad files is questionable. A boundary folder holds strictly its Triad members ($P, \pi, \lambda, S, T$) and promoted child boundaries—never miscellaneous "junk drawer" files. If unrelated files accumulate, the boundary abstraction is broken.
* **Fractal Boundary Promotion:** When a policy grows rich and complex—requiring internal sub-policies or dedicated layers—it naturally **promotes into its own primitive boundary folder** nested directly inside the parent boundary that owns it:
  ```text
  evaluator/
    evaluator_boundary       # Primary bedrock primitive
    heuristics/              # Promoted policy boundary
      heuristic_primitive
      threshold_policy
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

## 5. The Derivation & Refactoring Methodology

Designing or refactoring a domain boundary follows a strict derivation sequence:
1. **Bedrock Isolation:** Uncover the irreducible root primitive ($P$) by unifying fragmented interfaces around the core domain metaphor and verifying via the Subtraction Test.
2. **Policy Extraction:** Isolate variable operational algorithms into injected interfaces ($\pi$), ensuring the primitive contains zero hardcoded operational strategies.
3. **Layer Decomposition:** Extract cross-cutting flow concerns (caching, retries, checkpointing, metrics) into homomorphic decorator layers ($\lambda$), preserving contract purity and forward composition.
4. **Representation Reduction:** Eliminate pass-through wrappers, keep state ($S$) strictly immutable, express domain conversions as stateless pure transforms ($T$), and keep derivations beside their boundary—do not split into one-type-per-file or extra folders when a single file stays readable.
5. **Zero Dead Code & Zero Legacy Bloat:** When refactoring under ATA, ask the user and actively purge dead code, abandoned feature toggles, and speculative backward-compatibility layers. Never degrade or regress existing functional power—match or surpass it cleanly with a radically smaller footprint.

---

## 6. Conformance Verification Audit

| Test | Verification Criterion | Non-Conformance Signal |
| :--- | :--- | :--- |
| **Smell/Anti-ATA Test** | Validates absolute zero code smell. | Retaining anti-patterns, leaky wrappers, or hacky patches under the guise of ATA. |
| **Minimality Test** | Validates structural necessity. | Creating a standalone file, type, or DTO solely to satisfy a Quad category when the Subtraction Test would pass without it. |
| **Contract Rigor Test** | Every $P$ and $\pi$ defines a contract interface; all callers depend on it, never the concrete class. | A primitive/policy lacking a contract interface, or callers depending on the concrete class directly. |
| **Contract Immutability Test** | Validates universal stability & freedom from churn. | Chronic primitive contract churn for new requirements, or altering $P$ for an isolated caller rather than refining domain truth. |
| **Stream Purity Test** | Validates absence of primitive side-effects. | Inlining callbacks, hooks, events, or notifications inside $P$ instead of streaming state. |
| **DTO Purity Test** | Validates state inertia. | Attaching methods, mutating logic, or business rules to a DTO rather than in $P$ or $T$. |
| **Statelessness Test** | Validates encapsulation. | Using static classes or global mutable state instead of explicit composition roots. |
| **Local Transform Test** | Validates transform cohesion. | Dumping transforms into a monolithic helper junk drawer instead of beside the target contract. |
| **Teleological Test** | Validates consumer necessity. | Inventing a middleman or registry without an immediate caller needing it. |
| **Brevity/Barometer Test** | Validates line economy & directory hygiene. | Files crossing ~150 lines or boundary folders cluttered with miscellaneous non-Triad dumping grounds. |
| **Subtraction Test** | Validates $P$ irreducibility. | Capability still functions after removing $P$. |
| **Discovery Test** | Validates boundary cohesion. | Splitting one concept (e.g. registry vs. executor) into multiple fake interfaces. |
| **Policy Atomicity Test** | Validates strategy simplicity. | A policy internally juggling multiple sub-policies or hiding orchestration. |
| **Endomorphism Test** | Validates layer contract purity. | A layer that alters method signatures, leaks mechanics, or nests backwards. |
| **Redundancy Test** | Validates API economy. | Duplicate convenience overloads (e.g., `Add` vs `AddBatch`) or speculative DTO fields. |
