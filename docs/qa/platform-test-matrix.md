# AgentStation Platform Test Matrix

This matrix is a practical end-to-end checklist for validating major platform capabilities before release.

## 1) Backend/contract checks
- `python -m pytest tests/test_snapshot_schema_v1.py`
- `python -m pytest tests/test_state_sync_handler.py`
- `python -m pytest tests/test_websocket_handlers.py tests/test_websocket_namespaces.py`

## 2) UI state and settings checks
- `python -m pytest tests/test_settings_developer_sections.py`
- Verify settings modal tab filtering and tab switching.
- Verify save/cancel persistence behavior.

## 3) Session lifecycle checks
- Login/logout
- Create chat session
- Stream response chunks
- Reconnect browser tab and verify sync recovery
- Queue a message while running and verify dequeue behavior

## 4) Project workflow checks
- Create, edit, activate, deactivate, delete projects
- Validate project filter and empty/no-match states
- Validate project-scoped memory/skills/instructions views

## 5) File and scheduler checks
- Open file browser, rename, open editor, save
- Upload and download file flows
- Create/edit/disable/enable scheduler task

## 6) Security and policy checks (SaaS readiness)
- Verify no secret keys committed in repo
- Verify env-based API key loading works (`API_KEY_OPENROUTER` or `OPENROUTER_API_KEY`)
- Verify audit events/logging enabled for sensitive operations

## 7) Mobile + desktop UX checks
- Sidebar open/close and overlay behavior at <=768px
- Header status chip fit at <=768px
- Touch target size for quick actions
- Scroll stability during long streaming output
