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
            logger.info(f"Generating lyrics stream with theme: {theme}")
            
            prompt = f"请你作为一个专业作词人，创作一首关于'{theme}'的歌词。"
            if style:
                prompt += f"风格要求：{style}。"
            if length:
                prompt += f"歌词长度大约{length}字。"
            if language:
                prompt += f"语言要求：{language}。"
            
            stream = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个经验丰富的营销文案撰写师，擅长撰写有说服力和吸引力的内容，会利用 AIDA 公式和其他经过验证的策略来推动转化。## 任务\n 1. 你会将用户输入的内容改写成精确而有力的标题，以吸引目标受众的注意力。\n 2. 你会运用讲故事或提出有趣的问题，迅速引起读者的兴趣。\n 3. 你会基于消费者心理学原则，鼓励目标受众采取行动。"},
                    {"role": "user", "content": prompt}
                ],
                stream=True  # 启用流式输出
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