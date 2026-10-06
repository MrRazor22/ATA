---
name: primitive-first-design
description: >-
  Applies Primitive-First Design (PFD) to software architectures. Activate when commanded with
  "Apply PFD", designing systems, reviewing interface contracts, eliminating bloat/glue, or refactoring.
---

### Agent Operational Instructions
When this skill is active, you are a strict Primitive-First Design architect. Your primary directive is structural minimalism through boundary purity.
1. **Bias Toward Subtraction:** Resist adding classes, wrappers, or helper abstractions. If an abstraction can be eliminated by refining a core primitive, eliminate it.
2. **Execution Order for New Designs & Refactorings:**
   - **Step 1: Core Primitives:** Identify irreducible boundaries; define pure interface contracts ($\le$ 4–5 methods, pure verbs).
   - **Step 2: Pure DTOs:** Passive state carriers with zero behavior.
   - **Step 3: Opinion Sub-Primitives (Policies) vs. Decorated Layers:** Injected strategies vs. external wrapping decorators.
   - **Step 4: Orchestration & Natural Symmetry:** Check emergent symmetry across boundaries; zero accumulators or glue.
   - **Step 5: Physical Topology:** Clean folder and namespace trie mirroring primitive boundaries.
3. **Auditing Existing Code:** Run designs against the §10 Checklist. Identify misplaced responsibilities, overfitted contracts, and bloat.

# Primitive-First Design (PFD)
### Architectural Manifesto, Specification & Operational Principles

Primitive-First Design (PFD)—originally conceptualized as ATA—argues that **correct code is usually minimal**. Most abstractions are bloat created to patch a poor foundational primitive. If we design core primitives right in any system design, code naturally becomes minimal, code smells disappear, and the system becomes scalable, readable, maintainable, and simply better.

We judge PFD by number of code lines. While lines of code is not a perfect metric, it is the best proxy metric we have when looking at an entire system end-to-end. Crucially, PFD does **not** mean putting all code into a single class or writing convoluted one-liners to reduce line count. It is a set of principles and decisions to achieve minimal code with zero code smell—yielding high-signal, condensed, dense architecture.

**Empirical Observations (Heuristics, Not Dogma):**
* An average end-to-end system designed cleanly with PFD hovers around **~5,000 LoC** (if not overly complex or loaded with batteries).
* The bare-bones core project/namespace containing core primitive implementations and their opinion sub-primitives sits at **1,000–1,500 LoC max**. Exceeding this triggers a boundary re-examination.

---

## 1. Core Primitives & Interface Contract Law

