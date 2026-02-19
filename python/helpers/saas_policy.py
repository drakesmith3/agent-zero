"""SaaS policy guard helpers for plan-based tool governance.

These helpers are intentionally framework-agnostic and side-effect free so they can
be reused by HTTP routes, websocket handlers, and async workers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


DANGEROUS_KEYWORDS = ("delete", "iam", "billing", "destroy", "drop", "revoke")


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_confirmation: bool = False
    reason: str = "allowed"


@dataclass(frozen=True)
class UsageSnapshot:
    actions_last_minute: int
    spend_today_usd: float


@dataclass(frozen=True)
class PolicyContext:
    tool_name: str
    org_id: str
    plan: str
    usage: UsageSnapshot


def _normalize_set(values: Iterable[str] | None) -> set[str]:
    return {str(v).strip().lower() for v in (values or []) if str(v).strip()}


def _is_dangerous_tool(tool_name: str) -> bool:
    lowered = (tool_name or "").strip().lower()
    return any(token in lowered for token in DANGEROUS_KEYWORDS)


def evaluate_tool_policy(
    context: PolicyContext,
    *,
    allowed_tools: Iterable[str] | None,
    rate_limit_per_minute: int,
    daily_budget_usd: float,
    confirmation_required_tools: Iterable[str] | None = None,
) -> PolicyDecision:
    """Evaluate allowlist/rate-limit/budget/confirmation in deterministic order.

    Order matters to provide consistent user messaging and telemetry.
    """

    tool = (context.tool_name or "").strip().lower()
    if not tool:
        return PolicyDecision(False, reason="invalid_tool")

    allow = _normalize_set(allowed_tools)
    if allow and tool not in allow:
        return PolicyDecision(False, reason="tool_not_allowed")

    if rate_limit_per_minute >= 0 and context.usage.actions_last_minute >= rate_limit_per_minute:
        return PolicyDecision(False, reason="rate_limit_exceeded")

    if daily_budget_usd >= 0 and context.usage.spend_today_usd >= daily_budget_usd:
        return PolicyDecision(False, reason="budget_exceeded")

    confirmation_set = _normalize_set(confirmation_required_tools)
    requires_confirmation = tool in confirmation_set or _is_dangerous_tool(tool)

    return PolicyDecision(True, requires_confirmation=requires_confirmation)


def default_plan_policy(plan: str) -> Mapping[str, object]:
    """Provide a safe default policy map per plan tier."""

    tier = (plan or "free").strip().lower()
    if tier == "team":
        return {
            "max_active_sessions": 10,
            "rate_limit_per_minute": 120,
            "daily_budget_usd": 100.0,
            "allowed_tools": [],  # empty == unrestricted (except runtime-level checks)
        }
    if tier == "pro":
        return {
            "max_active_sessions": 5,
            "rate_limit_per_minute": 60,
            "daily_budget_usd": 30.0,
            "allowed_tools": [],
        }
    return {
        "max_active_sessions": 1,
        "rate_limit_per_minute": 20,
        "daily_budget_usd": 5.0,
        "allowed_tools": [],
    }
