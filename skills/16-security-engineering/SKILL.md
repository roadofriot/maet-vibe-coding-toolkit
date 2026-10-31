# Skill 16: Application Security Auditing & Hardening
**Trigger:** Reviewing code safety, auth flows, file uploads, or external integrations.
## Workflow
1. Scan for hardcoded credentials, unsafe `eval`/`exec`, unvalidated redirects, SSRF, XSS, and SQL injection.
2. Verify authentication token lifecycle, password hashing, CORS configuration, and role-based access control.
3. Ensure sensitive data is excluded from logs, crash reports, and Git commits.
