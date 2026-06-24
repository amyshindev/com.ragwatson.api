from siliconvalley.adapter.inbound.mcp.mcp_registry import mcp


@mcp.tool()
async def gilfoyle_myself() -> str:
    """Pied Piper 시스템·인프라 엔지니어 Gilfoyle 자기소개."""
    return "파이프파이퍼 시스템 엔지니어 길포일 입니다"
