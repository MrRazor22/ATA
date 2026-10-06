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
   - **Step 1: Boundary Discovery:** Identify irreducible domain boundaries before designing contracts. Apply the Primitive vs. Collaborator test; resist converting existing classes or components directly into interfaces.
   - **Step 2: Core Primitive Contracts:** Define the sovereign contracts ($\le$ 4–5 methods, pure verbs).
   - **Step 3: Boundary Representations / State DTOs:** Define passive carriers with domain fidelity. Never choose representations merely to escape a dependency.
   - **Step 4: Injected Policies vs. Decorated Layers:** Apply the preceding primitive completeness test before classifying policies or layers.
   - **Step 5: Baseline Implementations & Substrate Encapsulation:** Encapsulate third-party runtimes and substrates strictly within implementations.
   - **Step 6: Orchestration & Emergent Symmetry:** Verify top-level orchestration loop purity (zero accumulators, natural symmetry).
   - **Step 7: Physical Topology:** Align namespace and directory trie 1:1 with discovered primitive boundaries.
3. **Auditing Existing Code:** Run user designs directly against the §10 Checklist. Identify false primitives, premature abstractions, substrate leaks, and local minimization traps.


# Primitive-First Design (PFD)
### Architectural Manifesto, Specification & Operational Principles

---

## 1. Core Philosophy & Empirical Heuristics
**Primitive-First Design (PFD)**—originally conceptualized as ATA (Zero-Smell Architecture)—asserts that **correct code is usually minimal code**. Minimality means the *minimum structural complexity required to express the domain cleanly*, not minimum characters or lines at any cost. Abstractions and boilerplate are usually patches over poorly conceived primitives; modeling foundational primitives correctly allows codebases to contract naturally to their minimal theoretical footprint with zero cosmetic code-golfing or god-class hacks.
* **~5k System Observation:** An end-to-end system hovers around **~5,000 LoC** without bloat.
* **1k–1.5k Core Engine Observation:** The bare-bones core engine (contracts, clean baseline implementations, sub-primitives) sits around **1,000–1,500 LoC max**. Exceeding this triggers boundary re-examination.
*(These are observational warning thresholds from practical experience, not design targets or dogmatic laws.)*
* **Global vs. Local Minimization:** PFD does not mean minimizing the immediate artifact locally (e.g., deleting a component, then patching the type signature with `Any`, then narrowing to a raw primitive type). PFD means **discovering the correct domain boundary first**, and then subtracting everything that existed solely because that boundary was wrong.

---

## 2. Boundary Discovery Before Abstraction
**Never begin by converting existing classes, files, or components into primitives or interfaces. First discover the irreducible responsibilities of the system.**

* **Primitive vs. Collaborator Diagnostic:** Do not infer a primitive from the existence of a class, file, reusable component, or multiple callers.
  * **Primitive:** An independent domain responsibility whose operation is meaningful as a boundary to its external callers.
  * **Collaborator:** An internal mechanism used to realize part of another primitive's execution. It must remain encapsulated inside the implementation, regardless of how substantial, reusable, or technically complex it is.
* **The Capability vs. Mechanism Test:**
  > **Ask:** If this component disappeared, would the surrounding system lose a distinct domain capability, or merely lose one implementation mechanism?
  * *Distinct domain capability* $\longrightarrow$ Candidate Primitive (deserves an independent contract).
  * *Implementation mechanism* $\longrightarrow$ Internal Collaborator (encapsulate inside the concrete implementation; do not create an interface).
* **Anti-Pattern (The False Primitive):** Never create an interface merely because a class exists, has multiple callers, could be mocked in unit tests, or seems conceptually reusable.

---

