# Axiomatic Derivation Architecture (ADA)
## A Foundational Theory of Bedrock Axioms and Derived Software Systems

---

### The Core Thesis & The Soul of ADA

> **"Correctly identifying the fundamental primitive of a system naturally minimizes its architecture, because unnecessary abstractions become redundant when the primitive itself correctly represents the underlying problem; once the primitive is correct, composition, injectable policies, and generic layers provide extensibility without requiring the core primitive to continuously grow new abstractions."**

### 1. Correct Code Will Always Be Minimal
A smell-less design is **naturally minimal**. 
- Whatever the intrinsic difficulty of a domain, the correct design is its **minimal possible representation**.
- Not all minimal code is correct (code golf is an anti-pattern), but **correct code is always minimal**. Minimal code is the natural side-effect of good design.

### 2. The Root Cause of Bloat: Developer Laziness & Convenience Layers
Software bloats when developers ask *"What feature do I add?"* rather than *"What is the irreducible primitive of this domain?"*:
- **Convenience Bloat:** When a requirement doesn't fit, developers lazily invent wrapper layers, helper overloads, and pass-through adapters instead of fixing the latent design flaw in the primitive.
- **The "Inside vs. Outside" Script Fallacy:** Treating operational tasks (training, benchmarks, evaluation) as loose procedural scripts creates untyped hack sinkholes.
- **Abstraction Theater:** Wrapping procedural spaghetti in superficial interfaces without identifying the underlying primitive creates indirection without abstraction.
- **The Anti-Bloat Imperative:** If you fix the root design smell in the existing primitive, the refinement cleanly covers both existing and new requirements—eliminating the need for wrappers.

### 3. A Universal Lens for Representation Reduction
At its deepest level, ADA is a method for **reducing and restructuring representations** across technical domains:
- **In Software Systems:** Primitive ($P$) + Injected Policies ($\pi$) + Composable Layers ($\lambda$).
- **In Storage Systems:** Block Storage Engine (Axiom) + Eviction/Partitioning (Policies) + WAL/Encryption/Caching (Layers).
- **In Documentation:** Canonical System Spec (Axiom) + Audience Lenses (Policies) + Version/Auth Guards (Layers). Docs rot when developers lazily append contradictory convenience pages instead of updating the bedrock spec.
- **In User Interfaces:** Semantic Layout Component (Axiom) + Breakpoint/Theme Policies + Auth/Boundary Layers.

### 4. Applying ADA: Greenfield vs. Legacy
- **Greenfield Construction:** Identify the irreducible domain primitive first. Parameterize internal execution via injected policies, and decorate cross-cutting concerns via composable layers.
- **Legacy Infrastructure Unbloating (The Diagnostic Lens):** Look *through* accidental complexity: isolate what the system was actually trying to achieve (the latent Axiom), strip away accumulated convenience wrappers and glue, and re-derive the capability cleanly.

---

## 1. The Architecture: The Axiom & Its Derivations

Every operational domain decomposes into an irreducible bedrock truth (**The Axiom** or **Primitive**) and its clean **Derivations**:

