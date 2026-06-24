from siliconvalley.adapter.inbound.mcp.mcp_registry import mcp


@mcp.tool()
async def dunn_myself() -> str:
    """Pied Piper COO Dunn 자기소개."""
    return "파이프파이퍼 COO 던 입니다"
