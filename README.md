# Primitive-First Design (PFD)

> Correct code is usually minimal.

PFD is a design philosophy that simplifies architecture down to irreducible boundaries. It does two things at the same time:

1. **Makes code genuinely human-readable:** Every implementation reads like plain English pseudo-code. Anyone can open a file, understand the system in minutes, and hold the entire architecture in their head (~1k–3k lines end-to-end).
2. **Forces AI agents to code clean and minimal:** Agents naturally drift into wrapper sprawl, defensive boilerplate, and patchwork band-aids unless constrained. PFD gives the agent tight, non-negotiable boundaries — forcing it to produce high-signal code that is both clean and minimal.

They complement each other: minimal code shrinks token context and cognitive load; clean boundaries eliminate hallucinated abstractions and regression loops.

## The Idea

Every system has a few core boundaries — **primitives** — that define what the system fundamentally does. An agent framework needs context, an LLM interface, and a toolbox. A car needs an engine, body, chassis, cabin, and a control bus. That's it.

If you get these primitives right, everything else falls into place naturally. The code reads like plain English, scales without rewrites, and stays small. If you get them wrong, you spend the rest of the project writing wrappers, adapters, managers, and utilities to compensate.

PFD forces you to discover these primitives upfront — and hold the line.

## How It Works

Every component in a system falls into one of four roles:

- **Core Primitive** — The irreducible boundary. The interface contract. This is the thing itself.
- **Policy** — An injected opinion inside the primitive. Strategy, algorithm, threshold — anything that can vary.
- **Layer** — A decorator on the outside. Logging, caching, telemetry — anything that observes or extends without changing the core.
- **DTO** — Pure data. No behavior. Just carries state between boundaries.

A policy is a primitive on the inside. A layer is the same primitive on the outside. DTOs are the passive glue. That's the entire model.

## The Rules That Matter

- **Every boundary is an interface.** No backdoor concrete access. The contract is the only truth.
- **Interfaces stay small.** 4-5 methods max. More means the boundary is wrong.
- **Implementations read like English.** If a method body isn't plain sequential logic, something wasn't extracted.
- **Zero private methods.** Every private method is an un-extracted policy or a mismodeled boundary. Extract it.
- **~150 lines per file.** Exceeding this signals un-extracted opinions, not genuine complexity.
- **All opinions are injected.** Even simple numbers that can change. Hardcoded decisions become invisible constraints.
- **DTOs have zero behavior.** If a data class needs methods, responsibilities are misplaced.
- **No meta-names.** `Manager`, `Service`, `Helper`, `Utils`, `Common` — all banned. Name things after what they actually are.
- **No untyped escape hatches.** `Any`, `object`, `dynamic` — if you need these, your domain types aren't modeled.
- **Folders mirror architecture.** Every primitive gets its own directory. Disk layout = boundary tree.

## The End Result

When PFD is applied correctly, total code lines go **down**, not up. Not because you're trying to write less code, but because clean design is naturally minimal. Bug fixes become design fixes where the bug vanishes as a side effect. Regressions disappear because there's nothing fragile left to regress.

A well-designed PFD system hovers around ~1k lines end-to-end. A human can't hold more than ~3k lines in working memory. If you're past that without massive external domain logic, something is wrong.

## For AI Agents

PFD ships as an official skill triad for Google Antigravity (AGY) agents:

- **`/pfd`** — The full design philosophy and operational rules
- **`/pfd-audit`** — 50-rule hard violation checklist + mechanical Python scanner
- **`/pfd-iterate`** — Forces iterative self-audit and compression until zero violations

Install into your Antigravity environment by running:

```bash
python scripts/sync-pfd.py install
```

## Case Studies

- **[AgentCore](https://github.com/MrRazor22/AgentCore)** — Where PFD was discovered. An experimental agent framework built end-to-end with 3 core primitives.
- **[NanoLLM](https://github.com/MrRazor22/NanoLLM)** — PFD applied to high-performance model inference.

---

*PFD applies to everything — backend, UI, specifications, creative work. Anywhere there are boundaries, there are primitives, policies, layers, and data.*