```text
┌─────────────────────────────────────────────────────────────┐
│                 External Consumers & Runners                │
│                 (CLIs, Host Apps, Orchestrators)            │
└──────────────────────────────┬──────────────────────────────┘
                               │ orchestrates
┌──────────────────────────────▼──────────────────────────────┐
│             THE AXIOMATIC DERIVATION (BOUNDARY)             │
│                                                             │
│       ┌──────────────────────────────────────────────┐      │
│       │      Derived Layers: Composable Decorators   │      │
│       │      (Cross-cutting concerns wrapping P)     │      │
│       └──────────────────────┬───────────────────────┘      │
│                              │ wraps                        │
│       ┌──────────────────────▼───────────────────────┐      │
│       │      The Core Axiom / Primitive (P)          │      │
│       │      (Irreducible Bedrock: WHAT it does)     │      │
│       └──────────────────────▲───────────────────────┘      │
│                              │ injects                      │
│       ┌──────────────────────┴───────────────────────┐      │
│       │      Derived Policies: Swappable Strategies  │      │
│       │      (HOW internal steps execute)            │      │
│       └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### The Irreducible Components:
1. **The Core Axiom / Primitive ($P$):** Irreducible contract defining *what* the capability is, grounded in real-world domain metaphors. Minimal surface area, single responsibility, pure semantic intent.
2. **Derived Injected Policies ($\pi$):** Swappable strategies injected at initialization defining *how* internal steps execute (algorithms, tokenizers, loss objectives). Keeps the primitive stable and invariant forever. Named with pure agentive/doer nouns (`Resolver`, `Selector`, `Sampler`), avoiding redundant `*Policy` suffixes.
3. **Derived Composable Layers ($\lambda$):** Endomorphic decorators ($\lambda: P \to P$) wrapping the primitive externally without interface drift. Any cross-cutting concern (retries, rate limiting, persistence, guardrails, latency profiling) is a Layer—never internal logic. Every layer must carry the `*Layer` suffix.
4. **External Consumers & Runners:** Host applications, CLI entrypoints, and benchmark harnesses that instantiate and drive boundaries from the outside. Verification and evaluation are operational consumers, not architectural boundaries; running a benchmark against ground truth is simply exercising the execution primitive (`decide()`) over test data.
5. **Universal Boundary Invariance ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$):** Every operational boundary encapsulates exactly ONE primary primitive. Shared foundations (e.g. neural weights substrates) co-consumed across multiple boundaries command their own autonomous foundation boundary.

---

## 2. The Behavioral Interface Mandate

### 2.1 Interface-First for Any Object That Exhibits Behavior
> **"Every class or object that performs computation, transformation, execution, or I/O must be defined by an explicit interface. Never expose or depend directly upon concrete classes."**

#### Why Concrete Classes Without Interfaces Cause Decay:
1. **Unchecked Bloat Creep:** Without an interface contract, developers casually append convenience methods, internal getters, and procedural mutations, causing classes to balloon into God objects.
2. **Hidden Internal Coupling:** Callers bind to implementation quirks and private data representations, making refactoring or swapping substrates impossible.
3. **Breakdown of Layering:** Endomorphic layering ($\lambda_P: P \to P$) mathematically requires a stable contract $P$. Without an interface, decoration degenerates into fragile subclassing or procedural monkey-patching.

### 2.2 The Anatomy of an Irreducible Contract
An interface in ADA is strictly **irreducible**:
1. **Minimal Surface Area:** Single-responsibility capability with minimal methods. A 15-method interface monster is an immediate smell of a bloated God contract.
2. **Zero Convenience Bloat:** Exactly one canonical method per distinct semantic capability. Absolute prohibition on helper overloads (`With*`, `Run*`, sync-over-async wrappers). Redundant caller sugar is forbidden.
3. **Pure Semantic Intent:** Defines *what* is achieved in domain language, completely abstracted from underlying hardware, network, or storage mechanics.

### 2.3 The Rule of Two (No 1-to-1 Mirror Interfaces)
> **"Never mirror a single concrete class with a 1-to-1 interface or intermediate pass-through wrapper unless there are at least two distinct concrete implementations or consumers."**
- **Indirection Without Abstraction:** Declaring an interface that merely mirrors a single concrete class 1:1 adds cognitive clutter without polymorphic value.
- **When Interfaces Are Mandatory:**
  - **Boundary Primitives ($P$):** The root primitive must have an explicit interface to anchor the endomorphic layer decorator ($\lambda_P: P \to P$) and decouple callers.
  - **Swappable Injected Policies ($\pi$):** Required when an internal step admits multiple strategies or algorithms ($\ge 2$ implementations or consumers).
- If a class represents a single concrete dependency with zero polymorphic alternatives and no layer decoration, consume it directly. Zero speculative abstractions.

---

## 3. Boundary & Repository Topology

ADA enforces strict geometric alignment between **logical namespaces** and **physical directory structures**. 

### 3.1 The Canonical Topology: Boundary-First Cohesive Derivation
Horizontal tier-first dumping (`core/`, `policies/`, `layers/` at root) is strictly forbidden. Every operational boundary commands its own cohesive derivation centered around **exactly one irreducible primitive** ($1 \text{ Boundary} \equiv 1 \text{ Primitive}$):

```text
RepositoryRoot/
├── [DomainBoundaryA]/          # Boundary A: Encapsulates Primitive A (Cluttered Scale)
│   ├── primitive.ext           # THE ONE PRIMITIVE (Contract & Implementation)
│   ├── schema.ext              # Pure immutable domain value objects
│   ├── policies/               # Injected strategies (partitioned when >= 4-5 items)
│   │   ├── strategy_1.ext
│   │   └── strategy_2.ext
│   ├── layers/                 # Composable decorators (λ_A: A -> A)
│   │   ├── profiling_layer.ext
│   │   └── guardrail_layer.ext
│   └── data/                   # Boundary-owned assets (fixtures, baselines, weights)
├── [DomainBoundaryB]/          # Boundary B: Encapsulates Primitive B (Lean Scale: Flat)
│   ├── primitive.ext           # THE ONE PRIMITIVE (Contract & Implementation)
│   ├── objective.ext           # Injected policy (flat, no 1-file folder ceremony)
│   └── checkpoint_layer.ext    # Composable decorator (self-documenting via *Layer suffix)
├── cli.ext                     # Root external runner / orchestration entrypoint
└── tests/                      # Contract verification & regression tests
```

### 3.2 The Clutter-Threshold Rule (When to Subfolder vs. Stay Flat)
- **Lean Boundaries ($\le 3–4$ files):** Keep the boundary flat. The primitive (`trainer.py`), policy (`loss.py`), and layer (`checkpoint_layer.py`) live directly at the boundary root.
- **Cluttered Boundaries ($\ge 4–5$ policies or layers):** Subordinate policies and layers into dedicated `policies/` and `layers/` subfolders.
- **Zero Single-File Folders:** Never create a directory or separate namespace for a single file.

### 3.3 Functional Asset Ownership & The Pristine Root
- **The Functional Ownership Principle:** Every dataset, benchmark fixture, or weight checkpoint must be co-located with the specific operational boundary that produces or exclusively consumes it (e.g. golden evaluation fixtures in `inference/data/`). Never scatter assets into horizontal dumping grounds at root (`data/`, `results/`).
- **The Pristine Root Principle:** The repository root contains only primary operational packages, orchestration entrypoint (`cli.ext`), contract tests (`tests/`), and standard packaging configs (`pyproject.toml`, `.gitignore`, `README.md`, `AGENT.md`). Everything else is an architectural leak.
- **Zero Residual Debris:** Build caches (`__pycache__`), temporary logs, scratch runs, and disposable experiment debris must never linger in source trees.

---

## 4. Concrete Domain Instantiations

ADA has been empirically proven across fundamentally different software domains:

### 4.1 Autonomous Agent Execution (e.g., [AgentCore](file:///D:/CodeBase/AgentCore))
- **The Primitive Triple:**
  - Reasoning: `ILLM` (`GenerateAsync`) — 16 lines.
  - Acting: `IToolbox` (`GetDefinitionsAsync`, `ExecuteAsync`) — 28 lines.
  - Remembering: `IContext` (`WriteAsync`, `ReadAsync`) — 20 lines.
- **The Execution Loop:** ReAct fixed-point loop expressed in **35 lines of code**.
- **The Layer Suite:** `InputGuardrailLayer`, `RetryLayer`, `ToolApprovalLayer`, `ChatPersistenceLayer` (WAL durability).
- **Result:** Complete agent framework implemented in under 1,000 lines of code, outperforming 20,000-line competing frameworks in latency, complexity metrics, and test coverage.

### 4.2 Neural Decision Engines (e.g., [NanoLLM](file:///D:/CodeBase/NanoLLM))
- **The Decision Basis:**
  - `IDecisionEngine`: Domain semantic decision (`decide`).
  - `NanoModel`: Foundational tensor substrate (`forward`).
- **Injected Policies:** `ISlotAssembler` (token layout), `IResolver` (logit calibration), `CalibratedLoss` (multi-task objective).
- **Composable Layers:** `ProfilingLayer` (CUDA-synchronized latency), `HierarchicalLayer` ($O(\sqrt{N})$ clustered routing).
- **Result:** Sub-35ms calibrated decision-making on 149M parameters, beating commercial frontier models on tool-routing accuracy and latency.

---

## 5. Summary Checklist: The ADA Smell Detector

| Diagnostic Question | If YES (Clean Design) | If NO (Smell Detected) |
|---|---|---|
| **Irreducible Primitive?** | Contract defines pure domain capability ($P$) | God class, procedural manager, or multiple overlapping types |
| **Injected Execution?** | Internal steps injected via swappable policy interfaces ($\pi$) | Hardcoded switches, boolean toggles, or inheritance subclasses |
| **Cross-Cutting Layers?** | Composable endomorphic decorator ($\lambda: P \to P$) with `*Layer` suffix | Bloating the execution loop or mutating the base contract |
| **Behavior Behind Interfaces?** | 100% of behavioral components defined by explicit interfaces | Concrete classes directly exposed to callers |
| **Method Surface & Overloads?** | Minimal methods, zero convenience aliases or `With*` sugar | Bloated interfaces with convenience overloads and helper wrappers |
| **Interface Mirroring?** | Decouples polymorphism or layer decoration ($\ge 2$ impls/consumers) | 1:1 mechanical passthrough interfaces adding indirection without abstraction |
| **Boundary Independence?** | Exactly 1 primitive per boundary; shared substrates autonomous | Multiple primitives per boundary, or horizontal tier-first dumping (`core/`) |
| **Asset Ownership & Clean Root?** | Assets co-located in consuming boundary; pristine root | Loose `data/`, `results/`, or scripts scattered at repo root |

