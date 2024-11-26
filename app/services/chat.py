from openai import OpenAI
from app.core.config import settings
from fastapi import HTTPException
from typing import Optional, AsyncGenerator, List
from app.models.schemas import ChatMessage
import logging
import asyncio

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.BASE_URL
        )

    async def generate_suggestions(self, messages: List[ChatMessage]) -> List[str]:
        """生成后续提问建议"""
        try:
            # 构建提示词
            suggestion_prompt = {
                "role": "user",
                "content": "基于以上对话内容，给出3个可能的后续提问建议，直接以简洁的问题形式输出，每行一个问题，不要有序号。"
            }
            
            # 复制最后两轮对话用于生成建议
            context_messages = messages[-2:] if len(messages) >= 2 else messages
            
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[*context_messages, suggestion_prompt],
                temperature=0.8,
                stream=False
            )
            
            suggestions = response.choices[0].message.content.strip().split('\n')
            return suggestions[:3]  # 确保只返回3个建议
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return []

    async def chat_stream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[dict, None]:
        try:
            logger.info(f"Starting chat stream with {len(messages)} messages")
            
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            stream = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield {
                        "content": chunk.choices[0].delta.content,
                        "done": False
                    }
                    await asyncio.sleep(0.05)
            
            # 生成建议
            suggestions = await self.generate_suggestions(messages)
            
            # 发送完成标记和建议
            yield {
                "content": "",
                "done": True,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error in chat stream: {str(e)}")
            yield {
                "content": "",
                "done": True,
                "error": f"聊天过程发生错误: {str(e)}",
                "suggestions": []
            }

    async def predict_completion(
        self,
        input_text: str,
        context_messages: List[ChatMessage] = None
    ) -> Optional[str]:
        """预测用户输入的完整内容"""
        try:
            if not input_text or len(input_text.strip()) < 2:
                return None

            messages = [
                ChatMessage(
                    role="system",
                    content="你是一个智能助手，需要基于用户当前的输入预测他们可能想要问的完整问题。直接返回预测的完整问题，不要有任何解释或额外内容。"
                ),
                ChatMessage(
                    role="user",
                    content=f"基于这个输入预测完整的问题：{input_text}"
                )
            ]

            if context_messages:
                messages = [*context_messages[-2:], *messages]

            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[{"role": msg.role, "content": msg.content} for msg in messages],
                max_tokens=50,
                temperature=0.3,
                stream=False
            )

            prediction = response.choices[0].message.content.strip()
            
            if not prediction.startswith(input_text):
                prediction = input_text + prediction.lstrip(input_text)
                
            return prediction

        except Exception as e:
            logger.error(f"Error in predict_completion: {str(e)}")
            return None