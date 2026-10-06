---
name: primitive-first-design
description: >-
  Applies Primitive-First Design (PFD) to software architectures. Activate when commanded with
  "Apply PFD", designing systems, reviewing interface contracts, eliminating bloat/glue, or refactoring.
---

ATA (shall be renamed Primitive-First Design / PFD) basically argues that **correct code is usually minimal**. Most abstractions are bloat to patch a poor foundational design primitive. If we design core primitives right in any system design, then naturally code gets minimal, code smells get reduced, and the system becomes scalable, readable, maintainable, and just better.

We judge ATA by number of code lines, which is not completely correct, but it is the best proxy metric we can have when you take an entire codebase of a system end to end. Most importantly, ATA is **not** putting all code in a single class or writing convoluted one-liners to reduce code lines.

ATA is a set of principles and decisions to get minimal code with no code smell—yielding high-signal, condensed, and dense output.

A rough test is that an average system designed cleanly end to end usually hovers around **~5k lines** with ATA if not too complex or hugely loaded with batteries. The core of the core project or namespace that contains all core primitive implementations and its opinion primitives—in other words, the bare-bones project that can run—will be around **1–1.5k lines max**. This is just to give an idea, not a hard rule or magic number.

*Interface* is a Java/C# term, but means traits in Rust, protocols in Python, or abstract contracts in Go/C++.

---

## CORE PRIMITIVES

Everything is and must be an interface (of course except DTOs, transforms, helpers, etc.). No concrete access anywhere: **the interface is the only truth**. Zero backdoor access; the interface must always be respected.

This interface mandate is a cognitive forcing mechanism to force you to think and design contracts better, instead of conveniently abusing a class to expose anything you want at any time.

An interface should be a symbol of decoupling—never add coupling into it. A concrete implementation can have hard couplings injected (and even then, injected via interfaces) or have its own internal opinions, but the interface itself is meant to be pure. For example, a car engine primitive contract shouldn't take a `MitsubishiEngineCylinder` as a parameter; it should take `IEngineCylinder`, or simpler types.

Any complex object in a core primitive contract should also be an interface defined by us (our own DTO or sub-primitive). Rarely, we may need something external—for example, like `Newtonsoft.Json` in C# long ago where everyone used it like second nature as if it were a native C# object. Even in those rare cases it is still not preferred. Types crossing a core primitive contract should either be fundamental language primitives (`int`, `string`, `decimal`, etc.), our own passive DTOs, or `I<OurInterface>`.

A primitive represents what we expect from something. In OOP, we design based on real-world objects. For example, if a car is designed, the primitives define clearly what the core primitives in a car are:
* **Engine** (gearbox, fuel tank, etc.)
* **Body** (lights, door, storage, etc.)
* **Chassis** (wheels, steering)
* **Usable Area / Cabin** (seats & dashboard)
* **Control Bus**

The entire car, if done cleanly, has only 5 primitives. These primitives can be modeled into clean interface contracts, and if done right, a car can be built end to end with just these 5 contracts used together.

