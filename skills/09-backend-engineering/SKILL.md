# Skill 09: Robust Backend & Service Engineering
**Trigger:** Building APIs, background workers, CLI tools, or server logic (Python/FastAPI/Node/Edge Functions).
## Workflow
1. Enforce strict request schema validation (Pydantic / Zod / JSON Schema).
2. Make write operations idempotent where possible and wrap multi-step database writes in atomic transactions.
3. Implement structured error responses (`{ code, message, details }`), rate limiting, and clean timeout handling.
