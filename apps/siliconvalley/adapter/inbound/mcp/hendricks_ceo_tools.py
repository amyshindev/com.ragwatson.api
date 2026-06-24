from siliconvalley.adapter.inbound.mcp.mcp_registry import mcp


@mcp.tool()
async def hendricks_myself() -> str:
    """Pied Piper CEO Richard Hendricks 자기소개."""
    return "파이프파이퍼 CEO 헨드릭스 입니다"
