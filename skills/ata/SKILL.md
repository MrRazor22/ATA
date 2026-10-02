---
name: ata
description: >-
  The Axiomatic Triad Architecture (ATA) skill and specification. Activate when designing software,
  auditing systems for bloat, refactoring complex codebases, or executing the "Apply ATA" directive.
---

# Axiomatic Triad Architecture (ATA)
## The Theory of Primitives & Representation Reduction

---

## 1. The Core Idea

> **"Correct design will always be minimal. Minimal code is not code golf; it is the natural, inevitable side-effect of truth in representation. When a bedrock primitive accurately reflects reality, unnecessary abstractions evaporate; what remains is a complete, minimal basis where every capability is expressed through composition, orthogonal policy, and contract-preserving layers."**

* **Zero Code Smell is the Only Goal:** ATA is not code golf. We do not shrink code or count lines just to be clever. The goal is zero code smell. When you model the domain truthfully, bloat has nowhere to hide, and the code naturally becomes small.
* **Plain Language Everywhere:** ATA eliminates bloat in code, architecture, and language. Speak and write in plain, simple English. Fancy jargon and inflated abstractions are just bloat that hides lazy thinking.
* **The Diagnostic Warning Light (~150 Lines):** Line count is a symptom, not a hard rule or quota. When code is clean, it naturally stays small. If a file grows past ~150 lines, do not celebrate its thoroughness—use it as a warning light on the dashboard: Did you inline policies? Did you tangle flow? Did you bundle multiple responsibilities together?
* **The Subtraction Rule:** Never introduce a type, file, parameter, or helper unless the system breaks without it. If you can delete something and the capability still works, it was bloat. Throw it away.
* **Reject the Append-Only Trap:** When requirements change, never take the easy route of slapping on convenience wrapper classes, adapter shims, or boolean flags. Every character must earn its existence. Always diagnose the flaw in the contract and fix it directly in place.
* **Caller Demand:** "Who is actually using it?" Every boundary begins and ends here. Never build speculative abstractions or middleman services for callers that do not exist yet. If an active caller does not demand it right now, it does not exist.

---

## 2. Interface Sovereignty (Everything is an Interface)

In ATA, everything callers touch is an interface. The concrete implementation is completely invisible.

* **Every Object is an Interface:** Callers interact strictly through contracts (interfaces, protocols, traits), never concrete classes. The only concrete classes that exist are pure data containers (DTOs) that carry zero behavior.
* **Actions, Not Internals:** An interface defines what action the capability performs for the caller. It must never expose stored variables, configuration settings, or internal machinery (memory management, device placement, hardware details, or framework plumbing).
* **Recursive Scrutiny:** Every method on an interface must earn its place. Every parameter must be inspected deeply: if a parameter is a complex object, recursively inspect its methods, parameters, and return types. The return type must be scrutinized with the same rigor.
* **Self-Contained Contracts:** The contract captures the domain concept in its purest form, free from the implementation's own dependencies. Reading the contract alone tells you exactly what the capability does, with zero knowledge of how any class implements it.
* **Zero Backdoors:** Bypassing the interface to access the concrete class directly is unconditionally forbidden. Callers, policies, layers, and future extensions attach strictly through the contract. Interface purity is what fundamentally solves all code smells; less code is merely the side-effect.

---

## 3. The Operational Triad (The LEGO System)

Every operational boundary encapsulates **exactly one root primitive** ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$). 

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

The three members form a self-reinforcing system: each exists to complement and enable the other two.

### 1. The Root Primitive ($P$): Bedrock Domain Mechanism
* **The Irreducible Bedrock:** Defines strictly *what* the capability is. Contains only universal, unopinionated operations that never change across callers.
* **Pure Output Streams:** Primitives yield their results naturally through their return values or streams. Never inline callbacks, event listeners, lifecycle hooks, or notification handlers inside a root primitive.
* **Zero Static Classes or Global State:** Never hide dependencies in static helper classes or global mutable state. Pass dependencies cleanly into the constructor at the boundary root.
* **Direct Policy Consumption:** When multiple policies share an interface, the primitive directly accepts the policy it needs. Never invent fake middleman services or switch-case registries.

### 2. The Injected Policy ($\pi$): Sub-Primitive Extraction
* **A Policy IS a Primitive:** Policies are primitives extracted from inside another primitive ($P_{\pi} \to P$). Every interface rule, recursive scrutiny, and discipline that applies to root primitives applies identically to policies.
* **Why Policies Exist:** If a primitive handles its own variations and heuristics internally, it inevitably blows up into a god class. More importantly, **it kills layers**: if the primitive hardcodes its internal rules, you cannot control or decorate it without replacing the entire primitive. Extracting sub-primitives as injected interfaces keeps the parent lean and unlocks the full power of layers.
* **Policy Atomicity:** A policy must remain atomic. If a policy begins needing subordinate policies of its own, it has matured into its own autonomous child primitive managing a sub-boundary.

### 3. The Composable Layer ($\lambda: P \to P$): LEGO-Like Extension
* **Same Interface, Total Control:** A layer decorates the exact same contract ($P \to P$). Because it uses the exact same interface, you literally control the input and output of every method the capability exposes—giving you the power of middleware without framework bloat. The primitive has zero awareness of its decorators.
* **LEGO Composition:** The core primitive stays pure and general. Layers from different sources add different flavors—like snapping on LEGO blocks. Caching, retries, rate limits, telemetry, scaling, and cross-cutting controls all snap on externally without touching the primitive's code.
* **Forward Pipeline Order:** Layers are composed around $P$ in forward execution order using pure transform functions ($T$) rather than nesting constructors inside-out.

