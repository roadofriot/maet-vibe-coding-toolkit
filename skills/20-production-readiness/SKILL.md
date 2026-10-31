# Skill 20: Production Readiness & Release Verification Gate
**Trigger:** Preparing any application for final delivery, client handover, or deployment.
## Workflow
1. Run the 10-point Release Gate:
   - [ ] Zero compiler/analyzer errors or warnings.
   - [ ] Zero hardcoded secrets or debug flags (`debugShowCheckedModeBanner: false`, production env).
   - [ ] All buttons and navigation routes tested and working.
   - [ ] Offline/error/empty states verified.
   - [ ] Database migrations and backups verified.
   - [ ] Build artifact generated and smoke-tested.
