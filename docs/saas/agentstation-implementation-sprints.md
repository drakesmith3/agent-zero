# AgentStation SaaS Implementation Sprints (Production-Ready Path)

This plan turns the current single-runtime product into a low-cost, high-concurrency SaaS without breaking current APIs/websocket contracts.

## Sprint 1 — Safety + Tenancy

### Goals
- Introduce tenant boundaries and policy controls before broad external rollout.
- Keep current UX intact while adding server-side governance.

### Deliverables
1. **Data model v1**
   - `organizations`, `users`, `workspaces`, `sessions`, `usage_events`, `audit_events`, `tool_policies`.
2. **Policy middleware**
   - Enforce allowlist, rate limit, budget, and dangerous-action confirmation requirement.
3. **Usage metering events**
   - Emit usage rows for each model/tool call and session lifecycle event.
4. **Audit log plumbing**
   - Record sensitive events (`project_delete`, `task_delete`, `backup_restore`, policy denials).

### Edge Cases Covered
- Missing/invalid tenant context → deny with explicit reason.
- Unknown plan tier → fallback to `free` policy.
- Missing policy config → safe defaults.
- Clock skew for usage windows → rely on server-side timestamps only.

## Sprint 2 — Reliability

### Goals
- Ensure session continuity while reducing infra cost.

### Deliverables
1. **Checkpoint/restore v1 service**
   - Snapshot workspace, chat/log cursor, settings snapshot, and memory index pointers.
2. **Idle-stop lifecycle**
   - Auto-checkpoint + stop worker after idle timeout.
3. **Reconnect replay UX**
   - Clear sync status states: reconnecting, replaying, synced.
4. **CI gate with platform matrix subset**
   - Add automated checks from `docs/qa/platform-test-matrix.md`.

### Edge Cases Covered
- Partial checkpoint upload failure → mark checkpoint failed and keep previous healthy checkpoint.
- Restore mismatch/version drift → fail fast with migration hint.
- Duplicate websocket replay envelopes → dedupe by event id/correlation id.

## Sprint 3 — Differentiation

### Goals
- Move from “works” to “state-of-the-art operator product”.

### Deliverables
1. **Timeline playback**
   - Session timeline with step groups, durations, and artifacts.
2. **Approvals UX**
   - “Pending approval” queue for dangerous or high-cost actions.
3. **Workspace templates**
   - Prebuilt templates (engineering, support, ops, research).
4. **Cost dashboard**
   - Per-org and per-workspace spend/usage with budget thresholds.

### Edge Cases Covered
- High-volume timeline rendering → paginate or virtualize timeline entries.
- Approval timeout/no response → auto-cancel risky actions.
- Template drift → immutable template versions + explicit migration.

## Non-goals during current test phase
- Full auth rollout (intentionally postponed while testing).
- Vendor lock-in abstractions beyond required cloud primitives.

## Suggested milestones
- Sprint 1: 2 weeks
- Sprint 2: 2 weeks
- Sprint 3: 2 weeks

## Exit Criteria for “Production Candidate”
- Zero P0 regressions on test matrix.
- Policy denial + approval flows covered by unit/integration tests.
- Checkpoint/restore tested across restart + reconnect scenarios.
- Usage + audit pipelines visible in admin UI/log sinks.