---

## 4. State ($S$) & Transforms ($T$): Pure Data and Pure Math

Every line of code belongs to one of four categories in the **Code Completeness Quad**:
1. **Behavior:** The contracts and implementations ($P, \pi, \lambda$).
2. **State ($S$):** Pure immutable data containers (DTOs) with zero methods and zero business logic.
3. **Transforms ($T$):** Pure, stateless functions ($f: S_1 \to S_2$) for calculations, formatting, data mappings, and forward layer composition.
4. **Wiring:** Zero-logic composition roots that instantiate objects and wire dependencies at application startup.

* **DTOs Carry Zero Behavior:** State is strictly inert data. If a DTO has methods, mutating logic, or calculations, it is a code smell. Put operations in $P$ or in pure transforms $T$.
* **Zero Method Redundancy:** Eliminate duplicate convenience overloads (like `Add` vs `AddBatch`). Use universal collection or span types so single items and batches flow through the exact same minimal signature.
* **Keep Transforms Beside the Type:** Pure transforms and state DTOs belong in the exact same file as the contract they support, keeping related definitions together and preventing dumping grounds.

---

## 5. Natural Directory Structure & Fractal Boundaries

File organization should follow natural engineering, not framework rituals:
* **Start Flat Inside Boundaries:** Keep the contract, derivations, DTOs, and transforms in the same boundary folder. Name strategies naturally (`SqliteSource`, `CosineSimilarity`) and use clean hints for decorators (`RetryLayer`, `CachingLayer`). Only split into subfolders when files genuinely multiply.
* **Boundary Cleanliness:** A boundary folder holds strictly its Triad members ($P, \pi, \lambda, S, T$) and nested child boundaries—never miscellaneous "junk drawer" files.
* **Fractal Promotion:** When an extracted policy grows rich and complex—requiring its own sub-policies or layers—it naturally promotes into its own child boundary folder nested directly inside the parent:
  ```text
  evaluator/
    evaluator_boundary       # Primary bedrock primitive
    heuristics/              # Promoted policy boundary
      heuristic_primitive
      threshold_policy
  ```
* **Shared Dependencies Live as Siblings:** If a primitive is used by multiple peer primitives, place it at their shared sibling level. Never bury a shared dependency deep inside one consumer.

---

## 6. How to Build & Refactor (Outside-In)

When designing or refactoring code, follow this sequence:
1. **Design Outside-In from the Caller:** Start with what the caller actually needs. Never mechanically "extract an interface" by copy-pasting an existing class's method signatures and internal types. The contract is the sovereign domain definition; the concrete class conforms to it.
2. **Isolate the Bedrock Primitive ($P$):** Find the core capability and lock its interface. Scrutinize every method, parameter, and return type.
3. **Extract Policies ($\pi$):** Pull out internal heuristics, algorithms, and varying rules into injected sub-primitive interfaces.
4. **Decorate with Layers ($\lambda$):** Move cross-cutting flow (retries, caching, logging, metrics) into layers wrapping the exact same contract.
5. **Clean Data & Transforms ($S, T$):** Strip behavior from DTOs and make transforms pure stateless functions.
6. **Delete the Bloat:** Purge dead code, unused flags, and backward-compatibility wrappers. If removing something doesn't break the system, delete it.

---

## 7. The Conformance Checklist

When auditing code, verify against these direct questions:

| Test | What to Verify | Red Flag / Smell |
| :--- | :--- | :--- |
| **Interface Sovereignty** | Every caller interacts through an interface; zero access to concrete classes. | Callers depending on concrete classes, or any backdoor bypassing the contract. |
| **Actions, Not Internals** | Interface defines actions for callers only; zero variables, settings, or internal plumbing. | Exposing config fields, state variables, hardware details, or framework mechanics on the contract. |
| **Recursive Scrutiny** | Every method, parameter, and return type is deeply verified for clean abstraction. | Leaking complex internal types or unscrutinized objects across the boundary. |
| **Sub-Primitive Extraction** | Volatile rules and strategies are extracted as injected policies ($\pi$). | A primitive hardcoding its own variations, becoming a god class, or blocking layers. |
| **Layer Homomorphism** | Layers decorate the exact same interface ($P \to P$) to control flow like LEGO bricks. | A layer that changes method signatures, leaks mechanics, or cannot be freely composed. |
| **State Purity** | State ($S$) consists of pure inert DTOs with zero methods or mutating behavior. | DTOs containing business logic, calculations, or helper methods. |
| **Transform Purity** | Transforms ($T$) are pure, stateless functions ($f: S_1 \to S_2$). | Transforms that hide state, hold references, or smuggle domain logic outside $P$ and $\pi$. |
| **Subtraction Test** | Every file, type, method, and parameter is strictly necessary. | Removing a component leaves the capability intact (meaning it was unnecessary bloat). |
| **Dashboard Warning Light** | Files that grow large (~150 lines) are diagnosed for bundled responsibilities. | Ignoring long files that bundle multiple policies or hardcode flow. |
| **Append-Only Trap** | New requirements refine the contract in place rather than adding wrapper band-aids. | Adding convenience wrapper classes, adapter shims, or boolean flags to avoid contract work. |
