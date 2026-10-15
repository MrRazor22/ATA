---
name: pfd-audit
description: >-
  Post-implementation PFD violation scanner. Invoke after any implementation, refactor, or bug fix
  to catch violations against primitive-first-design rules. Hard checklist, zero tolerance.
---

Scan all changed/created files against every rule below. For each violation: report the file, line, and rule number. A rule is a rule — zero softening, zero excuses.

**Mechanical Scanner:** Run [scan.py](./scripts/scan.py) (`python <skill_dir>/scripts/scan.py <project_path> [previous_line_count]`) first to catch automatable violations (line counts, private methods, banned names, interface method counts, untyped escapes, callbacks). Then manually verify the semantic rules below that the script cannot check.

Authoritative source of truth: the `pfd` skill (`/pfd`). To iteratively fix violations and compress, invoke the `pfd-iterate` skill.

---

## CONTRACT PURITY
1. Every component with behavior has an explicit interface contract — zero un-interfaced workers, zero intermediate classes.
2. Interface methods ≤ 4–5 max — exceeding means wrong boundary or god-class.
3. Every method signature takes and returns pure passive DTOs or native primitives only — zero framework, runtime, hardware, or third-party types crossing the boundary.
4. Zero `Any`, `object`, `dynamic`, untyped containers, or generic property bags (`dict[str, Any]`) in any contract or DTO.
5. Zero convenience overloads, parallel variants (`Do()`/`DoBatch()`), or bloat helpers (`IsAvailable()`, `ShouldProcess()`, `GetBatch()`) in contracts — one sovereign signature per operation.
6. Zero callbacks, delegates, or hooks in core primitive contracts — permitted only at higher application layers (UI, event dispatchers, plugin loaders).
7. Zero exposed properties in interfaces — action methods are the rule. Only exception: a simple synchronous getter that genuinely avoids two methods.
8. Interface is pure decoupling — zero coupling, zero framework opinions, zero implementation machinery leaked into the contract.
9. Every injected collaborator defined by an explicit interface contract — zero concrete backdoor classes anywhere.
10. Sub-primitives and policies are constructor-injected dependencies, NEVER passed as method parameters across contract boundaries.

## IMPLEMENTATION DISCIPLINE
11. Every file ≤ ~150 lines — zero exceptions, zero `partial class`, zero subclassing gimmicks, zero artificial file splitting to game the number.
12. Exact 1:1 correspondence between interface contract and concrete implementation — each public method maps directly to one contract method.
13. Zero private methods — any private method is an un-extracted policy, improperly modeled contract, or misplaced responsibility. Extract it.
14. When PFD is done right, methods read like plain English with zero eccentric paradigm smells — an outsider with zero PFD knowledge finds the code immediately obvious, natural, and clean.
15. All opinions and policies injected — even simple changeable numbers injected, never hardcoded.
16. Constructor injection with built-in defaults for every parameter — zero mandatory policy assembly, fully functional out of the box with no arguments.
17. Only the owning primitive imports and instantiates its internal default policies (self-wiring) — callers outside the boundary NEVER import or pass internal defaults.
18. Policies composed at build-time only — zero runtime swapping.
19. Zero `ref`, `out`, or language quirks as lazy patchwork to avoid modeling the actual smell.
20. Extension methods live in the same file as their class/interface — zero giant static utility classes (`TransformUtils`, `CommonUtils`).

## POLICY & LAYER ARCHITECTURE
21. A core primitive is functionally sound alone — if an external layer is required for its primary responsibility, the primitive is incomplete.
22. Policies within `policies/` are strictly independent flat siblings — one policy NEVER consumes another beside it.
23. If a policy consumes another policy, the core primitive design is wrong or the policy has become its own primitive and must be promoted to its own directory.
24. Policies obey the exact same rules as core primitives: interface contract, pure DTOs, 1:1 directness, ≤150 lines, zero private methods.
25. Zero nested containers (collections of collections, nested dicts/maps, lists of tuples, deep generic wrapper chains) across contracts or DTOs — model as explicit typed domain DTOs.
26. Zero substrate or runtime type leakage (framework handles, tensors, cursors, HTTP contexts, vendor SDK types) across any primitive boundary — encapsulate behind pure DTO boundaries.
27. Zero silent fallbacks, hidden degraded modes, or swallowed errors — fail fast. Fallback resilience is an explicit outer composable layer ($\lambda: P \to P$), never sneaky backdoor logic.
28. Factory patterns and switch-case dispatch must be explicitly justified — they almost always signal un-extracted primitive boundaries or lazy polymorphic modeling.

## DTO DISCIPLINE
29. Pure data classes have zero business behavior — if behavior is needed, responsibilities are misplaced or a sub-primitive is missing.
30. DTOs are concrete types by default — interface contracts only for polymorphic data streams (domain event/union hierarchies) or cross-cutting data capabilities.
31. Pure transforms (e.g. `ToString()`) are colocated extension helpers, never methods on the DTO class itself.
32. DTO file names represent all items by shared concept or common suffix — zero meta cop-outs (`dto`, `dtos`, `models`, `types`, `contract`, `schema`).

## NAMING & FOLDER STRUCTURE
33. 1:1 folder/namespace topology — disk layout directly mirrors the architectural boundary tree, zero orphan files.
34. Every true primitive has its own holistic directory — a bare isolated file sitting beside another primitive is a smell (it is a policy, not a primitive).
35. Directory names holistically represent everything inside as collective capability — never duplicate an inner class name.
36. Zero meta-naming anywhere: `Manager`, `Service`, `Helper`, `Utils`, `Common`, `DTO`, `Contract`, `Components` are banned in all namespaces, directories, and files.
37. All names use strict domain nouns — zero procedural verbs, zero gerunds.
38. Files named after the primary concrete class; interface-only files take the contract's name — zero meta-labels (`contract`, `interface`, `impl`, `base`).
39. Domain-named folders OVER `policies/`/`layers/` when a clear domain noun exists — meta folder names are fallback only, never default.

## DESIGN INTEGRITY
40. Interface design is broad enough for foreseeable future scaling — not narrowly restricted to just the current situation. Future requirements must fit naturally without changing the contract.
41. Highest-level orchestration reads like pseudo-code or plain English — zero intermediate glue, mediators, transient state holders, or coordinator shims between sovereign primitives.
42. Seek symmetry across peer primitives — artificial asymmetry signals unexamined assumptions or overfitted boundaries.
43. Symmetrical domain naming across all peer contracts — zero procedural verbs or action cop-outs (`tooling`, `tool_executor`).
44. Distinct sovereign entities stay as explicit parameters — zero artificial wrapper DTOs or middleman parameter bags. Fragmented attributes of the same entity collapse into a single cohesive DTO with defaults.
45. Zero `partial class`, subclassing, or artificial file splitting to circumvent the ~150-line limit — cohesive units stay together; exceeding signals un-extracted policies or god-object logic.
46. When a policy grows complex enough to warrant its own sub-policies or strategies, it has become a primitive — promote it to its own sibling directory. Never leave it buried in the consumer's folder.

## CODE ECONOMY (THE END RESULT)
47. After applying PFD, total code lines went DOWN or stayed the same — never up. If lines increased, PFD was not correctly applied.
48. Bug fixes are fundamental design fixes where the bug disappears as a side effect of clean architecture — zero patchwork band-aids, zero defensive checks bolted on.
49. Zero speculative code, zero unsolicited additions, zero defensive boilerplate — do exactly what is needed, nothing more.
50. 100% zero regression verified against prior code — total lines must decrease with zero capability lost; bonus if design naturally improves resilience or performance.
