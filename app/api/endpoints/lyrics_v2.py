from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import SimpleLyricRequest
from app.services.lyrics import LyricGenerator
from app.api.deps import get_lyrics_generator

router = APIRouter(prefix="/lyrics", tags=["歌词生成 V2"])

@router.post("/", response_model=str)
async def generate_lyrics(
    request: SimpleLyricRequest = SimpleLyricRequest(),
    generator: LyricGenerator = Depends(get_lyrics_generator)
) -> str:
    """
    V2 歌词生成接口 - 仅需一个提示词
    
    如果不提供提示词，将默认生成一首优美的歌词
    """
    try:
        lyrics = await generator.generate_simple_lyrics(prompt=request.prompt)
        return lyrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))