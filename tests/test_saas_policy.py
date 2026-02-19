from python.helpers.saas_policy import (
    PolicyContext,
    UsageSnapshot,
    default_plan_policy,
    evaluate_tool_policy,
)


def _ctx(tool: str, actions: int = 0, spend: float = 0.0, plan: str = "free"):
    return PolicyContext(
        tool_name=tool,
        org_id="org_1",
        plan=plan,
        usage=UsageSnapshot(actions_last_minute=actions, spend_today_usd=spend),
    )


def test_allowlist_blocks_disallowed_tool():
    decision = evaluate_tool_policy(
        _ctx("terminal"),
        allowed_tools=["search", "read_file"],
        rate_limit_per_minute=10,
        daily_budget_usd=10,
    )
    assert not decision.allowed
    assert decision.reason == "tool_not_allowed"


def test_rate_limit_blocks_even_if_tool_allowed():
    decision = evaluate_tool_policy(
        _ctx("search", actions=15),
        allowed_tools=["search"],
        rate_limit_per_minute=10,
        daily_budget_usd=10,
    )
    assert not decision.allowed
    assert decision.reason == "rate_limit_exceeded"


def test_budget_blocks_when_spend_exceeds_cap():
    decision = evaluate_tool_policy(
        _ctx("search", spend=11.5),
        allowed_tools=["search"],
        rate_limit_per_minute=20,
        daily_budget_usd=10,
    )
    assert not decision.allowed
    assert decision.reason == "budget_exceeded"


def test_confirmation_for_dangerous_tool_keywords():
    decision = evaluate_tool_policy(
        _ctx("iam_delete_policy"),
        allowed_tools=[],
        rate_limit_per_minute=20,
        daily_budget_usd=50,
    )
    assert decision.allowed
    assert decision.requires_confirmation


def test_default_plan_policy_values():
    assert default_plan_policy("free")["max_active_sessions"] == 1
    assert default_plan_policy("pro")["max_active_sessions"] == 5
    assert default_plan_policy("team")["max_active_sessions"] == 10
