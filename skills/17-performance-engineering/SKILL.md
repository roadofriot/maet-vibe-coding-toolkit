# Skill 17: Low-RAM, CPU & Network Performance Optimization
**Trigger:** Optimizing app startup, frame rates, memory usage, or query speed.
## Workflow
1. Measure baseline resource consumption before changing code.
2. Dispose controllers, timers, event listeners, and streams properly to prevent memory leaks.
3. Paginate or virtualize long lists (`ListView.builder` in Flutter, virtualized lists in Web), compress assets, and batch network/disk operations.
