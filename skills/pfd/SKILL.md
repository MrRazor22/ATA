---
name: primitive-first-design
description: >-
  Applies Primitive-First Design (PFD) to software architectures. Activate when commanded with
  "Apply PFD", designing systems, reviewing interface contracts, eliminating bloat/glue, or refactoring.
---

### Agent Operational Instructions
When this skill is active, you are a strict Primitive-First Design architect. Your primary directive is structural minimalism through boundary purity.
1. **Bias Toward Subtraction:** Resist adding classes, wrappers, or helper abstractions. If an abstraction can be eliminated by refining a core primitive, eliminate it.
2. **Execution Order for New Designs:** 
   - Step 1: Core Primitives (Contracts only, $\le$ 4–5 methods).
   - Step 2: Pure DTOs (Zero behavior).
   - Step 3: Injected Policies vs. Decorated Layers.
   - Step 4: Illustrative Orchestration Loop (Check for emergent symmetry; zero accumulators).
   - Step 5: Directory & Namespace Topology.
3. **Auditing Existing Code:** Run user designs directly against the §9 Checklist. Identify misplaced responsibilities, overfitted contracts, and bloat.


# Primitive-First Design (PFD)
### Architectural Manifesto, Specification & Operational Principles

---

## 1. Core Philosophy & Empirical Heuristics
**Primitive-First Design (PFD)**—originally conceptualized as ATA (Zero-Smell Architecture)—asserts that **correct code is usually minimal code**. Minimality means the *minimum structural complexity required to express the domain cleanly*, not minimum characters or lines at any cost. Abstractions and boilerplate are usually patches over poorly conceived primitives; modeling foundational primitives correctly allows codebases to contract naturally to their minimal theoretical footprint with zero cosmetic code-golfing or god-class hacks.
* **~5k System Observation:** An end-to-end system hovers around **~5,000 LoC** without bloat.
* **1k–1.5k Core Engine Observation:** The bare-bones core engine (contracts, clean baseline implementations, sub-primitives) sits around **1,000–1,500 LoC max**. Exceeding this triggers boundary re-examination.
*(These are observational warning thresholds from practical experience, not design targets or dogmatic laws.)*

---

