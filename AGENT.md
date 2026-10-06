# PFD Repository Agent Guidelines

## 1. Documentation Separation (Human vs. Agent)
- **`README.md` is for Humans:** Architectural manifesto and foundational theory for software engineers. Grounded with production case studies (`AgentCore`, `NanoLLM`) and direct comparisons with enterprise frameworks (LangChain, Microsoft Agent Framework). Zero granular operational runbook directions (which belong exclusively in `SKILL.md`), zero AI-prompt checklists, zero YAML frontmatter.
- **`skills/pfd/SKILL.md` is for AI Agents:** Actionable operational runbook, step-by-step audit checklists, and strict execution constraints. Zero hardcoded personal repo links or ephemeral project leakage.
- **Never Mirror Blindly:** Never copy-paste content between `README.md` and `SKILL.md`. Each file must speak directly to its distinct audience.
- **Reflect What It Preaches (First-Class Proof Beyond Code):** Both `SKILL.md` and `README.md` must strictly embody PFD itself: rich in detail, high signal density, strictly compressed, with zero convenience bloat or fluff. This serves as primary proof that PFD is a universal creative discipline beyond code.

## 2. Core Architectural Invariants (PFD)
- **Always Apply PFD:** Apply Primitive-First Design (PFD) across all software architecture, boundary definitions, audits, refactorings, and reviews. Always read and strictly adhere to the complete, authoritative PFD doctrine in `skills/pfd/SKILL.md` (and global `~/.gemini/config/skills/pfd/SKILL.md`). Never use partial heuristics, speculative layers, or ad-hoc wrapper abstractions.


## 3. Operational & Git Workflow
- **Commit on Every Considerable Update:** Always create a clean, descriptive git commit upon completing any considerable architectural, documentation, or skill update. Never leave significant milestones, syntheses, or refactorings uncommitted in the working tree.
- **Pre-Commit User-Point Audit & Absolute Honesty:** Before or upon committing, always perform a rigorous, exhaustive audit of all user requirements and nuanced insights. Honestly and explicitly confirm to the user whether every single point was captured in full, or openly identify any friction, omission, or necessary adaptation.
- **Mandatory Synchronization Checklist:** Whenever updating PFD architecture, doctrine, or skills, always synchronize the following three locations:
  1. `skills/pfd/SKILL.md` (Repo skill file)
  2. `~/.gemini/config/skills/pfd/SKILL.md` (Global Antigravity skill directory)
  3. `~/.gemini/config/AGENTS.md` (Global user rules Section 5)
  *Always run `powershell -File scripts/sync-pfd.ps1` to automatically sync the skill and verify status.*
