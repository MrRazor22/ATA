---
name: primitive-first-design
description: >-
  Applies Primitive-First Design (PFD) to software architectures. Activate when commanded with
  "Apply PFD", designing systems, reviewing interface contracts, eliminating bloat/glue, or refactoring.
---

Primitive-First Design (PFD) basically argues that **correct code is usually minimal**. Most abstractions are bloat to patch a poor foundational design primitive. If we design core primitives right in any system design, then naturally code gets minimal, code smells get reduced, and the system becomes scalable, readable, maintainable, and just better.

We judge PFD by number of code lines, which is not completely correct, but it is the best proxy metric we can have when you take an entire codebase of a system end to end. Most importantly, PFD is **not** putting all code in a single class or writing convoluted one-liners to reduce code lines.

PFD is a set of principles and decisions to get minimal code with no code smell—yielding high-signal, condensed, and dense output.

Aim for absolute minimal code: a cleanly designed system with PFD should naturally hover around **~1k lines end-to-end**. A human cannot easily comprehend an entire codebase beyond **~3k lines** in working memory. If a project exceeds these limits without immense external domains, it is carrying speculative bloat, redundant boilerplate, or misplaced boundaries.

*Interface* is a Java/C# term, but means traits in Rust, protocols in Python, or abstract contracts in Go/C++.

---

## REFACTORING EXISTING CODE: BRUTAL HONESTY & ZERO COMPROMISE

When asked to refactor or evaluate existing code with PFD, you are here to **enforce PFD, not adapt to existing smells**.
* **Be Absolutely Honest & Zero-Loss Compression:** Do not adapt to existing smells or accept legacy layouts as given. Loop and iterate until you achieve a zero-loss functional compression—preserving all original system capabilities within minimal, high-density primitives while boldly deleting legacy shapes, dead overloads, and wrapper shims.
* **Never Mechanically Transpose Classes or Files into Interfaces (The Inventory Smell):** Copying existing classes with an `I` prefix or giving every file/utility an interface is lazy transposition. Primitives derive strictly from irreducible domain transformations, never file inventories. Encapsulate implementation mechanics privately inside concrete implementations or model passive observers/state transmitters as outer Layers ($\lambda: P \to P$).
* **Ignore Legacy Documentation & Enforce Structural Purity:** Ignore legacy labels or conventional coding patterns. The design must resolve into few irreducible core primitives and explicit injected sub-primitives (policies), where all callers strictly follow interface contracts with zero concrete backdoor access, all DTOs are pure data, and transforms are colocated directly with the primitives or DTOs they extend.

---

## CORE PRIMITIVES

Everything is and must be an interface contract (except pure DTOs and pure transforms). A concrete class exists for strictly two reasons: either to implement an explicit primitive/policy/layer interface contract, or as a pure behaviorless DTO. Anything with behavior must be modeled as a proper primitive contract—zero intermediate classes, zero un-interfaced workers. Pure transform functions or extension classes are colocated directly with the primitive contract or DTO they extend.

This interface mandate is a cognitive forcing mechanism to force you to think and design contracts better, instead of conveniently abusing a class to expose anything you want at any time. No concrete access anywhere: **the interface is the only truth**. Zero backdoor access; the interface must always be respected.

An interface is a symbol of decoupling—never add coupling into it. A concrete implementation can have hard couplings injected (via interfaces) or have its own internal opinions, but the interface contract itself is meant to be pure.

Every operational method on a primitive contract that exchanges data (methods can obviously be void or parameterless when appropriate) must strictly take and return pure passive DTOs or native language primitives. Never allow external framework, computational, hardware device, or runtime types across an interface contract or DTO—all framework execution and third-party dependencies belong strictly encapsulated inside concrete implementations behind that pure DTO boundary. Never use `Any`, `object`, `dynamic`, or untyped containers as escape hatches across contracts or DTOs; domain types must be modeled strictly. Every collaborator or policy injected into a primitive must itself be defined by an explicit interface contract—zero concrete backdoor classes. Sub-primitives, policies, or complex collaborators are dependencies injected into concrete implementations, NEVER passed as parameters across caller contract methods.

