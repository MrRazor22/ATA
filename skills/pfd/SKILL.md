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
   - **Step 1: Core Primitives:** Identify irreducible boundaries; define pure interface contracts ($\le$ 4–5 methods).
   - **Step 2: Pure DTOs:** Passive state carriers with zero behavior.
   - **Step 3: Opinion Sub-Primitives (Policies) vs. Decorated Layers:** Injected strategies vs. external wrapping decorators.
   - **Step 4: Orchestration & Natural Symmetry:** Check emergent symmetry across boundaries; zero accumulators or glue.
   - **Step 5: Physical Topology:** Clean folder and namespace trie mirroring primitive boundaries.
3. **Auditing Existing Code:** Run designs against the §10 Checklist. Identify misplaced responsibilities, overfitted contracts, and bloat.

# Primitive-First Design (PFD)

Primitive-First Design (PFD)—originally conceptualized as ATA—basically argues that **correct code is usually minimal**. Most abstractions are bloat created to patch a poor foundational primitive. If we design core primitives right in any system design, code naturally becomes minimal, code smells disappear, and the system becomes scalable, readable, maintainable, and simply better.

We judge PFD by number of code lines. While lines of code is not a perfect metric, it is the best proxy metric we have when looking at an entire system end-to-end. Crucially, PFD does **not** mean putting all code into a single class or writing convoluted one-liners to reduce line count.

PFD is a set of principles and decisions to achieve minimal code with zero code smell—yielding high-signal, condensed, dense architecture.

A rough test is that an average system designed cleanly end-to-end with PFD usually hovers around **~5k lines** if not overly complex or loaded with batteries. The core of the project or namespace that contains all core primitive implementations and their opinion sub-primitives—in other words, the bare-bones project that can run—will sit around **1k–1.5k lines max**. This is just to give an idea, not a hard rule or magic number.

*Interface* is a Java/C# term, but means traits in Rust, protocols in Python, or abstract contracts in Go/C++.

---

## 1. Core Primitives

Everything is and must be an interface (except DTOs, transforms, helpers, etc.). No concrete access anywhere: **the interface is the only truth**. Zero backdoor access; contracts must always be respected.

This interface mandate is a cognitive forcing mechanism to force you to think and design contracts better, instead of conveniently abusing a class to expose whatever you want at any time.

A primitive represents what we expect from something. In OOP, we design based on real-world objects. For example, if a car is designed, we clearly define what the core primitives in a car are:
* **Engine** (gearbox, fuel tank, etc.)
* **Body** (lights, doors, storage, etc.)
* **Chassis** (wheels, steering)
* **Usable Area / Cabin** (seats, dashboard)
* **Control Bus**

The entire car, if done cleanly, has only 5 primitives. These primitives can be modeled into clean interface contracts, and if done right, a car can be built end-to-end with just these 5 contracts used together.

