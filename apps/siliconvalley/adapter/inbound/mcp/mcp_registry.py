from mcp.server.fastmcp import FastMCP

mcp = FastMCP("siliconvalley")


def run() -> None:
    """Load tool modules and start the MCP server (stdio)."""
    from siliconvalley.adapter.inbound.mcp import (  # noqa: F401
        bighetti_hr_tools,
        dinesh_dash_tools,
        dunn_coo_tools,
        gilfoyle_system_tools,
        hendricks_ceo_tools,
    )

    mcp.run()


if __name__ == "__main__":
    run()
