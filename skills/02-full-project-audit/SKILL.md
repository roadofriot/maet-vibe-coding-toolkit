# Skill 02: Full Project Technical Audit (Read-Only)
**Trigger:** User asks to audit, review, inspect, or check a project.
## Workflow
1. **Strict Read-Only Mode:** Do not modify any files during the audit.
2. **Six-Pillar Inspection:**
   - **Architecture & Modularity:** God classes, circular imports, tight coupling.
   - **Functional Completeness:** Dead buttons, unimplemented stubs, hardcoded mock data.
   - **Code Quality & Typing:** Missing types, duplicated logic, swallowed exceptions (`except Exception: pass`).
   - **Security & Secrets:** Exposed keys, missing auth checks, unsafe SQL/eval/shell calls.
   - **Performance & Memory:** Unbounded lists, unclosed streams/controllers, blocking I/O on UI thread.
   - **Testing & Build Health:** Missing tests, broken build scripts, deprecated APIs.
3. **Output Format:** Deliver a structured table and detailed cards sorted by severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) with exact `file_path:line_number`, impact explanation, and exact remediation plan.
