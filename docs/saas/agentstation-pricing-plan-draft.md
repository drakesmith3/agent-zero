# AgentStation Pricing Plan (Draft for Testing Stage)

> Draft only. Do not enforce in product until billing + tenancy controls are complete.

## Pricing principles
- Align pricing to actual cost drivers: compute, model tokens, storage, and tool calls.
- Keep entry tier low-friction, with strict concurrency and budget guardrails.
- Make overages transparent and controllable with hard caps.

## Proposed tiers

### Free (builder trial)
- Active sessions: **1**
- Concurrent tasks: **1**
- Daily spend cap: **$5** equivalent
- Features:
  - Core chat/session UI
  - Basic scheduler
  - Projects
  - Community support
- Limits:
  - No always-on worker
  - Limited retention window

### Pro
- Active sessions: **5**
- Concurrent tasks: **3**
- Daily spend cap: **$30** (configurable)
- Features:
  - Full scheduler
  - File editor/browser advanced workflows
  - MCP integrations
  - Priority runtime queue

### Team
- Active sessions: **10+** (configurable per contract)
- Concurrent tasks: **10**
- Daily spend cap: **$100+**
- Features:
  - Org roles and workspace governance
  - Audit exports
  - Approval workflows
  - SSO-ready integration path

## Add-ons
- Always-on worker (1 warm instance)
- Private networking/VPC connectors
- Extended retention and checkpoint frequency
- Dedicated model routing controls

## Metering dimensions
- CPU-seconds / memory-seconds for workers
- LLM input/output tokens
- Storage GB-month and egress
- MCP/tool invocation count

## Guardrails before launch
- Hard budget limit at org + workspace scope
- Per-minute rate limit controls
- Tool allowlist by plan
- Mandatory confirmation for dangerous actions

## Rollout recommendation
1. Internal alpha: free/pro behavior flags only (no billing).
2. Closed beta: soft metering + visible cost dashboard.
3. Public beta: enable billing with hard caps and alerts.
