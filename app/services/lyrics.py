from openai import OpenAI
from app.core.config import settings
from fastapi import HTTPException
from typing import Optional, AsyncGenerator
import logging
import asyncio

logger = logging.getLogger(__name__)

class LyricGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.BASE_URL
        )

    async def generate_lyrics_stream(
        self, 
        theme: str, 
        style: Optional[str] = None, 
        length: Optional[str] = None,
        language: Optional[str] = None
    ) -> AsyncGenerator[dict, None]:
        try:
            logger.info(f"Generating lyrics with theme: {theme}")
            
            system_prompt = """你是一位专业作词人。
            要求：
            1. 直接输出歌词内容，不要有任何其他说明或注释
            2. 每行歌词结尾不要加标点符号
            3. 保持简洁优美的表达
            4. 每行都是独立的句子
            5. 需要添加歌词结构说明（如"[Chorus]"、"[Verse]"等）
            6. 优化歌词结构，使歌词更押韵、更流畅
            7. 不要对歌词做任何解释"""
            
            user_prompt = f"创作一首关于'{theme}'的歌词"
            if style:
                user_prompt += f"，风格为{style}"
            if length:
                user_prompt += f"，长度约{length}字"
            if language:
                user_prompt += f"，使用{language}"
            
            stream = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield {
                        "content": chunk.choices[0].delta.content,
                        "done": False
                    }
                    # 添加小延迟使输出更平滑
                    await asyncio.sleep(0.1)
            
            # 标记完成
            yield {
                "content": "",
                "done": True
            }
            
        except Exception as e:
            logger.error(f"Error generating lyrics: {str(e)}")
            yield {
                "content": "",
                "done": True,
                "error": f"生成歌词时发生错误: {str(e)}"
            }