## 2. Primitives & Interface Contract Law
> *(Case Study: **[AgentCore](https://github.com/MrRazor22/AgentCore)**, the author's experimental agent framework, illustrates PFD principles throughout.)*
* **Contract as Boundary:** "Interface" means the abstract conceptual contract (C#/Java `interface`, Rust `trait`, Go `interface`, C++ abstract base concept). Every operational boundary is an interface; pure DTOs, transforms, and helpers are the only exceptions.
* **The Cognitive Forcing Mechanism:** Enforcing interface contracts across every boundary—even for single implementations—is a deliberate cognitive forcing mechanism. It forces upfront boundary design, preventing developers from lazily abusing concrete classes to leak internal state, expose convenience variables, or graft on quick hacks.
* **The Interface is the Truth:** Concrete implementations are never exposed across boundaries; zero backdoor access. Callers, policies, layers, and future extensions attach strictly through the contract.
* **The 80% Rule:** Finalizing core primitives correctly solves ~80% of the architecture; downstream implementation flows downhill.
* **Conceptual Boundary vs. Component:** A primitive is an irreducible boundary of responsibility, not an arbitrary OOP component.
  * *Car Analogy (5 Primitives):* *Engine*, *Body*, *Chassis*, *Cabin*, *Control Bus*. A piston or fuel injector is an internal component; the Engine is the primitive boundary.
  * *AgentCore:* 3 core primitives—`ILlm` (intelligence), `IToolbox` (executable tools), `IContent` (operational context window).

---

## 3. Future-Proofing & Contract Scrutiny
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
* **Properties & Strict Typing:** Avoid interface properties unless representing simple, obvious, synchronous state where methods add needless noise. Enforce strict typing system-wide; never use `object`/`dynamic` escape hatches.
* **Universal Opinion vs. Coupling:** Contracts encode universal domain truths (e.g., streaming in `AgentCore`), while strictly excluding implementation-specific mechanics.

---

## 4. Concrete Implementations & Recursive Policies
A concrete implementation represents an opinionated execution strategy. Baseline implementations must be clean and vanilla; their structure dictates downstream extensibility.
* **The ~150-Line Heuristic:** A cohesive implementation scope (colocated interface, implementation, extensions) should hover within **~150 LoC max**. Exceeding this warns of hidden god-objects or un-extracted policies.
* **The Anti-Gaming Law:**
  * *The File Fragmentation Trap:* Never dice a 150-line file into five 30-line files just to pass a line check. Keep cohesive units together. The ~150 LoC heuristic is a smoke detector for architectural sprawl, not a formatting mandate.
  * *No Cosmetic Cheats:* Never use `partial class`, unnatural subclassing, `ref`/`out`, or helper indirection to disguise line bloat.
* **Extracting Policies (Algorithms to Meaningful Values):** Changeable implementation opinions—from complex algorithms down to meaningful thresholds and operating limits—must be extracted as **Opinion Sub-Primitives (Policies)** rather than buried as magic constants (e.g., an `Engine` implementation injects `IFuelSystem`, timing schemes, and operating thresholds).
* **Recursive Hierarchy:** When an injected policy grows complex, it forms its own sovereign boundary: $\text{Core} \to \text{Policy} \to \text{Sub-Policy}$.

---

## 5. Taxonomy: Policies vs. Layers
**A Policy completes the primitive from within; a Layer extends a complete primitive from outside.**
* **The Power of Layers:** Wrapping a primitive with a decorator grants direct, non-invasive access to inspect, monitor, persist, or modify complete I/O flows (analogous to a mechanic connecting diagnostic leads directly to an engine, or ASP.NET Core middlewares).
* **Functional Completeness Test (Primary):** Can the primitive function without it?
  * **NO** $\to$ **Policy** (injected strategy).
  * **YES** $\to$ **Layer** (external concern: logging, persistence, telemetry).
* **Case Study (Context Compactor vs. Persistence):**
  * *Context Compactor is a Policy:* An agent cannot function once its context window overflows. Compaction is functionally required to complete the primitive, though the strategy (sliding window vs. summarizer) varies.
  * *Persistence is a Layer:* The agent functions completely in-memory without a database.
* **Shared Dependency Diagnostic:** If multiple layers require a specific capability, do not duplicate it across decorators; evaluate whether it represents a shared internal policy.
* **Higher-Layer Pragmatism:** Callbacks, events, delegates, hooks, factories, and switch-initializers are design smells in core primitives, but entirely legitimate conveniences at higher application layers (UI bindings, orchestration, plugin loaders).

---

## 6. DTOs & Boundary Diagnostics
* **Pure State Carriers:** DTOs hold data and zero business logic; they require no interface abstractions. Operational primitives are never data wrappers (`IContent` is an active boundary, not a `ChatHistory` wrapper). Transformations belong in external helpers.
* **DTO Impurity as a Boundary Diagnostic:** When data objects accumulate execution, assembly, or routing behavior, responsibilities were misplaced or a policy was misclassified.
* *AgentCore Evolution:* Stripping `Message` of delta-assembly and removing `IBlockEvent.Start()` (which acted as a hidden factory on an event DTO). Assembly belongs strictly to operational primitives (`Content`), keeping DTOs purely passive.

---

## 7. Architectural Purity & Emergent Symmetry
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

## 8. Physical Topology & Universal Scope
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

## 9. The PFD Practitioner's Reference Checklist
| Focus Area | Diagnostic Question | Heuristic / Action |
| :--- | :--- | :--- |
| **Existence** | Can type/method/helper/boundary be removed without loss? | Subtraction test: If yes, remove; if no, explain structural necessity. |
| **Cognitive Forcing**| Is concrete class exposed or leaking internals? | Hide concrete implementation; interact strictly through contract. |
| **Future-Proofing**| Is contract overfitted or carrying speculative guesses? | Pass the 3 tests: zero speculative bloat, zero narrow blindspots, natural expansion. |
| **Narrow Overfitting**| Inventing separate contracts for operational context subsets (e.g. Memory vs Context)? | Collapse into root operational primitive (`IContent`); extract sources into policies/layers. |
| **Purity & Symmetry**| Does orchestration require accumulators, adapters, or glue? | Boundary smell. Align streaming/contracts for natural symmetry (e.g. `IMessageEvent`). |
| **Contract Scrutiny**| Crossing 4–5 methods? Exposing lifecycle (`Clear`) or side-channels (`TokenUsage`)? | Scrutinize methods; stream metadata on events; delegate lifecycle to higher tiers. |
| **Extensions** | Are convenience helpers in core contract or in static grab-bags? | Colocate extension methods beside primitive ("Useful $\ne$ Fundamental"). Ban `CommonUtils`. |
| **Properties/Types**| Exposing mutable properties? Escaping via `object`/`dynamic`? | Prefer methods unless simple synchronous state. Enforce strict typing. |
| **Implementation** | Exceeding ~150 lines? Arbitrarily dicing files? | Extract policies (algorithms down to thresholds). Obey anti-gaming laws. |
| **Taxonomy** | Can primitive work without it? Shared across contexts? | NO $\to$ Policy (injected). YES $\to$ Layer. If shared across layers, check if internal policy. |
| **DTO Boundaries**| DTO holding logic, assembly, or hidden factories (`Start()`)? | Keep DTOs passive. Move delta assembly and orchestration to primitives. |
| **Topology** | Mismatch between disk and namespaces? Orphan root files? | Small scopes flat; align disk 1:1 to namespaces; mirror primitive trie. |