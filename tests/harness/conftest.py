"""Harness fixtures — emulate hub & spokes for isolated / wired tests.

Recommended layout (star topology + clean hex layers):

    backend/
      apps/
        siliconvalley/           # star-topology app
          domain/
            hendricks_ceo_topology.py   # hub ontology (graph nodes)
          dependencies/
            providers.py              # hub DI wiring
          adapter/inbound/
            api/router_registry.py    # HTTP hub
            mcp/mcp_registry.py       # MCP hub
            mcp/*_tools.py            # spokes (one per character)
          app/                        # clean_modules (use cases, ports)
        titanic/                      # linear clean-arch reference app
      tests/
        harness/
          conftest.py                 # this file
          test_harness.py             # marker examples
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys
from typing import Any

import pytest

_BACKEND = Path(__file__).resolve().parents[2]
_APPS = _BACKEND / "apps"

for path in (str(_BACKEND), str(_APPS)):
    if path not in sys.path:
        sys.path.insert(0, path)


@pytest.fixture
def hub_mcp() -> Any:
    """Central MCP hub — spokes attach via @mcp.tool decorators."""
    from siliconvalley.adapter.inbound.mcp.mcp_registry import mcp

    return mcp


@pytest.fixture
def hub_router_registry() -> Any:
    """HTTP hub that aggregates spoke routers (skips if outbound pg adapters missing)."""
    pytest.importorskip("siliconvalley.adapter.outbound.pg")
    from siliconvalley.adapter.inbound.api.router_registry import siliconvalley_router

    return siliconvalley_router


@pytest.fixture
def load_all_spokes() -> tuple[Any, ...]:
    """Import every spoke so tool decorators register on the hub."""
    from siliconvalley.adapter.inbound.mcp import (
        bighetti_hr_tools,
        dinesh_dash_tools,
        dunn_coo_tools,
        gilfoyle_system_tools,
        hendricks_ceo_tools,
    )

    return (
        bighetti_hr_tools,
        dinesh_dash_tools,
        dunn_coo_tools,
        gilfoyle_system_tools,
        hendricks_ceo_tools,
    )


@pytest.fixture
def spoke_hendricks_myself() -> Callable[[], Any]:
    """Single spoke callable — no other spokes required."""
    from siliconvalley.adapter.inbound.mcp.hendricks_ceo_tools import hendricks_myself

    return hendricks_myself


@pytest.fixture
def harness_mcp(hub_mcp: Any, load_all_spokes: tuple[Any, ...]) -> Any:
    """Fully wired hub with every spoke registered."""
    return hub_mcp
