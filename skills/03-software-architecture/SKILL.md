# Skill 03: Enterprise & Local-First Software Architecture
**Trigger:** Designing a new application, major module, or system refactor.
## Workflow
1. Establish clear separation of concerns:
   - **Presentation Layer:** UI widgets/components + lightweight view controllers/state notifiers.
   - **Domain / Service Layer:** Pure business rules and use-case orchestration.
   - **Data Layer:** Local persistence (SQLite/IndexedDB/Isar/Hive) + Remote API/Supabase repository with offline sync queue.
2. Compare trade-offs briefly and select the most maintainable, lowest-overhead pattern for the target hardware.
3. Produce a clear directory tree and data-flow diagram in Markdown/ASCII.