The same applies to [AgentCore](https://github.com/MrRazor22/AgentCore): look at how cleanly `IContent`, `ILlm`, and `IToolbox` compare to even Microsoft Agent Framework or LangChain.

Core primitives must be irreducible and represent an operational boundary, not simply an arbitrary OOP component.

We see clear, obvious boundaries like the examples given. Sometimes, if a boundary is not clear, we model it based on the need for it: who uses it and what the user wants from it gives a hint of the boundary.

However, **we should never narrowly design an abstraction to satisfy the immediate need**. Through the current need, look in general at what is expected that satisfies the current need perfectly, but will also be ideal for future needs and scaling. That is where great primitive design lies. In rare cases, we model based on other examples of similar works.

For example, in AI agents we have RAG, memory, and content. But if you see clearly, an agent fundamentally needs current content in its context window to work. The primary need is `IContent`. All the rest—memory and RAG—are either policies (injected sub-primitives) or layers (decorators, middlewares).

A poor design would create `IMemory` and `IContent`, saying `IMemory` will have `IRag` and store memory, while `IContent` will have working memory. That sounds neat and resembles textbook OOP, but it falls into the trap of **"only narrowly satisfying the current need."** What if in the future you want to add a new source of context? Or expose memory as tools the AI agent invokes rather than auto-injecting it? This overfitting should be avoided. A simple `IContent` where memory and RAG are layers remains naturally minimal, neither overfitting nor underfitting. In some cases where the domain is very new, boundaries can be unclear to model based on pure OOP.

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

Interface design must be done meticulously. For example, in `AgentCore`, `IContent` could simply expose messages or synchronous/asynchronous write methods. But we took a universal opinion: an agent streams from the LLM level to the user. If needed, let the user accumulate it, or expose helper transfer methods at the top, not as a core contract.
* In `WriteAsync`, we could have simply returned `IContentEvent` because the user agent only exposes that. That exact narrow trap was avoided. The interface was not restricted: `IContent` returns complete `IMessageEvent` streams with full message and content events, and the agent decides to cast and expose content events as needed. Present needs are satisfied perfectly without awkward, future-only designs.
* Unnecessary methods were excluded from `IContent`:
  * *No `Clear()`:* Agents in the future do not need to clear their own memory (a universal opinion taken). If needed, session injection exists in the persistence layer; let the session store clear itself at a higher level.
  * *No raw chat history getters:* An operational boundary is an active contract, not a passive data holder.
  * *No narrow methods like `UpdateTokenUsage()`:* Token usage arrives directly from LLM response events (`IMessageEvent`), not through separate mutation methods.
  * *No update full message methods:* We made a universal opinion to support stream injection directly, with helpers to directly append messages if needed via the same primitive.

Sometimes a natural symmetry arises in primitive design across the system. In `AgentCore`, all three pillars have symmetry where they become the core pillars the agent needs, and all three are streaming. Initially, tooling was not streaming. But the motivation to find symmetry pushed the realization: tools stream too (if not literal text like an LLM, tools stream notifications and progress for long-running executions). Since the UI for the agent streams, tooling was designed to stream the same message events. Tooling streams `IContentEvent`, which can also be complete content. Finding symmetry revealed that tools are fundamentally the same as LLMs: both stream context into the agent's content, which is literally the agent loop. Without seeking symmetry, this insight would never have emerged.

Exposing properties in interfaces (in languages like C#) is usually not preferred. It cannot be cleanly layered, intercepted, or scaled if a getter or setter requires complex asynchronous operations in the future. If simple synchronous exposure avoids two getter/setter methods, it can be exposed, but pure action methods remain preferred.

A good test is if an interface crosses more than **4–5 methods**: usually its needs are not correctly judged, it is doing too much, or it is modeled around a wrong or non-existent boundary. The 4–5 method rule is not strict, but serves as a warning to think deeper.

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

Layers may feel unnecessary at first, but decorating a layer over a core primitive gives entire input and output control. This offers the power of ASP.NET Core middleware with less bloat (pure decorators with no before/after delegate complexity).

Layers provide direct extension over core primitives—like a mechanic plugging measuring instruments directly into an engine, body, chassis, or cabin to diagnose or customize it. That is how powerful they are for extensibility, scaling, and control.
* An `Engine` primitive can have a sensor layer monitoring engine parameters and telemetry, or a user-mod layer improving mileage, without altering the core engine.

**Smells in Core Primitives vs. Higher Layers:**
* Callbacks, events, delegates, and hooks are usually code smells resulting from poor primitives, but can be used as conveniences at higher layers of an application design (UI bindings, orchestration, plugin loaders)—never as part of core primitive design.
* Factory patterns and switch-case initializations are usually smells hiding fundamental design issues. Genuine needs can warrant them, but using them is usually a sign of lazy design.
* Always use strictly typed code where supported (e.g., avoiding `object` in C# to get around design issues).

**Testing Policy vs. Layer:**
* If something is needed by other layers, it is an injected opinion sub-primitive, not a layer.
* If it is an independent extension on top of a core primitive, it is a layer.
* For example, in `AgentCore`, summarization was originally considered a layer on top of content. But compaction is triggered on token usage: if the context window fills, it must compact. Without a form of compaction, the agent cannot function. **A core primitive on its own must be functionally sound; if a layer is needed to make a primitive functional, that is a design smell.** If compaction were an external layer, the core primitive would be incomplete. Therefore, compaction is an injected policy (opinion sub-primitive) with strategies like sliding window or summarizer, while persistence is clearly a layer because the agent functions completely in-memory without persisting.

---

## DTOS

Pure data classes must not have business behavior in their core class. If they need behavior, it indicates misplaced responsibilities, missing opinion sub-primitives, or poor foundational primitive design.
* Pure transform methods (e.g., `ToString()`) can be separate extension helpers close to or in the same file as the DTO class.
* DTOs do not need interfaces because they are data. Conversely, primitives are not mere data holders or wrappers (`IContent` is not a wrapper for chat history in `AgentCore`).
* In `AgentCore`, `Message` could have been made to hold assembling logic and metadata accessors, but that hurts extensibility. `Message` is purely a DTO. In older drafts, `Message` handled delta assembly, and `IBlockEvent` had a `Start()` method so each content type knew which delta object to receive (acting as a hidden factory on a DTO). Removing those mixed smells made content an operational primitive, messages pure DTOs, and message/content events pure passive DTOs.

---

## NATURAL SYMMETRY AND PURITY

In `AgentCore`, the ReAct loop does not contain anything other than the three core primitives—no extra abstractions like assemblers or accumulators. In previous drafts, tools and LLMs streamed, and an assembler assembled complete messages before adding them to context. With the right primitive design, content accepts message events directly, and adding full messages became an optional helper. Content owns assembly internally. Keeping the ReAct loop pure makes it as simple as pseudo-code:
```csharp
while (content.NeedsExecution()) {
    for (event in llm.Generate(content))       content.Consume(event);
    for (event in toolbox.Execute(content))   content.Consume(event);
}
```

When designing correctly, a natural symmetry emerges that unlocks the best interface design for primitives.

Naming should be done meticulously. In `AgentCore`, folder and namespace names are clean, symmetrical nouns (`llm`, `content`, `tools`), and the core primitives are parallel nouns (`ILlm`, `IContent`, `IToolbox`). `IToolbox` is a parallel noun, avoiding awkward verbs like `ITooling` or `IToolExecutor`.

As you plan core primitives, hints of symmetry indicate a clean representation of the system. For purity, high-level orchestration layers (`Agent.cs`) use clean fluent builders, avoiding lazy `var app = app.Start()` god-classes.

**The Unified Symmetry:**
* A **Policy** is just a Primitive on the *inside*.
* A **Layer** is just the same Primitive on the *outside*.
* **DTOs and transforms** are the glue or binder that holds them together.

---

## FOLDER / NAMESPACE STRUCTURE

Folder structure and namespace boundaries are critical:
* If a codebase has 2–3 files, keeping them flat in a single folder is fine.
* When files grow, create clear namespace and folder boundaries for correlated items. Primitives represent file-level boundaries; namespaces represent the layer above.
* Folders and namespaces must match 1:1. Disk layout is the physical representation of the namespace hierarchy.
* Solutions, projects, and folders are boundaries. Scope related items together; **zero orphan files in root** under any boundary.
* **The Trie Test:** The directory structure should match the trie you would draw of the system's primitives end to end. In `AgentCore`, 3 clean folders mirror the 3 core primitives (`Llm`, `Content`, `Toolbox`), keeping the entire design walkthrough visible at a glance.

---

## IT APPLIES TO ALL CREATIVE WORK

PFD is not limited to backend code. It applies to UI, low-level code, specifications, and all creative work. Every creative work has core primitives, opinion sub-primitives, and layered co-primitives:
* **UI Architecture (WPF / Forms / Web):** A Form `UserControl` is the Core Primitive (exposing parameters, bounds, styling, and action buttons); form inputs (Name, Email) are DTOs; validation rules and template styles are Policies; host page wrappers, modal dialogs, and container templates are Layers that decorate the form without modifying its core control.
* **Text Documents & Specifications:** The core thesis is the Primitive; decision rules and methodologies are Policies; examples, appendices, and walkthroughs are Layers.