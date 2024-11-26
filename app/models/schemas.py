from pydantic import BaseModel, Field
from typing import Optional, List

class LyricRequest(BaseModel):
    theme: str
    style: Optional[str] = None
    length: Optional[str] = None
    language: Optional[str] = None

class LyricResponse(BaseModel):
    status: str
    lyrics: Optional[str] = None
    usage: Optional[dict] = None
    message: Optional[str] = None

# 用于SSE流式响应的模型
class LyricStreamResponse(BaseModel):
    content: str
    done: bool = False
    error: Optional[str] = None

class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色: system/user/assistant")
    content: str = Field(..., description="消息内容")

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="对话历史")
    temperature: Optional[float] = Field(0.7, description="温度参数", ge=0, le=2)
    max_tokens: Optional[int] = Field(None, description="最大生成长度")

class ChatStreamResponse(BaseModel):
    content: str
    done: bool = False
    error: Optional[str] = None