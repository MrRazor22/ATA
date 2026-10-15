---
name: pfd
description: >-
  Applies Primitive-First Design (PFD) to software architectures. Activate when designing systems,
  reviewing interface contracts, auditing code smells, reducing code lines, eliminating bloat/glue,
  refactoring for clean minimal design, or when commanded with "Apply PFD".
---

Primitive-First Design (PFD) argues that **correct code is usually minimal**. Most abstractions are bloat patching a poor foundational primitive. If core primitives are designed right, code naturally becomes minimal, code smells reduce, and the system becomes scalable, readable, and maintainable. We judge PFD by line count—not perfectly, but it is the best end-to-end proxy. PFD is **not** cramming code into one class or writing convoluted one-liners; it is a set of principles yielding high-signal, condensed, dense output with zero code smell. A cleanly designed PFD system should hover around **~1k lines end-to-end**; a human cannot hold beyond **~3k lines** in working memory. Exceeding these limits without immense external domains signals speculative bloat, redundant boilerplate, or misplaced boundaries. *Interface* means traits (Rust), protocols (Python), or abstract contracts (Go/C++).

**The End Result:** Correct PFD application always reduces total code lines — not because line reduction is the goal, but because clean design is naturally minimal. If code lines went up after applying PFD, the design is wrong. Bug fixes under PFD are fundamental design fixes where the bug disappears as a side effect of clean architecture, not patchwork band-aids. Clean PFD design naturally avoids regressions and produces better code as a side effect. For a hard post-implementation violation checklist, invoke the `pfd-audit` skill; to force iterative self-audit and compression, invoke the `pfd-iterate` skill.

---

## REFACTORING: BRUTAL HONESTY & ZERO COMPROMISE
When refactoring or evaluating existing code with PFD, **be absolutely honest and enforce PFD, not adapt to existing smells**:
- **Zero-Loss Compression:** Loop and iterate until achieving zero-loss functional compression—preserving all capabilities within minimal, high-density primitives while boldly deleting legacy shapes, dead overloads, and wrapper shims.
- **Never Mechanically Transpose Classes into Interfaces (Inventory Smell):** Copying classes with an `I` prefix or giving every file an interface is lazy transposition. Primitives derive strictly from irreducible domain transformations, never file inventories. Encapsulate implementation mechanics privately; model passive observers/state transmitters as outer Layers ($\lambda: P \to P$).
- **Ignore Legacy Documentation & Enforce Structural Purity:** The design must resolve into few irreducible core primitives and explicit injected sub-primitives (policies), where all callers strictly follow interface contracts with zero concrete backdoor access, all DTOs are pure data, and transforms are colocated with the primitives or DTOs they extend.
- **"Zero Private Methods" Refactoring Diagnostic:** Private methods are an undeniable diagnostic smell indicating un-extracted policies, missing primitive contracts, or leaky substrate operations. Use them as an architectural roadmap to extract sovereign sub-primitives, injected policies, or pure DTO transformations until the primary implementation has zero private methods and reads in plain English.

---

## CORE PRIMITIVES
Everything must be an interface contract (except pure DTOs and pure transforms). A concrete class exists for strictly two reasons: implementing an explicit primitive/policy/layer interface, or as a pure behaviorless DTO. Anything with behavior must be a proper primitive contract—zero intermediate classes, zero un-interfaced workers. Pure transforms or extensions are colocated with the contract or DTO they extend. This mandate is a cognitive forcing mechanism: **the interface is the only truth**, zero backdoor access. An interface is a symbol of decoupling—never add coupling into it. Concrete implementations can have hard couplings injected (via interfaces), but the contract itself must be pure.

Every operational method on a primitive contract exchanging data must strictly take and return pure passive DTOs or native language primitives. Never allow external framework, computational, hardware, or runtime types across contracts or DTOs—all framework dependencies belong encapsulated inside concrete implementations behind pure DTO boundaries. Never use `Any`, `object`, `dynamic`, or untyped containers as escape hatches; domain types must be modeled strictly. Every collaborator injected into a primitive must itself be defined by an explicit interface contract. Sub-primitives, policies, or complex collaborators are dependencies injected into concrete implementations, NEVER passed as parameters across caller contract methods.

