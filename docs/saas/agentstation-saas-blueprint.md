# AgentStation SaaS Blueprint (Low Cost, High Concurrency)

## Viability Summary
Yes—this platform is viable as a SaaS if you separate **control plane** and **worker plane** and add checkpoint/restore.

## Recommended Architecture
- **Control Plane (Cloud Run + Cloud SQL + GCS)**: auth, orgs, plans, quotas, routing, billing usage records, audit logs.
- **Worker Plane (Cloud Run sessions)**: one container per active session, scale-to-zero when idle.

## Concurrency and Cost Controls
- Plan-based active session limits (e.g., Free=1, Pro=3, Team=10).
- Idle timeout (e.g., 10–20 min), checkpoint state, terminate worker.
- Resume by restoring latest checkpoint into a new worker.

## Minimal Data Model (starter)
- `organizations(id, name, plan, created_at)`
- `users(id, org_id, email, role, created_at)`
- `workspaces(id, org_id, name, created_at)`
- `sessions(id, workspace_id, status, worker_url, last_checkpoint_at, created_at)`
- `session_checkpoints(id, session_id, storage_uri, size_bytes, created_at)`
- `usage_events(id, org_id, user_id, session_id, metric_type, value, ts)`
- `tool_policies(id, org_id, policy_json, updated_at)`
- `audit_events(id, org_id, user_id, action, resource, metadata_json, ts)`

## Session Checkpoint Format (v1)
```json
{
  "version": "v1",
  "session_id": "sess_123",
  "created_at": "2026-01-01T12:00:00Z",
  "workspace_archive_uri": "gs://bucket/checkpoints/sess_123/ckpt_001.tar.zst",
  "log_cursor": 12345,
  "memory_index_uri": "gs://bucket/checkpoints/sess_123/memory.faiss",
  "settings_snapshot": {"chat_model_provider": "openrouter"}
}
```

## Policy Layer (must-have)
Before each tool call, enforce:
1. **allowlist** for current plan/org/user
2. **rate limit** (actions/min)
3. **budget guard** (token/spend threshold)
4. **confirmation gate** for dangerous actions (`delete`, `iam`, `billing`)

## Google Cloud MCP Server Setup (practical path)
1. Deploy maintained Google Cloud MCP server to Cloud Run with authenticated ingress.
2. If server only supports stdio, place an adapter service that maps authenticated HTTP requests to isolated stdio invocations.
3. Use two service accounts:
   - **runner-sa** (Cloud Run runtime; least privilege)
   - **caller-sa** (control plane invoker)
4. Log all tool calls to Cloud Logging with identity + tool + summary params.

## Least-Privilege IAM Starter Roles
- Deploy Cloud Run only:
  - `roles/run.developer`
  - `roles/iam.serviceAccountUser` (on deploy target SA)
  - `roles/logging.viewer`
- Read-only operations:
  - `roles/viewer`
  - `roles/logging.viewer`
- Avoid `Owner` for SaaS operations.

## Phased Rollout
1. **Phase 1**: single-region control plane + Cloud Run workers + checkpoint/restore.
2. **Phase 2**: background tasks with Cloud Tasks / PubSub, improved billing metering.
3. **Phase 3**: multi-region, optional GKE Autopilot for heavy long-running workloads.