The same applies to [AgentCore](https://github.com/MrRazor22/AgentCore): look at how cleanly `IContent`, `ILlm`, and `IToolbox` compare to even Microsoft Agent Framework or LangChain.

Core primitives must be irreducible and represent an operational boundary, not merely an arbitrary OOP component.

---

## 2. Boundary Discovery & Avoiding Narrow Overfitting

We look for clear, obvious boundaries like the examples above. Sometimes, if a boundary is not obvious, we model it based on consumer demand: who uses it and what the user wants from it gives a hint of the boundary.

However, **we should never narrowly design an abstraction merely to satisfy the immediate need**. Look at what satisfies current needs perfectly while also being ideal for future needs and scaling. That is where great primitive design lies. In rare cases, we model based on similar existing domains.

For example, in AI agents we have RAG, memory, and context. But an agent fundamentally only needs current content in its context window to work. The primary need is `IContent`. Everything else—memory and RAG—is either a policy (an injected sub-primitive) or a layer (decorators, middlewares).

A poor design would create `IMemory` and `IContent`, where `IMemory` has `IRag` and long-term storage, while `IContent` has working memory. That sounds neat and resembles textbook OOP, but it falls into the trap of **"only narrowly satisfying the current need."** What if in the future you want to add a new context source? Or expose memory as tools the agent invokes rather than auto-injecting it? This overfitting should be avoided. A simple `IContent` where memory and RAG are layers remains naturally minimal, neither overfitting nor underfitting.

A primitive must be designed based on who uses it today, but also who may use it in the future. A well-designed primitive ensures:
1. It does not carry speculative bloat (nothing added solely anticipating an unverified future need).
2. It does not lack a future capability that may reasonably arise.
3. It naturally fits present needs perfectly while making future expansion trivial for any anticipated situation.

An interface is future-proof not because it has generic methods with catch-all parameters for tomorrow's guesses, but because it is so fundamentally unconstrained and pure that future requirements fit naturally without changing the contract.

---

## 3. Meticulous Contract Scrutiny & Universal Opinions

Every method added to an interface must be meticulously questioned multiple times:
* *Is it truly needed?*
* *Is it needed with this many parameters?*
* *Can the return type be better, or can we design it in a general way that serves current and future needs cleanly?*

Scrutinize every detail to reduce surface area. Finalizing core primitives correctly solves ~80% of the entire system architecture; implementation flows downhill naturally.

**Universal Opinions vs. Coupling:**
Are we adding opinions into the contract? Are we coupling anything? Are we exposing something that belongs in an injected concrete implementation rather than the core interface?

You cannot have zero opinions, but any opinion baked into a core contract must be a **justifiable universal need**:
* In `AgentCore`, `IContent` could simply expose messages or async/sync write methods. But we took a universal opinion: an agent streams from the LLM to the user. Instead of restricting write operations to return narrow content events, `IContent` returns complete `IMessageEvent` streams, allowing the agent to cast or pass events cleanly.
* We deliberately excluded unnecessary methods from `IContent`:
  * *No `Clear()`:* Agents never clear their own memory. If needed, session management is injected into a persistence layer; let higher-level session stores handle clearing.
  * *No raw chat history getters:* An operational boundary is an active contract, not a passive data holder.
  * *No `UpdateTokenUsage()`:* Token usage streams directly from LLM response events, not through side-channel mutation methods.

**Interface Properties:**
Exposing properties in interfaces (in languages like C#) is generally not preferred because they cannot be cleanly layered, intercepted, or converted to async operations if complex logic is needed later. If simple synchronous exposure avoids boilerplate get/set methods, an exception can be made, but pure action methods remain preferred.

**The 4–5 Method Heuristic:**
If an interface crosses 4–5 methods, its boundaries are usually misjudged, doing too much, or modeled around a non-existent boundary. The 4–5 method rule is a warning light to think deeper.

**Colocated Extension Methods ("Useful $\ne$ Fundamental"):**
You often need convenience methods, but those belong in extension methods colocated with the primitive, not in the core contract. A core primitive contract stays minimal; helpers change based on usage.
* *The Fruit Rule:* A `Fruit` primitive defines `Taste()` and `Size()`. An `IsApple()` query is an extension helper, not part of the core primitive contract.
* *Ban on Static Utility Grab-Bags:* Never create monolithic static classes (`CommonUtils`, `TransformUtils`) that dump helper methods across all primitives. Keep extension methods scoped and colocated with the primitive file.

---

## 4. Concrete Implementations, Opinion Sub-Primitives & Policies

The concrete implementation of a primitive is itself an opinion on how it should function. It must remain decoupled, vanilla, and adhere to universal design principles to ensure future extensibility.

**The ~150-Line Heuristic (Anti-Bloat Smoke Detector):**
If a concrete implementation exceeds **~150 lines**, it is usually a code smell: it is doing more than it should and harboring hardcoded opinions.
* Extract opinions, variable numbers, and complex algorithms into injected **Opinion Sub-Primitives (Policies)**. (For example, an `Engine` primitive may reach 1,000 lines if implemented monolithically, but extracting `IFuelSystem` and engine timing as injected policies keeps the core engine implementation clean and readable like plain English).
* *Cohesive File Scope:* If an interface has one primary implementation, keeping the interface, implementation, and extension methods together in one file within ~150 lines is preferred for easy maintenance.

**Anti-Gaming Laws (Strictly Banned):**
* Never dice one 150-line file into five 30-line files just to game the metric. Keep cohesive pieces together.
* Never use `partial class`, unnatural subclassing, `ref`/`out`, or language quirks to hide line bloat.

**Recursive Hierarchy:**
When an injected policy grows complex enough to form its own logical boundary, it can have its own sub-opinions injected: $\text{Core Primitive} \to \text{Opinion Sub-Primitive} \to \text{Sub-Policy}$.

---

## 5. Layers & Middlewares (Decorated Co-Primitives)

While Policies are injected *inside* core primitives to decouple internal strategies, **Layers** decorate primitives from the *outside* to intercept, observe, modify, or control end-to-end I/O flow.

Layers provide direct extension over core primitives—like a mechanic plugging diagnostic instruments directly into an engine, body, or chassis. They offer the power of ASP.NET Core middleware without delegate bloat (pure decorators).
* An `Engine` primitive can have a sensor layer monitoring telemetry, or a tuning layer improving mileage, without modifying the core engine.

**Preceding Diagnostic (Primitive Completeness):**
A core primitive must be functionally sound on its own. If you need a layer to make a primitive functional, that is a design smell indicating a missing internal responsibility or policy.

**Functional Completeness Test:**
Once the primitive is sound:
* **NO** (primitive cannot function without it) $\to$ **Policy** (injected opinion sub-primitive, e.g., context compaction in `AgentCore`—an agent cannot function once its context window overflows).
* **YES** (primitive functions completely in-memory without it) $\to$ **Layer** (external concern, e.g., persistence, logging, telemetry).

**Shared Dependency Rule:**
If multiple layers require a specific capability, evaluate whether it is a shared internal policy rather than duplicating it across decorators.

**Higher-Layer Pragmatism:**
Callbacks, events, delegates, hooks, factories, and switch-case initializers are design smells in core primitives, but legitimate conveniences at higher application layers (UI bindings, orchestration, plugin loaders).

**Strict Typing:**
Always use strictly typed code; avoid `object`, `dynamic`, or unchecked casting escape hatches unless the benefits overwhelmingly outweigh the design smell.

---

## 6. Passive State DTOs

Pure data classes must not contain business logic. If a DTO requires behavior, it indicates misplaced responsibilities or a missing policy sub-primitive.
* Pure transform helpers (e.g., `ToString()`) can be extension methods staying close to or in the same file as the DTO.
* DTOs do not earn interfaces, and primitives are never passive data wrappers (`IContent` is an active operational boundary, not a `ChatHistory` wrapper).
* *AgentCore Diagnostic:* Stripping `Message` of delta-assembly logic and removing `IBlockEvent.Start()` (which acted as a hidden factory on an event DTO) restored purity. Delta assembly belongs strictly in operational primitives, keeping DTOs purely passive.

---

## 7. Natural Symmetry, Orchestrator Purity & Naming

When core primitives are modeled correctly, a natural symmetry emerges across the system:
* **Symmetry as a Discovery Tool:** In `AgentCore`, LLMs streamed tokens while tools originally returned static DTOs, requiring an intermediate accumulator. Seeking architectural symmetry prompted the realization: *tools stream too* (progress updates, long-running chunks). Both LLMs and tools stream context into `IContent` via `IMessageEvent`. Unifying them under streaming symmetry eliminated accumulators entirely.
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