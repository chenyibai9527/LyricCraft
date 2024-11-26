from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.models.schemas import LyricRequest, LyricStreamResponse
from app.services.lyrics import LyricGenerator
from app.api.deps import get_lyrics_generator
import json

router = APIRouter(prefix="/lyrics", tags=["歌词生成"])

@router.post("/generate/stream")
@router.options("/generate/stream")
async def generate_lyrics_stream(
    request: LyricRequest,
    generator: LyricGenerator = Depends(get_lyrics_generator)
):
    """
    流式生成歌词的API端点
    """
    async def event_generator():
        async for chunk in generator.generate_lyrics_stream(
            theme=request.theme,
            style=request.style,
            length=request.length,
            language=request.language
        ):
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    )