A primitive represents what we expect from something. In OOP, we design based on real-world objects. For example, if a car is designed, the primitives define clearly what the core primitives in a car are:
* **Engine** (gearbox, fuel tank, etc.)
* **Body** (lights, door, storage, etc.)
* **Chassis** (wheels, steering)
* **Usable Area / Cabin** (seats & dashboard)
* **Control Bus**

The entire car, if done cleanly, has only 5 primitives. These primitives can be modeled into clean interface contracts, and if done right, a car can be built end to end with just these 5 contracts used together.

The same applies to [AgentCore](https://github.com/MrRazor22/AgentCore): look at how cleanly `IContext`, `ILLM`, and `IToolbox` compare to even Microsoft Agent Framework or LangChain.

Core primitives must be irreducible and represent an operational boundary, not simply an arbitrary OOP component.

We see clear, obvious boundaries like the examples given. Sometimes, if a boundary is not clear, we model it based on the need for it: who uses it and what the user wants from it gives a hint of the boundary.

However, **we should never narrowly design an abstraction to satisfy the immediate need**. Through the current need, look in general at what is expected that satisfies the current need perfectly, but will also be ideal for future needs and scaling. That is where great primitive design lies. In rare cases, we model based on other examples of similar works.

For example, in AI agents we have RAG, memory, and context. But if you see clearly, an agent fundamentally needs context in its context window to work. The primary need is `IContext`. All the rest—memory and RAG—are either policies (injected sub-primitives) or layers (decorators, middlewares).

A poor design would create `IMemory` and `IContext`, saying `IMemory` will have `IRag` and store memory, while `IContext` will have working memory. That sounds neat and resembles textbook OOP, but it falls into the trap of **"only narrowly satisfying the current need."** What if in the future you want to add a new source of context? Or expose memory as tools the AI agent invokes rather than auto-injecting it? This overfitting should be avoided. A simple `IContext` where memory and RAG are layers remains naturally minimal, neither overfitting nor underfitting. In some cases where the domain is very new, boundaries can be unclear to model based on pure OOP.

A primitive must be designed based on who uses it today, but most importantly who may use it in the future as well. The design should be so well conceived that:
1. It won't look like it has something obviously added only anticipating a future need with no current use.
2. It clearly won't lack a future need that may come as a possibility.
3. It will naturally be a great design that is perfect for present needs, but also trivial to expand in the future for any possible situation we could think of today (we can only think with today's knowledge of the future, but if we think right, it holds the design for years, if not decades).

For good interface design, every method added to it must be meticulously questioned multiple times:
* *Is it needed?*
* *Is it really needed with this many parameters?*
* *Can we do better with this return type, or can we design it in a general way that serves current and future needs cleanly?*

Scrutinize every detail at the micro level by asking: *Is this needed? Is it better to have it this way to reduce that? Is it better to have this over that?* Finalizing core primitives correctly solves ~80% of the architecture; implementation flows downhill naturally.

**Universal Design:**
Are we adding opinions into it? Are we coupling anything? Are we exposing something that must be injected into a concrete implementation rather than being part of the core interface contract? Are we coupling something, or making a policy decision that cannot be changed?

You cannot never have zero opinions, but any policy or opinion decided as a core part of the contract must be a **justifiable universal need** that happens to also fit present needs perfectly. This is what it means for a primitive to be generic and universal.

Interface design must be done meticulously. For example, in `AgentCore`, `IContext` could simply expose messages or synchronous/asynchronous write methods. But we took a universal opinion: an agent streams from the LLM level to the user. If needed, let the user accumulate it, or expose helper transfer methods at the top, not as a core contract.
* In `WriteAsync`, we could have simply returned `IContentEvent` because the user agent only exposes that. That exact narrow trap was avoided. The interface was not restricted: `IContext` returns complete `IMessageEvent` streams with full message and content events, and the agent decides to cast and expose content events as needed. Present needs are satisfied perfectly without awkward, future-only designs.
* Unnecessary methods were excluded from `IContext`:
  * *No `Clear()`:* Agents in the future do not need to clear their own memory (a universal opinion taken). If needed, session injection exists in the persistence layer; let the session store clear itself at a higher level.
  * *No raw chat history getters:* An operational boundary is an active contract, not a passive data holder.
  * *No narrow methods like `UpdateTokenUsage()`:* Token usage arrives directly from LLM response events (`IMessageEvent`), not through separate mutation methods.
  * *No update full message methods:* We made a universal opinion to support stream injection directly, with helpers to directly append messages if needed via the same primitive.

Sometimes a natural symmetry arises in primitive design across the system. In `AgentCore`, all three pillars have symmetry where they become the core pillars the agent needs, and all three are streaming. Initially, tooling was not streaming. But the motivation to find symmetry pushed the realization: tools stream too (if not literal text like an LLM, tools stream notifications and progress for long-running executions). Since the UI for the agent streams, tooling was designed to stream the same message events. Tooling streams `IContentEvent`, which can also be complete content. Finding symmetry revealed that tools are fundamentally the same as LLMs: both stream context into the agent's context, which is literally the agent loop. Without seeking symmetry, this insight would never have emerged.

Exposing properties in interfaces (in languages like C#) is usually not preferred. It cannot be cleanly layered, intercepted, or scaled if a getter or setter requires complex asynchronous operations in the future. If simple synchronous exposure avoids two getter/setter methods, it can be exposed, but pure action methods remain preferred.

A good test is if an interface crosses more than **4–5 methods**: usually its needs are not correctly judged, it is doing too much, or it is modeled around a wrong or non-existent boundary. Never carelessly dump multiple convenience overloads or parallel variants (like `Do()` and `DoBatch()`) into a contract interface; design a single, sovereign operational signature that handles the general case cleanly. Convenience overloads belong in callers or extension helpers, never polluting the root contract.

You may need more methods, but usually those are helper methods that can be added as extension methods on concrete implementations or colocated extensions. The core primitive stays minimal; helper methods change based on implementation and shouldn't pollute the core contract.
* *The Fruit Rule:* A `Fruit` primitive defines `Taste()`, `Size()`, etc., but `IsApple()` is an extension method, not part of the core primitive contract.

Future-proof does not mean having generic methods with catch-all parameters for tomorrow's guesses. It means the design is so fundamentally unconstrained and **PURE** that it represents the system's core primitives so clearly that future requirements fit naturally without changing the contract.

---

## CONCRETE IMPLEMENTATION OF CORE PRIMITIVES AND ITS OPINION AND POLICIES

Once the interface contract of core primitives is well designed, the concrete implementation is itself an opinion on how it should function. By default it is decoupled, but the concrete implementation must follow the same universal, generic, non-overfitting design. How good the design is defines future extensibility and scaling.

**The ~150-Line Heuristic:**
If a concrete implementation of a primitive exceeds **~150 lines**, it is usually a code smell: it is doing more than it should and taking on hardcoded opinions inside.

All opinions and policies inside must be injected. Even simple numbers that can change should be injected rather than hardcoded. Complex opinionated logic can be cleanly separated into its own primitive whose interface follows the same rules described above.
* For example, the `Engine` primitive of a car, if implemented monolithically, could reach 1,000+ lines even if its interface is only 2–3 methods. Extracting `FuelSystem` as an injected opinion rather than hardcoding it, and handling engine timing separately, keeps the core engine primitive clean, simple, and readable like plain English.

These sub-primitives are not core primitives that define the entire product end to end; they are **opinion and policy component primitives**.

Sometimes these extracted opinion sub-primitives become complex enough to form their own boundary (an interface is decided from a logical boundary), so they can have their own sub-opinions injected.

The ~150-line rule applies across primitive implementations. If an interface has one primary implementation, keeping both the interface and concrete implementation in the same file within ~150 lines is preferred for easy maintenance. The rule also applies when combining the interface, concrete class, and extension methods in one file.

**Anti-Gaming Laws (Strictly Banned):**
* Using `partial class`, subclassing, or language gimmicks to circumvent the ~150-line test is strictly a code smell.
* Using `ref`, `out`, or language quirks is lazy patchwork to avoid dealing with the actual smell.
* If someone splits one 150-line file into five 30-line files, that is terrible. Do not just split files for the sake of a line number. Keep cohesive pieces together; if a single implementation exceeds ~150 lines, it is secretly hiding un-extracted policies or god-object logic.

**Renaming Clarity:**
* Policy $\to$ **Opinion Sub-Primitives**
* Primitive $\to$ **Core Primitives**
* Layer $\to$ **Layered Co-Primitives**
Overall, all are primitives, and everything is an interface.

Extension methods can reside in the same file as the class or interface for easy management. Never create giant static classes (`TransformUtils`, `CommonUtils`) that dump helper extension methods for all primitives in one place. Keep related logic scoped together.

While policies are injected into core primitive implementations to decouple internal strategy and functioning, **LAYERS** are used to observe, modify, intercept, or control end-to-end I/O flow externally.

---

## LAYERS, MIDDLEWARES

Layers are meant for core primitives. Core primitives control the core pillars of the entire system end to end.

Layers may feel unnecessary at first, but decorating a layer over a core primitive gives entire input and output control. This offers the power of classic HTTP/request pipeline middlewares with less bloat (pure decorators with no before/after delegate complexity).

Layers provide direct extension over core primitives—like a mechanic plugging measuring instruments directly into an engine, body, chassis, or cabin to diagnose or customize it. That is how powerful they are for extensibility, scaling, and control.
* An `Engine` primitive can have a sensor layer monitoring engine parameters and telemetry, or a user-mod layer improving mileage, without altering the core engine. Layer classes typically adopt the `Layer` suffix for immediate architectural clarity.

**Architectural Smells & Invariant Violations:**
* **Nested Containers Smell:** Never use nested containers (collections of collections, nested dictionaries/maps, lists of tuples, or deep generic wrapper chains) across contracts or DTOs. A nested container is a lazy escape hatch used to dodge modeling a domain concept. If data has internal structure or associations, model them as explicit, typed domain DTOs.
* **Untyped Escape Hatches:** Always enforce strict, explicit typing system-wide. Never use `Any`, `object`, `dynamic`, or generic property bags (`dict[str, Any]`) across contracts or DTOs. If an abstraction requires `Any` or `object`, domain types were not properly modeled.
* **Substrate & Runtime Leakage:** Never leak execution substrate types (framework runtime handles, computational tensors, database cursors/connections, HTTP contexts, vendor SDK types) across primitive boundaries. All substrate interactions must be completely encapsulated behind pure DTO boundaries.
* **The Incomplete Primitive Smell:** A core primitive must be functionally sound and operational on its own. If an external layer or decorator is required for a primitive to perform its primary responsibility, the primitive is incomplete and secretly outsourcing its core mechanism.
* **Convenience Overload Sprawl:** Never pollute primitive contracts with convenience overloads or parallel method variants (such as `Do()` and `DoBatch()`). Design a single sovereign operational signature that handles the general case cleanly; convenience overloads belong in callers or extension helpers.
* **Callbacks, Delegates & Hooks in Core Contracts:** Delegates, callbacks, and hooks in core primitive contracts are architectural smells indicating leaky lifecycle control. They are permitted only at higher application layers (UI bindings, event dispatchers, plugin loaders), never inside core primitive interfaces.
* **Factory Patterns & Switch-Case Dispatch:** Factory patterns and switch-case initializations are usually smells hiding fundamental design issues and lazy polymorphic modeling. Genuine needs can warrant them, but using them is usually a sign of un-extracted primitive boundaries.
* **Meta-Naming Cop-Outs:** Never name namespaces, directories, or files after architectural patterns (`Manager`, `Service`, `Helper`, `Utils`, `Common`, `DTO`, `Contract`, `Components`). Everything must be named after its domain noun.

**Testing Policy vs. Layer:**
* If something is needed by other layers, it is an injected opinion sub-primitive, not a layer.
* If it is an independent extension on top of a core primitive, it is a layer.
* For example, in `AgentCore`, summarization was originally considered a layer on top of content. But compaction is triggered on token usage: if the context window fills, it must compact. Without a form of compaction, the agent cannot function. **A core primitive on its own must be functionally sound; if a layer is needed to make a primitive functional, that is a design smell.** If compaction were an external layer, the core primitive would be incomplete. Therefore, compaction is an injected policy (opinion sub-primitive) with strategies like sliding window or summarizer, while secondary snapshotting or externalization is clearly a layer because the primary domain primitive functions completely on its own without externalizing state.

---

## DTOS

Pure data classes must not have business behavior in their core class. If they need behavior, it indicates misplaced responsibilities, missing opinion sub-primitives, or poor foundational primitive design.
* Pure transform methods (e.g., `ToString()`) can be separate extension helpers close to or in the same file as the DTO class.
* **Concrete by Default:** DTOs are passive domain records representing pure facts, configurations, or isolated parameter bundles. For point-to-point data exchange, creating interface contracts for DTOs is pure ceremony and speculative bloat. DTOs are concrete types by default.
* **When DTOs Must Have Interface Contracts:** A DTO interface contract is required in exactly two structural circumstances:
  1. *Polymorphic Data Streams (Domain Event / Union Hierarchies):* When divergent data payloads flow through the same primitive boundary or stream, an explicit contract represents the shared domain concept without resorting to untyped escape hatches (`object`, `Any`). Consumers process the shared domain contract polymorphically, narrowing types via exhaustive pattern matching.
     * *Case Study (AgentCore `IMessageEvent`):* Streaming tokens (`MessageDelta`) and completed messages (`Message`) are separate concrete records carrying different internal structures, but both flow across the exact same context boundary as `IAsyncEnumerable<IMessageEvent>`. Callers inspect events polymorphically (`if (evt is MessageDelta { Content: ToolCall tc })`) without the pipeline degrading into untyped bags or inheritance coupling.
  2. *Cross-Cutting Domain Data Capabilities:* When heterogeneous DTOs share an orthogonal data trait that pipeline layers, storage engines, or decorators must inspect without coupling to specific concrete payloads. Examples include shared capability contracts for identity, timestamping, or multimodal binary transport (`IBinaryPayload` exposing raw bytes and MIME types across arbitrary artifact, image, or audio records).
* In older drafts of `AgentCore`, `Message` handled delta assembly, and `IBlockEvent` had a `Start()` method so each content type knew which delta object to receive (acting as a hidden factory on a DTO). Removing those mixed smells made context an operational primitive, messages pure DTOs, and message events pure passive event contracts.
* **DTO File Naming Invariant:** When multiple related DTOs are colocated in a single file, the file name must commonly represent all items it holds, strongly preferring their shared concept or common suffix. File names must never use architectural pattern labels or meta cop-outs (such as `dto`, `dtos`, `models`, `types`, `contract`, or `schema`).

---

## NATURAL SYMMETRY AND ARCHITECTURAL PURITY

Natural symmetry and architectural purity are two complementary, yet fundamentally distinct forces in Primitive-First Design:

### 1. Architectural Purity (The Deliberate Standard)
Purity is not an emergent accident; it is an uncompromising standard committed to upfront. It governs the highest-level layer or composition root that consumes the system's core primitives:
* **The High-Level Consumption Invariant:** When you design a system, look at the highest-level orchestration layer that consumes the core primitives. That layer must read as pure, transparent, and direct as pseudo-code or plain English. If orchestrating the primitives requires intermediate glue, state staging, or awkward mediation, the primitives themselves are improperly modeled. Never hide architectural sprawl behind a lazy god-class or opaque single-line launcher (`var app = app.start()`); provide a pure orchestration flow anchored by a clean, fluent composition builder.
* **Universal Invariant — Zero Intermediate Orchestration Glue:** Primitives natively encapsulate and own their internal data lifecycles, transformations, and aggregation policies. The primary orchestration flow must never be polluted by intermediate mediator abstractions, accumulators, assemblers, or coordinator shims sitting between primitives.
  * *Case Study (AgentCore Loop Purity):* In earlier iterations of `AgentCore`, an intermediate assembler component sat directly in the ReAct loop as an external coordinator, gathering streaming chunks before feeding full messages to context. Committing to architectural purity—demanding that the central loop read cleanly like plain pseudo-code—prompted the realization that message assembly is not an external orchestration concern; it belongs natively inside context. `Context` took internal ownership of assembly (injecting `IAssembler` as an internal policy), completely freeing the high-level orchestration loop from mediator glue:

```csharp
do {
    await foreach (var evt in Context.WriteAsync(LLM.GenerateAsync(prompt, toolDefs)))
        if (evt is MessageDelta { Content: ToolCall tc }) (toolCalls ??= []).Add(tc);

    if (toolCalls is not null)
        await foreach (var evt in Context.WriteAsync(Toolbox.ExecuteAsync(toolCalls))) ...
} while (toolCalls is not null);
```

### 2. Natural Symmetry (The Emergent Discovery)
While Purity is a deliberate constraint enforced by subtraction, Symmetry is an internal emergence discovered iteratively as you develop:
* **Symmetry as a Discovery Compass:** As you plan core primitives, you will naturally spot hints of symmetry across peer pillars. When one primitive exhibits a capability or interaction shape, ask why its peer does not. Artificial asymmetry is almost always evidence of an unexamined assumption or an overfitted boundary. Following hints of symmetry unlocks the deepest, most durable interface designs.
* **Universal Invariant — Parallel Flow Unification Across Interacting Boundaries:** When interacting peer boundaries appear fundamentally different, seeking symmetrical shapes often reveals that they are different manifestations of the exact same conceptual flow.
  * *Case Study (AgentCore Streaming Context Producers):* Initially, `Toolbox` was designed as non-streaming, returning isolated static results. The motivation to find symmetry across all three core pillars pushed the question: *why shouldn't tools stream?* Long-running executions, status notifications, and progress updates naturally stream, and the user interface was already streaming. Designing `Toolbox` to stream the same domain message events (`IMessageEvent`) unlocked the breakthrough insight: **tools are fundamentally the same as LLMs—both simply stream context into Context.** Without actively pursuing symmetry, this foundational architectural truth would never have been discovered.
* **Symmetrical Domain Naming:** Natural symmetry extends to naming. Parallel domain nouns must be chosen meticulously across all peer namespaces and contracts (`llm`, `context`, `tool` $\to$ `ILLM`, `IContext`, `IToolbox`), consciously rejecting procedural verbs or action cop-outs (such as `tooling` or `tool_executor`).

### 3. The Triad: Structural Symmetry & Purity
The structural convergence of symmetry and purity manifests in the boundary triad:
* A **Policy** is just a Primitive on the *inside* (an injected sub-primitive completing internal strategy).
* A **Layer** is just the same Primitive on the *outside* (a decorated co-primitive extending I/O externally: $\lambda: P \to P$).
* **DTOs and Pure Transforms** are the passive binder holding boundaries together without introducing behavioral coupling.

---

## FOLDER / NAMESPACE STRUCTURE

Folder structure and namespace boundaries are physical manifestations of the architectural model:
* **1:1 Topology Match:** Folders and namespaces must match 1:1. Disk layout directly reflects the architectural boundary tree. Solutions, projects, and directories define boundaries. The root hosts only sovereign entrypoints or composition roots, with zero orphan files.
* **Sovereign Primitive Root:** The root directory of a Core Primitive is reserved exclusively for the sovereign primitive contract, its primary concrete implementation, boundary exports, and root DTOs. This ensures the sovereign operational boundary is immediately identifiable at first glance, never obscured within flat directory clutter or arbitrary nesting.
* **Structural Boundary Separation (`policies/` and `layers/`):**
  * `policies/` and `layers/` exist exclusively for **simple, single interface-implementation** policies or decorators. They are flat directories housing individual files directly under the primitive root.
  * Simple policies that consist of a single interface and implementation remain individual files within `policies/`; never create single-file directory wrappers.
* **The Policy Promotion Invariant (Promoted to Sovereign Peer Primitive):**
  * When an injected capability becomes **more than a single interface-implementation** (multiple strategies, concrete variants, or internal contracts), **it ceases to be a mere policy—it promotes to become its own full Core Primitive pillar**.
  * It must **NEVER** be buried inside `policies/` or `layers/`. It is elevated to its own **dedicated domain directory at the SAME LEVEL as the primitive that originally used it**, becoming an independent sovereign primitive in the system.
  * The original consuming primitive now consumes this newly promoted peer primitive via interface injection as an equal peer boundary.
  * **Holistic Directory Naming Invariant:** The name of that promoted folder (and ANY primitive folder) must holistically represent *everything* inside it as a collective domain capability—never duplicating or shadowing an inner primitive class name, and never using meta-pattern cop-outs (`components`, `helpers`, `utils`, `common`, `services`, `managers`, `dto`).
  * As a sovereign primitive, its directory topology recursively obeys the sovereign primitive law: its root contract sits at the root, concrete implementations sit in their own behavioral files named after their concrete class, and any internal sub-policies or decorators live in its own `policies/` and `layers/`.
* **Behavioral File Naming:** Files containing behavior are named directly after the primary concrete class implemented within them (a concrete domain noun). If a file contains exclusively an abstract interface contract without an implementation, it takes the contract's name. Contracts define universal domain roles, while implementations express specific domain strategies; the file adopts the concrete implementation's name. File names must never adopt pattern meta-labels (`contract`, `interface`, `impl`, `base`).
* **Rigorous Domain Naming & Zero Meta Buckets:** All primitive boundaries, promoted domain folders, and behavioral files must be named using strict domain nouns representing what the entity is in the problem domain, avoiding procedural verbs or gerunds. Structural directory names are strictly confined to the internal boundary triad (`policies/`, `layers/`) for simple single-implementation files, or promoted peer domain directories. Directories must NEVER adopt generic bucket or meta-pattern names (`components`, `helpers`, `utils`, `common`, `services`, `managers`, `dto`).
* **The Cognitive Size Limit (~150 Lines):** A single source file must not exceed **~150 lines**. When small, colocate an interface with its primary concrete implementation and transforms in the same file named after the concrete implementation. If an implementation or contract approaches the cognitive ceiling, cleanly separate the contract, concrete class, or colocated helpers into dedicated adjacent files within their boundary.

---

## IT APPLIES TO ALL CREATIVE WORK

PFD is not limited to backend code. It applies to UI, low-level code, specifications, and all creative work. Every creative work has core primitives, opinion sub-primitives, and layered co-primitives:
* **UI Architecture (WPF / Forms / Web):** A Form `UserControl` is the Core Primitive (exposing parameters, bounds, styling, and action buttons); form inputs (Name, Email) are DTOs; validation rules and template styles are Policies; host page wrappers, modal dialogs, and container templates are Layers that decorate the form without modifying its core control.
* **Text Documents & Specifications:** The core thesis is the Primitive; decision rules and methodologies are Policies; examples, appendices, and walkthroughs are Layers.