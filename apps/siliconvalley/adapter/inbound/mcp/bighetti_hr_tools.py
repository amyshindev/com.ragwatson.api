from siliconvalley.adapter.inbound.mcp.mcp_registry import mcp


@mcp.tool()
async def bighetti_myself() -> str:
    """Pied Piper HR 담당 Bighetti 자기소개."""
    return "파이프파이퍼 HR 담당 비게티 입니다"
