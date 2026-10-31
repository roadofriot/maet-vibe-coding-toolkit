# Skill 15: Evidence-Based Debugging & Root Cause Analysis
**Trigger:** Encountering any runtime error, compiler failure, broken UI, or unexpected behavior.
## Workflow
1. **Stop & Read:** Capture the exact error message, stack trace, and reproduction steps.
2. **Trace Upstream:** Follow the corrupted variable or failed call back to where it was created or mutated.
3. **Hypothesis Test:** Formulate the root cause, verify it against the code, apply the minimal targeted fix at the source, and verify no side effects occurred.
