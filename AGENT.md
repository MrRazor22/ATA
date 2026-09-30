# ATA Repository Agent Guidelines

## 1. Documentation Separation (Human vs. Agent)
- **`README.md` is for Humans:** Architectural manifesto and foundational theory for software engineers. Grounded with production case studies (`AgentCore`, `NanoLLM`) and direct comparisons with enterprise frameworks (LangChain, Microsoft Agent Framework). Zero AI-prompt runbook steps, zero YAML frontmatter.
- **`skills/ata/SKILL.md` is for AI Agents:** Actionable operational runbook, step-by-step audit checklists, and strict execution constraints. Zero hardcoded personal repo links or ephemeral project leakage.
- **Never Mirror Blindly:** Never copy-paste content between `README.md` and `SKILL.md`. Each file must speak directly to its distinct audience.
- **Reflect What It Preaches:** Both `SKILL.md` and `README.md` must embody ATA itself: rich in detail, high signal density, strictly compressed, with zero fluff or boilerplate.

## 2. Core Architectural Invariants
- **Intellectual Honesty Over Dogma:** Never apply ATA blindly. If applying ATA introduces practical friction, unnatural ceremony, or a design smell in a given scenario, point it out explicitly rather than force-fitting dogma.
- **Triad Components Are Optional Primitives, Not Mandates:** $P, \pi, \lambda$ are stages of primitives. Forcing every boundary to have policies or layers when none are needed is an anti-ATA smell.
- **Why Policy Exists:** Policies ($\pi: P_{\pi} \to P$) exist specifically to extract opinionated heuristics, algorithms, and volatile strategies out of $P$, preserving $P$ as an irreducible, unopinionated domain mechanism.
- **Policy is a Primitive:** Policies are extracted subordinate primitives ($P_{\pi}$). Every policy contract demands the exact same 80/20 minimalism and Subtraction Test as root primitives ($P$).
- **Fractal Boundaries:** When a policy primitive expands in complexity to require its own layers or subordinate policies, it promotes directly into the root primitive ($P$) of an independent operational boundary.
- **Everything is a Primitive:** Layers ($\lambda: P \to P$) are endomorphic primitive decorators. Policies ($\pi: P_{\pi} \to P$) are extracted subordinate primitives. All behavioral contracts in ATA are primitives.
- **Bedrock Contract Purity & Chaining:** The primitive interface ($P$) encapsulates domain capabilities only. It must never contain chaining, piping, or layer-composition mechanics. Chaining belongs strictly to external Transforms ($T$).
- **Zero Language Hardcoding:** Architecture specifications and skills must remain 100% language-agnostic. Never mention language-specific operators or mechanics (`__or__`, `|`, `extension methods`) in foundational doctrine.
- **Brevity as the Invariant:** Line count is the empirical mirror of representational fidelity. Code sprawl indicates an incomplete abstraction.

## 3. Operational & Git Workflow
- **Commit on Every Considerable Update:** Always create a clean, descriptive git commit upon completing any considerable architectural, documentation, or skill update. Never leave significant milestones, syntheses, or refactorings uncommitted in the working tree.

