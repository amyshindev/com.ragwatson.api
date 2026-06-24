from siliconvalley.adapter.inbound.mcp.mcp_registry import mcp


@mcp.tool()
async def dinesh_myself() -> str:
    """Pied Piper 대시보드·지표 담당 Dinesh 자기소개."""
    return "파이프파이퍼 대시보드 엔지니어 디니시 입니다"