## 3. Primitives & Interface Contract Law
> *(Case Study: **[AgentCore](https://github.com/MrRazor22/AgentCore)**, the author's experimental agent framework, illustrates PFD principles throughout.)*
* **Contract as Boundary:** "Interface" means the abstract conceptual contract (C#/Java `interface`, Rust `trait`, Go `interface`, C++ abstract base concept). Every operational boundary is an interface; pure DTOs, transforms, and helpers are the only exceptions.
* **The Cognitive Forcing Mechanism:** Enforcing interface contracts across every boundary—even for single implementations—is a deliberate cognitive forcing mechanism. It forces upfront boundary design, preventing developers from lazily abusing concrete classes to leak internal state, expose convenience variables, or graft on quick hacks.
* **The Interface is the Truth:** Concrete implementations are never exposed across boundaries; zero backdoor access. Callers, policies, layers, and future extensions attach strictly through the contract.
* **The 80% Rule:** Finalizing core primitives correctly solves ~80% of the architecture; downstream implementation flows downhill.
* **Conceptual Boundary vs. Component:** A primitive is an irreducible boundary of responsibility, not an arbitrary OOP component.
  * *Car Analogy (5 Primitives):* *Engine*, *Body*, *Chassis*, *Cabin*, *Control Bus*. A piston, fuel injector, or spark plug is an internal collaborator; the Engine is the primitive boundary.
  * *AgentCore:* 3 core primitives—`ILlm` (intelligence), `IToolbox` (executable tools), `IContent` (operational context window).

---

## 4. Future-Proofing & Contract Scrutiny
**Future-proofing is the removal of unnecessary restrictions, not the addition of speculative capabilities.** A primitive must fit today perfectly while making tomorrow trivial without contract breakage.
* **The Three Future-Proofing Litmus Tests:**
  1. *Zero Speculative Bloat:* Is any method, parameter, or type present solely anticipating an unverified future need?
  2. *Zero Narrow Blindspots:* Does the contract overfit today's consumer, preventing obvious adjacent workflows?
  3. *Natural Expansion:* Can tomorrow's valid requirement fit cleanly without altering this contract?
* **The "Narrow Satisfaction Trap" (Memory vs. Context Case Study):** In AI agent frameworks, designers frequently overfit by creating `IMemory`, `IRagContext`, `IWorkingMemory`, and `ILongTermMemory`. But an agent engine fundamentally only requires an operational context window (`IContent`). RAG and memory retrieval are either injected policies or external layers feeding context. Splitting memory interfaces is an overfitting trap that creates rigid, redundant boundaries.
* **Contract Scrutiny in Practice (`IContent` Exclusions):**
  * *No `Clear()`:* Agents never clear their own memory; lifetime management belongs to higher session layers.
  * *No `UpdateTokenUsage()`:* Token usage arrives naturally on streaming event chunks (`IMessageEvent`), not via mutation side-channels.
  * *No Raw History Getters:* Operational boundaries perform actions; they are not passive data wrappers.
* **The 4–5 Method Heuristic:** Interfaces crossing 4–5 methods trigger immediate scrutiny for boundary sprawl.
* **Colocated Extensions ("Useful $\ne$ Fundamental"):** Core contracts define pure domain primitives. Convenience overloads and query helpers belong in scoped extension methods colocated with the primitive.
  * *The Fruit Rule:* A `Fruit` primitive defines `Taste()` and `Size()`. An `IsApple()` query is an extension method, not a contract method.
  * *Ban on Utility Grab-Bags:* Never create monolithic static dumping grounds (`CommonUtils`, `TransformUtils`). Keep helpers strictly colocated within the primitive's scope.
* **Universal Opinion vs. Coupling:** Contracts encode universal domain truths (e.g., streaming in `AgentCore`), while strictly excluding implementation-specific mechanics.

---

## 5. Substrate Encapsulation & Representation Integrity
When designing primitive contracts and representations, strictly decouple domain intent from execution substrate.

* **Substrate Encapsulation:**
  * When a primitive is implemented using an execution substrate—ML runtime, database engine, message broker, graphics API, OS handle, vendor SDK—the substrate's execution mechanics belong strictly to the implementation.
  * Do not expose substrate types (`torch.Tensor`, `DbContext`, `HttpClient`, OpenGL handles, vendor SDK types), execution contexts, lifecycle controls, or device placements across a primitive boundary unless the substrate itself is genuinely the domain boundary.
  * *Key Distinction:* Third-party dependency in implementation $\ne$ third-party execution mechanism leaked through primitive boundary.
* **Representation Integrity (Do Not Choose Representations Merely to Escape a Dependency):**
  * Boundary representations must express the actual structural domain requirement without prematurely specializing to one modality or storage format, and without artificially dumbing down types to raw primitives (e.g., escaping `torch.Tensor` by falling back to `List[int]` or `str`).
  * If removing a substrate dependency forces the contract into an artificially narrow representation, the abstraction was designed from the implementation outward rather than from the domain inward. Re-examine the boundary.
* **Escape Hatches are Evidence, Not Solutions:**
  * If a boundary requires `Any`, `object`, `dynamic`, unchecked casts, downcasts, or runtime type inspection to remain usable, stop and reconsider the boundary.
  * An escape hatch is diagnostic evidence that the abstraction is either exposing an unmodeled concept or attempting to paper over an incompatible substrate. Strict typing must be preserved system-wide.

---

## 6. Concrete Implementations & Recursive Policies
A concrete implementation represents an opinionated execution strategy. Baseline implementations must be clean and vanilla; their structure dictates downstream extensibility.
* **The ~150-Line Heuristic:** A cohesive implementation scope (colocated interface, implementation, extensions) should hover within **~150 LoC max**. Exceeding this warns of hidden god-objects or un-extracted policies.
* **The Anti-Gaming Law:**
  * *The File Fragmentation Trap:* Never dice a 150-line file into five 30-line files just to pass a line check. Keep cohesive units together. The ~150 LoC heuristic is a smoke detector for architectural sprawl, not a formatting mandate.
  * *No Cosmetic Cheats:* Never use `partial class`, unnatural subclassing, `ref`/`out`, or helper indirection to disguise line bloat.
* **Extracting Policies (When Opinions Warrant a Boundary):** Changeable implementation opinions—from complex algorithms to variable operating strategies—should be extracted as **Opinion Sub-Primitives (Policies)** *only when they warrant an architectural boundary*, rather than buried as magic constants or mechanically turned into premature abstractions for every configurable number. (e.g., an `Engine` injects `IFuelSystem` or a timing strategy when the mechanism is genuinely variable; simple thresholds can remain plain configuration). Classification is not a mandate to spawn an interface for every variable.
* **Recursive Hierarchy:** When an injected policy grows complex, it forms its own sovereign boundary: $\text{Core} \to \text{Policy} \to \text{Sub-Policy}$.

---

## 7. Taxonomy: Policies vs. Layers
**A Policy completes the primitive from within; a Layer extends a complete primitive from outside.**
* **The Preceding Diagnostic (Primitive Completeness):** Before mechanically classifying an abstraction as a Policy or Layer, always ask: **Is the foundational primitive itself poorly conceived or incomplete?**
  * *The Incomplete Primitive Smell:* A primitive on its own must be functionally sound. If the primitive cannot function meaningfully without the external concern, the concern may represent a missing internal responsibility rather than a Layer (e.g., an agent context that cannot function within finite limits unless an external layer rescues it). Fix the primitive's contract and internal policy first before inventing wrappers.
  * *Masquerading Bloat:* A missing fundamental responsibility often masquerades as an external abstraction, wrapper, or glue service.
* **The Power of Layers:** Wrapping a primitive with a decorator grants direct, non-invasive access to inspect, monitor, persist, or modify complete I/O flows (analogous to a mechanic connecting diagnostic leads directly to an engine, or ASP.NET Core middlewares).
* **Functional Completeness Test (Primary):** Once the primitive is sound, test external concerns: Can the primitive function without it?
  * **NO** $\to$ **Policy** (injected strategy completing the internal mechanism).
  * **YES** $\to$ **Layer** (external concern: logging, persistence, telemetry).
* **Case Study (Context Compactor vs. Persistence):**
  * *Context Compactor is a Policy:* An agent cannot function once its context window overflows. Compaction is fundamentally required to complete the primitive, though the strategy (sliding window vs. summarizer) varies. If compaction were an external layer, the core primitive would be incomplete and unable to function meaningfully on its own.
  * *Persistence is a Layer:* The agent functions completely in-memory without a database.
* **Shared Dependency Diagnostic:** If multiple layers require a specific capability, do not duplicate it across decorators; evaluate whether it represents a shared internal policy.
* **Higher-Layer Pragmatism:** Callbacks, events, delegates, hooks, factories, and switch-initializers are design smells in core primitives, but entirely legitimate conveniences at higher application layers (UI bindings, orchestration, plugin loaders).

---

## 8. DTOs & Boundary Diagnostics
* **Pure State Carriers:** DTOs hold data and zero business logic; they require no interface abstractions. Operational primitives are never data wrappers (`IContent` is an active boundary, not a `ChatHistory` wrapper). Transformations belong in external helpers.
* **DTO Impurity as a Boundary Diagnostic:** When data objects accumulate execution, assembly, or routing behavior, responsibilities were misplaced or a policy was misclassified.
* *AgentCore Evolution:* Stripping `Message` of delta-assembly and removing `IBlockEvent.Start()` (which acted as a hidden factory on an event DTO). Assembly belongs strictly to operational primitives (`Content`), keeping DTOs purely passive.

---

## 9. Architectural Purity & Emergent Symmetry
**Purity is the pressure to remove responsibilities that do not belong to a boundary until each boundary represents exactly what it fundamentally is:** *Universal truth $\to$ Primitive; Variable strategy $\to$ Policy; External concerns $\to$ Layer; Passive state $\to$ DTO.*
* **Symmetry as a Discovery Tool:** Symmetry is both evidence of correctness and an active tool for discovering boundaries. In early `AgentCore` drafts, LLMs streamed tokens while tools returned static DTOs, requiring an intermediate accumulator. Seeking symmetry prompted the insight: *tools stream too* (progress, intermediate notifications, long-running chunks). Both perform the identical role—streaming conversational context into `IContent`. Unifying both under `IMessageEvent` eliminated accumulators entirely.
* **Internal Purity (Conceptual ReAct Loop):** High-level orchestration mirrors the fundamental domain algorithm without accumulators or glue:
```csharp
// Conceptual PFD ReAct loop — simplified from AgentCore
while (content.NeedsExecution()) {
    for (event in llm.Generate(content))       content.Consume(event);
    for (event in toolbox.Execute(content))   content.Consume(event);
}
```
* **External Purity & Naming:** Foundational purity allows top-level coordinators (`Agent.cs`) to expose clean fluent builders (avoiding `app.Start()` god-classes). Mirror boundaries with parallel nouns: `llm` (`ILlm`), `content` (`IContent`), `toolbox` (`IToolbox`). `IToolbox` is a parallel noun, avoiding verb awkwardness like `ITooling` or `IToolExecutor`.

---

## 10. Physical Topology & Universal Scope
* **Structure Rules:** Flat is fine for small scopes (2–3 files; do not manufacture folders). Group correlated units into matching folders/namespaces. Disk directories naturally align 1:1 with project and namespace boundaries.
* **Topology Trie:** Directory trees mirror the system's primitive trie:
```text
/Context/
│   ├── IContext.cs                   <-- Primitive Contract
│   ├── Context.cs                    <-- Baseline Implementation (~150 LoC)
│   ├── /Compactor/                   <-- Policy Scope (ICompactorPolicy.cs, SlidingWindowCompactor.cs)
│   └── /Persistence/                 <-- Layer Scope (PersistenceContextLayer.cs)
```
* **Universal Scope (PFD Beyond Backend):**
  * *WPF / UI Architecture:* `UserControl: Form` is the Primitive (defines parameters, bounds, core actions); form data (Name, Email) is the DTO; input validation rules and styling templates are Policies; modal dialog wrappers and host page decorators are Layers.
  * *Documentation & Specifications:* Core thesis is the Primitive; methodologies and decision rules are Policies; illustrative examples and appendices are Layers.

---

## 11. The PFD Practitioner's Reference Checklist
| Focus Area | Diagnostic Question | Heuristic / Action |
| :--- | :--- | :--- |
| **Boundary Discovery** | Is this an independent domain capability or an implementation mechanism? | If component disappeared, does system lose capability or mechanism? Keep collaborator encapsulated. |
| **Existence** | Can type/method/helper/boundary be removed without loss? | Subtraction test: If yes, remove; if no, explain structural necessity. |
| **Cognitive Forcing**| Is concrete class exposed or leaking internals? | Hide concrete implementation; interact strictly through contract. |
| **Substrate Encapsulation**| Are runtime/substrate types (`Tensor`, `DbContext`, handles) leaking across the contract? | Encapsulate substrate in implementation. Keep contract domain-centric. |
| **Representation Integrity**| Did we dumb down types to escape a dependency, or use `Any`/`object`? | Stop. Do not choose narrow types merely to escape coupling. Preserve domain structural fidelity. |
| **Future-Proofing**| Is contract overfitted or carrying speculative guesses? | Pass the 3 tests: zero speculative bloat, zero narrow blindspots, natural expansion. |
| **Narrow Overfitting**| Inventing separate contracts for operational context subsets (e.g. Memory vs Context)? | Collapse into root operational primitive (`IContent`); extract sources into policies/layers. |
| **Purity & Symmetry**| Does orchestration require accumulators, adapters, or glue? | Boundary smell. Align streaming/contracts for natural symmetry (e.g. `IMessageEvent`). |
| **Contract Scrutiny**| Crossing 4–5 methods? Exposing lifecycle (`Clear`) or side-channels (`TokenUsage`)? | Scrutinize methods; stream metadata on events; delegate lifecycle to higher tiers. |
| **Extensions** | Are convenience helpers in core contract or in static grab-bags? | Colocate extension methods beside primitive ("Useful $\ne$ Fundamental"). Ban `CommonUtils`. |
| **Implementation** | Exceeding ~150 lines? Arbitrarily dicing files? | Extract policies *only when opinions warrant a boundary*. Obey anti-gaming laws. |
| **Taxonomy** | Is primitive incomplete on its own? Can it function without concern? | If primitive needs a layer to work $\to$ primitive smell. Otherwise: NO $\to$ Policy, YES $\to$ Layer. |
| **DTO Boundaries**| DTO holding logic, assembly, or hidden factories (`Start()`)? | Keep DTOs passive. Move delta assembly and orchestration to primitives. |
| **Topology** | Mismatch between disk and namespaces? Orphan root files? | Small scopes flat; align disk 1:1 to namespaces; mirror primitive trie. |