# Skill 10: Database Architecture, SQL & Local-First Sync
**Trigger:** Designing schemas for PostgreSQL/Supabase, SQLite, or IndexedDB.
## Workflow
1. Normalize tables appropriately, define explicit primary/foreign keys, `created_at`/`updated_at` timestamps, and `NOT NULL` / `CHECK` constraints.
2. Add indexes on foreign keys and frequently filtered/sorted columns.
3. For Supabase: write explicit Row-Level Security (RLS) policies for `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
4. Never run destructive migrations without backup and explicit user confirmation.
