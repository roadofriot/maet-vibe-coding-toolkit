# Skill 13: Model Context Protocol (MCP) Server & Tool Engineering
**Trigger:** Building or configuring MCP servers and IDE tool integrations.
## Workflow
1. Expose focused, well-typed tools with clear descriptions and strict input schemas.
2. Default to read-only operations; gate file deletion, shell execution, or database mutations behind explicit parameters and safety checks.
3. Keep memory footprint minimal (prefer stdio or remote HTTP endpoints over heavy container stacks).
