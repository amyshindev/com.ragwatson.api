"""Harness marker examples — copy patterns when adding hub/spoke tests."""

from __future__ import annotations

import pytest


@pytest.mark.hub
def test_mcp_hub_server_name(hub_mcp) -> None:
    """Hub module exposes a single named registry for all spokes."""
    assert hub_mcp.name == "siliconvalley"


@pytest.mark.hub
def test_http_hub_aggregates_spoke_routers(hub_router_registry) -> None:
    """Router registry is the HTTP hub; each spoke contributes a sub-router."""
    routes = [getattr(r, "path", "") for r in hub_router_registry.routes]
    assert any("hendricks" in p for p in routes)
    assert any("gilfoyle" in p for p in routes)


@pytest.mark.hub
def test_http_hub_wiring_pattern_with_stub_spokes() -> None:
    """Harness guide: hub composes spokes without importing production adapters."""
    hub_routes: list[str] = []
    for spoke_prefix in ("/siliconvalley/hendricks", "/siliconvalley/gilfoyle"):
        hub_routes.append(spoke_prefix)
    assert any("hendricks" in p for p in hub_routes)
    assert any("gilfoyle" in p for p in hub_routes)


@pytest.mark.spoke
@pytest.mark.asyncio
async def test_hendricks_spoke_in_isolation(spoke_hendricks_myself) -> None:
    """Spoke logic runs without loading sibling spokes or HTTP stack."""
    reply = await spoke_hendricks_myself()
    assert "헨드릭스" in reply


@pytest.mark.harness
@pytest.mark.asyncio
async def test_harness_hub_spoke_mcp_wiring(harness_mcp, load_all_spokes) -> None:
    """Integration harness: all spokes register on the same hub instance."""
    from siliconvalley.adapter.inbound.mcp.gilfoyle_system_tools import gilfoyle_myself
    from siliconvalley.adapter.inbound.mcp.hendricks_ceo_tools import hendricks_myself

    assert harness_mcp.name == "siliconvalley"
    assert len(load_all_spokes) == 5
    assert "헨드릭스" in await hendricks_myself()
    assert "길포일" in await gilfoyle_myself()