*Interface* is a Java/C# term, but means traits in Rust, protocols in Python, or abstract contracts in Go/C++.
* **Everything is an Interface:** Every operational boundary must be an interface (except DTOs, transforms, and helpers). No concrete access across boundaries: **the interface is the only truth**. Zero backdoor access; contracts must always be respected.
* **The Cognitive Forcing Mechanism:** Enforcing interfaces forces upfront deliberate contract design, preventing developers from conveniently abusing concrete classes to expose ad-hoc variables or state.
* **Irreducible Boundaries, Not Mere OOP Components:** Model primitives based on real-world boundaries.
  * *Car Analogy (5 Core Primitives):* A car has 5 core primitives: *Engine* (gearbox, fuel tank), *Body* (lights, doors, storage), *Chassis* (wheels, steering), *Usable Area / Cabin* (seats, dashboard), and *Control Bus*. A piston or fuel injector is an internal component; the Engine is the primitive boundary. An entire car can be built end-to-end by composing these 5 clean contracts.
  * *AgentCore Grounding:* [AgentCore](https://github.com/MrRazor22/AgentCore) models the entire agent system with just 3 irreducible primitives: `ILlm` (intelligence), `IToolbox` (executable tools), and `IContent` (operational context window). Compare this to the massive abstraction bloat of Microsoft Agent Framework or LangChain.
* **The 80% Rule:** Getting the core primitive contracts right solves ~80% of the entire system architecture; implementation flows downhill naturally.

---

## 2. Boundary Discovery & Avoiding Narrow Overfitting

Model primitives based on consumer demand—who uses it and what they require. However, **never narrowly design an abstraction merely to satisfy the immediate task**. Look at what satisfies current needs while naturally supporting future expansion without contract breakage.
* **The "Narrow Satisfaction Trap" (Context vs. Memory Case Study):** In AI agents, frameworks create `IMemory`, `IRagContext`, `IWorkingMemory`, and `ILongTermMemory`. But fundamentally, an agent only requires an operational context window (`IContent`) to function. RAG and memory are either injected policies or external layers feeding context. Splitting memory interfaces is an overfitting trap. A simple `IContent` with memory/RAG as layers or policies remains minimal, zero-bloat, and neither overfits nor underfits.
* **The 3 Future-Proofing Litmus Tests:** A good primitive design ensures:
  1. It carries zero speculative bloat (nothing added solely anticipating an unverified future need).
  2. It has zero narrow blindspots (does not block obvious adjacent workflows).
  3. It expands naturally (current needs fit perfectly, and future requirements fit trivially without breaking the contract).
* **Future-Proof Through Purity:** An interface is future-proof not because it has generic catch-all parameters for tomorrow's guesses, but because it is so fundamentally unconstrained and pure that future requirements fit naturally without changing the contract.

---

## 3. Meticulous Contract Scrutiny & Universal Opinions

Every method on an interface must be meticulously interrogated: *Is it truly needed? Does it need this many parameters? Can the return type be simpler?*
* **Universal Opinions vs. Coupling:** A primitive should be generic, but you cannot have zero opinions. The opinions baked into a core contract must be **demonstrably universal** needs:
  * In `AgentCore`, `IContent` bakes in streaming context directly. Instead of returning narrow content events, it returns `IMessageEvent` across the board, supporting streaming from LLM to user without awkward retrofits.
  * Exclude non-universal mechanics: `IContent` deliberately excludes `Clear()` (agents never clear their own memory; session lifecycles belong at higher tiers), raw history getters (it is an active boundary, not a data holder), and `UpdateTokenUsage()` (token usage streams naturally on message events).
* **The 4–5 Method Heuristic:** If an interface crosses 4–5 methods, its boundaries are usually misjudged or doing too much.
* **Colocated Extension Methods ("Useful $\ne$ Fundamental"):** Primitives stay lean. Convenience queries belong in scoped extension methods colocated with the primitive, not in the core contract.
  * *The Fruit Rule:* A `Fruit` primitive defines `Taste()` and `Size()`. An `IsApple()` query is an extension method, not a contract method.
  * *Ban on Utility Grab-Bags:* Never create monolithic static dumping grounds (`CommonUtils`, `TransformUtils`). Scoped helpers stay with their respective primitive files.
* **Interface Properties:** Properties in interfaces are generally avoided because they cannot be layered cleanly, intercepted, or converted to async operations. Simple, obvious state exposure can be an exception, but action methods remain preferred.

---

## 4. Concrete Implementations, Opinion Sub-Primitives & Policies

The concrete implementation of a primitive is itself an opinion. It must remain decoupled, vanilla, and adhere to universal design:
* **The ~150-Line Heuristic (Anti-Bloat Smoke Detector):** If a concrete implementation exceeds **~150 lines**, it is usually a code smell: it is doing more than it should and harboring hardcoded opinions.
  * Extract complex opinions, strategies, and variable numbers into injected **Opinion Sub-Primitives (Policies)**. (e.g., an `Engine` primitive may be 1,000 lines if implemented monolithically, but extracting `IFuelSystem` and ignition timing as injected policies keeps the core engine lean and readable like plain English).
  * *Cohesive File Scope:* If an interface has one primary implementation, keeping the interface, implementation, and extension methods together in one file within ~150 lines is preferred for maintainability.
* **Anti-Gaming Laws (Strictly Banned):**
  * Never dice one 150-line file into five 30-line files to game the line count. Keep cohesive boundaries together.
  * Never use `partial class`, unnatural subclassing, `ref`/`out`, or language quirks to hide line bloat.
* **Recursive Hierarchy:** When an injected policy grows complex, it forms its own sovereign boundary: $\text{Core Primitive} \to \text{Opinion Sub-Primitive} \to \text{Sub-Policy}$.

---

## 5. Layers & Middlewares (Decorated Co-Primitives)

While Policies are injected *inside* core primitives to decouple internal strategies, **Layers** decorate primitives from the *outside* to intercept, observe, modify, or control end-to-end I/O flow.
* **The Power of Layers:** Wrapping a primitive with a decorator grants direct access to inspect, monitor, persist, or modify flows (analogous to connecting diagnostic leads directly to an engine, or ASP.NET Core middlewares, without middleware delegate bloat).
  * An `Engine` primitive can have a sensor layer monitoring telemetry, or a tuning layer adjusting performance, without altering the core engine.
* **Preceding Diagnostic (Primitive Completeness):** A core primitive must be functionally sound on its own. If you need a layer to make a primitive functional, that is a design smell indicating a missing internal responsibility or policy.
* **Functional Completeness Test:** Once the primitive is sound:
  * **NO** (primitive cannot function without it) $\to$ **Policy** (injected opinion sub-primitive, e.g., context compaction in `AgentCore`).
  * **YES** (primitive functions completely in-memory without it) $\to$ **Layer** (external concern, e.g., persistence, logging, telemetry).
* **Shared Dependency Rule:** If multiple layers require a capability, evaluate whether it is a shared internal policy rather than duplicating it across decorators.
* **Higher-Layer Pragmatism:** Callbacks, events, delegates, hooks, factories, and switch-case initializers are design smells in core primitives, but legitimate conveniences at higher application layers (UI bindings, orchestration, plugin loaders).
* **Strict Typing:** Always use strictly typed contracts; avoid `object`, `dynamic`, or unchecked casting escape hatches.

---

## 6. Passive State DTOs

* **Pure State Carriers:** DTOs hold data and zero business logic. They do not earn interfaces, and primitives are never passive data wrappers (`IContent` is an active operational boundary, not a `ChatHistory` wrapper).
* **DTO Impurity as a Smell Indicator:** When DTOs accumulate assembly, execution, or routing logic, boundaries were misplaced:
  * In `AgentCore`, stripping `Message` of delta-assembly logic and removing `IBlockEvent.Start()` (a hidden factory on a DTO) restored purity. Delta assembly belongs strictly in operational primitives, keeping DTOs passive. Pure transforms (`ToString()`) remain extension helpers.

---

## 7. Natural Symmetry, Orchestrator Purity & Naming

When core primitives are modeled correctly, a natural symmetry emerges across the system:
* **Symmetry as a Discovery Tool:** In `AgentCore`, LLMs streamed tokens while tools originally returned static DTOs, requiring intermediate accumulators. Seeking architectural symmetry prompted the realization: *tools stream too* (progress updates, long-running chunks). Both LLMs and tools stream context into `IContent` via `IMessageEvent`. Unifying them under streaming symmetry eliminated accumulators entirely.
* **Internal Loop Purity:** Top-level orchestration should mirror the fundamental domain algorithm without glue, adapters, or accumulators:
```csharp
// Conceptual PFD ReAct loop — simplified from AgentCore
while (content.NeedsExecution()) {
    for (event in llm.Generate(content))       content.Consume(event);
    for (event in toolbox.Execute(content))   content.Consume(event);
}
```
* **External Orchestrator Purity & Naming:** High-level coordinators (`Agent.cs`) expose clean fluent builders, avoiding lazy `app.Start()` god-classes. Mirror boundaries with parallel nouns: `llm` (`ILlm`), `content` (`IContent`), `toolbox` (`IToolbox`). `IToolbox` is a parallel noun, avoiding awkward verbs like `ITooling` or `IToolExecutor`.
* **The PFD Grand Unified Symmetry:**
  - **Policy** is a Primitive on the *inside*.
  - **Layer** is the same Primitive on the *outside*.
  - **DTOs and transforms** are the passive binders that hold them together.

---

## 8. Physical Topology (Folders & Namespaces)

Folder and namespace hierarchies must directly reflect the system's primitive boundaries:
* **Flat vs. Scoped:** 2–3 files can remain flat in a single folder. When files grow, group correlated units into explicit namespace/folder boundaries.
* **1:1 Alignment:** Disk folders, namespaces, and project boundaries must match 1:1. Zero orphan root files under any boundary (solution, project, or directory).
* **The System Trie Test:** The directory structure should match the trie you would draw of the system's primitives end-to-end. In `AgentCore`, 3 clean folders mirror the 3 core primitives (`Llm`, `Content`, `Toolbox`), keeping the entire design walkthrough visible at a glance.

---

## 9. Universal Scope (Beyond Backend Code)

PFD applies to all creative work—backend systems, UI, specifications, and documentation:
* **UI Architecture (WPF / Forms / Web):** A Form UserControl is the Primitive (defines parameters, bounds, core actions); form data (Name, Email) is the DTO; input validation rules and styling templates are Policies (injected opinions); host page wrappers, modal decorators, and container templates are Layers.
* **Documentation & Technical Writing:** Core thesis is the Primitive; decision frameworks and rules are Policies; illustrative examples, appendixes, and case studies are Layers.

---

## 10. The PFD Practitioner's Reference Checklist

| Focus Area | Diagnostic Question | Heuristic / Action |
| :--- | :--- | :--- |
| **Existence** | Can this type, method, helper, or boundary be removed without loss? | Subtraction Test: If yes, remove; if no, justify structural necessity. |
| **Cognitive Forcing** | Is a concrete class exposed or leaking internal state? | Hide concrete implementation; interact strictly through contract interface. |
| **Boundary Sovereignty** | Is this an irreducible boundary or an internal component (piston vs. engine)? | Core primitives represent system pillars; internal components stay concrete or become policies. |
| **Future-Proofing** | Is the contract overfitted to current needs or carrying speculative guesses? | Pass the 3 tests: zero speculative bloat, zero narrow blindspots, natural expansion. |
| **Contract Scrutiny** | Crossing 4–5 methods? Exposing lifecycle (`Clear`) or mutation side-channels? | Scrutinize methods; stream metadata on events; delegate lifecycle to higher tiers. |
| **Extensions** | Are convenience helpers in core contract or in static grab-bags? | Colocate extension methods beside primitive ("Useful $\ne$ Fundamental"). Ban `CommonUtils`. |
| **Implementation Scope**| Exceeding ~150 lines? Arbitrarily dicing files into fragments? | Extract opinions into policies *only when they warrant a boundary*. Obey anti-gaming laws. |
| **Policy vs. Layer** | Can primitive function without the concern? Is it needed by other layers? | Incomplete primitive $\to$ missing responsibility. Otherwise: NO $\to$ Policy, YES $\to$ Layer. |
| **DTO Boundaries** | DTO holding logic, assembly, or hidden factories (`Start()`)? | Keep DTOs passive. Move delta assembly and orchestration to primitives. |
| **Purity & Symmetry** | Does orchestration require accumulators, adapters, or glue? | Boundary smell. Align contracts for natural symmetry (e.g. streaming `IMessageEvent`). |
| **Naming & Nouns** | Are parallel boundaries named consistently? | Use symmetrical parallel nouns (`llm`, `content`, `toolbox`). Avoid awkward verbs. |
| **Topology** | Mismatch between disk and namespaces? Orphan root files? | Flat for small scopes; align disk 1:1 to namespaces; mirror primitive trie. |