# PFD Repository Agent Guidelines

## 1. Documentation Separation (Human vs. Agent)
- **`README.md` is for Humans (Strictly Zero Unprompted Edits):** Foundational theory for software engineers, written plainly. Zero granular operational runbook directions (which belong exclusively in skills), zero AI-prompt checklists, zero YAML frontmatter. **NEVER modify `README.md` unless the user explicitly commands it.**
- **Skills are for AI Agents:** The PFD skill triad (`pfd`, `pfd-audit`, `pfd-iterate`) in `~/.gemini/config/skills/` contains the actionable operational runbook, audit checklists, and execution constraints.
- **Never Mirror Blindly:** Never copy-paste content between `README.md` and skills. Each speaks to its distinct audience.

## 2. Core Architectural Invariants (PFD)
- **Always Apply PFD:** Apply Primitive-First Design (PFD) across all software architecture, boundary definitions, audits, refactorings, and reviews. Always read and strictly adhere to the complete, authoritative PFD doctrine in `~/.gemini/config/skills/pfd/SKILL.md` (invocable via `/pfd`). Never use partial heuristics, speculative layers, or ad-hoc wrapper abstractions.

## 3. The Refinement Cycle: Correction -> Proposal -> Sharpen (Never Blindly Append)
- **Root-Cause Correction:** When gaps, omissions, or smells are identified, diagnose the fundamental structural cause calmly. Zero panic edits, zero blind reverts, zero knee-jerk patches.
- **Ultra-Concise Proposal First:** State intent in 1–2 crisp sentences or bullets before touching workspace state. Strictly zero code dumps or text previews before editing.
- **Sharpen, Don't Blindly Append:** When updating skills, rules, or docs, improve and densify existing statements within their strict line budgets. Never blindly append lines or destroy hard-won prior instructions in the name of reckless "improving".

## 4. Skill Synchronization
- **Repository Triad:** The repo `skills/` folder holds the version-controlled distribution of the PFD triad (`pfd`, `pfd-audit`, `pfd-iterate`).
- **Sync Tool:** Use `python scripts/sync-pfd.py update-repo` to pull live edits from `~/.gemini/config/skills/` into the repo, or `python scripts/sync-pfd.py install` to install repo skills into Antigravity. Always verify with `python scripts/sync-pfd.py check`.

## 5. Git Workflow & Immediate Commits
- **Commit Immediately on Every Sync or Update:** Never leave synced skills or documentation uncommitted in the working tree. Immediately create a clean, descriptive git commit upon completing any sync, architectural refinement, or skill update.
- **Pre-Commit Audit:** Before committing, perform a rigorous audit of all user requirements. Honestly confirm whether every point was captured, or openly identify any omission.
