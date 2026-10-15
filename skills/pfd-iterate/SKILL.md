---
name: pfd-iterate
description: >-
  Post-implementation PFD iteration trigger. Forces the agent to self-audit via pfd-audit,
  verify code economy, and iteratively compress until zero violations. Reusable prompt skill.
---

After completing any implementation, refactor, or bug fix, perform this mandatory self-audit iteration. Do NOT skip steps. Do NOT report "done" until clean. For the full design philosophy, see the `pfd` skill (`/pfd`).

---

## STEP 1: RUN PFD AUDIT
Run the mechanical scanner first: [scan.py](../pfd-audit/scripts/scan.py) (`python <pfd-audit skill_dir>/scripts/scan.py <project_path> [previous_line_count]`). Then invoke the `pfd-audit` skill checklist for semantic rule verification. Report every violation found with file, line, and rule number. Zero tolerance.

## STEP 2: VERIFY CODE ECONOMY
Compare total code lines before and after your changes:
- **Lines went UP:** You did not apply PFD correctly. More code means more bloat, not better design. Explain why and compress.
- **Lines stayed SAME or went DOWN:** Verify this is genuine compression with zero functionality loss — not deleted features.
- Remember: correct PFD application ALWAYS reduces code. Not because you target line count, but because clean design is naturally minimal. If you see more code, the design is wrong.

## STEP 3: VERIFY FUNDAMENTAL FIXES (NOT PATCHWORK)
For every bug fix or change, answer honestly:
- Did you **patchwork** the symptom (defensive check, fallback path, band-aid conditional), or **fundamentally fix** the design?
- Under PFD, the bug must disappear as a **side effect** of clean architecture — not be directly patched.
- If you added code to work around a bug rather than fixing the root cause: that is patchwork. Redo it.
- A correct PFD fix doesn't just fix the bug — it makes the code cleaner, shorter, and more resilient than before. You get regression prevention for free.

## STEP 4: VERIFY ZERO-LOSS COMPRESSION & ZERO REGRESSION
- Compare old code directly against new code to verify **100% zero regression** — all capabilities, features, and edge cases preserved.
- Total code lines must be **less than or equal to before** — line reduction is mandatory. If lines increased, compress further.
- Bonus points if clean architecture naturally improved resilience, throughput, or capabilities as a zero-bloat side effect.
- **The Outsider Litmus Test:** When PFD is done right, code never looks like an eccentric paradigm — an engineer with zero knowledge of PFD will naturally find it obvious, standard, and clean. If it feels weird or contrived to an outsider, the design is wrong.

## STEP 5: ITERATE UNTIL CLEAN
If ANY violations were found in Steps 1–4:
1. Fix all violations.
2. Re-run the full audit from Step 1.
3. Repeat until zero violations remain and code lines are at or below the starting count.

**Do NOT report "done" until the audit is completely clean.**
