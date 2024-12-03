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

    async def generate_simple_lyrics(self, prompt: str) -> str:
        """基于单个提示词生成歌词"""
        try:
            system_prompt = """你是一位专业作词人，擅长创作打动人心的歌词。

                创作要求：
                1. 结构规范：
                - 使用[Instrumental Intro]、[Verse]、[Pre-Chorus]、[Chorus]、[合适的乐器 solo]、[Bridge]、[Outro] 等结构标记
                - 每个部分至少4行歌词
                - Chorus 部分要朗朗上口，适合反复吟唱
                - 结构标记使用中括号，并单独成行

                2. 格式要求：
                - 直接输出歌词内容，不要有任何说明或注释
                - 每行歌词结尾不加任何标点符号
                - 每行都是完整的句子
                - 结构标记与歌词之间要空行

                3. 艺术性要求：
                - 运用押韵技巧，注重音韵和谐
                - 善用比喻、象征等修辞手法
                - 避免陈词滥调和过于直白的表达
                - 保持语言的简洁优美
                - 每个段落要有独特的意境和画面感

                4. 情感表达：
                - 围绕核心主题展开叙述
                - 注重情感的递进和铺陈
                - 创造共鸣点，引发听众情感共振
                - 副歌要突出主题，便于记忆

                5. 禁止事项：
                - 不要对歌词做任何解释或说明
                - 不要加入任何标点符号
                - 避免过于口语化的表达
                - 不要出现不恰当或敏感的内容
                - 不要使用数字作为段落编号"""
            
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"根据这个提示词创作歌词：{prompt}"}
                ],
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating lyrics: {str(e)}")
            raise Exception(f"生成歌词时发生错误: {str(e)}")