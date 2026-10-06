---
name: primitive-first-design
description: Use when designing software architectures, reviewing interface contracts, eliminating boilerplate/glue abstractions, or refactoring codebases for minimalism. Applies Primitive-First Design (PFD) to separate Primitives, Policies, Layers, and DTOs.
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

## 2. Primitives & Interface Contract Law
> *(Case Study: **AgentCore**, the author's experimental agent framework, illustrates PFD principles throughout.)*
* **Contract as Boundary:** "Interface" means the abstract conceptual contract (C#/Java `interface`, Rust `trait`, Go `interface`, C++ abstract base concept). Every operational boundary is an interface; pure DTOs, transforms, and helpers are the only exceptions.
* **The Interface is the Truth:** Concrete implementations are never exposed across boundaries; zero backdoor access. The constraint is a deliberate cognitive forcing mechanism to mandate upfront contract design over implementation convenience.
* **The 80% Rule:** Finalizing core primitives correctly solves ~80% of the architecture; downstream implementation flows downhill.
* **Conceptual Boundary vs. Component:** A primitive is an irreducible boundary of responsibility, not an arbitrary OOP component.
  * *Illustrative Car Analogy:* 5 primitives—*Engine*, *Body*, *Chassis*, *Cabin*, *Control Bus*. A piston is an internal component; the Engine is the primitive. (Do not confuse physical components with architectural boundaries).
  * *AgentCore:* 3 core primitives—`ILlm` (intelligence), `IToolbox` (executable tools), `IContent` (operational context window).

## 3. Future-Proofing & Contract Scrutiny
**Future-proofing is the removal of unnecessary restrictions, not the addition of speculative capabilities.** A primitive must simultaneously contain zero speculative bloat, contain zero narrow blindspots, and fit today perfectly while making tomorrow trivial.
* **Discovery in Novel Domains:** Trace what consumers fundamentally require. When intuition fails, use analogous systems as orienting hints.
* **The Narrow Satisfaction Trap & Anti-Append Discipline:** Avoid overfitting (e.g., creating `IMemory`/`IRagContext` when the universal need is just `IContent`). Before appending methods, ask: *Can the existing primitive express this by improving its fundamental shape?* (e.g., `IContent.WriteAsync()` returns `IMessageEvent` rather than a narrow UI-only `IContentEvent`).
* **The 4–5 Method Heuristic:** Interfaces crossing 4–5 methods trigger scrutiny for boundary sprawl.
* **Colocated Extensions:** Convenience overloads and transforms belong in scoped extension methods colocated with the primitive ("useful != fundamental"), never in core contracts or giant static `CommonUtils` grab-bags.
* **Properties & Strict Typing:** Avoid interface properties unless representing simple, obvious, synchronous state where methods add needless noise. Enforce strict typing system-wide; never use `object`/`dynamic` escape hatches to bypass boundary problems.
* **Universal Opinion vs. Coupling:** Purity is not opinionlessness. Contracts encode universal domain truths (e.g., streaming in `AgentCore`), while excluding non-intrinsic lifecycle operations (e.g., no `IContent.Clear()` or `UpdateTokenUsage()`).

## 4. Concrete Implementations & Recursive Policies
A concrete implementation represents an opinionated execution strategy. Baseline implementations must be clean and relatively vanilla; their structure dictates extensibility. Do not pair a pure interface with a heavily coupled implementation that requires layers to undo.
* **The ~150-Line Heuristic:** A cohesive implementation scope (colocated interface, implementation, extensions) should stay within **~150 LoC max**. Exceeding this warns of hidden god-objects or un-extracted policies.
* **Anti-Gaming Law:** Never alter code shape (`partial class`, file fragmentation, `ref`/`out`, deep subclassing, helper indirection) to conceal architectural line sprawl. Keep cohesive units together.
* **Extracting Policies (Algorithms to Meaningful Values):** Changeable implementation opinions—from complex algorithms to meaningful thresholds and configurations—should be extracted as **Opinion Sub-Primitives (Policies)** when they warrant a boundary, rather than buried as magic constants (e.g., `Engine` injects `IFuelSystem`, timing, or operating thresholds).
* **Recursive Hierarchy:** When an injected policy grows complex, it forms its own boundary: $\text{Core} \to \text{Policy} \to \text{Sub-Policy}$.

## 5. Taxonomy: Policies vs. Layers
**A Policy completes the primitive from within; a Layer extends a complete primitive from outside.**
* **The Power of Layers:** Wrapping a primitive with a decorator gives direct access to inspect, monitor, persist, or modify complete I/O flows without altering internal mechanics (like a mechanic attaching diagnostic leads directly to an engine).
* **Functional Completeness Test (Primary):** Can the primitive function without it? **NO** $\to$ **Policy** (injected strategy); **YES** $\to$ **Layer** (external concern: logging, persistence, telemetry).
* **Shared Dependency Diagnostic:** If several layers require a capability, do not duplicate it blindly; evaluate if it is a shared internal policy.
* *AgentCore Case Study:* Context-window management is an injected **Policy** (the primitive must stay within finite limits, though compaction/truncation strategies vary). Persistence is a **Layer** (the agent functions in-memory without a database).
* **Higher-Layer Pragmatism:** Callbacks, events, delegates, hooks, factories, and switch-initializers are design smells in core primitives, but entirely legitimate conveniences at higher application layers (UI bindings, orchestration, plugin loaders).

## 6. DTOs & Boundary Diagnostics
* **Pure State Carriers:** DTOs hold data and zero business logic; they require no interface abstractions. Operational primitives are never data wrappers (`IContent` is an active boundary, not a `ChatHistory` wrapper). Transformations belong in external helpers.
* **DTO Impurity as a Boundary Diagnostic:** When data objects accumulate execution, assembly, or routing behavior, responsibilities were misplaced or a policy was misclassified.
* *AgentCore Evolution:* Stripped `Message` of delta-assembly and removed `IBlockEvent.Start()`. Assembly belongs strictly to operational primitives (`Content`), keeping DTOs purely passive.

## 7. Architectural Purity & Emergent Symmetry
**Purity is the pressure to remove responsibilities that do not belong to a boundary until each boundary represents exactly what it fundamentally is:** *Universal truth $\to$ Primitive; Variable strategy $\to$ Policy; External concerns $\to$ Layer; Passive state $\to$ DTO.* DTOs and pure transforms provide the passive binding (**binder**) holding them together.
* **Symmetry as a Discovery Tool:** Symmetry is both evidence of correctness and an active tool for discovering boundaries. In early `AgentCore` drafts, LLMs streamed tokens while tools returned static DTOs, requiring an intermediate accumulator. Seeking symmetry prompted the insight: *tools stream too* (progress, intermediate notifications, long-running chunks). Both perform the identical role—streaming conversational context into `IContent`. Unifying both under `IMessageEvent` eliminated accumulators entirely.
* **Internal Purity (Conceptual Loop):** High-level orchestration mirrors the fundamental domain algorithm without accumulators or glue:
```text
// Conceptual PFD ReAct loop — simplified from AgentCore
while (content.NeedsExecution()) {
    for (event in llm.Generate(content))       content.Consume(event);
    for (event in toolbox.Execute(content))   content.Consume(event);
}
```
* **External Purity & Naming:** Foundational purity allows top-level coordinators (`Agent.cs`) to expose clean fluent builders (avoiding `app.Start()` god-classes). Mirror boundaries with parallel nouns: `llm` (`ILlm`), `content` (`IContent`), `toolbox` (`IToolbox`).

## 8. Physical Topology & Universal Scope
* **Structure Rules:** Flat is fine for small scopes (2–3 files; do not manufacture folders). Group correlated units into matching folders/namespaces. Disk directories naturally align with project and namespace boundaries, avoiding virtual mismatches.
* **Topology Trie:** Directory trees mirror the system's primitive trie:
```text
/Context/
│   ├── IContext.cs                   <-- Primitive Contract
│   ├── Context.cs                    <-- Baseline Implementation (~150 LoC)
│   ├── /Compactor/                   <-- Policy Scope (ICompactorPolicy.cs, SlidingWindowCompactor.cs)
│   └── /Persistence/                 <-- Layer Scope (PersistenceContextLayer.cs)
```
* **Universal Scope:** In UI (e.g., WPF), `UserControl: Form` is the primitive, DTOs carry data, validation/templates are policies, and modal/theme wrappers are layers. In documentation, core thesis is primitive, methodologies are policies, and examples are layers.

## 9. The PFD Practitioner's Reference Checklist
| Focus Area | Diagnostic Question | Heuristic / Action |
| :--- | :--- | :--- |
| **Existence** | Can type/method/helper/boundary be removed without loss? | Subtraction test: If yes, remove; if no, explain structural necessity. |
| **Future-Proofing**| Is contract narrowly fitted to today's consumer? | Remove unnecessary restrictions; add zero speculative capabilities. |
| **Purity** | Does orchestration require accumulators, adapters, or glue? | Boundary smell. Re-examine boundaries and seek natural symmetry. |
| **Contract** | Does opinion represent universal truth? Crossing 4–5 methods? | Keep universal truths; inject policies. Trigger scrutiny if > 4–5 methods. |
| **Properties/Types**| Exposing properties? Escaping via `object`/`dynamic`? | Prefer methods unless simple synchronous state. Enforce strict typing. |
| **Implementation** | Cohesive scope > ~150 lines? Hardcoding changeable values? | Extract policies (algorithms down to thresholds). Obey anti-gaming laws. |
| **Composition** | Can primitive work without it? Shared across contexts? | NO $\to$ Policy (injected). YES $\to$ Layer. If shared, check if internal policy. |
| **Data & Topology**| DTO holding logic? Orphan files or needless folders? | Keep DTOs passive. Small scopes flat; align disk to namespaces naturally. |