A primitive represents what we expect from something. A car's core primitives: **Engine** (gearbox, fuel tank), **Body** (lights, door, storage), **Chassis** (wheels, steering), **Cabin** (seats & dashboard), **Control Bus**—5 primitives total. If done right, a car is built end-to-end with just these 5 contracts. Same applies to [AgentCore](https://github.com/MrRazor22/AgentCore): `IContext`, `ILLM`, `IToolbox` vs. Microsoft Agent Framework or LangChain.

Core primitives must be irreducible and represent an operational boundary, not arbitrary OOP components. Sometimes, if a boundary is unclear, model based on who uses it and what the user wants. **Never narrowly design an abstraction for the immediate need**—through the current need, look at what satisfies it perfectly but will also be ideal for future needs and scaling. That is great primitive design. In rare cases, model from similar existing works. For example: agents need context, memory, RAG. But fundamentally, an agent needs context in its window. `IContext` is the primary need; memory and RAG are policies or layers. A poor design creates `IMemory` and `IContext` separately—overfitting to the current need. What if you want new context sources, or expose memory as tools? A simple `IContext` with memory and RAG as layers remains naturally minimal, neither overfitting nor underfitting.

A primitive must be designed for who uses it today and who may use it in the future: (1) It won't look like something was added only anticipating a future need with no current use. (2) It clearly won't lack a foreseeable future need. (3) It will be perfect for present needs and trivial to expand for any foreseeable situation (we can only think with today's knowledge of the future, but if we think right, it holds the design for years, if not decades). For good interface design, every method must be meticulously questioned: *Is it needed? Is it needed with this many parameters? Can we design the return type more generally?* Scrutinize every detail: *Is this needed? Is it better this way to reduce that?* Finalizing core primitives correctly solves ~80% of the architecture.

**Universal Design:** Are we adding opinions? Coupling anything? Exposing something that must be injected rather than live in the contract? Making an unchangeable policy decision? You cannot have zero opinions, but any policy or opinion decided as a core part of the contract must be a **justifiable universal need** that also fits present needs perfectly—that is what it means for a primitive to be generic and universal.

Interface design must be meticulous. In AgentCore, `IContext` could expose messages or sync/async write methods. We took a universal opinion: agents stream from LLM to user. If needed, let the user accumulate, or expose helper transfers at the top, not as a core contract. `WriteAsync` returns complete `IMessageEvent` streams (not narrowed to `IContentEvent`), and the agent casts as needed—present needs satisfied without awkward future-only designs. Unnecessary methods excluded: *No `Clear()`:* agents don't clear their own memory (universal opinion); session stores clear at higher levels. *No raw history getters:* operational boundaries are active contracts, not passive holders. *No `UpdateTokenUsage()`:* token usage arrives directly from LLM response events (`IMessageEvent`), not through separate mutation methods. *No update-full-message methods:* stream injection directly supported, with helpers to directly append messages via the same primitive.

Sometimes natural symmetry arises in primitive design across the system. In AgentCore, all three pillars have symmetry—all streaming. Initially tooling was not streaming, but the motivation to find symmetry pushed the realization: tools stream too (notifications, progress for long-running executions). Since the UI for the agent streams, tooling was designed to stream the same message events. Tooling streams `IContentEvent`, which can also be complete content. Finding symmetry revealed tools are fundamentally the same as LLMs: both stream context into the agent's context, which is literally the agent loop. Without seeking symmetry, this insight would never have emerged.

Exposing properties in interfaces (C#-style) is usually not preferred—cannot be cleanly layered, intercepted, or scaled for future async operations. If simple synchronous exposure avoids two getter/setter methods it can be exposed, but action methods remain preferred. A good test: if an interface crosses **4–5 methods**, usually its needs are misjudged, it does too much, or models a wrong boundary. Never dump convenience overloads or parallel variants (`Do()` / `DoBatch()`) into a contract; design a single sovereign signature for the general case. Convenience overloads belong in callers or extension helpers. Helper methods that change per implementation go as extensions, not core contract pollution. *The Fruit Rule:* `Fruit` defines `Taste()`, `Size()`; `IsApple()` is an extension, not core contract.

Future-proof means the design is so fundamentally unconstrained and **PURE** that it represents core primitives so clearly that future requirements fit naturally without changing the contract—not generic catch-all parameters for tomorrow's guesses.

---

## CONCRETE IMPLEMENTATION & POLICIES
Once the contract is well designed, the concrete implementation is itself an opinion on how it should function. By default it is decoupled, but the concrete implementation must follow the same universal, generic, non-overfitting design. **The ~150-Line Heuristic:** If a concrete implementation exceeds **~150 lines**, it is a code smell—doing more than it should with hardcoded opinions inside. All opinions and policies must be injected. Even simple numbers that can change should be injected rather than hardcoded. Complex opinionated logic is cleanly separated into its own primitive whose interface follows the same rules. Example: the `Engine` primitive, if monolithic, could reach 1,000+ lines even with 2–3 interface methods. Extracting `FuelSystem` as injected opinion and handling timing separately keeps the core engine clean, readable like plain English.

**Policy Injection & Sensible Defaults Invariant:**
- **Constructor Injection with Built-In Defaults (Zero Mandatory Parameters):** Concrete implementations accept policy contracts via constructor for full caller control. Injection must never be mandatory or burdensome: primitives and policies must be self-contained. Every constructor parameter (policies, counts, limits, thresholds, buffer sizes) must define sensible built-in defaults. Calling without arguments must yield a fully functional primitive. Callers never forced to manually assemble standard policies.
- **Directionality & Self-Wiring:** A sovereign concrete implementation is the sole authorized consumer that directly imports and instantiates its internal default policies for constructor default self-wiring. Callers outside the boundary must NEVER import, instantiate, or pass internal default policies. Internal default policy import by its owning primitive is intentional self-wiring, never an architectural leak.
- **Constructor-Configurable Policies (Build-Time Granularity):** Policies are composed at build-time, never swapped at runtime. Policies accept configurable thresholds/options/parameters in their own constructor with defaults for every parameter—eliminating need to pollute the primitive's contract with policy-specific settings while giving callers surgical, granular configuration control.

**1:1 Interface Directness & "Zero Private Methods" Litmus Test:**
- **Ultimate PFD Litmus Test:** The implementation has exact **1:1 correspondence** to the contract. Each public method reads top-to-bottom like plain English—pure sequential orchestration or direct transformation without branching mazes or indirection.
- **Zero Private Methods Invariant:** In a cleanly architected PFD system, there is virtually zero need for private helpers. If you designed the interface clearly, modeled DTOs strictly, and extracted opinions into injected policies, private methods signal: (1) *Un-Extracted Policy:* algorithm/strategy/calculation/threshold trapped inside—extract into policy contract. (2) *Improperly Modeled Contract:* interface fails to capture the true boundary, forcing multi-stage internal staging. (3) *Misplaced Responsibilities:* substrate wrangling belongs with domain DTOs or an outer decorator layer. When tempted by a private method, ask: *what boundary or policy did I fail to model?*

**Policy Architecture & File Layout:** Policies obey the exact same interface decoupling, pure DTO exchange, and 1:1 directness as core primitives. Three layout preferences: (1) *Single-File:* interface + small DTOs + concrete implementation (e.g. `SlidingWindowCompaction.cs`). (2) *Policy with Complex DTOs:* DTOs extracted to separate file alongside policy. (3) *Folder-Contained (Rich Sub-Domain):* multiple strategies/configurations contained in a dedicated domain folder (e.g. `compaction/`, `storage/`). This is organizational preference for cohesion—not dogmatically rigid.

These are **opinion and policy component primitives**, not core end-to-end primitives. Sometimes they grow complex enough to form their own boundary with own sub-opinions injected. The ~150-line rule applies across implementations. If an interface has one primary implementation, keeping both in the same file within ~150 lines is preferred. Same applies when combining interface, concrete class, and extensions.

**Anti-Gaming Laws (Strictly Banned):** Using `partial class`, subclassing, or language gimmicks to circumvent ~150-line test is a code smell. Using `ref`, `out`, or quirks is lazy patchwork. Splitting one 150-line file into five 30-line files is terrible—keep cohesive pieces together; exceeding ~150 lines signals un-extracted policies or god-object logic.

**Renaming Clarity:** Policy → **Opinion Sub-Primitives** | Primitive → **Core Primitives** | Layer → **Layered Co-Primitives**. All are primitives; everything is an interface.

Extension methods reside in the same file as their class/interface. Never create giant static classes (`TransformUtils`, `CommonUtils`) dumping helpers for all primitives. While policies are injected into implementations to decouple internal strategy, **LAYERS** observe, modify, intercept, or control end-to-end I/O flow externally.

---

## LAYERS & MIDDLEWARES
Layers are meant for core primitives controlling the system's core pillars end-to-end. Layers may feel unnecessary at first, but decorating a layer over a core primitive gives entire I/O control—classic HTTP/request pipeline middleware power with less bloat (pure decorators, no before/after delegate complexity). Like a mechanic plugging instruments directly into engine, body, chassis, or cabin. An `Engine` can have a sensor layer monitoring telemetry, or a user-mod layer improving mileage, without altering the core engine. Layer classes adopt the `Layer` suffix.

**Architectural Smells & Invariant Violations:**
- **Nested Containers Smell:** Never use nested containers (collections of collections, nested dicts, lists of tuples, deep generic wrappers) across contracts/DTOs. Model structured data as explicit, typed domain DTOs.
- **Untyped Escape Hatches:** Never use `Any`, `object`, `dynamic`, or generic property bags across contracts/DTOs. If an abstraction requires `Any`, domain types were not modeled.
- **Substrate & Runtime Leakage:** Never leak execution substrate types (framework handles, tensors, cursors, HTTP contexts, vendor SDK types) across primitive boundaries—encapsulate behind pure DTO boundaries.
- **Incomplete Primitive Smell:** A core primitive must be functionally sound alone. If an external layer is required for its primary responsibility, the primitive is incomplete.
- **Convenience Overload Sprawl:** Never pollute contracts with convenience overloads or parallel variants. Design a single sovereign signature; convenience belongs in callers/extensions.
- **Callbacks/Delegates/Hooks in Core Contracts:** Delegates and hooks in core contracts are smells indicating leaky lifecycle control. Permitted only at higher application layers (UI bindings, event dispatchers, plugin loaders).
- **Factory Patterns & Switch-Case Dispatch:** Usually smells hiding fundamental design issues and lazy polymorphic modeling. Genuine needs can warrant them, but usually signal un-extracted primitive boundaries.
- **Fragmented Parameters vs. Artificial Wrapper Bags:** *Distinct entities stay explicit:* sovereign primitives passed directly as arguments—**never manufacture artificial wrapper DTOs or middleman parameter bags** (Middleman Bag Smell). *Fragmented attributes collapse into cohesive DTOs:* loose strings/paths/IDs/flags describing the same entity belong in a single cohesive DTO with sensible defaults.
- **Meta-Naming Cop-Outs:** Never name namespaces/directories/files after patterns (`Manager`, `Service`, `Helper`, `Utils`, `Common`, `DTO`, `Contract`, `Components`). Name after domain nouns.
- **Silent Fallback & Implicit Degradation:** Never implement silent fallback paths or hidden downgraded modes within primitives/policies. Fail fast. When fallback is a genuine domain requirement, model explicitly as an outer composable policy or layer ($\lambda: P \to P$).

**Testing Policy vs. Layer:** If something is needed by other layers, it is an injected opinion sub-primitive. If it is an independent extension on a core primitive, it is a layer. Example: in AgentCore, compaction was considered a layer on context, but without compaction the agent cannot function when the window fills—making the primitive incomplete. Compaction is therefore an injected policy with strategies (sliding window, summarizer), while secondary snapshotting/externalization is clearly a layer since the primitive functions completely without it.

---

## DTOs
Pure data classes must not have business behavior. If they need behavior, it indicates misplaced responsibilities, missing sub-primitives, or poor primitive design. Pure transforms (e.g. `ToString()`) can be separate extension helpers colocated with the DTO. **Concrete by Default:** DTOs are passive domain records; interface contracts for DTOs are pure ceremony and speculative bloat. DTOs are concrete types by default.

**When DTOs Must Have Interface Contracts** (exactly two structural circumstances): (1) *Polymorphic Data Streams (Domain Event/Union Hierarchies):* Divergent data payloads flowing through the same boundary need an explicit contract for the shared domain concept. Consumers process polymorphically via exhaustive pattern matching. Case Study: AgentCore `IMessageEvent`—`MessageDelta` and `Message` are separate records with different structures, both flowing as `IAsyncEnumerable<IMessageEvent>`. Callers inspect polymorphically without degrading to untyped bags. (2) *Cross-Cutting Domain Data Capabilities:* Heterogeneous DTOs sharing an orthogonal data trait inspected by pipeline layers/storage without coupling to specific payloads (e.g. `IBinaryPayload` exposing bytes and MIME types across artifact/image/audio records).

In older AgentCore drafts, `Message` handled delta assembly and `IBlockEvent` had a `Start()` method (hidden factory on DTO). Removing those smells made context operational, messages pure DTOs, events pure passive contracts. **DTO Placement:** *Inline (1–2 small):* colocate at top of file before contract. *Dedicated file:* when complex, multi-field, or numerous—named after shared domain concept. **DTO File Naming Invariant:** File names must commonly represent all items held, preferring shared concept or common suffix. Never use meta cop-outs (`dto`, `dtos`, `models`, `types`, `contract`, `schema`).

---

## NATURAL SYMMETRY & ARCHITECTURAL PURITY
Natural symmetry and architectural purity are two complementary, yet fundamentally distinct forces in Primitive-First Design:

### 1. Architectural Purity (The Deliberate Standard)
Purity is not an emergent accident; it is an uncompromising standard committed to upfront, governing the highest-level composition root:
- **The High-Level Consumption Invariant:** The highest-level orchestration layer consuming core primitives must read as pure and direct as pseudo-code or plain English. If orchestrating primitives requires intermediate glue, state staging, or awkward mediation, the primitives are improperly modeled. Never hide sprawl behind a god-class or opaque single-line launcher (`var app = app.start()`); provide a pure orchestration flow anchored by a clean, fluent composition builder.
- **Universal Invariant — Zero Intermediate Orchestration Glue:** Primitives natively own their internal data lifecycles, preparation, and boundary transformations. The primary orchestration flow must never be polluted by mediator abstractions, transient state holders, or coordinator shims. The central loop consists purely of direct interactions between sovereign primitives.
  - *Case Study:* In earlier AgentCore iterations, an intermediate component gathered streaming chunks before handing completed messages to context. Demanding purity—that the central loop read like pseudo-code—revealed chunk assembly was an internal ingestion policy owned by context (via injected policy), eliminating mediator glue:
```csharp
do {
    await foreach (var evt in Context.WriteAsync(LLM.GenerateAsync(prompt, toolDefs)))
        if (evt is MessageDelta { Content: ToolCall tc }) (toolCalls ??= []).Add(tc);
    if (toolCalls is not null)
        await foreach (var evt in Context.WriteAsync(Toolbox.ExecuteAsync(toolCalls))) ...
} while (toolCalls is not null);
```

### 2. Natural Symmetry (The Emergent Discovery)
While Purity is a deliberate constraint enforced by subtraction, Symmetry is an internal emergence discovered iteratively:
- **Symmetry as Discovery Compass:** As you plan core primitives, spot hints of symmetry across peer pillars. When one primitive exhibits a capability, ask why its peer does not. Artificial asymmetry is almost always evidence of unexamined assumptions or overfitted boundaries.
- **Universal Invariant — Parallel Flow Unification Across Interacting Boundaries:** When peer boundaries appear fundamentally different, seeking symmetrical shapes often reveals they are different manifestations of the same conceptual flow. Case Study: Initially `Toolbox` was non-streaming. Seeking symmetry pushed: *why shouldn't tools stream?* Long-running executions, status notifications, and progress updates naturally stream, and the UI was already streaming. Designing `Toolbox` to stream the same domain message events (`IMessageEvent`) revealed **tools are fundamentally the same as LLMs—both stream context into Context**. Without pursuing symmetry, this truth would never have emerged.
- **Symmetrical Domain Naming:** Parallel domain nouns chosen meticulously across all peer contracts (`llm`, `context`, `tool` → `ILLM`, `IContext`, `IToolbox`), rejecting procedural verbs or action cop-outs (`tooling`, `tool_executor`).

### 3. The Triad: Structural Symmetry & Purity
- A **Policy** is a Primitive on the *inside* (injected sub-primitive completing internal strategy).
- A **Layer** is the same Primitive on the *outside* (decorated co-primitive extending I/O: $\lambda: P \to P$).
- **DTOs and Pure Transforms** are the passive binder holding boundaries together without behavioral coupling.

---

## FOLDER / NAMESPACE STRUCTURE
Folder structure and namespaces are physical manifestations of the architectural model:
- **1:1 Topology Match:** Folders/namespaces match 1:1. Disk layout directly reflects the boundary tree. Solutions, projects, and directories define boundaries. Root hosts only sovereign entrypoints or composition roots, zero orphan files.
- **Every Primitive Gets Its Own Holistic Directory:** A true primitive is never a bare isolated file beside another. If a component has no policies or layers, it is not independent—it is a policy of an existing primitive. Because any true primitive has policies (and optional layers), it naturally commands its own directory. **Holistic Directory Naming:** represents everything inside as collective capability—never duplicating an inner class name, never meta cop-outs (`components`, `helpers`, `utils`, `common`, `services`, `managers`, `dto`).
- **Primitive Directory Root:** Reserved for sovereign primitive contract, primary concrete implementation, boundary exports, and root DTOs—immediately identifiable at first glance.
- **Policies & Layers (`policies/`, `layers/` or Domain-Named Folders):** `policies/` and `layers/` are structural defaults under a primitive root. **Zero Cross-Policy Coupling & Flat Siblings Invariant:** policies within `policies/` are strictly independent flat siblings consumed only by the sovereign primitive. One policy must NEVER consume another beside it—if it does, it has become an independent primitive and must be promoted to its own folder. **Domain naming always preferred** when a clear domain noun exists (e.g. `storage/`, `auth/`), rather than blindly falling back to the meta names `policies/` or `layers/`. Decorator classes adopt `Layer` suffix. Keep simple folders flat; no single-file directory wrappers.
- **Natural Primitive Promotion Law (Sibling Placement):** When an injected policy grows complex enough for own policies/strategies/layers, it has become a primitive. It must never remain buried in the consumer's folder—promoted to its own holistic domain directory as a sibling. This rule is fractal: `Car/` consumes `Engine/` beside it; `Engine/` can consume another sub-primitive beside it when complexity warrants.
- **Behavioral File Naming:** Files named after the primary concrete class. Interface-only files take the contract's name. Contracts define universal domain roles, while implementations express specific domain strategies; the file adopts the concrete implementation's name. Never adopt meta-labels (`contract`, `interface`, `impl`, `base`).
- **Rigorous Domain Naming:** All boundaries and files named using strict domain nouns, avoiding procedural verbs or gerunds. Directories NEVER adopt generic bucket or meta-pattern names.
- **~150-Line Cognitive Limit & Co-Location:** Single source file must not exceed **~150 lines**. Never blur interfaces, implementations, and multiple DTOs in one tangled file. Clean co-location patterns: **Option A (Contract + Concrete):** colocate in single file named after concrete class; 1–2 small DTOs can live at top, complex DTOs extracted. **Option B (Policy File):** single-file (interface + small DTOs + concrete), or complex DTOs in separate file, or folder-contained for rich sub-domains. **Option C (Boundary Definition):** interface + tightly coupled DTOs in one file for boundary clarity, concrete in its own file. **Option D (Dedicated DTO File):** numerous/shared DTOs grouped by collective domain concept. If any file approaches ~150 lines, separate into dedicated adjacent files.

---

## IT APPLIES TO ALL CREATIVE WORK
PFD is not limited to backend code. It applies to UI, low-level code, specifications, and all creative work. Every creative work has core primitives, opinion sub-primitives, and layered co-primitives:
- **UI Architecture (WPF / Forms / Web):** A Form `UserControl` is the Core Primitive (exposing parameters, bounds, styling, and action buttons); form inputs (Name, Email) are DTOs; validation rules and template styles are Policies; host page wrappers, modal dialogs, and container templates are Layers.
- **Text Documents & Specifications:** The core thesis is the Primitive; decision rules and methodologies are Policies; examples, appendices, and walkthroughs are Layers.