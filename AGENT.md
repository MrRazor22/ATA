# ATA Repository Agent Guidelines

## 1. Documentation Separation (Human vs. Agent)
- **`README.md` is for Humans:** Architectural manifesto and specification for software engineers. Retains real-world reference implementations (`AgentCore`, `NanoLLM`) for grounding. Zero AI-prompt runbook steps, zero YAML frontmatter.
- **`skills/ata/SKILL.md` is for AI Agents:** Actionable operational runbook, step-by-step audit checklists, and strict execution constraints. Zero hardcoded personal repo links or ephemeral project leakage.
- **Never Mirror Blindly:** Never copy-paste content between `README.md` and `SKILL.md`. Each file must speak directly to its distinct audience.

## 2. Core Architectural Invariants
- **Why Policy Exists:** Policies ($\pi: P_{\pi} \to P$) exist specifically to extract opinionated heuristics, algorithms, and volatile strategies out of $P$, preserving $P$ as an irreducible, unopinionated domain mechanism.
- **Policy is a Primitive:** Policies are extracted subordinate primitives ($P_{\pi}$). Every policy contract demands the exact same 80/20 minimalism and Subtraction Test as root primitives ($P$).
- **Fractal Boundaries:** When a policy primitive expands in complexity to require its own layers or subordinate policies, it promotes directly into the root primitive ($P$) of an independent operational boundary.
- **Everything is a Primitive:** Layers ($\lambda: P \to P$) are endomorphic primitive decorators. Policies ($\pi: P_{\pi} \to P$) are extracted subordinate primitives. All behavioral contracts in ATA are primitives.
- **Bedrock Contract Purity & Chaining:** The primitive interface ($P$) encapsulates domain capabilities only. It must never contain chaining, piping, or layer-composition mechanics. Chaining belongs strictly to external Transforms ($T$).
- **Zero Language Hardcoding:** Architecture specifications and skills must remain 100% language-agnostic. Never mention language-specific operators or mechanics (`__or__`, `|`, `extension methods`) in foundational doctrine.
- **Brevity as the Invariant:** Line count is the empirical mirror of representational fidelity. Code sprawl indicates an incomplete abstraction.
